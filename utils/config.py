import os
import json


def get_key(key, default_value, parse=True):
    value = os.environ.get(key)
    return (value if not parse else json.loads(value or 'null')) or default_value


class AppConfig:
    def __init__(self):
        self.HOSTNAME = get_key('APP_HOSTNAME', 'http://localhost:8080', False)
        self.PORT = get_key('PORT', 8080)


class MediaConfig:
    def __init__(self):
        self.BUCKETS = get_key('MEDIA_BUCKETS', ['media'])
        self.PATHS = get_key('MEDIA_PATHS', ['img', 'audio', 'video', 'doc'])
        self.URL_EXPIRY = get_key('MEDIA_URL_EXPIRY', 60 * 60)  # self signed url expiry time
        # Metadata fields which client can set (apart from x-amz-* fields).
        # Do not allow Content-Length if you don't want clients sending in arbitrary file sizes.
        self.META_ALLOWED = get_key('MEDIA_META_ALLOWED',
                                    ['Cache-Control', 'Content-Disposition', 'Content-Encoding', 'Content-Language',
                                     'Content-Type', 'Expires', 'Website-Redirect-Location'])
        self.CONTENT_LENGTH = get_key('MEDIA_CONTENT_LENGTH', 5242880)  # default 5MB
        self.DEFAULT_SIZE = get_key('MEDIA_DEFAULT_SIZE', [400, 400])
        self.SIZES_ALLOWED = get_key('MEDIA_SIZES_ALLOWED',
                                     [[0, 0], [90, 90], [200, 200], [400, 400], [600, 600], [900, 900]])


class Config:
    APP = AppConfig()
    MEDIA = MediaConfig()
