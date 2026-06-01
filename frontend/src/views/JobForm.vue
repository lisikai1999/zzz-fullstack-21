<template>
  <div>
    <div class="page-header">
      <h2>{{ isEdit ? '编辑岗位' : '新建岗位' }}</h2>
      <el-button @click="$router.back()">返回</el-button>
    </div>

    <div class="card">
      <el-form :model="form" label-width="120px" style="max-width: 700px">
        <el-form-item label="岗位名称" required>
          <el-input v-model="form.title" placeholder="如：高级前端工程师" />
        </el-form-item>
        <el-form-item label="部门">
          <el-input v-model="form.department" placeholder="技术部" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="form.status">
            <el-option label="招聘中" value="open" />
            <el-option label="草稿" value="draft" />
            <el-option label="已关闭" value="closed" />
          </el-select>
        </el-form-item>
        <el-form-item label="岗位描述">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>

        <el-divider>硬性要求</el-divider>

        <el-form-item label="最低学历">
          <el-select v-model="form.min_education" clearable placeholder="不限">
            <el-option label="高中/中专" value="high_school" />
            <el-option label="本科" value="bachelor" />
            <el-option label="硕士" value="master" />
            <el-option label="博士" value="phd" />
          </el-select>
        </el-form-item>
        <el-form-item label="最低年限">
          <el-input-number v-model="form.min_years" :min="0" :max="30" :step="1" />
        </el-form-item>
        <el-form-item label="必备技能">
          <div>
            <el-tag v-for="(skill, i) in form.required_skills" :key="i" closable @close="form.required_skills.splice(i, 1)" style="margin: 0 4px 4px 0">
              {{ skill }}
            </el-tag>
            <el-input v-model="newRequiredSkill" size="small" style="width: 150px" placeholder="输入后回车" @keyup.enter="addRequiredSkill" />
          </div>
        </el-form-item>

        <el-divider>软性偏好</el-divider>

        <el-form-item label="偏好行业">
          <el-input v-model="form.preferred_industry" placeholder="如：互联网、金融" />
        </el-form-item>
        <el-form-item label="加权技能">
          <div v-for="(ws, i) in form.weighted_skills" :key="i" style="display: flex; align-items: center; margin-bottom: 8px; gap: 8px">
            <el-input v-model="ws.skill" style="width: 160px" placeholder="技能名" />
            <el-slider v-model="ws.weight" :min="1" :max="10" style="width: 200px" show-input />
            <el-button link type="danger" @click="form.weighted_skills.splice(i, 1)">移除</el-button>
          </div>
          <el-button size="small" @click="form.weighted_skills.push({ skill: '', weight: 5 })">添加技能</el-button>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">保存</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { createJob, getJob, updateJob } from '../api/jobs'

const route = useRoute()
const router = useRouter()
const isEdit = computed(() => route.name === 'JobEdit')
const submitting = ref(false)
const newRequiredSkill = ref('')

const form = ref({
  title: '',
  department: '',
  description: '',
  status: 'open',
  min_education: '',
  min_years: 0,
  required_skills: [] as string[],
  preferred_industry: '',
  weighted_skills: [] as { skill: string; weight: number }[],
})

function addRequiredSkill() {
  const s = newRequiredSkill.value.trim()
  if (s && !form.value.required_skills.includes(s)) {
    form.value.required_skills.push(s)
  }
  newRequiredSkill.value = ''
}

async function handleSubmit() {
  if (!form.value.title) {
    ElMessage.warning('请填写岗位名称')
    return
  }
  submitting.value = true
  try {
    const payload = {
      ...form.value,
      min_education: form.value.min_education || undefined,
      min_years: form.value.min_years || undefined,
      weighted_skills: form.value.weighted_skills.filter(ws => ws.skill.trim()),
    }
    if (isEdit.value) {
      await updateJob(Number(route.params.id), payload)
      ElMessage.success('岗位已更新')
    } else {
      await createJob(payload)
      ElMessage.success('岗位已创建')
    }
    router.push('/jobs')
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '保存失败')
  } finally {
    submitting.value = false
  }
}

onMounted(async () => {
  if (isEdit.value) {
    const job = await getJob(Number(route.params.id))
    form.value = {
      title: job.title,
      department: job.department || '',
      description: job.description || '',
      status: job.status,
      min_education: job.min_education || '',
      min_years: job.min_years || 0,
      required_skills: job.required_skills || [],
      preferred_industry: job.preferred_industry || '',
      weighted_skills: job.weighted_skills || [],
    }
  }
})
</script>
