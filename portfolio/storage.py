from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class ProxiedS3Storage(S3Boto3Storage):
    """Neon buckets are private, so serve file URLs through the /media/ proxy view"""

    def url(self, name, parameters=None, expire=None, http_method=None):
        return settings.MEDIA_URL + self._normalize_name(self._clean_name(name)).lstrip("/")
