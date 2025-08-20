from abc import ABC, abstractmethod
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document 
from langchain_community.vectorstores import Chroma
from Services.MongoDBService import MongoDBHandler
from Services.embedding_service import GoogleEmbeddingService
from datasetHandler import DatasetHandler

class IVectorDBService(ABC):
    @abstractmethod
    def initialize_collection(self, collection_name: str):
        pass
    
    @abstractmethod
    def query(self, query_embedding, n_results: int = 5):
        pass

class ChromaDBService(IVectorDBService):
    def __init__(self):
        self.embedding_service = GoogleEmbeddingService()
        self.mongoDBHandler = MongoDBHandler()
        self.datasetHandler = DatasetHandler()
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
        self.vectorstore = None

    def initialize_collection(self, collection_name: str, data_source: str):
        
        if data_source == "mongo":
            text_context = self.mongoDBHandler.get_all_policies()
        elif data_source == "textfile":
            data_doc = open(self.datasetHandler.get_dataset_file_by_index(2), "r")
            text_context = data_doc.read()
            print(text_context)

        chunks = self.splitter.split_text(text_context)
        documents = [Document(page_content=chunk) for chunk in chunks]
        
        self.vectorstore = Chroma.from_documents(
                documents= documents,
                collection_name= collection_name,
                embedding= self.embedding_service.embedder
                )
        
        return self.vectorstore

    def query(self, user_query, n_results: int = 5):
        return self.vectorstore.similarity_search(user_query, k = n_results)