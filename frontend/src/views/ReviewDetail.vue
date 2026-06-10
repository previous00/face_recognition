<template>
  <div class="review-detail" v-if="review">
    <el-card>
      <div class="review-header">
        <h2>{{ review.title }}</h2>
        <div class="meta">
          <span class="author">{{ review.user.nickname || review.user.username }}</span>
          <el-rate :model-value="review.rating" disabled />
          <span class="date">{{ new Date(review.created_at).toLocaleString() }}</span>
          <router-link :to="`/movies/${review.movie}`" class="movie-link">电影: {{ review.movie_title }}</router-link>
        </div>
      </div>
      <div class="content">{{ review.content }}</div>
    </el-card>

    <el-card class="comments-section">
      <template #header>
        <h3>评论 ({{ review.comments?.length || 0 }})</h3>
      </template>

      <div v-if="userStore.isLoggedIn" class="comment-form">
        <el-input v-model="commentContent" type="textarea" :rows="3" placeholder="写下你的评论..." />
        <el-button type="primary" size="small" @click="submitComment" :loading="submitting" style="margin-top: 8px;">发表评论</el-button>
      </div>
      <p v-else class="login-hint"><router-link to="/login">登录</router-link>后参与评论</p>

      <div class="comments-list">
        <div v-for="comment in review.comments" :key="comment.id" class="comment-item">
          <div class="comment-header">
            <strong>{{ comment.user.nickname || comment.user.username }}</strong>
            <span class="time">{{ new Date(comment.created_at).toLocaleString() }}</span>
          </div>
          <p>{{ comment.content }}</p>
          <div class="reply-area">
            <el-button text size="small" @click="replyTo = comment.id" v-if="userStore.isLoggedIn">回复</el-button>
            <div v-if="replyTo === comment.id" class="reply-form">
              <el-input v-model="replyContent" size="small" placeholder="回复..." />
              <el-button size="small" type="primary" @click="submitReply(comment.id)">发送</el-button>
              <el-button size="small" @click="replyTo = null">取消</el-button>
            </div>
          </div>
          <div v-if="comment.replies && comment.replies.length" class="nested-replies">
            <div v-for="reply in comment.replies" :key="reply.id" class="reply-item">
              <strong>{{ reply.user.nickname || reply.user.username }}</strong>
              <span class="time">{{ new Date(reply.created_at).toLocaleString() }}</span>
              <p>{{ reply.content }}</p>
            </div>
          </div>
        </div>
        <el-empty v-if="!review.comments || review.comments.length === 0" description="暂无评论" />
      </div>
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
const review = ref(null)
const commentContent = ref('')
const replyTo = ref(null)
const replyContent = ref('')
const submitting = ref(false)

async function fetchReview() {
  const res = await api.get(`/reviews/${route.params.id}/`)
  review.value = res.data
}

async function submitComment() {
  if (!commentContent.value.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }
  submitting.value = true
  try {
    await api.post(`/reviews/${route.params.id}/comments/`, { content: commentContent.value })
    ElMessage.success('评论成功')
    commentContent.value = ''
    fetchReview()
  } catch {
    ElMessage.error('评论失败')
  } finally {
    submitting.value = false
  }
}

async function submitReply(parentId) {
  if (!replyContent.value.trim()) return
  try {
    await api.post(`/reviews/${route.params.id}/comments/`, { content: replyContent.value, parent: parentId })
    ElMessage.success('回复成功')
    replyContent.value = ''
    replyTo.value = null
    fetchReview()
  } catch {
    ElMessage.error('回复失败')
  }
}

onMounted(fetchReview)
</script>

<style scoped>
.review-header h2 { margin-bottom: 12px; }
.meta { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; color: #666; font-size: 14px; }
.movie-link { color: #409eff; }
.content { margin-top: 20px; line-height: 1.8; white-space: pre-wrap; }
.comments-section { margin-top: 20px; }
.comment-form { margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid #f0f0f0; }
.login-hint { color: #999; margin-bottom: 16px; }
.login-hint a { color: #409eff; }
.comment-item { padding: 12px 0; border-bottom: 1px solid #f5f5f5; }
.comment-header { display: flex; align-items: center; gap: 12px; margin-bottom: 6px; }
.time { color: #999; font-size: 12px; }
.reply-area { margin-top: 6px; }
.reply-form { display: flex; gap: 8px; margin-top: 8px; align-items: center; }
.nested-replies { margin-left: 24px; margin-top: 8px; padding-left: 12px; border-left: 2px solid #f0f0f0; }
.reply-item { padding: 8px 0; }
.reply-item p { margin-top: 4px; }
</style>
