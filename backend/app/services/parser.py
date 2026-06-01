from pathlib import Path

from app.services.pdf_parser import extract_text_from_pdf
from app.services.docx_parser import extract_text_from_docx
from app.services.field_extractor import (
    extract_name,
    extract_email,
    extract_phone,
    detect_education_level,
    extract_education_history,
    extract_work_experience,
    compute_years_of_experience,
    extract_skills,
)
from app.services.skill_normalizer import SkillNormalizer


_normalizer = SkillNormalizer()


def parse_resume(file_path: Path) -> dict:
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        raw_text = extract_text_from_pdf(file_path)
    elif suffix in (".docx", ".doc"):
        raw_text = extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    education_history = extract_education_history(raw_text)
    work_experience = extract_work_experience(raw_text)
    raw_skills = extract_skills(raw_text)
    normalized_skills = _normalizer.normalize_list(raw_skills)

    education_level = detect_education_level(raw_text)
    if not education_level and education_history:
        for entry in education_history:
            if entry.get("degree"):
                education_level = entry["degree"]
                break

    years = compute_years_of_experience(work_experience)

    return {
        "name": extract_name(raw_text),
        "email": extract_email(raw_text),
        "phone": extract_phone(raw_text),
        "education_level": education_level,
        "education_history": education_history,
        "work_experience": work_experience,
        "skills": normalized_skills,
        "years_of_experience": years,
        "raw_text": raw_text,
    }
