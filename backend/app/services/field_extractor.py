import re
from datetime import datetime


EDUCATION_LEVELS = {
    "phd": ["phd", "ph.d", "博士", "doctorate"],
    "master": ["master", "硕士", "msc", "m.s.", "研究生"],
    "bachelor": ["bachelor", "本科", "学士", "bsc", "b.s.", "大学"],
    "high_school": ["高中", "中专", "high school", "diploma"],
}

EDUCATION_ORDER = {"high_school": 1, "bachelor": 2, "master": 3, "phd": 4}

SECTION_HEADERS = {
    "education": ["education", "学历", "教育", "教育背景", "教育经历"],
    "experience": ["experience", "work", "工作经历", "工作经验", "项目经历", "职业经历"],
    "skills": ["skills", "技能", "技术栈", "专业技能", "技术能力", "skill"],
}


def extract_email(text: str) -> str | None:
    match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    return match.group(0) if match else None


def extract_phone(text: str) -> str | None:
    patterns = [
        r"1[3-9]\d{9}",
        r"\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return None


def extract_name(text: str) -> str:
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    for line in lines[:5]:
        if re.search(r"@|http|www\.|\.com", line):
            continue
        if re.search(r"1[3-9]\d{9}", line):
            continue
        cleaned = re.sub(r"[:\s\-|/]", " ", line).strip()
        words = cleaned.split()
        if 1 <= len(words) <= 4 and not any(c.isdigit() for c in cleaned):
            is_header = any(
                cleaned.lower().startswith(h)
                for headers in SECTION_HEADERS.values()
                for h in headers
            )
            if not is_header:
                return cleaned
    return lines[0] if lines else "Unknown"


def detect_education_level(text: str) -> str | None:
    text_lower = text.lower()
    for level in ["phd", "master", "bachelor", "high_school"]:
        for keyword in EDUCATION_LEVELS[level]:
            if keyword in text_lower:
                return level
    return None


def extract_education_history(text: str) -> list[dict]:
    entries = []
    lines = text.split("\n")
    edu_section = _extract_section(lines, "education")
    if not edu_section:
        level = detect_education_level(text)
        if level:
            return [{"school": "", "degree": level, "major": "", "year": ""}]
        return []

    current_entry: dict = {}
    for line in edu_section:
        years = re.findall(r"((?:19|20)\d{2})", line)
        level = detect_education_level(line)
        if years or level:
            if current_entry:
                entries.append(current_entry)
            current_entry = {
                "school": "",
                "degree": level or "",
                "major": "",
                "year": years[0] if years else "",
            }
            remaining = re.sub(r"(19|20)\d{2}[\s\-~至./]*(?:(19|20)\d{2})?", "", line).strip()
            for kw_list in EDUCATION_LEVELS.values():
                for kw in kw_list:
                    remaining = re.sub(re.escape(kw), "", remaining, flags=re.IGNORECASE).strip()
            remaining = re.sub(r"[-|/\s]+", " ", remaining).strip()
            if remaining:
                current_entry["school"] = remaining
        elif current_entry:
            if not current_entry["school"]:
                current_entry["school"] = line.strip()

    if current_entry:
        entries.append(current_entry)
    return entries


def extract_work_experience(text: str) -> list[dict]:
    entries = []
    lines = text.split("\n")
    work_section = _extract_section(lines, "experience")
    if not work_section:
        work_section = lines

    date_pattern = r"((?:19|20)\d{2})[./\-]?(\d{1,2})?[\s]*[-–~至][\s]*((?:19|20)\d{2}|至今|present|现在)[./\-]?(\d{1,2})?"

    current_entry: dict | None = None
    for line in work_section:
        match = re.search(date_pattern, line, re.IGNORECASE)
        if match:
            if current_entry:
                entries.append(current_entry)
            start_year = match.group(1)
            start_month = match.group(2) or "1"
            end_year = match.group(3)
            end_month = match.group(4) or "12"

            remaining = re.sub(date_pattern, "", line, flags=re.IGNORECASE).strip()
            remaining = re.sub(r"[-|/\s]+", " ", remaining).strip()

            current_entry = {
                "company": remaining,
                "title": "",
                "start": f"{start_year}.{start_month}",
                "end": f"{end_year}.{end_month}" if end_year not in ("至今", "present", "现在") else "present",
                "description": "",
            }
        elif current_entry:
            if not current_entry["title"] and line.strip():
                current_entry["title"] = line.strip()
            elif line.strip():
                current_entry["description"] += line.strip() + " "

    if current_entry:
        entries.append(current_entry)
    return entries


def compute_years_of_experience(work_experience: list[dict]) -> float:
    if not work_experience:
        return 0.0

    total_months = 0
    now = datetime.now()

    for entry in work_experience:
        start = _parse_date(entry.get("start", ""))
        end_str = entry.get("end", "")
        if end_str in ("present", "至今", "现在", ""):
            end = now
        else:
            end = _parse_date(end_str)

        if start and end:
            months = (end.year - start.year) * 12 + (end.month - start.month)
            total_months += max(0, months)

    return round(total_months / 12.0, 1)


def extract_skills(text: str) -> list[str]:
    lines = text.split("\n")
    skill_section = _extract_section(lines, "skills")

    skills = set()
    if skill_section:
        for line in skill_section:
            parts = re.split(r"[,，;；、/|·•\t]+", line)
            for part in parts:
                cleaned = part.strip().strip("-").strip("•").strip()
                if cleaned and len(cleaned) < 30 and not cleaned[0].isdigit():
                    skills.add(cleaned)
    return list(skills)


def _extract_section(lines: list[str], section_type: str) -> list[str] | None:
    headers = SECTION_HEADERS.get(section_type, [])
    start_idx = None
    for i, line in enumerate(lines):
        line_lower = line.strip().lower()
        for h in headers:
            if h in line_lower:
                start_idx = i + 1
                break
        if start_idx is not None:
            break

    if start_idx is None:
        return None

    end_idx = len(lines)
    all_headers = [h for hlist in SECTION_HEADERS.values() for h in hlist]
    for i in range(start_idx, len(lines)):
        line_lower = lines[i].strip().lower()
        for h in all_headers:
            if h in line_lower and line_lower != lines[start_idx - 1].strip().lower():
                end_idx = i
                break
        if end_idx != len(lines):
            break

    section = lines[start_idx:end_idx]
    return section if section else None


def _parse_date(date_str: str) -> datetime | None:
    if not date_str:
        return None
    match = re.match(r"((?:19|20)\d{2})[./\-]?(\d{1,2})?", date_str)
    if match:
        year = int(match.group(1))
        month = int(match.group(2)) if match.group(2) else 1
        return datetime(year, max(1, min(12, month)), 1)
    return None
