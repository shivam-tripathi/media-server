from utils.s3 import S3
from utils.config import Config
from uuid import uuid4
from utils.helpers import generate_url


def get_upload_url(bucket: str, path: str, metadata: dict):
    if bucket not in Config.MEDIA.BUCKETS:
        raise Exception("Invalid bucket")

    if path not in Config.MEDIA.PATHS:
        raise Exception("Invalid path")

    file_name = uuid4()
    key = f"{path}/{file_name}"
    pre_signed_url = S3().get_upload_url(bucket, key, metadata)
    return pre_signed_url | {"downloadUrl": generate_url(f'{bucket}/{key}')}
