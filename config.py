
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


system_prompt = """You are an expert at converting questions about employees into MongoDB queries.
        You are querying a collection named 'employees' with documents that have fields like:
        - name (string)
        - id (int)
        - department (string, e.g., 'Engineering', 'Sales')
        - job_title (string)
        - date_joined: write any date in this format --> (Ex: 2022-03-23T00:00:00.000+00:00, 2025-02-15T00:00:00.000+00:00, 2024-03-02T00:00:00.000+00:00)
        
        Your goal is to create a precise MongoDB 'find()' filter based on the user's input.
        Use MongoDB operators like:
        - $eq: Equals
        - $ne: Not equals
        - $gt/$gte: Greater than/greater than or equal
        - $lt/$lte: Less than/less than or equal
        - $in: In an array
        - $regex: Regular expression (for partial text matches)
        - $and/$or: Logical operators

        **CRITICAL: Always assume the field names are exact as listed above.**
        **IMPORTANT: For text searches, use case-insensitive regex for partial matches: {{"$regex": "pattern", "$options": "i"}}**

        Output Format: ALWAYS return valid JSON with exactly these two fields:
            - 'filter': MongoDB filter object (e.g., {{"department": "Engineering"}})
            - 'explanation': Brief explanation of the filter
    
            IMPORTANT: 
            - No additional text before or after the JSON
            - No code formatting with backticks (```json or ```)
            - No markdown of any kind
            - Just pure JSON

        Example: 
        User: "Find engineers in the Engineering department"
        Output: {{"filter": {{"department": "Engineering"}}, "explanation": "Filtering for Engineering department"}}

        """
