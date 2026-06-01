import client from './client'
import type { MatchResult } from '../types'

export async function getTopCandidatesForJob(jobId: number, k = 10): Promise<MatchResult[]> {
  const { data } = await client.get(`/matching/job/${jobId}/top`, { params: { k } })
  return data
}

export async function getTopJobsForCandidate(candidateId: number, k = 5): Promise<MatchResult[]> {
  const { data } = await client.get(`/matching/candidate/${candidateId}/top`, { params: { k } })
  return data
}
