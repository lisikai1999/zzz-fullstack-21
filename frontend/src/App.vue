<template>
  <div>
    <nav class="nav-bar">
      <el-menu mode="horizontal" :default-active="activeRoute" router>
        <el-menu-item index="/candidates">简历库</el-menu-item>
        <el-menu-item index="/candidates/upload">上传简历</el-menu-item>
        <el-menu-item index="/jobs">岗位管理</el-menu-item>
      </el-menu>
    </nav>
    <div class="app-container">
      <router-view />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const activeRoute = computed(() => {
  if (route.path.startsWith('/jobs')) return '/jobs'
  if (route.path === '/candidates/upload') return '/candidates/upload'
  return '/candidates'
})
</script>
