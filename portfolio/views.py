import json, os, uuid
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from .data import SYSTEM

_HAS_DB = bool(os.getenv("DATABASE_URL")) or not (os.getenv("VERCEL") == "1")


def home(request):
    if _HAS_DB:
        from .models import Profile, Project, StackItem
        profile = Profile.objects.first()
        projects = Project.objects.filter(is_active=True)
        stack = StackItem.objects.filter(is_active=True)
    else:
        profile, projects, stack = None, [], []
    return render(request, "index.html", {"profile": profile, "projects": projects, "stack": stack})


def media_proxy(request, path):
    """Proxy media files from Neon S3 (no public bucket support)"""
    import boto3
    from django.conf import settings
    from django.http import HttpResponse, Http404
    try:
        s3 = boto3.client('s3',
            endpoint_url=settings.AWS_ENDPOINT_URL_S3,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION_NAME,
        )
        obj = s3.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=path)
        content_type = obj['ContentType']
        response = HttpResponse(obj['Body'].read(), content_type=content_type)
        response['Cache-Control'] = 'public, max-age=86400'
        return response
    except Exception:
        raise Http404


def set_bucket_public(request):
    import boto3, json
    from django.conf import settings
    s3 = boto3.client('s3',
        endpoint_url=settings.AWS_ENDPOINT_URL_S3,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION_NAME,
    )
    policy = json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Sid": "PublicRead",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": f"arn:aws:s3:::{settings.AWS_STORAGE_BUCKET_NAME}/*"
        }]
    })
    try:
        s3.put_bucket_policy(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Policy=policy)
        return JsonResponse({"ok": True})
    except Exception as e:
        return JsonResponse({"error": str(e)})


@require_POST
def chat(request):
    from openai import OpenAI
    try:
        msgs = json.loads(request.body)["messages"][-8:]
        msgs = [{"role": m["role"], "content": str(m["content"])[:500]} for m in msgs if m["role"] in ("user", "assistant")]
    except (KeyError, ValueError, TypeError):
        return JsonResponse({"error": "Bad request"}, status=400)
    try:
        client = OpenAI(api_key=os.environ["GROQ_API_KEY"].strip(), base_url="https://api.groq.com/openai/v1", timeout=25)
        r = client.chat.completions.create(
            model="openai/gpt-oss-20b", max_tokens=800, extra_body={"reasoning_effort": "low"},
            messages=[{"role": "system", "content": SYSTEM}, *msgs])
        return JsonResponse({"reply": r.choices[0].message.content or "Sorry, I could not answer that."})
    except Exception as e:
        print("CHAT ERROR:", type(e).__name__, str(e)[:300])
        return JsonResponse({"error": type(e).__name__}, status=502)


@require_POST
def call_token(request):
    from livekit import api
    room = f"visitor-{uuid.uuid4().hex[:8]}"
    t = (api.AccessToken(os.environ["LIVEKIT_API_KEY"], os.environ["LIVEKIT_API_SECRET"])
         .with_identity(room).with_grants(api.VideoGrants(room_join=True, room=room)))
    return JsonResponse({"url": os.environ["LIVEKIT_URL"], "token": t.to_jwt()})
