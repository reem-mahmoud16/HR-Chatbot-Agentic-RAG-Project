import os
from typing import Dict, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from Services.llm_service import GoogleLLMService
from config import DATA_SOURCES



class DataSourceDecision(BaseModel):
    """Model for the data source decision"""
    primary_source: str = Field(description="The primary data source to query")
    reasoning: str = Field(description="Brief explanation of why that source was chosen")

class RoutingService:
    def __init__(self):
        googleLLMService = GoogleLLMService()
        self.llm = googleLLMService.llm
        self.parser = JsonOutputParser(pydantic_object=DataSourceDecision)
        
        self.routing_agent_system_prompt = """You are an expert data retrieval routing system. 
        Your task is to analyze the user's question and determine the most appropriate data source(s) to retrieve information from.

        Available Data Sources:
        {data_sources}

        Guidelines:
        1. Choose MongoDB for HR policies about Purpose, Scope, Workplace Conduct, Compensation and Benefits and Leave Policies
        2. Choose the text File for HR policies about Working Hours and Attendance, Termination and Resignation, Confidentiality and Data Protection


        Respond with JSON containing:
        - primary_source: the main data source to query first (textfile or mongo)
        - reasoning: brief explanation of your choice

        Current user query: {query}
        """
    
    def format_data_sources(self) -> str:
        """Format available data sources for the prompt"""
        sources_info = []
        for key, source in DATA_SOURCES.items():
            sources_info.append(f"- {key}: {source['name']} ({source['description']})")
        return "\n".join(sources_info)
    
    def determine_data_source(self, query: str) -> DataSourceDecision:
        """Determine the best data source for a given query"""
        prompt = ChatPromptTemplate.from_template(self.routing_agent_system_prompt)
        
        chain = prompt | self.llm | self.parser
        
        response = chain.invoke({
            "data_sources": self.format_data_sources(),
            "query": query
        })
        
        return DataSourceDecision(**response)