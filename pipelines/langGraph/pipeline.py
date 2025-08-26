from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
from langchain_core.documents import Document
from ..interfaces.pipeline import IRAGPipeline
from Services.vector_db_service import ChromaDBService
from Services.llm_service import GoogleLLMService
from Services.MongoDBService import MongoDBHandler
from models.stateScema import AgentState
from pipelines.langGraph.dataSourceRouter import RoutingService
from config import generator_node_system_prompt


class AgenticLangGraphRAGPipeline(IRAGPipeline):
    
    def __init__(self):
        self.chromaDBService = ChromaDBService()
        self.vectorstore = None
        self.googleLLMService = GoogleLLMService()
        self.llm = self.googleLLMService.llm
        self.mongoDBHandler = MongoDBHandler()
        self.routingService = RoutingService()
        self.app = None
        self.build_graph()
    

    def route_by_query(self, state: dict):
        """Main method to choose the appropriate sources and route to its node"""
        # First, determine the best data source
        decision = self.routingService.determine_data_source(state.question)

        primary_source = decision.primary_source
        employees_query = decision.employees_query

        if employees_query == True:
            return "employees_data_retriever"

        elif "mongo" in primary_source.lower():
            return "hr_mongodb_retriever"

        elif "text" in primary_source.lower():
            return "hr_textfile_retriever"
        
        else:
            state["context"] = "irrelevant data"
            return "generator"


    def HR_Policy_MongoDB_Node(self, state: dict):
        self.vectorstore = self.chromaDBService.initialize_collection(collection_name="HR_Policy_Collection", data_source = "mongo")
        docs = self.vectorstore.as_retriever().invoke(state.question)
        return {"context": docs}
    

    def HR_Policy_TextFileDB_Node(self, state: dict):
        self.vectorstore = self.chromaDBService.initialize_collection(collection_name="HR_Policy_Collection", data_source = "textfile")
        docs = self.vectorstore.as_retriever().invoke(state.question)
        return {"context": docs}
    
    
    def Employees_Data_Query_Tool_Node(self, state: dict):
    
        docs = self.mongoDBHandler.query_employees_database(state.question)

        # Convert MongoDB dicts to LangChain Documents
        document_objects = []
        for emp in docs["results"]:
            # Create a string representation for the LLM
            content = f"Employee: {emp['employee_name']}, Department: {emp['department']}, Title: {emp['job_title']}, Joined: {emp['date_joined'].strftime('%Y-%m-%d')}"
            
            document_objects.append(
                Document(
                    page_content=content,  # ← Required field for Document
                    metadata={
                        "employee_id": emp["employee_id"],
                        "department": emp["department"],
                        "date_joined": emp["date_joined"]
                    }
                )
            )
        
        return {"context": document_objects}
        

    def generator_node(self, state: dict):

        hr_prompt = ChatPromptTemplate.from_messages([
            ("system", generator_node_system_prompt),
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
        workflow.add_node("hr_mongodb_retriever", self.HR_Policy_MongoDB_Node)
        workflow.add_node("hr_textfile_retriever", self.HR_Policy_TextFileDB_Node)
        workflow.add_node("employees_data_retriever", self.Employees_Data_Query_Tool_Node)
        workflow.add_node("generator", self.generator_node)

        workflow.add_conditional_edges(
            START,
            self.route_by_query,
            {
                "hr_mongodb_retriever": "hr_mongodb_retriever",
                "hr_textfile_retriever":"hr_textfile_retriever",
                "employees_data_retriever":"employees_data_retriever",
                "generator":"generator"
            }
        )

        workflow.add_edge("hr_mongodb_retriever", "generator")

        workflow.add_edge("hr_textfile_retriever", "generator")

        workflow.add_edge("employees_data_retriever", "generator")

        workflow.add_edge("generator", END)

        
        # Compile
        self.app = workflow.compile()
        


    def generate_LLM_Answer(self, user_prompt: str) -> str:
        result = self.app.invoke({"question": user_prompt})
        return result["response"].content
        
    