<template>
  <div class="page-container">
    <el-card v-loading="loading">
      <template #header>
        <div class="page-header">
          <h2>{{ project.title }}</h2>
          <div>
            <el-button :type="isFavorited ? 'warning' : 'default'" @click="toggleFavorite">
              <el-icon><Star /></el-icon>{{ isFavorited ? '已收藏' : '收藏' }}
            </el-button>
            <el-button type="success" @click="handleJoin" v-if="!isMember">加入项目</el-button>
            <el-button type="warning" @click="handleLeave" v-else>退出项目</el-button>
            <el-button @click="$router.back()">返回</el-button>
          </div>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="项目负责人">{{ project.principal_investigator }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="statusTagType(project.status)">{{ statusLabel(project.status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="资助来源">{{ project.funding_source }}</el-descriptions-item>
        <el-descriptions-item label="经费(万元)">{{ project.budget }}</el-descriptions-item>
        <el-descriptions-item label="开始日期">{{ project.start_date }}</el-descriptions-item>
        <el-descriptions-item label="结束日期">{{ project.end_date }}</el-descriptions-item>
        <el-descriptions-item label="浏览次数">{{ project.view_count }}</el-descriptions-item>
        <el-descriptions-item label="创建者">{{ project.created_by_name }}</el-descriptions-item>
      </el-descriptions>

      <div style="margin-top: 20px" v-if="project.description">
        <h4 style="margin-bottom: 10px">项目描述</h4>
        <p style="line-height: 1.8; color: #606266">{{ project.description }}</p>
      </div>

      <div style="margin-top: 20px" v-if="project.members?.length">
        <h4 style="margin-bottom: 10px">项目成员 ({{ project.members.length }}人)</h4>
        <el-tag v-for="m in project.members" :key="m.id" style="margin-right: 8px; margin-bottom: 5px">
          {{ m.username }} <span v-if="m.institution">- {{ m.institution }}</span>
        </el-tag>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getProject, joinProject, leaveProject } from '@/api/projects'
import { checkFavorite, addFavorite, removeFavorite, getFavoriteProjects } from '@/api/favorites'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const route = useRoute()
const authStore = useAuthStore()
const project = ref({})
const loading = ref(false)
const isFavorited = ref(false)
const favoriteId = ref(null)

const isMember = computed(() => {
  return project.value.members?.some(m => m.id === authStore.user?.id)
})

const statusLabel = (s) => ({ planning: '规划中', active: '进行中', completed: '已完成', suspended: '已暂停' }[s] || s)
const statusTagType = (s) => ({ planning: 'info', active: 'success', completed: '', suspended: 'warning' }[s] || '')

onMounted(async () => {
  loading.value = true
  try {
    const res = await getProject(route.params.id)
    project.value = res.data
    const favRes = await checkFavorite({ type: 'project', object_id: parseInt(route.params.id) })
    isFavorited.value = favRes.data.is_favorited
    if (isFavorited.value) {
      const allFavs = await getFavoriteProjects()
      const found = allFavs.data.find(f => f.object_id === parseInt(route.params.id))
      if (found) favoriteId.value = found.id
    }
  } catch {
    ElMessage.error('获取项目详情失败')
  } finally {
    loading.value = false
  }
})

const toggleFavorite = async () => {
  try {
    if (isFavorited.value) {
      if (favoriteId.value) await removeFavorite(favoriteId.value)
      isFavorited.value = false
      ElMessage.success('已取消收藏')
    } else {
      const res = await addFavorite({ type: 'project', object_id: parseInt(route.params.id) })
      isFavorited.value = true
      if (res.data.id) favoriteId.value = res.data.id
      ElMessage.success('收藏成功')
    }
  } catch {
    ElMessage.error('操作失败')
  }
}

const handleJoin = async () => {
  try {
    await joinProject(route.params.id)
    ElMessage.success('已加入项目')
    const res = await getProject(route.params.id)
    project.value = res.data
  } catch {
    ElMessage.error('操作失败')
  }
}

const handleLeave = async () => {
  try {
    await leaveProject(route.params.id)
    ElMessage.success('已退出项目')
    const res = await getProject(route.params.id)
    project.value = res.data
  } catch {
    ElMessage.error('操作失败')
  }
}
</script>
