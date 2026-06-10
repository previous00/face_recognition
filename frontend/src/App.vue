<template>
  <el-container class="app-container">
    <el-header class="app-header">
      <div class="header-left">
        <router-link to="/" class="logo">电影交流社区</router-link>
      </div>
      <div class="header-right">
        <template v-if="userStore.isLoggedIn">
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              {{ userStore.userInfo?.nickname || userStore.userInfo?.username }}
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                <el-dropdown-item v-if="userStore.isAdmin" command="admin">电影管理</el-dropdown-item>
                <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <router-link to="/login"><el-button type="primary" size="small">登录</el-button></router-link>
          <router-link to="/register"><el-button size="small">注册</el-button></router-link>
        </template>
      </div>
    </el-header>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { useUserStore } from './stores/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

function handleCommand(cmd) {
  if (cmd === 'profile') router.push('/profile')
  else if (cmd === 'admin') router.push('/admin/movies')
  else if (cmd === 'logout') {
    userStore.logout()
    router.push('/')
  }
}
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f7fa; }
.app-container { min-height: 100vh; }
.app-header { display: flex; align-items: center; justify-content: space-between; background: #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.06); padding: 0 24px; }
.header-left .logo { font-size: 20px; font-weight: bold; color: #409eff; text-decoration: none; }
.header-right { display: flex; align-items: center; gap: 12px; }
.user-info { cursor: pointer; display: flex; align-items: center; gap: 4px; }
.el-main { max-width: 1200px; margin: 0 auto; padding: 24px; width: 100%; }
</style>
