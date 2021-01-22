from fastapi import APIRouter, Path, Query
from fastapi.responses import RedirectResponse
from controllers.resource import get_resource_url
from typing import Optional

router = APIRouter()


@router.get('/{path:path}')
async def resource_get(
        path: str = Path(...),
        width: Optional[int] = Query(None),
        height: Optional[int] = Query(None),
):
    resource_url = get_resource_url(path, width, height)
    return RedirectResponse(url=resource_url, headers={'Access-Control-Allow-Origin': '*'})
