import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import Base, get_db
from app.models.candidate import Candidate  # noqa: F401
from app.models.job import Job  # noqa: F401
from app.main import app
from app.services.skill_normalizer import SkillNormalizer


@pytest.fixture
def db_session(tmp_path):
    db_path = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    engine.dispose()


@pytest.fixture
def client(db_session):
    from fastapi.testclient import TestClient

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def normalizer():
    return SkillNormalizer()


@pytest.fixture
def sample_candidate():
    return {
        "name": "张三",
        "education_level": "master",
        "years_of_experience": 5.0,
        "skills": ["Python", "Vue.js", "Docker", "PostgreSQL"],
        "work_experience": [
            {"company": "腾讯科技", "title": "高级工程师", "start": "2019.1", "end": "present", "description": "负责后端架构设计"},
            {"company": "百度", "title": "工程师", "start": "2017.7", "end": "2018.12", "description": "搜索引擎开发"},
        ],
    }


@pytest.fixture
def sample_job():
    return {
        "title": "高级后端工程师",
        "min_education": "bachelor",
        "min_years": 3.0,
        "required_skills": ["Python", "Docker"],
        "preferred_industry": "互联网",
        "weighted_skills": [
            {"skill": "Python", "weight": 8},
            {"skill": "Docker", "weight": 6},
            {"skill": "Kubernetes", "weight": 7},
            {"skill": "PostgreSQL", "weight": 5},
        ],
    }
