import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import EntryDetail from '../views/EntryDetail.vue'
import Settings from '../views/Settings.vue'
import Login from '../views/Login.vue'
import { checkAuthStatus } from '../services/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true },
  },
  {
    path: '/entry/:id?',
    name: 'EntryDetail',
    component: EntryDetail,
    meta: { requiresAuth: true },
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation guard to check authentication
router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    const authStatus = await checkAuthStatus()
    if (!authStatus.authenticated) {
      next('/login')
      return
    }
  }
  next()
})

export default router

