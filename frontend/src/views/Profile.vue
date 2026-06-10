<template>
  <div class="profile">
    <el-card class="user-card">
      <h2>个人中心</h2>
      <div class="user-info" v-if="userStore.userInfo">
        <p><strong>用户名:</strong> {{ userStore.userInfo.username }}</p>
        <p><strong>昵称:</strong> {{ userStore.userInfo.nickname || '未设置' }}</p>
        <p><strong>邮箱:</strong> {{ userStore.userInfo.email }}</p>
        <p><strong>简介:</strong> {{ userStore.userInfo.bio || '这个人很懒，什么都没写' }}</p>
      </div>
    </el-card>

    <el-tabs v-model="activeTab" @tab-change="handleTabChange">
      <el-tab-pane label="我的收藏" name="favorites">
        <div v-for="fav in favorites" :key="fav.id" class="list-item" @click="$router.push(`/movies/${fav.movie_detail.id}`)">
          <div class="item-info">
            <h4>{{ fav.movie_detail.title }}</h4>
            <p>导演: {{ fav.movie_detail.director }} | 评分: {{ fav.movie_detail.rating }}</p>
          </div>
          <el-button type="danger" size="small" @click.stop="removeFavorite(fav.id)">取消收藏</el-button>
        </div>
        <el-empty v-if="favorites.length === 0" description="暂无收藏" />
      </el-tab-pane>

      <el-tab-pane label="我的影评" name="reviews">
        <div v-for="review in myReviews" :key="review.id" class="list-item" @click="$router.push(`/reviews/${review.id}`)">
          <div class="item-info">
            <h4>{{ review.title }}</h4>
            <p>电影: {{ review.movie_title }} | <el-rate :model-value="review.rating" disabled size="small" /></p>
          </div>
          <span class="date">{{ new Date(review.created_at).toLocaleDateString() }}</span>
        </div>
        <el-empty v-if="myReviews.length === 0" description="暂无影评" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '../stores/user'
import { ElMessage } from 'element-plus'
import api from '../api'

const userStore = useUserStore()
const activeTab = ref('favorites')
const favorites = ref([])
const myReviews = ref([])

async function fetchFavorites() {
  const res = await api.get('/favorites/')
  favorites.value = res.data.results
}

async function fetchMyReviews() {
  const res = await api.get('/reviews/', { params: { user: userStore.userInfo.id } })
  myReviews.value = res.data.results
}

async function removeFavorite(id) {
  await api.delete(`/favorites/${id}/`)
  ElMessage.success('已取消收藏')
  fetchFavorites()
}

function handleTabChange(tab) {
  if (tab === 'favorites') fetchFavorites()
  else fetchMyReviews()
}

onMounted(() => {
  fetchFavorites()
  fetchMyReviews()
})
</script>

<style scoped>
.user-card { margin-bottom: 20px; }
.user-card h2 { margin-bottom: 16px; }
.user-info p { margin-bottom: 8px; color: #555; }
.list-item { display: flex; justify-content: space-between; align-items: center; padding: 12px 16px; border-bottom: 1px solid #f0f0f0; cursor: pointer; border-radius: 4px; }
.list-item:hover { background: #fafafa; }
.item-info h4 { margin-bottom: 4px; }
.item-info p { color: #666; font-size: 13px; display: flex; align-items: center; gap: 8px; }
.date { color: #999; font-size: 13px; }
</style>
