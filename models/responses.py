from pydantic import BaseModel

class ChatResponse(BaseModel):
    Answer: str 