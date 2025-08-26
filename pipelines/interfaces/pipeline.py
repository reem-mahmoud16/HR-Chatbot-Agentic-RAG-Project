from abc import ABC, abstractmethod

class IRAGPipeline(ABC):
    @abstractmethod
    def generate_LLM_Answer(self, user_prompt: str) -> str:
        pass

        