import { createRouter, createWebHistory } from 'vue-router'
import { useDataStore } from '../stores/counter'

import App from '../App.vue'
import Login from '../page/login.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'App',
      component: App,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
  ],
})

router.beforeEach((to, from, next) => {
  const store = useDataStore()

  if (to.meta.requiresAuth) {
    if (!store.auth_key) {
      return next('/login')
    }

    if (to.meta.requiredRole && store.role !== to.meta.requiredRole) {
      return next('/')
    }
  }

  next()
})

export default router
