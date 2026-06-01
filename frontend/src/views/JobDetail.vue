<template>
  <div v-if="job">
    <div class="page-header">
      <h2>{{ job.title }}</h2>
      <div>
        <el-button type="primary" @click="$router.push(`/jobs/${job.id}/matches`)">查看匹配候选人</el-button>
        <el-button @click="$router.push(`/jobs/${job.id}/edit`)">编辑</el-button>
        <el-button @click="$router.back()">返回</el-button>
      </div>
    </div>

    <div class="card">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="部门">{{ job.department || '-' }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="job.status === 'open' ? 'success' : 'info'" size="small">
            {{ { open: '招聘中', closed: '已关闭', draft: '草稿' }[job.status] }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="最低学历">{{ eduLabel(job.min_education) }}</el-descriptions-item>
        <el-descriptions-item label="最低年限">{{ job.min_years ? `${job.min_years}年` : '不限' }}</el-descriptions-item>
        <el-descriptions-item label="偏好行业">{{ job.preferred_industry || '不限' }}</el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">{{ job.description || '-' }}</el-descriptions-item>
      </el-descriptions>
    </div>

    <div class="card">
      <h3 style="margin-bottom: 12px">必备技能</h3>
      <span v-for="s in job.required_skills" :key="s" class="skill-tag skill-tag--neutral">{{ s }}</span>
      <span v-if="!job.required_skills.length" style="color: #999">无</span>
    </div>

    <div class="card" v-if="job.weighted_skills.length">
      <h3 style="margin-bottom: 12px">加权偏好技能</h3>
      <div v-for="ws in job.weighted_skills" :key="ws.skill" style="display: flex; align-items: center; margin-bottom: 6px">
        <span class="skill-tag skill-tag--neutral" style="width: 120px">{{ ws.skill }}</span>
        <el-progress :percentage="ws.weight * 10" :stroke-width="12" style="flex: 1; margin-left: 12px" />
        <span style="margin-left: 8px; font-size: 13px; color: #666">权重: {{ ws.weight }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getJob } from '../api/jobs'
import { EDUCATION_LABELS, type Job } from '../types'

const route = useRoute()
const job = ref<Job | null>(null)
const eduLabel = (level: string | null) => level ? (EDUCATION_LABELS[level] || level) : '不限'

onMounted(async () => {
  job.value = await getJob(Number(route.params.id))
})
</script>
