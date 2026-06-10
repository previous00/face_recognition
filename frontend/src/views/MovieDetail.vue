<template>
  <div class="movie-detail" v-if="movie">
    <el-card>
      <div class="movie-header">
        <div class="poster">
          <img v-if="movie.poster" :src="movie.poster" :alt="movie.title" />
          <div v-else class="no-poster">暂无海报</div>
        </div>
        <div class="info">
          <h1>{{ movie.title }}</h1>
          <p><strong>导演:</strong> {{ movie.director }}</p>
          <p><strong>主演:</strong> {{ movie.actors }}</p>
          <p><strong>上映日期:</strong> {{ movie.release_date }}</p>
          <p><strong>片长:</strong> {{ movie.duration }}分钟</p>
          <p><strong>分类:</strong> {{ movie.category_name }}</p>
          <p><strong>评分:</strong> <el-rate :model-value="Number(movie.rating)" disabled allow-half />
            <span v-if="movie.rating > 0">{{ movie.rating }}分 ({{ movie.rating_count }}人评价)</span>
            <span v-else style="color: #999;">暂无评分</span>
          </p>
          <div class="actions">
            <el-button :type="isFavorited ? 'warning' : 'default'" @click="toggleFavorite" :disabled="!userStore.isLoggedIn">
              <el-icon><Star /></el-icon> {{ isFavorited ? '已收藏' : '收藏' }}
            </el-button>
          </div>
        </div>
      </div>
      <div class="description">
        <h3>剧情简介</h3>
        <p>{{ movie.description }}</p>
      </div>
    </el-card>

    <el-card class="reviews-section">
      <template #header>
        <div class="section-header">
          <h3>影评 ({{ reviews.length }})</h3>
          <el-button v-if="userStore.isLoggedIn" type="primary" size="small" @click="showReviewForm = true">写影评</el-button>
        </div>
      </template>

      <el-dialog v-model="showReviewForm" title="发表影评" width="500px">
        <el-form :model="reviewForm">
          <el-form-item label="评分" required>
            <el-rate v-model="reviewForm.rating" />
          </el-form-item>
          <el-form-item label="标题">
            <el-input v-model="reviewForm.title" placeholder="选填" />
          </el-form-item>
          <el-form-item label="内容">
            <el-input v-model="reviewForm.content" type="textarea" :rows="5" placeholder="选填，写下你的观影感受" />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="showReviewForm = false">取消</el-button>
          <el-button type="primary" @click="submitReview" :loading="submitting">发表</el-button>
        </template>
      </el-dialog>

      <div v-for="review in reviews" :key="review.id" class="review-item" @click="$router.push(`/reviews/${review.id}`)">
        <div class="review-header">
          <span class="author">{{ review.user.nickname || review.user.username }}</span>
          <el-rate :model-value="review.rating" disabled size="small" />
          <span class="date">{{ new Date(review.created_at).toLocaleDateString() }}</span>
        </div>
        <h4>{{ review.title }}</h4>
        <p class="comments-count"><el-icon><ChatDotRound /></el-icon> {{ review.comments_count }} 条评论</p>
      </div>
      <el-empty v-if="reviews.length === 0" description="暂无影评" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '../stores/user'
import { ElMessage } from 'element-plus'
import api from '../api'

const route = useRoute()
const userStore = useUserStore()
const movie = ref(null)
const reviews = ref([])
const isFavorited = ref(false)
const favoriteId = ref(null)
const showReviewForm = ref(false)
const submitting = ref(false)
const reviewForm = ref({ title: '', content: '', rating: 5 })

async function fetchMovie() {
  const res = await api.get(`/movies/${route.params.id}/`)
  movie.value = res.data
}

async function fetchReviews() {
  const res = await api.get('/reviews/', { params: { movie: route.params.id } })
  reviews.value = res.data.results
}

async function checkFavorite() {
  if (!userStore.isLoggedIn) return
  try {
    const res = await api.get('/favorites/')
    const fav = res.data.results.find(f => f.movie == route.params.id)
    if (fav) {
      isFavorited.value = true
      favoriteId.value = fav.id
    }
  } catch {}
}

async function toggleFavorite() {
  if (!userStore.isLoggedIn) return
  try {
    if (isFavorited.value) {
      await api.delete(`/favorites/${favoriteId.value}/`)
      isFavorited.value = false
      favoriteId.value = null
      ElMessage.success('已取消收藏')
    } else {
      const res = await api.post('/favorites/', { movie: route.params.id })
      isFavorited.value = true
      favoriteId.value = res.data.id
      ElMessage.success('收藏成功')
    }
  } catch (e) {
    ElMessage.error('操作失败')
  }
}

async function submitReview() {
  submitting.value = true
  try {
    await api.post('/reviews/', { ...reviewForm.value, movie: route.params.id })
    ElMessage.success('发表成功')
    showReviewForm.value = false
    reviewForm.value = { title: '', content: '', rating: 5 }
    fetchReviews()
    fetchMovie()
  } catch (e) {
    if (e.response?.status === 400) ElMessage.error('您已对该电影发表过影评')
    else ElMessage.error('发表失败')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchMovie()
  fetchReviews()
  checkFavorite()
})
</script>

<style scoped>
.movie-header { display: flex; gap: 24px; margin-bottom: 24px; }
.poster { width: 240px; height: 340px; flex-shrink: 0; background: #f0f0f0; border-radius: 8px; overflow: hidden; }
.poster img { width: 100%; height: 100%; object-fit: cover; }
.no-poster { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; color: #999; }
.info h1 { margin-bottom: 12px; }
.info p { margin-bottom: 8px; color: #555; }
.actions { margin-top: 16px; }
.description { border-top: 1px solid #eee; padding-top: 16px; }
.description h3 { margin-bottom: 8px; }
.reviews-section { margin-top: 20px; }
.section-header { display: flex; justify-content: space-between; align-items: center; }
.review-item { padding: 12px 0; border-bottom: 1px solid #f0f0f0; cursor: pointer; }
.review-item:hover { background: #fafafa; }
.review-header { display: flex; align-items: center; gap: 12px; margin-bottom: 6px; }
.author { font-weight: 500; color: #333; }
.date { color: #999; font-size: 12px; }
.review-item h4 { margin-bottom: 4px; }
.comments-count { color: #999; font-size: 13px; display: flex; align-items: center; gap: 4px; }
</style>
