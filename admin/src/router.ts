import { createRouter, createWebHistory } from 'vue-router'
import { fetchMe } from './api/auth'
import { currentStaff } from './session'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('./views/LoginView.vue'),
      meta: { public: true },
    },
    {
      path: '/',
      name: 'bookings',
      component: () => import('./views/BookingsView.vue'),
    },
    {
      path: '/activities',
      name: 'activities',
      component: () => import('./views/ActivitiesView.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/',
    },
  ],
})

router.beforeEach(async (to) => {
  if (to.meta.public) {
    return true
  }
  try {
    currentStaff.value = await fetchMe()
    return true
  } catch {
    return { path: '/login' }
  }
})
