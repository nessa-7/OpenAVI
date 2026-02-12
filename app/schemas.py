from pydantic import BaseModel
from typing import Dict, List


class ProfileResult(BaseModel):
    profile: str
    score: int


class ResultResponse(BaseModel):
    dominant_profiles: List[ProfileResult]
    recommended_programs: List[str]


class QuestionRequest(BaseModel):
    riasec_scores: Dict[str, int]
    session_id: str


class QuestionResponse(BaseModel):
    question: str
    category: str
    session_id: str


class AnswerRequest(BaseModel):
    category: str
    answer: int
    riasec_scores: Dict[str, int]
