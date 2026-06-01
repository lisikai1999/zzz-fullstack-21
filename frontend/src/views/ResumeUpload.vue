<template>
  <div>
    <div class="page-header">
      <h2>上传简历</h2>
    </div>
    <div class="card">
      <el-upload
        drag
        :auto-upload="false"
        :on-change="handleFileChange"
        accept=".pdf,.docx,.doc"
        :limit="1"
        ref="uploadRef"
      >
        <el-icon style="font-size: 48px; color: #c0c4cc; margin-bottom: 12px"><UploadFilled /></el-icon>
        <div>将简历文件拖到此处，或<em>点击上传</em></div>
        <template #tip>
          <div style="color: #999; margin-top: 8px">支持 PDF、Word (.docx) 格式</div>
        </template>
      </el-upload>

      <el-button type="primary" style="margin-top: 20px" :loading="uploading" @click="doUpload" :disabled="!selectedFile">
        解析并保存
      </el-button>
    </div>

    <div v-if="result" class="card">
      <h3 style="margin-bottom: 16px">解析结果</h3>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="姓名">{{ result.name }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ result.email || '-' }}</el-descriptions-item>
        <el-descriptions-item label="电话">{{ result.phone || '-' }}</el-descriptions-item>
        <el-descriptions-item label="学历">{{ eduLabel(result.education_level) }}</el-descriptions-item>
        <el-descriptions-item label="年限">{{ result.years_of_experience || 0 }}年</el-descriptions-item>
        <el-descriptions-item label="技能" :span="2">
          <span v-for="skill in result.skills" :key="skill" class="skill-tag skill-tag--neutral">{{ skill }}</span>
        </el-descriptions-item>
      </el-descriptions>
      <el-button type="success" style="margin-top: 16px" @click="$router.push(`/candidates/${result.id}`)">
        查看详情
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { uploadResume } from '../api/candidates'
import { EDUCATION_LABELS, type Candidate } from '../types'

const selectedFile = ref<File | null>(null)
const uploading = ref(false)
const result = ref<Candidate | null>(null)

const eduLabel = (level: string | null) => level ? (EDUCATION_LABELS[level] || level) : '-'

function handleFileChange(file: any) {
  selectedFile.value = file.raw
}

async function doUpload() {
  if (!selectedFile.value) return
  uploading.value = true
  try {
    result.value = await uploadResume(selectedFile.value)
    ElMessage.success('简历解析成功')
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '上传失败')
  } finally {
    uploading.value = false
  }
}
</script>
