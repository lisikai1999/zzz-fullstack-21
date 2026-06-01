<template>
  <div>
    <div class="page-header">
      <h2>岗位管理</h2>
      <el-button type="primary" @click="$router.push('/jobs/new')">新建岗位</el-button>
    </div>

    <el-table :data="jobs" stripe style="width: 100%">
      <el-table-column prop="title" label="岗位名称" min-width="180">
        <template #default="{ row }">
          <router-link :to="`/jobs/${row.id}`" class="link">{{ row.title }}</router-link>
        </template>
      </el-table-column>
      <el-table-column prop="department" label="部门" width="120" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="statusType(row.status)" size="small">{{ statusLabel(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="必备技能" min-width="200">
        <template #default="{ row }">
          <span v-for="s in row.required_skills" :key="s" class="skill-tag skill-tag--neutral">{{ s }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="min_years" label="最低年限" width="100">
        <template #default="{ row }">{{ row.min_years ? `${row.min_years}年` : '-' }}</template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button link type="primary" @click="$router.push(`/jobs/${row.id}/matches`)">查看匹配</el-button>
          <el-button link type="warning" @click="$router.push(`/jobs/${row.id}/edit`)">编辑</el-button>
          <el-button link type="danger" @click="handleDelete(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { listJobs, deleteJob } from '../api/jobs'
import type { Job } from '../types'

const jobs = ref<Job[]>([])

const statusLabel = (s: string) => ({ open: '招聘中', closed: '已关闭', draft: '草稿' }[s] || s)
const statusType = (s: string) => ({ open: 'success', closed: 'info', draft: 'warning' }[s] || '')

async function fetchJobs() {
  jobs.value = await listJobs()
}

async function handleDelete(id: number) {
  await ElMessageBox.confirm('确定删除该岗位？', '确认')
  await deleteJob(id)
  ElMessage.success('已删除')
  fetchJobs()
}

onMounted(fetchJobs)
</script>

<style scoped>
.link { color: #409eff; text-decoration: none; font-weight: 500; }
.link:hover { text-decoration: underline; }
</style>
