<template>
  <div class="page-container">
    <div class="page-header">
      <h2>科研项目</h2>
      <el-button type="primary" @click="$router.push('/projects/create')">
        <el-icon><Plus /></el-icon>新建项目
      </el-button>
    </div>

    <el-card style="margin-bottom: 20px">
      <el-form :inline="true" :model="filters">
        <el-form-item>
          <el-input v-model="filters.search" placeholder="搜索项目名称/负责人" clearable @clear="fetchData" @keyup.enter="fetchData" />
        </el-form-item>
        <el-form-item>
          <el-select v-model="filters.status" placeholder="状态" clearable @change="fetchData">
            <el-option label="规划中" value="planning" />
            <el-option label="进行中" value="active" />
            <el-option label="已完成" value="completed" />
            <el-option label="已暂停" value="suspended" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-input v-model="filters.funding_source" placeholder="资助来源" clearable @clear="fetchData" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">搜索</el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-table :data="projects" v-loading="loading" style="width: 100%">
      <el-table-column prop="title" label="项目名称" min-width="200" show-overflow-tooltip>
        <template #default="{ row }">
          <router-link :to="`/projects/${row.id}`" class="link">{{ row.title }}</router-link>
        </template>
      </el-table-column>
      <el-table-column prop="principal_investigator" label="负责人" width="120" />
      <el-table-column prop="status" label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="statusTagType(row.status)" size="small">{{ statusLabel(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="funding_source" label="资助来源" width="150" show-overflow-tooltip />
      <el-table-column prop="member_count" label="成员" width="70" />
      <el-table-column prop="start_date" label="开始日期" width="110" />
      <el-table-column label="收藏" width="80" align="center">
        <template #default="{ row }">
          <el-button link :type="favoritedMap[row.id] ? 'warning' : 'default'" @click="toggleFavorite(row)">
            <el-icon :size="18"><StarFilled v-if="favoritedMap[row.id]" /><Star v-else /></el-icon>
          </el-button>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" v-if="canEdit(row)" @click="$router.push(`/projects/${row.id}/edit`)">编辑</el-button>
          <el-button link type="danger" v-if="canEdit(row)" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-if="total > 0"
      style="margin-top: 20px; justify-content: center"
      background
      layout="total, prev, pager, next, sizes"
      :total="total"
      :page-size="pageSize"
      :current-page="currentPage"
      :page-sizes="[10, 20, 50]"
      @current-change="handlePageChange"
      @size-change="handleSizeChange"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getProjects, deleteProject } from '@/api/projects'
import { getFavoriteProjects, addFavorite, removeFavorite } from '@/api/favorites'
import { useAuthStore } from '@/stores/auth'
import { ElMessage, ElMessageBox } from 'element-plus'

const authStore = useAuthStore()
const projects = ref([])
const loading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const favoritedMap = ref({})
const favoriteIdMap = ref({})

const filters = reactive({
  search: '',
  status: '',
  funding_source: '',
})

const statusLabel = (s) => ({ planning: '规划中', active: '进行中', completed: '已完成', suspended: '已暂停' }[s] || s)
const statusTagType = (s) => ({ planning: 'info', active: 'success', completed: '', suspended: 'warning' }[s] || '')

const canEdit = (row) => {
  return authStore.isAdmin || row.created_by_name === authStore.user?.username
}

const fetchFavorites = async () => {
  try {
    const res = await getFavoriteProjects()
    const map = {}
    const idMap = {}
    res.data.forEach(fav => {
      map[fav.object_id] = true
      idMap[fav.object_id] = fav.id
    })
    favoritedMap.value = map
    favoriteIdMap.value = idMap
  } catch {}
}

const toggleFavorite = async (row) => {
  try {
    if (favoritedMap.value[row.id]) {
      await removeFavorite(favoriteIdMap.value[row.id])
      delete favoritedMap.value[row.id]
      delete favoriteIdMap.value[row.id]
      ElMessage.success('已取消收藏')
    } else {
      const res = await addFavorite({ type: 'project', object_id: row.id })
      favoritedMap.value[row.id] = true
      favoriteIdMap.value[row.id] = res.data.id
      ElMessage.success('收藏成功')
    }
  } catch {
    ElMessage.error('操作失败')
  }
}

const fetchData = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      search: filters.search || undefined,
      status: filters.status || undefined,
      funding_source: filters.funding_source || undefined,
    }
    const res = await getProjects(params)
    projects.value = res.data.results
    total.value = res.data.count
  } catch {
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  filters.search = ''
  filters.status = ''
  filters.funding_source = ''
  currentPage.value = 1
  fetchData()
}

const handlePageChange = (page) => { currentPage.value = page; fetchData() }
const handleSizeChange = (size) => { pageSize.value = size; currentPage.value = 1; fetchData() }

const handleDelete = async (row) => {
  await ElMessageBox.confirm('确定要删除该项目吗？', '提示', { type: 'warning' })
  try {
    await deleteProject(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch {
    ElMessage.error('删除失败')
  }
}

onMounted(() => {
  fetchData()
  fetchFavorites()
})
</script>

<style scoped>
.link { color: #409eff; text-decoration: none; }
.link:hover { text-decoration: underline; }
</style>
