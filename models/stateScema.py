from typing import Dict, List, Optional
from pydantic import BaseModel
from langchain_core.documents import Document

class AgentState(BaseModel):
    # User Input
    question: str  
    
    # Retrieval
    context: List[Document] = []    # Retrieved policy documents from ChromaDB
    
    # Generation
    response: Optional[str] = None  # LLM's final answer