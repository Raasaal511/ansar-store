import uvicorn

from fastapi import FastAPI
from backend.src.modules.orders.routers import router as orders_router


app =  FastAPI()
app.include_router(orders_router)



if __name__ == "__main__":
    uvicorn.run(app=app, host="localhost", port=8000)