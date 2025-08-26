import os
from typing import Dict, List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from Services.llm_service import GoogleLLMService
from config import DATA_SOURCES, routing_agent_system_prompt



class DataSourceDecision(BaseModel):
    """Model for the data source decision"""
    primary_source: str = Field(description="The primary data source to query")
    reasoning: str = Field(description="Brief explanation of why that source was chosen")
    employees_query: bool = Field(description="tells if user asks about employees")

class RoutingService:
    def __init__(self):
        googleLLMService = GoogleLLMService()
        self.llm = googleLLMService.llm
        self.parser = JsonOutputParser(pydantic_object=DataSourceDecision)
        
        self.routing_agent_system_prompt = routing_agent_system_prompt
    
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