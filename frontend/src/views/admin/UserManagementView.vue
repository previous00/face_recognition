<template>
  <div class="page-container">
    <h2 style="margin-bottom: 20px">用户管理</h2>
    <el-alert
      v-if="authStore.user?.role === 'super_admin'"
      type="info"
      :closable="false"
      style="margin-bottom: 16px"
    >
      当前身份：超级管理员，可以设置管理员和普通用户角色
    </el-alert>
    <el-alert
      v-else
      type="warning"
      :closable="false"
      style="margin-bottom: 16px"
    >
      当前身份：管理员，只能管理普通用户（如需设置管理员角色请联系超级管理员）
    </el-alert>

    <el-table :data="users" v-loading="loading" style="width: 100%">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="username" label="用户名" width="120" />
      <el-table-column prop="email" label="邮箱" width="200" />
      <el-table-column prop="role" label="角色" width="120">
        <template #default="{ row }">
          <el-tag :type="roleTagType(row.role)">{{ roleLabel(row.role) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="institution" label="机构" show-overflow-tooltip />
      <el-table-column prop="is_active" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'info'">
            {{ row.is_active ? '正常' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="date_joined" label="注册时间" width="120">
        <template #default="{ row }">{{ row.date_joined?.slice(0, 10) }}</template>
      </el-table-column>
      <el-table-column label="操作" width="240" fixed="right">
        <template #default="{ row }">
          <template v-if="canManage(row)">
            <el-dropdown v-if="authStore.user?.role === 'super_admin'" trigger="click" @command="(cmd) => handleSetRole(row, cmd)">
              <el-button link type="primary">设置角色</el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="admin" :disabled="row.role === 'admin'">设为管理员</el-dropdown-item>
                  <el-dropdown-item command="user" :disabled="row.role === 'user'">设为普通用户</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
            <el-button link :type="row.is_active ? 'danger' : 'success'" @click="handleToggleActive(row)">
              {{ row.is_active ? '禁用' : '启用' }}
            </el-button>
          </template>
          <span v-else style="color: #c0c4cc; font-size: 12px">无权操作</span>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getUsers, setUserRole, toggleUserActive } from '@/api/users'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'

const authStore = useAuthStore()
const users = ref([])
const loading = ref(false)

const roleLabel = (r) => ({ super_admin: '超级管理员', admin: '管理员', user: '普通用户' }[r] || r)
const roleTagType = (r) => ({ super_admin: 'danger', admin: 'warning', user: '' }[r] || '')

const canManage = (row) => {
  if (row.id === authStore.user?.id) return false
  if (row.role === 'super_admin') return false
  if (row.role === 'admin' && authStore.user?.role !== 'super_admin') return false
  return true
}

const fetchData = async () => {
  loading.value = true
  try {
    const res = await getUsers()
    users.value = res.data.results || res.data
  } catch {} finally {
    loading.value = false
  }
}

const handleSetRole = async (row, newRole) => {
  try {
    const res = await setUserRole(row.id, newRole)
    row.role = res.data.role
    ElMessage.success(`已将 ${row.username} 设为${roleLabel(newRole)}`)
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '操作失败')
  }
}

const handleToggleActive = async (row) => {
  try {
    const res = await toggleUserActive(row.id)
    row.is_active = res.data.is_active
    ElMessage.success(row.is_active ? '已启用' : '已禁用')
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '操作失败')
  }
}

onMounted(fetchData)
</script>
