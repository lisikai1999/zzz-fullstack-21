<template>
  <div>
    <div class="page-header">
      <h2>{{ pageTitle }}</h2>
      <el-button @click="$router.back()">返回</el-button>
    </div>

    <div v-if="loading" style="text-align: center; padding: 40px">
      <el-icon class="is-loading" style="font-size: 32px"><Loading /></el-icon>
      <p style="margin-top: 12px; color: #999">正在计算匹配...</p>
    </div>

    <div v-else-if="results.length === 0" class="card" style="text-align: center; padding: 40px">
      <p style="color: #999">暂无匹配结果</p>
    </div>

    <div v-else>
      <div v-for="(item, index) in results" :key="index" class="card" style="cursor: pointer" @click="goDetail(item)">
        <div style="display: flex; justify-content: space-between; align-items: flex-start">
          <div style="flex: 1">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px">
              <h3 style="font-size: 16px">{{ isJobMode ? item.candidate_name : item.job_title }}</h3>
              <el-tag v-if="!item.score.passes_hard_requirements" type="danger" size="small">不满足硬性要求</el-tag>
            </div>

            <div style="margin-bottom: 12px">
              <div class="score-bar" style="width: 300px">
                <div
                  class="score-bar-fill"
                  :class="scoreClass(item.score.total_score)"
                  :style="{ width: item.score.total_score + '%' }"
                ></div>
              </div>
              <span style="font-size: 20px; font-weight: 700; margin-left: 12px" :style="{ color: scoreColor(item.score.total_score) }">
                {{ item.score.total_score.toFixed(1) }}
              </span>
            </div>

            <div v-if="item.score.hard_requirement_failures.length" style="margin-bottom: 8px">
              <span v-for="f in item.score.hard_requirement_failures" :key="f" class="skill-tag skill-tag--missing">{{ f }}</span>
            </div>

            <div>
              <span v-for="s in item.score.matched_skills" :key="s" class="skill-tag skill-tag--matched">{{ s }}</span>
              <span v-for="s in item.score.missing_skills" :key="s" class="skill-tag skill-tag--missing">{{ s }}</span>
            </div>
          </div>

          <div style="text-align: right; min-width: 200px">
            <div style="font-size: 12px; color: #999; margin-bottom: 4px">
              技能 {{ item.score.skill_score.toFixed(0) }} · 经验 {{ item.score.experience_score.toFixed(0) }} · 学历 {{ item.score.education_score.toFixed(0) }} · 行业 {{ item.score.industry_score.toFixed(0) }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Loading } from '@element-plus/icons-vue'
import { getTopCandidatesForJob, getTopJobsForCandidate } from '../api/matching'
import type { MatchResult } from '../types'

const route = useRoute()
const router = useRouter()
const results = ref<MatchResult[]>([])
const loading = ref(true)

const isJobMode = computed(() => route.name === 'JobMatches')
const pageTitle = computed(() => isJobMode.value ? '岗位匹配候选人' : '推荐岗位')

function scoreClass(score: number) {
  if (score >= 70) return 'score-high'
  if (score >= 40) return 'score-medium'
  return 'score-low'
}

function scoreColor(score: number) {
  if (score >= 70) return '#52c41a'
  if (score >= 40) return '#faad14'
  return '#ff4d4f'
}

function goDetail(item: MatchResult) {
  if (isJobMode.value) {
    router.push(`/candidates/${item.candidate_id}`)
  } else {
    router.push(`/jobs/${item.job_id}`)
  }
}

onMounted(async () => {
  try {
    const id = Number(route.params.id)
    if (isJobMode.value) {
      results.value = await getTopCandidatesForJob(id, 20)
    } else {
      results.value = await getTopJobsForCandidate(id, 10)
    }
  } finally {
    loading.value = false
  }
})
</script>
