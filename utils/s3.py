import boto3
from utils.config import Config
from functools import reduce
from botocore.exceptions import ClientError
from mypy_boto3_output.mypy_boto3_s3_package.mypy_boto3_s3.client import S3Client


class S3:
    s3 = None
    init = False

    def __init__(self):
        if not self.init:
            self.s3 = boto3.client("s3")
            self.init = True

    def client(self) -> S3Client:
        return self.s3

    def get_upload_url(self, bucket: str, key: str, metadata=None):
        if metadata is None:
            metadata = {}

        if bucket not in Config.MEDIA.BUCKETS:
            raise Exception("Invalid Bucket")

        valid_metadata_fields = filter(
            lambda k: k in Config.MEDIA.META or k.lower().startswith('x-amz-'),
            metadata.keys()
        )

        fields = reduce(
            lambda acc, k: acc | {k: metadata.get(k)},
            valid_metadata_fields,
            {"acl": "public-read"}
        )

        conditions = reduce(
            lambda acc, k: acc.append(["starts-with", f"${k}", ""]),
            valid_metadata_fields,
            [{"acl": "public-read"}, ["content-length-range", 0, Config.MEDIA.CONTENT_LENGTH]]
        )

        presigned_post = self.client().generate_presigned_post(
            Bucket=bucket,
            Key=key,
            Fields=fields,
            Conditions=conditions,
            ExpiresIn=Config.MEDIA.URL_EXPIRY
        )
        print(presigned_post)
        return presigned_post

    def assert_file_exists(self, bucket: str, key: str, throw=False):
        try:
            header = self.client().head_object(Bucket=bucket, Key=key)
            return True, header, None
        except ClientError as e:
            if throw:
                raise Exception(e)
            return False, None, e
