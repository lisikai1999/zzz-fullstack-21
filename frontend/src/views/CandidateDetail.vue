<template>
  <div v-if="candidate">
    <div class="page-header">
      <h2>{{ candidate.name }}</h2>
      <div>
        <el-button type="primary" @click="$router.push(`/candidates/${candidate.id}/matches`)">推荐岗位</el-button>
        <el-button @click="$router.back()">返回</el-button>
      </div>
    </div>

    <div class="card">
      <el-descriptions :column="2" border title="基本信息">
        <el-descriptions-item label="姓名">{{ candidate.name }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ candidate.email || '-' }}</el-descriptions-item>
        <el-descriptions-item label="电话">{{ candidate.phone || '-' }}</el-descriptions-item>
        <el-descriptions-item label="学历">{{ eduLabel(candidate.education_level) }}</el-descriptions-item>
        <el-descriptions-item label="工作年限">{{ candidate.years_of_experience || 0 }}年</el-descriptions-item>
        <el-descriptions-item label="简历文件">{{ candidate.file_name || '-' }}</el-descriptions-item>
      </el-descriptions>
    </div>

    <div class="card">
      <h3 style="margin-bottom: 12px">技能</h3>
      <span v-for="skill in candidate.skills" :key="skill" class="skill-tag skill-tag--neutral">{{ skill }}</span>
      <span v-if="!candidate.skills.length" style="color: #999">暂无技能信息</span>
    </div>

    <div class="card" v-if="candidate.education_history.length">
      <h3 style="margin-bottom: 12px">教育经历</h3>
      <el-timeline>
        <el-timeline-item v-for="(edu, i) in candidate.education_history" :key="i" :timestamp="edu.year">
          <strong>{{ edu.school || '未知学校' }}</strong>
          <span v-if="edu.degree"> · {{ eduLabel(edu.degree) }}</span>
          <span v-if="edu.major"> · {{ edu.major }}</span>
        </el-timeline-item>
      </el-timeline>
    </div>

    <div class="card" v-if="candidate.work_experience.length">
      <h3 style="margin-bottom: 12px">工作经历</h3>
      <el-timeline>
        <el-timeline-item v-for="(work, i) in candidate.work_experience" :key="i" :timestamp="`${work.start} - ${work.end}`">
          <strong>{{ work.company }}</strong>
          <span v-if="work.title"> · {{ work.title }}</span>
          <p v-if="work.description" style="color: #666; margin-top: 4px; font-size: 13px">{{ work.description }}</p>
        </el-timeline-item>
      </el-timeline>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getCandidate } from '../api/candidates'
import { EDUCATION_LABELS, type Candidate } from '../types'

const route = useRoute()
const candidate = ref<Candidate | null>(null)

const eduLabel = (level: string | null) => level ? (EDUCATION_LABELS[level] || level) : '-'

onMounted(async () => {
  const id = Number(route.params.id)
  candidate.value = await getCandidate(id)
})
</script>
