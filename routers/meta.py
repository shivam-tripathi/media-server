from fastapi import APIRouter
from utils.config import Config

router = APIRouter()


@router.get("/")
def get_health():
    return {'status': 'ok', 'host': Config.APP.HOSTNAME, 'port': Config.APP.PORT}

