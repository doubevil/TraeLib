import { createRouter, createWebHistory } from 'vue-router'
import ScoreView from '../views/ScoreView.vue'
import RelationView from '../views/RelationView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'score',
      component: ScoreView
    },
    {
      path: '/relation',
      name: 'relation',
      component: RelationView
    }
  ]
})

export default router
