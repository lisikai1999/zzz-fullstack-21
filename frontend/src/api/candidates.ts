import client from './client'
import type { Candidate } from '../types'

interface CandidateUpdate {
  name?: string
  email?: string
  phone?: string
  education_level?: string
  skills?: string[]
  years_of_experience?: number
}

export async function uploadResume(file: File): Promise<Candidate> {
  const formData = new FormData()
  formData.append('file', file)
  const { data } = await client.post('/candidates/upload', formData)
  return data
}

export async function listCandidates(search = '', skip = 0, limit = 50): Promise<Candidate[]> {
  const { data } = await client.get('/candidates', { params: { search, skip, limit } })
  return data
}

export async function getCandidate(id: number): Promise<Candidate> {
  const { data } = await client.get(`/candidates/${id}`)
  return data
}

export async function updateCandidate(id: number, payload: CandidateUpdate): Promise<Candidate> {
  const { data } = await client.put(`/candidates/${id}`, payload)
  return data
}

export async function deleteCandidate(id: number): Promise<void> {
  await client.delete(`/candidates/${id}`)
}
