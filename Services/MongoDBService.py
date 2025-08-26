from pymongo import MongoClient
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import json
from Services.llm_service import GoogleLLMService
from config import question_query_Converter_system_prompt

load_dotenv()


class MongoDBHandler:
    def __init__(self):
        MONGO_URI = os.getenv("MONGO_URI")
        self.Client = MongoClient(MONGO_URI)

        self.Policies_db = self.Client["Policies"]  
        self.Policy_collection = self.Policies_db["HRPolicy"]

        self.Employees_db = self.Client['XYZCompanyData']
        self.Employees_collection = self.Employees_db['Employees Data']  


    def get_all_policies(self):
        policies = list(self.Policy_collection.find({}))
        return policies[0]["full_text"]
    
    def employeesBD_query_Tool_init(self):
        googleLLMService = GoogleLLMService()
        self.llm = googleLLMService.llm

        self.system_prompt = question_query_Converter_system_prompt

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "Convert this question into a MongoDB query: {question}")
        ])

        # Chain returns JSON string (not structured object)
        query_analysis_chain = prompt_template | self.llm | StrOutputParser()

        return query_analysis_chain
    

    @tool
    def query_employees_database(question: str): 
        """
        Useful for searching and analyzing employee data from the company database.
        Input should be a clear, natural language question about employees, their departments, salaries, or roles.
        
        Examples:
        - "How many engineers are in the IT department?"
        - "Find all managers earning more than $100,000"
        - "Show me employees who joined after January 2023"
        - "Who works in the Sales department?
        """

        mongoDBHandler = MongoDBHandler()

        query_chain = mongoDBHandler.employeesBD_query_Tool_init()

        try:
            # Get JSON response as string
            json_response = query_chain.invoke({"question": question})
            print(f"[DEBUG] Raw JSON response: {json_response}")
            
            # Parse JSON manually
            analysis = json.loads(json_response)
            print(analysis)
            # Extract values
            generated_filter = analysis["filter"]
            explanation = analysis["explanation"]
            
            # Step 2: Execute the generated query against MongoDB
            results = mongoDBHandler.Employees_collection.find(generated_filter)
            
            results_list = list(results)
            
            # Step 3: Handle and format the results
            if not results_list:
                return f"No employees found. The query was: {explanation}"
            
            # Format the results simply - another LLM could be used here for final formatting
            formatted_results = []
            for doc in results_list:
                # Clean up the document: remove MongoDB's _id and format
                doc.pop('_id', None)  # Remove the ObjectId which isn't JSON serializable
                formatted_results.append(doc)
            
            # Return the raw results and explanation - the agent's LLM will format the final answer
            return {
                "explanation": explanation,
                "results": formatted_results,
                "result_count": len(results_list)
            }
            
        except Exception as e:
            # Handle any errors gracefully
            return f"An error occurred while querying the database: {str(e)}"
    


