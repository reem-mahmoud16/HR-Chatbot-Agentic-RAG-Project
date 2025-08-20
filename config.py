
GOOGLE_EMBEDDING_MODEL = "models/embedding-001"

LLM_CHAT_MODEL = "gemini-2.5-flash"

DATABASE_FULL_DOCUMENT_PATH = "E:\AI\RAG_project\documents\Full_HR_Policy_Dataset.txt"

DATABASE_FOLDER_PATH = "E:\AI\RAG_project\documents\HR_Policy_Datasets"

DATA_SOURCES = {
            "mongo_hr_policies": {
                "name": "MongoDB HR Policies",
                "description": "Contains HR policies about Purpose, Scope, Workplace Conduct, Compensation and Benefits and Leave Policies",
                "content_type": "unstructured policies",
                "collection": "hr_policies"
            },
            "text_hr_policies": {
                "name": "Text File HR Policies",
                "description": "Contains HR policies about Working Hours and Attendance, Termination and Resignation, Confidentiality and Data Protection",
                "content_type": "unstructured policies",
                "path": "data/hr_policies/"
            }
        }
