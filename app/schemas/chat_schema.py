from pydantic import BaseModel


class UserChatInput(BaseModel):
    message: str
