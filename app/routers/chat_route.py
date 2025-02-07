from fastapi import APIRouter
from app.schemas import chat_schema
from openai import OpenAI
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
key = os.environ.get("OPENAI_API_KEY")

chat_router = APIRouter()


@chat_router.post("/chat")
def chat(data: chat_schema.UserChatInput):
    # completion = client.chat.completions.create(
    #     model="gpt-4o-mini",
    # )
    # response = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #         {
    #             "role": "developer",
    #             "content": "You are a helpful python programming assistance. You will help user only in python, not any other programming language. Not answer more then 20 words.",
    #         },
    #         {
    #             "role": "user",
    #             "content": data.message,
    #         },
    #     ],
    # )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    system_prompt = """You are an AI car dealership assistant. Your goal is to help users find the perfect vehicle."""

    response = llm.invoke(f"{system_prompt}\n User input: '{data.message}'")
    print(response)

    return response.content
