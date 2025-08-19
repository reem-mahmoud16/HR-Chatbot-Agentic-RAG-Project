from abc import ABC, abstractmethod
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import GOOGLE_EMBEDDING_MODEL
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class IEmbeddingService(ABC):
    @abstractmethod
    def embed_query(self, text: str):
        pass

class GoogleEmbeddingService(IEmbeddingService):
    def __init__(self):
        if not os.environ.get("GOOGLE_API_KEY"):
            api_key = os.getenv('GOOGLE_API_KEY')
            os.environ["GOOGLE_API_KEY"] = api_key
        self.embedder = GoogleGenerativeAIEmbeddings(model=GOOGLE_EMBEDDING_MODEL)

    def embed_query(self, text: str):
        return self.embeddings.embed_query(text)