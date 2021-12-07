from fastapi import FastAPI
from .routers.v1 import auth
from .routers.v1 import job_submit
from .routers.v1 import job_info
from .routers.v1 import cluster_info

def api_registry(app: FastAPI):
    app.include_router(auth.router, prefix="/v1")
    app.include_router(job_submit.router, prefix="/v1")
    app.include_router(job_info.router, prefix="/v1")
    app.include_router(cluster_info.router, prefix="/v1")

