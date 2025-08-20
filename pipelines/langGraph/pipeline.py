from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END

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
    

    def route_by_query(self, state: dict):
        """Main method to choose the appropriate sources and route to its node"""
        # First, determine the best data source
        decision = self.routingService.determine_data_source(state.question)

        # Retrieve from primary source
        primary_source = decision.primary_source

        if "mongo" in primary_source.lower():
            return "mongodb_retriever"

        elif "text" in primary_source.lower():
            return "textfile_retriever"
        else:
            state["context"] = "irrelevant data"
            return "generator"


    def MongoDB_Node(self, state: dict):
        self.vectorstore = self.chromaDBService.initialize_collection(collection_name="HR_Policy_Collection", data_source = "mongo")
        docs = self.vectorstore.as_retriever().invoke(state.question)
        print(docs)
        return {"context": docs}

    def TextFileDB_Node(self, state: dict):
        self.vectorstore = self.chromaDBService.initialize_collection(collection_name="HR_Policy_Collection", data_source = "textfile")
        docs = self.vectorstore.as_retriever().invoke(state.question)
        return {"context": docs}

    def generator_node(self, state: dict):

        hr_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an HR policy assistant. Answer ONLY using:
            - Company Policies: {context}
            - Base your response strictly on the policies below.
            If context is irrelevant, explain that to the user
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
        workflow.add_node("mongodb_retriever", self.MongoDB_Node)
        workflow.add_node("textfile_retriever", self.TextFileDB_Node)
        workflow.add_node("generator", self.generator_node)

        workflow.add_conditional_edges(
            START,
            self.route_by_query,
            {
                "mongodb_retriever": "mongodb_retriever",
                "textfile_retriever":"textfile_retriever",
                "generator":"generator"
            }
        )

        workflow.add_edge("mongodb_retriever", "generator")

        workflow.add_edge("textfile_retriever", "generator")

        workflow.add_edge("generator", END)

        # Compile
        self.app = workflow.compile()
        


    def generate_LLM_Answer(self, user_prompt: str) -> str:
        result = self.app.invoke({"question": user_prompt})
        return result["response"].content
        
    
    def generate_system_prompt(self, query: str) -> str:
        pass
