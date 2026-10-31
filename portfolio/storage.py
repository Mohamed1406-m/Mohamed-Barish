from django.conf import settings
from django.utils.encoding import filepath_to_uri
from storages.backends.s3boto3 import S3Boto3Storage


class ProxiedS3Storage(S3Boto3Storage):
    """Neon buckets are private, so serve file URLs through the /media/ proxy view"""

    def url(self, name, parameters=None, expire=None, http_method=None):
        return settings.MEDIA_URL + filepath_to_uri(name).lstrip("/")
