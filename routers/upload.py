from controllers.upload import get_upload_url
from fastapi import APIRouter

router = APIRouter()


@router.get('/url')
async def upload_url(bucket: str, path: str, metadata: dict = None):
    if metadata is None:
        metadata = {}
    return get_upload_url(bucket, path, metadata)


@router.get('/media')
async def upload_post_media():
    pass
