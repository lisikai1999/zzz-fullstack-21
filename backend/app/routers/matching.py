from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.candidate import Candidate
from app.models.job import Job
from app.schemas.match import MatchResult, MatchScoreBreakdown
from app.services.matcher import compute_match_score

router = APIRouter()


@router.get("/job/{job_id}/top", response_model=list[MatchResult])
def top_candidates_for_job(
    job_id: int,
    k: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        return []

    job_dict = _job_to_dict(job)
    candidates = db.query(Candidate).all()

    results = []
    for c in candidates:
        c_dict = _candidate_to_dict(c)
        score = compute_match_score(c_dict, job_dict)
        results.append(MatchResult(
            candidate_id=c.id,
            candidate_name=c.name,
            job_id=job.id,
            job_title=job.title,
            score=MatchScoreBreakdown(**score),
        ))

    results.sort(key=lambda r: r.score.total_score, reverse=True)
    return results[:k]


@router.get("/candidate/{candidate_id}/top", response_model=list[MatchResult])
def top_jobs_for_candidate(
    candidate_id: int,
    k: int = Query(default=5, ge=1, le=50),
    db: Session = Depends(get_db),
):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        return []

    c_dict = _candidate_to_dict(candidate)
    jobs = db.query(Job).filter(Job.status == "open").all()

    results = []
    for job in jobs:
        job_dict = _job_to_dict(job)
        score = compute_match_score(c_dict, job_dict)
        results.append(MatchResult(
            candidate_id=candidate.id,
            candidate_name=candidate.name,
            job_id=job.id,
            job_title=job.title,
            score=MatchScoreBreakdown(**score),
        ))

    results.sort(key=lambda r: r.score.total_score, reverse=True)
    return results[:k]


def _candidate_to_dict(c: Candidate) -> dict:
    return {
        "name": c.name,
        "education_level": c.education_level,
        "years_of_experience": c.years_of_experience,
        "skills": c.skills,
        "work_experience": c.work_experience,
    }


def _job_to_dict(j: Job) -> dict:
    return {
        "title": j.title,
        "min_education": j.min_education,
        "min_years": j.min_years,
        "required_skills": j.required_skills,
        "preferred_industry": j.preferred_industry,
        "weighted_skills": j.weighted_skills,
    }
