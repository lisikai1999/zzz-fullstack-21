import json
from datetime import datetime

from sqlalchemy import Integer, String, Float, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    department: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="open")
    min_education: Mapped[str | None] = mapped_column(String(20), nullable=True)
    min_years: Mapped[float | None] = mapped_column(Float, nullable=True)
    required_skills_json: Mapped[str | None] = mapped_column("required_skills", Text, nullable=True)
    preferred_industry: Mapped[str | None] = mapped_column(String(100), nullable=True)
    weighted_skills_json: Mapped[str | None] = mapped_column("weighted_skills", Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    @property
    def required_skills(self) -> list[str]:
        return json.loads(self.required_skills_json) if self.required_skills_json else []

    @required_skills.setter
    def required_skills(self, value: list[str]):
        self.required_skills_json = json.dumps(value, ensure_ascii=False)

    @property
    def weighted_skills(self) -> list[dict]:
        return json.loads(self.weighted_skills_json) if self.weighted_skills_json else []

    @weighted_skills.setter
    def weighted_skills(self, value: list[dict]):
        self.weighted_skills_json = json.dumps(value, ensure_ascii=False)
