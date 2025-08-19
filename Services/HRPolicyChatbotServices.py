from config import DATABASE_FULL_DOCUMENT_PATH
from pipelines.langGraph.pipeline import AgenticLangGraphRAGPipeline

class HRPolicyChatbot:
    def __init__(self):
        self.RAG_pipeline = AgenticLangGraphRAGPipeline()

    def get_answer(self, user_prompt):
        LLM_response = self.RAG_pipeline.generate_LLM_Answer(user_prompt)
        return LLM_response