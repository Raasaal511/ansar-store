import uvicorn

from contextlib import asynccontextmanager

from fastapi import FastAPI
from modules.orders.routers import router as orders_router

import modules

from db.database import async_engine, Base


app =  FastAPI()
app.include_router(orders_router)

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def on_startup():
    await init_db()

if __name__ == "__main__":
    uvicorn.run(app=app, host="localhost", port=8000)