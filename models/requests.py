from pydantic import BaseModel

class ChatRequest(BaseModel):
    Prompt: str