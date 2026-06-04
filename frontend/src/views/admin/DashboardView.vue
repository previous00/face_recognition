<template>
  <div class="page-container">
    <h2 style="margin-bottom: 20px">系统数据概览</h2>
    <el-row :gutter="20" v-loading="loading">
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="注册用户" :value="overview.total_users" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="30天活跃用户" :value="overview.active_users_30d" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="论文总数" :value="overview.total_papers" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="项目总数" :value="overview.total_projects" />
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="行为记录总数" :value="overview.total_activities" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="30天行为记录" :value="overview.activities_30d" />
        </el-card>
      </el-col>
    </el-row>

    <el-card style="margin-top: 20px">
      <template #header>近30天行为分布</template>
      <el-table :data="overview.action_distribution || []" size="small">
        <el-table-column prop="action" label="行为类型" width="150">
          <template #default="{ row }">{{ actionLabel(row.action) }}</template>
        </el-table-column>
        <el-table-column prop="count" label="次数" width="100" />
        <el-table-column label="占比">
          <template #default="{ row }">
            <el-progress :percentage="getPercentage(row.count)" :stroke-width="16" :text-inside="true" />
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getSystemOverview } from '@/api/analytics'

const overview = ref({})
const loading = ref(false)

const actionLabel = (a) => ({
  view: '浏览', search: '搜索', download: '下载',
  favorite: '收藏', unfavorite: '取消收藏', create: '创建', update: '更新'
}[a] || a)

const getPercentage = (count) => {
  const total = overview.value.activities_30d || 1
  return Math.round((count / total) * 100)
}

onMounted(async () => {
  loading.value = true
  try {
    const res = await getSystemOverview()
    overview.value = res.data
  } catch {} finally {
    loading.value = false
  }
})
</script>
