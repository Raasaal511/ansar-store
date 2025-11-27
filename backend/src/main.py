import uvicorn

from contextlib import asynccontextmanager

from fastapi import FastAPI

import modules

from db.database import async_engine, Base


app =  FastAPI()
app.include_router(modules.router)


if __name__ == "__main__":
    uvicorn.run(app=app, host="localhost", port=8000)