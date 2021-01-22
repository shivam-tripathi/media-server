from fastapi import FastAPI
from routers.upload import router as upload_router
from routers.resource import router as resource_router
from routers.meta import router as meta_router
import uvicorn
from utils.config import Config

app = FastAPI()
app.include_router(upload_router, prefix="/upload")
app.include_router(resource_router, prefix="/resource")
app.include_router(meta_router, prefix="/meta")

if __name__ == '__main__':
    uvicorn.run(
        'manage:app',
        host='localhost',
        port=Config.APP.PORT,
        reload=Config.APP.ENV == 'dev',
        debug=Config.APP.ENV == 'dev',
        workers=3
    )
