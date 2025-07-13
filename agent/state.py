from pydantic import BaseModel
from typing import List, Optional, Dict
from langchain_core.documents import Document

class State(BaseModel):
    input: str                               # Current user message
    user_id: Optional[int] = None
    answer: Optional[str] = None             # Latest answer
    sql_query: Optional[str] = None          # For billing agent
    documents: Optional[List[Document]] = None  # For QnA
    messages: List[Dict[str, str]] = []      # 🧠 Full message history