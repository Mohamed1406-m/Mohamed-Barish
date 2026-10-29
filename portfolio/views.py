import json, os, uuid
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from .data import SYSTEM

def home(request):
    return render(request, "index.html")

@require_POST
def chat(request):
    from openai import OpenAI
    try:
        msgs = json.loads(request.body)["messages"][-8:]
        msgs = [{"role": m["role"], "content": str(m["content"])[:500]} for m in msgs if m["role"] in ("user", "assistant")]
    except (KeyError, ValueError, TypeError):
        return JsonResponse({"error": "Bad request"}, status=400)
    r = OpenAI(api_key=os.environ["GROQ_API_KEY"], base_url="https://api.groq.com/openai/v1").chat.completions.create(
        model="llama-3.3-70b-versatile", max_tokens=300, messages=[{"role": "system", "content": SYSTEM}, *msgs])
    return JsonResponse({"reply": r.choices[0].message.content})

@require_POST
def call_token(request):
    from livekit import api
    room = f"visitor-{uuid.uuid4().hex[:8]}"
    t = (api.AccessToken(os.environ["LIVEKIT_API_KEY"], os.environ["LIVEKIT_API_SECRET"])
         .with_identity(room).with_grants(api.VideoGrants(room_join=True, room=room)))
    return JsonResponse({"url": os.environ["LIVEKIT_URL"], "token": t.to_jwt()})
