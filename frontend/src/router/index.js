import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue'),
    meta: { guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/RegisterView.vue'),
    meta: { guest: true }
  },
  {
    path: '/',
    component: () => import('@/components/layout/AppLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      { path: '', name: 'Home', component: () => import('@/views/HomeView.vue') },
      { path: 'profile', name: 'Profile', component: () => import('@/views/ProfileView.vue') },
      { path: 'papers', name: 'Papers', component: () => import('@/views/papers/PaperListView.vue') },
      { path: 'papers/create', name: 'PaperCreate', component: () => import('@/views/papers/PaperFormView.vue') },
      { path: 'papers/:id', name: 'PaperDetail', component: () => import('@/views/papers/PaperDetailView.vue') },
      { path: 'papers/:id/edit', name: 'PaperEdit', component: () => import('@/views/papers/PaperFormView.vue') },
      { path: 'projects', name: 'Projects', component: () => import('@/views/projects/ProjectListView.vue') },
      { path: 'projects/create', name: 'ProjectCreate', component: () => import('@/views/projects/ProjectFormView.vue') },
      { path: 'projects/:id', name: 'ProjectDetail', component: () => import('@/views/projects/ProjectDetailView.vue') },
      { path: 'projects/:id/edit', name: 'ProjectEdit', component: () => import('@/views/projects/ProjectFormView.vue') },
      { path: 'favorites', name: 'Favorites', component: () => import('@/views/favorites/FavoritesView.vue') },
      { path: 'admin/dashboard', name: 'AdminDashboard', component: () => import('@/views/admin/DashboardView.vue'), meta: { adminOnly: true } },
      { path: 'admin/users', name: 'AdminUsers', component: () => import('@/views/admin/UserManagementView.vue'), meta: { adminOnly: true } },
      { path: 'admin/analytics', name: 'AdminAnalytics', component: () => import('@/views/admin/AnalyticsView.vue'), meta: { adminOnly: true } },
    ]
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')

  if (to.meta.requiresAuth && !token) {
    return next('/login')
  }
  if (to.meta.guest && token) {
    return next('/')
  }
  next()
})

export default router
