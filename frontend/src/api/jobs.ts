import client from './client'
import type { Job } from '../types'

export interface JobPayload {
  title: string
  department?: string
  description?: string
  status?: string
  min_education?: string
  min_years?: number
  required_skills?: string[]
  preferred_industry?: string
  weighted_skills?: { skill: string; weight: number }[]
}

export async function createJob(payload: JobPayload): Promise<Job> {
  const { data } = await client.post('/jobs', payload)
  return data
}

export async function listJobs(status = ''): Promise<Job[]> {
  const { data } = await client.get('/jobs', { params: { status } })
  return data
}

export async function getJob(id: number): Promise<Job> {
  const { data } = await client.get(`/jobs/${id}`)
  return data
}

export async function updateJob(id: number, payload: Partial<JobPayload>): Promise<Job> {
  const { data } = await client.put(`/jobs/${id}`, payload)
  return data
}

export async function deleteJob(id: number): Promise<void> {
  await client.delete(`/jobs/${id}`)
}
