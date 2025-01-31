from fastapi import FastAPI
from app.routers.user_route import user_router
from app.routers.chat_route import chat_router

app = FastAPI()

app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])


@app.get("/")
def welcome():
    return {"message": "Welcome to the FastAPI application!"}
