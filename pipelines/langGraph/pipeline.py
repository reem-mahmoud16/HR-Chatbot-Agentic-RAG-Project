from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph

from ..interfaces.pipeline import IRAGPipeline
from Services.vector_db_service import ChromaDBService
from Services.llm_service import GoogleLLMService
from models.stateScema import AgentState
from pipelines.langGraph.dataSourceRouter import RoutingService


class AgenticLangGraphRAGPipeline(IRAGPipeline):
    
    def __init__(self):
        self.chromaDBService = ChromaDBService()
        self.vectorstore = None
        self.googleLLMService = GoogleLLMService()
        self.llm = self.googleLLMService.llm
        self.routingService = RoutingService()
        self.app = None
        self.build_graph()
    
    def retriever(self, state: dict, data_source: str):
        # Retrieve relevant HR policies
        self.vectorstore = self.chromaDBService.initialize_collection(collection_name="HR_Policy_Collection", data_source = data_source)
        docs = self.vectorstore.as_retriever().invoke(state.question)
        return {"context": docs}


    def retriever_node(self, state: dict):
        """Main method to retrieve information from appropriate sources"""
        # First, determine the best data source
        decision = self.routingService.determine_data_source(state.question)
        context = ""
                
        # Retrieve from primary source
        primary_source = decision.primary_source
        if 'mongo' in primary_source.lower():
            context = self.retriever(state, "mongo")

        elif 'text' in primary_source.lower():
            context = self.retriever(state, "textfile")
        else:
            context = "irrelevant data"

        return context

    def generator_node(self, state: dict):

        hr_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an HR policy assistant. Answer ONLY using:
            - Company Policies: {context}
            - if context is irrelevant data explain that to user
            - Base your response strictly on the policies below.
            If unsure, say "I cannot find this in our policies"."""),
            ("user", "{question}")
        ])
        chain = hr_prompt | self.llm  
        return {"response": chain.invoke({
            "question": state.question,
            "context": state.context
        })}


    def build_graph(self):
        workflow = StateGraph(AgentState)

        # Add nodes
        workflow.add_node("retriever", self.retriever_node)
        workflow.add_node("generator", self.generator_node)

        # Connect nodes (retrieve → answer)
        workflow.add_edge("retriever", "generator")

        # Set entry point
        workflow.set_entry_point("retriever")

        # Compile
        self.app = workflow.compile()
        


    def generate_LLM_Answer(self, user_prompt: str) -> str:
        result = self.app.invoke({"question": user_prompt})
        return result["response"].content
        
    
    def generate_system_prompt(self, query: str) -> str:
        pass
