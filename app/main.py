from fastapi import FastAPI
from app.routers.v1.api_hpc import router


def create_app():
    app = FastAPI(title="HPC",
                  description="HPC service", docs_url="/v1/api-doc")
    app.include_router(router)

    return app
