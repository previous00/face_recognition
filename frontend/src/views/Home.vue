<template>
  <div class="home">
    <div class="search-bar">
      <el-input v-model="searchQuery" placeholder="搜索电影名称、导演、演员..." clearable @keyup.enter="fetchMovies" style="width: 300px;">
        <template #append>
          <el-button @click="fetchMovies"><el-icon><Search /></el-icon></el-button>
        </template>
      </el-input>
      <el-select v-model="selectedCategory" @change="fetchMovies" style="width: 150px; margin-left: 12px;">
        <el-option label="全部分类" value="" />
        <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
      </el-select>
    </div>

    <div class="movie-grid">
      <div v-for="movie in movies" :key="movie.id" class="movie-card" @click="$router.push(`/movies/${movie.id}`)">
        <div class="movie-poster">
          <img v-if="movie.poster" :src="movie.poster" :alt="movie.title" />
          <div v-else class="no-poster">{{ movie.title }}</div>
        </div>
        <div class="movie-info">
          <h3>{{ movie.title }}</h3>
          <p class="director">导演: {{ movie.director }}</p>
          <div class="meta">
            <el-rate :model-value="Number(movie.rating)" disabled allow-half />
            <span class="score">{{ movie.rating > 0 ? movie.rating + '分' : '暂无评分' }}</span>
            <span class="rating-count" v-if="movie.rating_count > 0">({{ movie.rating_count }}人评)</span>
          </div>
          <div class="stats">
            <span><el-icon><Star /></el-icon>{{ movie.favorites_count }}</span>
            <span><el-icon><ChatDotRound /></el-icon>{{ movie.reviews_count }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="pagination">
      <el-pagination v-model:current-page="currentPage" :page-size="10" :total="totalCount" layout="prev, pager, next" @current-change="fetchMovies" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const movies = ref([])
const categories = ref([])
const searchQuery = ref('')
const selectedCategory = ref('')
const currentPage = ref(1)
const totalCount = ref(0)

async function fetchMovies() {
  const params = { page: currentPage.value }
  if (searchQuery.value) params.search = searchQuery.value
  if (selectedCategory.value) params.category = selectedCategory.value
  const res = await api.get('/movies/', { params })
  movies.value = res.data.results
  totalCount.value = res.data.count
}

async function fetchCategories() {
  const res = await api.get('/categories/')
  categories.value = res.data
}

onMounted(() => {
  fetchMovies()
  fetchCategories()
})
</script>

<style scoped>
.search-bar { margin-bottom: 24px; display: flex; align-items: center; }
.movie-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 20px; }
.movie-card { background: #fff; border-radius: 8px; overflow: hidden; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.movie-card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,0.12); }
.movie-poster { height: 200px; overflow: hidden; background: #e8e8e8; display: flex; align-items: center; justify-content: center; }
.movie-poster img { width: 100%; height: 100%; object-fit: cover; }
.no-poster { color: #999; font-size: 16px; text-align: center; padding: 20px; }
.movie-info { padding: 12px 16px; }
.movie-info h3 { font-size: 16px; margin-bottom: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.director { color: #666; font-size: 13px; margin-bottom: 8px; }
.meta { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
.score { font-size: 13px; color: #ff9900; font-weight: 500; }
.rating-count { font-size: 12px; color: #999; }
.stats { font-size: 12px; color: #999; display: flex; align-items: center; gap: 12px; }
.stats span { display: flex; align-items: center; gap: 3px; }
.pagination { margin-top: 24px; display: flex; justify-content: center; }
</style>
