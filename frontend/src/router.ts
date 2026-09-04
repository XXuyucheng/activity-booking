import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './views/HomeView.vue'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    {
      path: '/activity/:id',
      name: 'activity',
      component: () => import('./views/ActivityDetailView.vue'),
    },
    {
      path: '/bookings',
      name: 'bookings',
      component: () => import('./views/MyBookingsView.vue'),
    },
    {
      path: '/bookings/:id',
      name: 'booking-detail',
      component: () => import('./views/BookingDetailView.vue'),
    },
    {
      path: '/camp',
      name: 'camp',
      component: () => import('./views/CampIntroView.vue'),
    },
    {
      path: '/rules',
      name: 'rules',
      component: () => import('./views/BookingRulesView.vue'),
    },
    {
      path: '/pack/:id',
      name: 'pack',
      component: () => import('./views/PackDetailView.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('./views/NotFoundView.vue'),
    },
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})
