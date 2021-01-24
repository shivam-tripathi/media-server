from flask import Flask
from views.upload import upload_bp
from views.resource import resource_bp
from views.health import health_check_bp
import os


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.cfg"), silent=True)
    app.register_blueprint(upload_bp, url_prefix="/upload")
    app.register_blueprint(resource_bp, url_prefix="/resource")
    app.register_blueprint(health_check_bp, url_prefix="/health")
    app.url_map.strict_slashes = False
    return app
