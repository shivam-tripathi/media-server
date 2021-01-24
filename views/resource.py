from flask import Blueprint, request, Response, redirect, url_for, make_response
from controllers.resource import get_resource_url

resource_bp = Blueprint('resource', __name__)


@resource_bp.route('/<path:path>/', methods=['GET'])
def resource_get(path):
    width = request.args.get('w')
    height = request.args.get('h')
    resource_url = get_resource_url(path, width, height)
    response = make_response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    return redirect(location=url_for(resource_url), code=301, Response=response)
