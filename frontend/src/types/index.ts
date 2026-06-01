export interface Candidate {
  id: number
  name: string
  email: string | null
  phone: string | null
  education_level: string | null
  education_history: EducationEntry[]
  work_experience: WorkEntry[]
  skills: string[]
  years_of_experience: number | null
  file_name: string | null
  created_at: string | null
}

export interface EducationEntry {
  school: string
  degree: string
  major: string
  year: string
}

export interface WorkEntry {
  company: string
  title: string
  start: string
  end: string
  description: string
}

export interface WeightedSkill {
  skill: string
  weight: number
}

export interface Job {
  id: number
  title: string
  department: string | null
  description: string | null
  status: string
  min_education: string | null
  min_years: number | null
  required_skills: string[]
  preferred_industry: string | null
  weighted_skills: WeightedSkill[]
  created_at: string | null
}

export interface MatchScoreBreakdown {
  skill_score: number
  experience_score: number
  education_score: number
  industry_score: number
  total_score: number
  matched_skills: string[]
  missing_skills: string[]
  passes_hard_requirements: boolean
  hard_requirement_failures: string[]
}

export interface MatchResult {
  candidate_id: number
  candidate_name: string
  job_id: number
  job_title: string
  score: MatchScoreBreakdown
}

export const EDUCATION_LABELS: Record<string, string> = {
  high_school: '高中/中专',
  bachelor: '本科',
  master: '硕士',
  phd: '博士',
}
