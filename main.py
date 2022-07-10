import uvicorn

from tools.settings import settings

if __name__ == "__main__":
    uvicorn.run(
        app="app:app", host=settings.HOST, port=settings.PORT, reload=settings.RELOAD
    )
