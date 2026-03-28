import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'upload',
      component: () => import('@/views/UploadView.vue'),
    },
    {
      path: '/result',
      name: 'result',
      component: () => import('@/views/ResultView.vue'),
    },
    {
      path: '/history',
      name: 'history',
      component: () => import('@/views/HistoryView.vue'),
    },
    {
      path: '/history/:id',
      name: 'detail',
      component: () => import('@/views/DetailView.vue'),
    },
  ],
})

export default router
