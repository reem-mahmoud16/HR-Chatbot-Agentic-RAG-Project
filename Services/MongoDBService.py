from pymongo import MongoClient
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()


class MongoDBService:
    def __init__(self):
        MONGO_URI = os.getenv("MONGO_URI")
        self.Client = MongoClient(MONGO_URI)

        self.Policies_db = self.Client["Policies"]  
        self.Policy_collection = self.Policies_db["HRPolicy"]

        self.Employees_db = self.Client['XYZCompanyData']
        self.Employees_collection = self.Employees_db['Employees Data']  

    
    