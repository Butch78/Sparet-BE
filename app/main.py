from fastapi import FastAPI
from app.utils.deps import create_db_and_tables
from app.api.api_v1.api import api_router
from fastapi.middleware.cors import CORSMiddleware
from app.utils.config import settings



def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(api_router)

    return _app

app = get_application()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


@app.on_event("startup")
async def on_startup():
    create_db_and_tables()


@app.on_event("shutdown")
async def on_shutdown():
    pass
