from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# Define the structure for a MongoDB query filter
class MongoDBQueryFilter(BaseModel):

    """A MongoDB query filter generated from a user's natural language question."""
    
    filter: Dict[str, Any] = Field(
        ...,
        description="A dictionary representing a MongoDB find() query filter. "
                    "Use operators like $eq, $gt, $regex, $in where necessary. "
                    "Example: {'department': 'Engineering', 'salary': {'$gt': 100000}}"
    )
    explanation: str = Field(
        ...,
        description="A brief explanation of why this filter was chosen for the query."
    )
