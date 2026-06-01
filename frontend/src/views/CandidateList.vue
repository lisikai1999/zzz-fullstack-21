<template>
  <div>
    <div class="page-header">
      <h2>简历库</h2>
      <div>
        <el-input v-model="search" placeholder="搜索姓名或技能" style="width: 240px; margin-right: 12px" @keyup.enter="fetchCandidates" clearable />
        <el-button type="primary" @click="$router.push('/candidates/upload')">上传简历</el-button>
      </div>
    </div>
    <el-table :data="candidates" stripe style="width: 100%">
      <el-table-column prop="name" label="姓名" width="120">
        <template #default="{ row }">
          <router-link :to="`/candidates/${row.id}`" class="link">{{ row.name }}</router-link>
        </template>
      </el-table-column>
      <el-table-column prop="education_level" label="学历" width="100">
        <template #default="{ row }">{{ eduLabel(row.education_level) }}</template>
      </el-table-column>
      <el-table-column prop="years_of_experience" label="年限" width="80">
        <template #default="{ row }">{{ row.years_of_experience || '-' }}年</template>
      </el-table-column>
      <el-table-column label="技能" min-width="300">
        <template #default="{ row }">
          <span v-for="skill in (row.skills || []).slice(0, 6)" :key="skill" class="skill-tag skill-tag--neutral">{{ skill }}</span>
          <span v-if="(row.skills || []).length > 6" style="color: #999; font-size: 12px">+{{ row.skills.length - 6 }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="file_name" label="文件" width="160" />
      <el-table-column label="操作" width="160">
        <template #default="{ row }">
          <el-button link type="primary" @click="$router.push(`/candidates/${row.id}/matches`)">匹配岗位</el-button>
          <el-button link type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { listCandidates, deleteCandidate } from '../api/candidates'
import { EDUCATION_LABELS, type Candidate } from '../types'

const candidates = ref<Candidate[]>([])
const search = ref('')

const eduLabel = (level: string | null) => level ? (EDUCATION_LABELS[level] || level) : '-'

async function fetchCandidates() {
  candidates.value = await listCandidates(search.value)
}

async function handleDelete(id: number) {
  await ElMessageBox.confirm('确定删除该候选人？', '确认')
  await deleteCandidate(id)
  ElMessage.success('已删除')
  fetchCandidates()
}

onMounted(fetchCandidates)
</script>

<style scoped>
.link { color: #409eff; text-decoration: none; font-weight: 500; }
.link:hover { text-decoration: underline; }
</style>
