from fastapi import APIRouter


chat_router = APIRouter()


@chat_router.get("/chats")
def get_chats():
    return {"message": "List of Chattings"}
