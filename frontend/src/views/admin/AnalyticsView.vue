<template>
  <div class="page-container">
    <h2 style="margin-bottom: 20px">统计分析</h2>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <template #header>用户活跃度排行 (Top 20)</template>
          <el-table :data="userStats" size="small" v-loading="loading">
            <el-table-column type="index" label="排名" width="60" />
            <el-table-column prop="username" label="用户" width="120" />
            <el-table-column prop="activity_count" label="行为次数" width="100" />
            <el-table-column prop="last_login" label="最后登录" show-overflow-tooltip>
              <template #default="{ row }">{{ row.last_login?.slice(0, 10) || '从未' }}</template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card style="margin-bottom: 20px">
          <template #header>热门论文 (按浏览量)</template>
          <el-table :data="popularPapers" size="small" v-loading="loading">
            <el-table-column type="index" label="排名" width="60" />
            <el-table-column prop="title" label="标题" show-overflow-tooltip />
            <el-table-column prop="view_count" label="浏览" width="70" />
            <el-table-column prop="download_count" label="下载" width="70" />
          </el-table>
        </el-card>

        <el-card>
          <template #header>近7天热门关键词</template>
          <div class="trending-tags">
            <el-tag v-for="item in trendingTopics" :key="item.keyword" style="margin: 4px" size="large">
              {{ item.keyword }} ({{ item.count }})
            </el-tag>
            <el-empty v-if="trendingTopics.length === 0" description="暂无数据" :image-size="60" />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getUserStats, getPopularPapers, getTrendingTopics } from '@/api/analytics'

const userStats = ref([])
const popularPapers = ref([])
const trendingTopics = ref([])
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    const [statsRes, papersRes, topicsRes] = await Promise.all([
      getUserStats(),
      getPopularPapers(),
      getTrendingTopics(),
    ])
    userStats.value = statsRes.data
    popularPapers.value = papersRes.data
    trendingTopics.value = topicsRes.data
  } catch {} finally {
    loading.value = false
  }
})
</script>

<style scoped>
.trending-tags {
  display: flex;
  flex-wrap: wrap;
  min-height: 60px;
}
</style>
