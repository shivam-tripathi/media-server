from flask import Blueprint, request
from controllers.upload import get_upload_url
from utils.helpers import sanitize_path

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/url/", methods=["POST"])
def upload_get_url():
    bucket: str = request.json.get("bucket")
    path: str = sanitize_path(request.json.get("path"))
    metadata: dict = request.json.get("metadata", {})
    return get_upload_url(bucket, path, metadata)


@upload_bp.route("/media", methods=["POST"])
def upload_post_media():
    pass
