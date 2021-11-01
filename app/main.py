from fastapi import FastAPI
from .api_registry import api_registry


def create_app():
    app = FastAPI(title="HPC",
                  description="HPC service", docs_url="/v1/api-doc")
    
    api_registry(app)

    return app
