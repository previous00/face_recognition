<template>
  <div class="page-container">
    <el-card v-loading="loading">
      <template #header>
        <div class="page-header">
          <h2>{{ paper.title }}</h2>
          <div>
            <el-button :type="isFavorited ? 'warning' : 'default'" @click="toggleFavorite">
              <el-icon><Star /></el-icon>{{ isFavorited ? '已收藏' : '收藏' }}
            </el-button>
            <el-button type="primary" v-if="paper.file" @click="handleDownload">
              <el-icon><Download /></el-icon>下载
            </el-button>
            <el-button type="primary" v-if="canEdit" @click="router.push(`/papers/${route.params.id}/edit`)">
              <el-icon><Edit /></el-icon>编辑
            </el-button>
            <el-button @click="$router.back()">返回</el-button>
          </div>
        </div>
      </template>

      <el-descriptions :column="2" border>
        <el-descriptions-item label="作者">{{ paper.authors }}</el-descriptions-item>
        <el-descriptions-item label="来源期刊">{{ paper.source_journal }}</el-descriptions-item>
        <el-descriptions-item label="发表日期">{{ paper.publication_date }}</el-descriptions-item>
        <el-descriptions-item label="DOI">{{ paper.doi }}</el-descriptions-item>
        <el-descriptions-item label="关键词" :span="2">
          <el-tag v-for="kw in keywords" :key="kw" style="margin-right: 5px">{{ kw }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="浏览次数">{{ paper.view_count }}</el-descriptions-item>
        <el-descriptions-item label="下载次数">{{ paper.download_count }}</el-descriptions-item>
        <el-descriptions-item label="上传者">{{ paper.uploaded_by_name }}</el-descriptions-item>
        <el-descriptions-item label="上传时间">{{ paper.created_at?.slice(0, 10) }}</el-descriptions-item>
      </el-descriptions>

      <div style="margin-top: 20px" v-if="paper.abstract">
        <h4 style="margin-bottom: 10px">摘要</h4>
        <p style="line-height: 1.8; color: #606266">{{ paper.abstract }}</p>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getPaper, downloadPaper } from '@/api/papers'
import { checkFavorite, addFavorite, removeFavorite, getFavoritePapers } from '@/api/favorites'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const paper = ref({})
const loading = ref(false)
const isFavorited = ref(false)
const favoriteId = ref(null)

const canEdit = computed(() => {
  return authStore.isAdmin || paper.value.uploaded_by_name === authStore.user?.username
})

const keywords = computed(() => {
  return paper.value.keywords ? paper.value.keywords.split(',').map(k => k.trim()).filter(Boolean) : []
})

onMounted(async () => {
  loading.value = true
  try {
    const res = await getPaper(route.params.id)
    paper.value = res.data
    const favRes = await checkFavorite({ type: 'paper', object_id: parseInt(route.params.id) })
    isFavorited.value = favRes.data.is_favorited
    if (isFavorited.value) {
      const allFavs = await getFavoritePapers()
      const found = allFavs.data.find(f => f.object_id === parseInt(route.params.id))
      if (found) favoriteId.value = found.id
    }
  } catch {
    ElMessage.error('获取论文详情失败')
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
      const res = await addFavorite({ type: 'paper', object_id: parseInt(route.params.id) })
      isFavorited.value = true
      if (res.data.id) favoriteId.value = res.data.id
      ElMessage.success('收藏成功')
    }
  } catch {
    ElMessage.error('操作失败')
  }
}

const handleDownload = async () => {
  try {
    const res = await downloadPaper(route.params.id)
    const url = URL.createObjectURL(new Blob([res.data]))
    const a = document.createElement('a')
    a.href = url
    a.download = paper.value.file?.split('/').pop() || 'paper'
    a.click()
    URL.revokeObjectURL(url)
  } catch {
    ElMessage.error('下载失败')
  }
}
</script>
