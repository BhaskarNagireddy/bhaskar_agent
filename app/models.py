from pydantic import BaseModel
from typing import List, Optional

class JobJSON(BaseModel):
    source: str = "bhaskar_chat"
    title: str
    company: str
    location: Optional[str] = None
    must_have: List[str] = []
    nice_to_have: List[str] = []
    description_text: str
    apply_url: Optional[str] = None

class AnalyzeResponse(BaseModel):
    must_have: List[str]
    nice_to_have: List[str]
    keywords: List[str]
    red_flags: List[str]
    score: float
    gaps: List[str]
