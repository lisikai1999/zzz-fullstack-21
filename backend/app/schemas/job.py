from pydantic import BaseModel
from datetime import datetime


class WeightedSkill(BaseModel):
    skill: str
    weight: float = 5.0


class JobCreate(BaseModel):
    title: str
    department: str | None = None
    description: str | None = None
    status: str = "open"
    min_education: str | None = None
    min_years: float | None = None
    required_skills: list[str] = []
    preferred_industry: str | None = None
    weighted_skills: list[WeightedSkill] = []


class JobUpdate(BaseModel):
    title: str | None = None
    department: str | None = None
    description: str | None = None
    status: str | None = None
    min_education: str | None = None
    min_years: float | None = None
    required_skills: list[str] | None = None
    preferred_industry: str | None = None
    weighted_skills: list[WeightedSkill] | None = None


class JobOut(BaseModel):
    id: int
    title: str
    department: str | None = None
    description: str | None = None
    status: str
    min_education: str | None = None
    min_years: float | None = None
    required_skills: list[str] = []
    preferred_industry: str | None = None
    weighted_skills: list[dict] = []
    created_at: datetime | None = None

    class Config:
        from_attributes = True
