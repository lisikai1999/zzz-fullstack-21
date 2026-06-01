from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate, JobOut

router = APIRouter()


@router.post("", response_model=JobOut)
def create_job(data: JobCreate, db: Session = Depends(get_db)):
    job = Job(
        title=data.title,
        department=data.department,
        description=data.description,
        status=data.status,
        min_education=data.min_education,
        min_years=data.min_years,
        preferred_industry=data.preferred_industry,
    )
    job.required_skills = data.required_skills
    job.weighted_skills = [ws.model_dump() for ws in data.weighted_skills]
    db.add(job)
    db.commit()
    db.refresh(job)
    return _to_out(job)


@router.get("", response_model=list[JobOut])
def list_jobs(
    status: str = Query(default="", description="Filter by status"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    query = db.query(Job)
    if status:
        query = query.filter(Job.status == status)
    jobs = query.order_by(Job.created_at.desc()).offset(skip).limit(limit).all()
    return [_to_out(j) for j in jobs]


@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(404, "Job not found")
    return _to_out(job)


@router.put("/{job_id}", response_model=JobOut)
def update_job(job_id: int, data: JobUpdate, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(404, "Job not found")

    if data.title is not None:
        job.title = data.title
    if data.department is not None:
        job.department = data.department
    if data.description is not None:
        job.description = data.description
    if data.status is not None:
        job.status = data.status
    if data.min_education is not None:
        job.min_education = data.min_education
    if data.min_years is not None:
        job.min_years = data.min_years
    if data.required_skills is not None:
        job.required_skills = data.required_skills
    if data.preferred_industry is not None:
        job.preferred_industry = data.preferred_industry
    if data.weighted_skills is not None:
        job.weighted_skills = [ws.model_dump() for ws in data.weighted_skills]

    db.commit()
    db.refresh(job)
    return _to_out(job)


@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(404, "Job not found")
    db.delete(job)
    db.commit()
    return {"detail": "Deleted"}


def _to_out(j: Job) -> JobOut:
    return JobOut(
        id=j.id,
        title=j.title,
        department=j.department,
        description=j.description,
        status=j.status,
        min_education=j.min_education,
        min_years=j.min_years,
        required_skills=j.required_skills,
        preferred_industry=j.preferred_industry,
        weighted_skills=j.weighted_skills,
        created_at=j.created_at,
    )
