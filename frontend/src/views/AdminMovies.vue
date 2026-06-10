<template>
  <div class="admin-movies">
    <div class="page-header">
      <h2>电影管理</h2>
      <el-button type="primary" @click="openDialog()">添加电影</el-button>
    </div>

    <el-table :data="movies" stripe>
      <el-table-column prop="title" label="片名" width="180" />
      <el-table-column prop="director" label="导演" width="120" />
      <el-table-column prop="category_name" label="分类" width="100" />
      <el-table-column prop="rating" label="评分" width="120">
        <template #default="{ row }">
          {{ row.rating > 0 ? row.rating + '分(' + row.rating_count + '人)' : '暂无' }}
        </template>
      </el-table-column>
      <el-table-column prop="release_date" label="上映日期" width="120" />
      <el-table-column label="操作" width="160">
        <template #default="{ row }">
          <el-button size="small" @click="openDialog(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="deleteMovie(row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination v-model:current-page="currentPage" :total="total" layout="prev, pager, next" @current-change="fetchMovies" style="margin-top: 16px; justify-content: center; display: flex;" />

    <el-dialog v-model="dialogVisible" :title="editingId ? '编辑电影' : '添加电影'" width="600px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="片名"><el-input v-model="form.title" /></el-form-item>
        <el-form-item label="导演"><el-input v-model="form.director" /></el-form-item>
        <el-form-item label="主演"><el-input v-model="form.actors" /></el-form-item>
        <el-form-item label="分类">
          <el-select v-model="form.category" placeholder="选择分类">
            <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="上映日期"><el-date-picker v-model="form.release_date" type="date" value-format="YYYY-MM-DD" /></el-form-item>
        <el-form-item label="片长(分钟)"><el-input-number v-model="form.duration" :min="1" /></el-form-item>
        <el-form-item label="简介"><el-input v-model="form.description" type="textarea" :rows="4" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveMovie" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '../api'

const movies = ref([])
const categories = ref([])
const currentPage = ref(1)
const total = ref(0)
const dialogVisible = ref(false)
const editingId = ref(null)
const saving = ref(false)

const emptyForm = { title: '', director: '', actors: '', category: null, release_date: '', duration: 120, description: '' }
const form = ref({ ...emptyForm })

async function fetchMovies() {
  const res = await api.get('/movies/', { params: { page: currentPage.value } })
  movies.value = res.data.results
  total.value = res.data.count
}

async function fetchCategories() {
  const res = await api.get('/categories/')
  categories.value = res.data
}

function openDialog(movie) {
  if (movie) {
    editingId.value = movie.id
    form.value = { title: movie.title, director: movie.director, actors: movie.actors, category: movie.category, release_date: movie.release_date, duration: movie.duration, description: movie.description }
  } else {
    editingId.value = null
    form.value = { ...emptyForm }
  }
  dialogVisible.value = true
}

async function saveMovie() {
  saving.value = true
  try {
    if (editingId.value) {
      await api.put(`/movies/${editingId.value}/`, form.value)
      ElMessage.success('更新成功')
    } else {
      await api.post('/movies/', form.value)
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    fetchMovies()
  } catch (e) {
    ElMessage.error('保存失败，请检查信息')
  } finally {
    saving.value = false
  }
}

async function deleteMovie(id) {
  await ElMessageBox.confirm('确定删除该电影？', '提示', { type: 'warning' })
  try {
    await api.delete(`/movies/${id}/`)
    ElMessage.success('删除成功')
    fetchMovies()
  } catch {
    ElMessage.error('删除失败')
  }
}

onMounted(() => {
  fetchMovies()
  fetchCategories()
})
</script>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
</style>
