"""
from pathlib import Path
import os
import sys
from ..interfaces.pipeline import IRAGPipeline
from Services.embedding_service import GoogleEmbeddingService
from Services.vector_db_service import ChromaDBService
from Services.llm_service import GoogleLLMService

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

class LangChainRAGPipeline(IRAGPipeline):
    def __init__(self, document_path: str, collection_name: str = "HR_Policy"):
        self.embedding_service = GoogleEmbeddingService()
        self.vector_db_service = ChromaDBService(self.embedding_service)
        self.llm_service = GoogleLLMService()
        
        self.llm = self.llm_service.get_chat_model()
        self.collection = self.vector_db_service.initialize_collection(document_path, collection_name)

    def generate_system_prompt(self, user_prompt: str) -> str:
        user_prompt_embedding = self.embedding_service.embed_query(user_prompt)
        
        context = self.vector_db_service.query(user_prompt_embedding)
        
        system_prompt = f'''
            You are an HR-related questions assistant agent.
            Expect a question from the user.
            Make an answer based on the context you are provided only.
            Do not make up unreal information.

            Your context: {context["documents"][0]}

            Input: {user_prompt}
        '''
        return system_prompt

"""