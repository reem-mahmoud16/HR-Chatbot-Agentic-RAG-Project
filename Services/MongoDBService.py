from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()


class MongoDBHandler:
    def __init__(self):
        MONGO_URI = os.getenv("MONGO_URI")
        self.Client = MongoClient(MONGO_URI)
        self.db = self.Client["Policies"]  
        self.collection = self.db["HRPolicy"]  

    def get_all_policies(self):
        policies = list(self.collection.find({}))
        return policies[0]["full_text"] + policies[1]["full_text"]
    




