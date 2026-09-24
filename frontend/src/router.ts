import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './views/HomeView.vue'
import CampShell from './views/CampShell.vue'
import { campSlugFromPath } from './lib/camp'
import { peekOAuthReturn } from './lib/oauthReturn'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/luhe' },
    {
      path: '/activity/:id',
      redirect: (to) => `/luhe/activity/${String(to.params.id)}`,
    },
    { path: '/camp', redirect: '/luhe/camp' },
    {
      path: '/bookings/:id',
      redirect: (to) => `/luhe/bookings/${String(to.params.id)}`,
    },
    { path: '/bookings', redirect: '/luhe/bookings' },
    {
      path: '/rules',
      redirect: (to) => ({ path: '/luhe/rules', query: to.query }),
    },
    {
      path: '/pack/:id',
      redirect: (to) => `/luhe/pack/${String(to.params.id)}`,
    },
    {
      path: '/:campSlug',
      component: CampShell,
      children: [
        { path: '', name: 'home', component: HomeView },
        {
          path: 'activity/:id',
          name: 'activity',
          component: () => import('./views/ActivityDetailView.vue'),
        },
        {
          path: 'bookings',
          name: 'bookings',
          component: () => import('./views/MyBookingsView.vue'),
        },
        {
          path: 'bookings/:id',
          name: 'booking-detail',
          component: () => import('./views/BookingDetailView.vue'),
        },
        {
          path: 'camp',
          name: 'camp',
          component: () => import('./views/CampIntroView.vue'),
        },
        {
          path: 'rules',
          name: 'rules',
          component: () => import('./views/BookingRulesView.vue'),
        },
        {
          path: 'pack/:id',
          name: 'pack',
          component: () => import('./views/PackDetailView.vue'),
        },
        {
          path: ':pathMatch(.*)*',
          name: 'camp-not-found',
          component: () => import('./views/NotFoundView.vue'),
        },
      ],
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

router.beforeEach((to) => {
  if (to.name !== 'home') return
  const pending = peekOAuthReturn()
  if (!pending) return
  const slug = typeof to.params.campSlug === 'string' ? to.params.campSlug : ''
  if (campSlugFromPath(pending.path) !== slug) return
  return pending.path
})
