from fastapi import FastAPI, Body 
from typing import Annotated
from Services.HRPolicyChatbotServices import HRPolicyChatbot
from models.requests import ChatRequest
from models.responses import ChatResponse

hr_chatbot = HRPolicyChatbot()

app = FastAPI(
    title="HR Policy Chatbot", 
    description="A simple FastAPI backend to integrate with ASP.NET Core.",
    version="1.0.0",
)


@app.post("/api/HR-chatbot-V2")
async def process_data(user_query: ChatRequest):
    response = hr_chatbot.get_answer(user_query.Prompt)
    return ChatResponse(Answer=response)