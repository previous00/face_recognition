<template>
  <div class="page-container">
    <h2 style="margin-bottom: 20px">欢迎使用智能科研资源管理平台</h2>
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="论文总数" :value="stats.total_papers" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="科研项目" :value="stats.total_projects" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="我的收藏" :value="stats.total_favorites" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="近30天浏览" :value="stats.recent_views" />
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card>
          <template #header>热门论文</template>
          <el-table :data="popularPapers" size="small" style="width: 100%">
            <el-table-column prop="title" label="标题" show-overflow-tooltip />
            <el-table-column prop="view_count" label="浏览" width="70" />
            <el-table-column prop="download_count" label="下载" width="70" />
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>热门关键词</template>
          <div class="trending-tags">
            <el-tag v-for="item in trendingTopics" :key="item.keyword" class="tag-item" type="info">
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
import { getMySummary, getPopularPapers, getTrendingTopics } from '@/api/analytics'

const stats = ref({ total_papers: 0, total_projects: 0, total_favorites: 0, recent_views: 0 })
const popularPapers = ref([])
const trendingTopics = ref([])

onMounted(async () => {
  try {
    const [summaryRes, papersRes, topicsRes] = await Promise.all([
      getMySummary(),
      getPopularPapers(),
      getTrendingTopics(),
    ])
    stats.value = summaryRes.data
    popularPapers.value = papersRes.data
    trendingTopics.value = topicsRes.data
  } catch {}
})
</script>

<style scoped>
.trending-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  min-height: 100px;
}
.tag-item {
  cursor: pointer;
}
</style>
