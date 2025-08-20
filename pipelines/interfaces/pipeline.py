from abc import ABC, abstractmethod

class IRAGPipeline(ABC):
    @abstractmethod
    def generate_system_prompt(self, query: str) -> str:
        pass
    @abstractmethod
    def generate_LLM_Answer(self, user_prompt: str) -> str:
        pass

        