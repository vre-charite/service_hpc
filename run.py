import uvicorn
from app.main import create_app
from app.config import get_settings

app = create_app()
settings = get_settings()

if __name__ == '__main__':
    uvicorn.run("run:app", host=settings.host, port=settings.port, log_level=settings.log_level, reload=True)
