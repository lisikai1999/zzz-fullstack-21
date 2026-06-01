from pydantic import BaseModel


class MatchScoreBreakdown(BaseModel):
    skill_score: float = 0.0
    experience_score: float = 0.0
    education_score: float = 0.0
    industry_score: float = 0.0
    total_score: float = 0.0
    matched_skills: list[str] = []
    missing_skills: list[str] = []
    passes_hard_requirements: bool = True
    hard_requirement_failures: list[str] = []


class MatchResult(BaseModel):
    candidate_id: int
    candidate_name: str
    job_id: int
    job_title: str
    score: MatchScoreBreakdown
