from pydantic import BaseModel
from datetime import datetime


class EducationEntry(BaseModel):
    school: str = ""
    degree: str = ""
    major: str = ""
    year: str = ""


class WorkEntry(BaseModel):
    company: str = ""
    title: str = ""
    start: str = ""
    end: str = ""
    description: str = ""


class CandidateOut(BaseModel):
    id: int
    name: str
    email: str | None = None
    phone: str | None = None
    education_level: str | None = None
    education_history: list[dict] = []
    work_experience: list[dict] = []
    skills: list[str] = []
    years_of_experience: float | None = None
    file_name: str | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class CandidateUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    education_level: str | None = None
    education_history: list[dict] | None = None
    work_experience: list[dict] | None = None
    skills: list[str] | None = None
    years_of_experience: float | None = None
