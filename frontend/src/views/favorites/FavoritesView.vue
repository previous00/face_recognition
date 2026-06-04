<template>
  <div class="page-container">
    <h2 style="margin-bottom: 20px">我的收藏</h2>
    <el-tabs v-model="activeTab" @tab-change="handleTabChange">
      <el-tab-pane label="收藏的论文" name="papers">
        <el-table :data="papers" v-loading="loading">
          <el-table-column prop="content_object_data.title" label="标题" min-width="200" show-overflow-tooltip>
            <template #default="{ row }">
              <router-link :to="`/papers/${row.object_id}`" class="link">
                {{ row.content_object_data?.title }}
              </router-link>
            </template>
          </el-table-column>
          <el-table-column label="作者" width="150" show-overflow-tooltip>
            <template #default="{ row }">{{ row.content_object_data?.authors }}</template>
          </el-table-column>
          <el-table-column prop="created_at" label="收藏时间" width="180">
            <template #default="{ row }">{{ row.created_at?.slice(0, 10) }}</template>
          </el-table-column>
          <el-table-column label="操作" width="100">
            <template #default="{ row }">
              <el-button link type="danger" @click="handleRemove(row)">取消收藏</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <el-tab-pane label="收藏的项目" name="projects">
        <el-table :data="projects" v-loading="loading">
          <el-table-column label="项目名称" min-width="200" show-overflow-tooltip>
            <template #default="{ row }">
              <router-link :to="`/projects/${row.object_id}`" class="link">
                {{ row.content_object_data?.title }}
              </router-link>
            </template>
          </el-table-column>
          <el-table-column label="负责人" width="120">
            <template #default="{ row }">{{ row.content_object_data?.principal_investigator }}</template>
          </el-table-column>
          <el-table-column label="状态" width="90">
            <template #default="{ row }">{{ row.content_object_data?.status }}</template>
          </el-table-column>
          <el-table-column prop="created_at" label="收藏时间" width="180">
            <template #default="{ row }">{{ row.created_at?.slice(0, 10) }}</template>
          </el-table-column>
          <el-table-column label="操作" width="100">
            <template #default="{ row }">
              <el-button link type="danger" @click="handleRemove(row)">取消收藏</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getFavoritePapers, getFavoriteProjects, removeFavorite } from '@/api/favorites'
import { ElMessage } from 'element-plus'

const activeTab = ref('papers')
const papers = ref([])
const projects = ref([])
const loading = ref(false)

const fetchPapers = async () => {
  loading.value = true
  try {
    const res = await getFavoritePapers()
    papers.value = res.data
  } catch {} finally {
    loading.value = false
  }
}

const fetchProjects = async () => {
  loading.value = true
  try {
    const res = await getFavoriteProjects()
    projects.value = res.data
  } catch {} finally {
    loading.value = false
  }
}

const handleTabChange = (tab) => {
  if (tab === 'papers') fetchPapers()
  else fetchProjects()
}

const handleRemove = async (row) => {
  try {
    await removeFavorite(row.id)
    ElMessage.success('已取消收藏')
    if (activeTab.value === 'papers') fetchPapers()
    else fetchProjects()
  } catch {
    ElMessage.error('操作失败')
  }
}

onMounted(fetchPapers)
</script>

<style scoped>
.link { color: #409eff; text-decoration: none; }
.link:hover { text-decoration: underline; }
</style>
