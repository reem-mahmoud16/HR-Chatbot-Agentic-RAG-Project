from abc import ABC, abstractmethod
from langchain.chat_models import init_chat_model
from config import LLM_CHAT_MODEL

class ILLMService(ABC):
    @abstractmethod
    def get_chat_model(self):
        pass

class GoogleLLMService(ILLMService):
    def __init__(self):
        self.llm = init_chat_model(LLM_CHAT_MODEL, model_provider="google_genai")

    def get_chat_model(self):
        return self.llm