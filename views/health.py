from flask import Blueprint, make_response

health_check_bp = Blueprint("health_check", __name__)


@health_check_bp.route("/", methods=['GET'])
def health_get():
    return make_response("ok")
