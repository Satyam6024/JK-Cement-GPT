from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class UploadResponse:
    file_id: str
    status: str
    message: str
    validation: Optional[Dict[str, Any]] = None

@dataclass
class QueryRequest:
    query: str
    analysis_type: Optional[str] = 'general'
    file_ids: Optional[List[str]] = None

@dataclass
class QueryResponse:
    answer: str
    analysis_type: str
    confidence: float
    sources: List[Dict[str, Any]]