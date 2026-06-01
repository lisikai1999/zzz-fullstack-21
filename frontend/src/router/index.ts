import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/candidates' },
  { path: '/candidates', name: 'CandidateList', component: () => import('../views/CandidateList.vue') },
  { path: '/candidates/upload', name: 'ResumeUpload', component: () => import('../views/ResumeUpload.vue') },
  { path: '/candidates/:id', name: 'CandidateDetail', component: () => import('../views/CandidateDetail.vue') },
  { path: '/jobs', name: 'JobList', component: () => import('../views/JobList.vue') },
  { path: '/jobs/new', name: 'JobCreate', component: () => import('../views/JobForm.vue') },
  { path: '/jobs/:id', name: 'JobDetail', component: () => import('../views/JobDetail.vue') },
  { path: '/jobs/:id/edit', name: 'JobEdit', component: () => import('../views/JobForm.vue') },
  { path: '/jobs/:id/matches', name: 'JobMatches', component: () => import('../views/MatchResults.vue') },
  { path: '/candidates/:id/matches', name: 'CandidateMatches', component: () => import('../views/MatchResults.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
