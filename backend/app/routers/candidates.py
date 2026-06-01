import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.config import UPLOAD_DIR
from app.models.candidate import Candidate
from app.schemas.candidate import CandidateOut, CandidateUpdate
from app.services.parser import parse_resume

router = APIRouter()


@router.post("/upload", response_model=CandidateOut)
def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename:
        raise HTTPException(400, "No filename provided")

    suffix = Path(file.filename).suffix.lower()
    if suffix not in (".pdf", ".docx", ".doc"):
        raise HTTPException(400, "Only PDF and Word files are supported")

    file_id = uuid.uuid4().hex
    saved_path = UPLOAD_DIR / f"{file_id}{suffix}"
    with open(saved_path, "wb") as f:
        content = file.file.read()
        f.write(content)

    try:
        parsed = parse_resume(saved_path)
    except Exception as e:
        saved_path.unlink(missing_ok=True)
        raise HTTPException(422, f"Failed to parse resume: {str(e)}")

    candidate = Candidate(
        name=parsed["name"],
        email=parsed["email"],
        phone=parsed["phone"],
        education_level=parsed["education_level"],
        years_of_experience=parsed["years_of_experience"],
        raw_text=parsed["raw_text"],
        file_path=str(saved_path),
        file_name=file.filename,
    )
    candidate.education_history = parsed["education_history"]
    candidate.work_experience = parsed["work_experience"]
    candidate.skills = parsed["skills"]

    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return _to_out(candidate)


@router.get("", response_model=list[CandidateOut])
def list_candidates(
    search: str = Query(default="", description="Search by name or skill"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    query = db.query(Candidate)
    if search:
        query = query.filter(
            Candidate.name.ilike(f"%{search}%")
            | Candidate.skills_json.ilike(f"%{search}%")
        )
    candidates = query.order_by(Candidate.created_at.desc()).offset(skip).limit(limit).all()
    return [_to_out(c) for c in candidates]


@router.get("/{candidate_id}", response_model=CandidateOut)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(404, "Candidate not found")
    return _to_out(candidate)


@router.put("/{candidate_id}", response_model=CandidateOut)
def update_candidate(candidate_id: int, data: CandidateUpdate, db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(404, "Candidate not found")

    if data.name is not None:
        candidate.name = data.name
    if data.email is not None:
        candidate.email = data.email
    if data.phone is not None:
        candidate.phone = data.phone
    if data.education_level is not None:
        candidate.education_level = data.education_level
    if data.education_history is not None:
        candidate.education_history = data.education_history
    if data.work_experience is not None:
        candidate.work_experience = data.work_experience
    if data.skills is not None:
        candidate.skills = data.skills
    if data.years_of_experience is not None:
        candidate.years_of_experience = data.years_of_experience

    db.commit()
    db.refresh(candidate)
    return _to_out(candidate)


@router.delete("/{candidate_id}")
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(404, "Candidate not found")
    if candidate.file_path:
        Path(candidate.file_path).unlink(missing_ok=True)
    db.delete(candidate)
    db.commit()
    return {"detail": "Deleted"}


def _to_out(c: Candidate) -> CandidateOut:
    return CandidateOut(
        id=c.id,
        name=c.name,
        email=c.email,
        phone=c.phone,
        education_level=c.education_level,
        education_history=c.education_history,
        work_experience=c.work_experience,
        skills=c.skills,
        years_of_experience=c.years_of_experience,
        file_name=c.file_name,
        created_at=c.created_at,
    )
