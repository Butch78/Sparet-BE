from fastapi import FastAPI

app = FastAPI()

from app.database.db import init_db


@app.on_event("startup")
async def on_startup():
    await init_db()