import json
from datetime import datetime

from sqlalchemy import Integer, String, Float, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str | None] = mapped_column(String(200), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    education_level: Mapped[str | None] = mapped_column(String(20), nullable=True)
    education_history_json: Mapped[str | None] = mapped_column("education_history", Text, nullable=True)
    work_experience_json: Mapped[str | None] = mapped_column("work_experience", Text, nullable=True)
    skills_json: Mapped[str | None] = mapped_column("skills", Text, nullable=True)
    years_of_experience: Mapped[float | None] = mapped_column(Float, nullable=True)
    raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    file_name: Mapped[str | None] = mapped_column(String(300), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    @property
    def education_history(self) -> list:
        return json.loads(self.education_history_json) if self.education_history_json else []

    @education_history.setter
    def education_history(self, value: list):
        self.education_history_json = json.dumps(value, ensure_ascii=False)

    @property
    def work_experience(self) -> list:
        return json.loads(self.work_experience_json) if self.work_experience_json else []

    @work_experience.setter
    def work_experience(self, value: list):
        self.work_experience_json = json.dumps(value, ensure_ascii=False)

    @property
    def skills(self) -> list:
        return json.loads(self.skills_json) if self.skills_json else []

    @skills.setter
    def skills(self, value: list):
        self.skills_json = json.dumps(value, ensure_ascii=False)
