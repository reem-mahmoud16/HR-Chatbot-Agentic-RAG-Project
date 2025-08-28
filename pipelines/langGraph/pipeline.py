from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState
from langchain_core.tools import tool, Tool
from Services.llm_service import GoogleLLMService
from Services.MongoDBService import MongoDBService
from langchain_mongodb.agent_toolkit import (
    MongoDBDatabase,
    MongoDBDatabaseToolkit,
    MONGODB_AGENT_SYSTEM_PROMPT,
)
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.mongodb import MongoDBSaver
from ..interfaces.pipeline import IRAGPipeline
from Services.vector_db_service import ChromaDBService

class AgentCustomTools:

    def __init__(self):
        self.chromaDBService = ChromaDBService()

    @tool
    def TextFile_HR_policies_query(self, user_query):
        """
        Retrieves information from HR policies stored in a separate text file.

        Use this tool for queries related to the company's policies on:
        - Working Hours and Attendance
        - Termination and Resignation
        - Confidentiality and Data Protection

        Input should be the user's full, unedited question. The tool returns relevant
        text excerpts from the policy documents.
        """
        
        return self.chromaDBService.query(user_query)

class AgenticLangGraphRAGPipeline(IRAGPipeline):
    
    def __init__(self):
        Google_LLM = GoogleLLMService()
        mongoDBService = MongoDBService()
        agentCustomTools = AgentCustomTools()

        employees_db = MongoDBDatabase(client=mongoDBService.Client,database='XYZCompanyData')
        employees_toolkit = MongoDBDatabaseToolkit(db=employees_db, llm=Google_LLM.get_chat_model())
        employees_tools = employees_toolkit.get_tools()
        employees_tools = rename_tools(employees_tools, "XYZCompanyData")

        hr_policies_db = MongoDBDatabase(client=mongoDBService.Client,database='Policies')
        hr_policies_toolkit = MongoDBDatabaseToolkit(db=hr_policies_db, llm=Google_LLM.get_chat_model())
        hr_policies_tools = hr_policies_toolkit.get_tools()
        hr_policies_tools = rename_tools(hr_policies_tools, 'Policies')

        all_tools = employees_tools + hr_policies_tools

        all_tools.append(agentCustomTools.TextFile_HR_policies_query)

        #print(all_tools)

        model = Google_LLM.get_chat_model()
        self.agent = create_react_agent(
            # Dynamically configure the model with tools based on runtime context
            model,
            # Initialize with all tools available
            tools=all_tools,
            checkpointer=MongoDBSaver(mongoDBService.Client)
        )

        
    def generate_LLM_Answer(self, user_prompt: str) -> str:
        response = self.agent.invoke(
            {
                "messages": [SystemMessage(content=MONGODB_AGENT_SYSTEM_PROMPT), HumanMessage(content=user_prompt)]
            },
            {"configurable": {"thread_id": "movie_query_1"}}
        )
        return response["messages"][-1].content
    


def rename_tools(tools: list, name_suffix: str) -> list[Tool]:
    renamed_tools = []
    for tool in tools:
        # Create a copy of the tool to modify its name and description
        renamed_tool = tool.copy()
        
        # Modify the tool's name to include the suffix
        new_name = f"{renamed_tool.name}_{name_suffix}"
        
        # Update the tool's description to reflect the new name and purpose
        new_description = renamed_tool.description.replace(
            "the database", f"the {name_suffix} database"
        )
        
        renamed_tool.name = new_name
        renamed_tool.description = new_description
        renamed_tools.append(renamed_tool)
    return renamed_tools
    
