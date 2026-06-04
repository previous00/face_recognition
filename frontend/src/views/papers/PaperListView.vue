<template>
  <div class="page-container">
    <div class="page-header">
      <h2>论文管理</h2>
      <el-button type="primary" @click="$router.push('/papers/create')">
        <el-icon><Plus /></el-icon>添加论文
      </el-button>
    </div>

    <el-card style="margin-bottom: 20px">
      <el-form :inline="true" :model="filters">
        <el-form-item>
          <el-input v-model="filters.search" placeholder="搜索标题/作者/关键词" clearable @clear="fetchData" @keyup.enter="fetchData" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="filters.source_journal" placeholder="来源期刊" clearable @clear="fetchData" />
        </el-form-item>
        <el-form-item>
          <el-date-picker v-model="filters.dateRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">搜索</el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-table :data="papers" v-loading="loading" style="width: 100%">
      <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip>
        <template #default="{ row }">
          <router-link :to="`/papers/${row.id}`" class="link">{{ row.title }}</router-link>
        </template>
      </el-table-column>
      <el-table-column prop="authors" label="作者" width="150" show-overflow-tooltip />
      <el-table-column prop="source_journal" label="期刊" width="150" show-overflow-tooltip />
      <el-table-column prop="publication_date" label="发表日期" width="110" />
      <el-table-column prop="view_count" label="浏览" width="70" />
      <el-table-column label="收藏" width="80" align="center">
        <template #default="{ row }">
          <el-button link :type="favoritedMap[row.id] ? 'warning' : 'default'" @click="toggleFavorite(row)">
            <el-icon :size="18"><StarFilled v-if="favoritedMap[row.id]" /><Star v-else /></el-icon>
          </el-button>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" v-if="canEdit(row)" @click="$router.push(`/papers/${row.id}/edit`)">编辑</el-button>
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
import { getPapers, deletePaper } from '@/api/papers'
import { getFavoritePapers, addFavorite, removeFavorite } from '@/api/favorites'
import { useAuthStore } from '@/stores/auth'
import { ElMessage, ElMessageBox } from 'element-plus'

const authStore = useAuthStore()
const papers = ref([])
const loading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const favoritedMap = ref({})
const favoriteIdMap = ref({})

const filters = reactive({
  search: '',
  source_journal: '',
  dateRange: null,
})

const canEdit = (row) => {
  return authStore.isAdmin || row.uploaded_by_name === authStore.user?.username
}

const fetchFavorites = async () => {
  try {
    const res = await getFavoritePapers()
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
      const res = await addFavorite({ type: 'paper', object_id: row.id })
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
      source_journal: filters.source_journal || undefined,
      publication_date_after: filters.dateRange?.[0] || undefined,
      publication_date_before: filters.dateRange?.[1] || undefined,
    }
    const res = await getPapers(params)
    papers.value = res.data.results
    total.value = res.data.count
  } catch {
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  filters.search = ''
  filters.source_journal = ''
  filters.dateRange = null
  currentPage.value = 1
  fetchData()
}

const handlePageChange = (page) => {
  currentPage.value = page
  fetchData()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  fetchData()
}

const handleDelete = async (row) => {
  await ElMessageBox.confirm('确定要删除该论文吗？', '提示', { type: 'warning' })
  try {
    await deletePaper(row.id)
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
.link {
  color: #409eff;
  text-decoration: none;
}
.link:hover {
  text-decoration: underline;
}
</style>
