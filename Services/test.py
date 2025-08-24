import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


class MongoDBHandler:
    def __init__(self):
        MONGO_URI = os.getenv("MONGO_URI")
        self.Client = MongoClient(MONGO_URI)

        self.Policies_db = self.Client["Policies"]  
        self.Policy_collection = self.Policies_db["HRPolicy"]

        self.Employees_db = self.Client['XYZCompanyData']
        self.Employees_collection = self.Employees_db['Employees Data'] 

        self.query_employees_database_test() 

    def query_employees_database_test(self) -> str:
        eng = list(self.Employees_collection.find({"department": "Engineering"}))
        print(eng)
        return "\n".join(str(eng))
    
m = MongoDBHandler()