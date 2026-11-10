import { createRouter, createWebHistory } from 'vue-router'
import CategoriesView from '../views/CategoriesView.vue'
import ComponentsView from '../views/ComponentsView.vue'
import BuildRequestsView from '../views/BuildRequestsView.vue'
import AssemblyItemsView from '../views/AssemblyItemsView.vue'
import HandoverActsView from '../views/HandoverActsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/components'
    },
    {
      path: '/categories',
      name: 'categories',
      component: CategoriesView
    },
    {
      path: '/components',
      name: 'components',
      component: ComponentsView
    },
    {
      path: '/build-requests',
      name: 'build-requests',
      component: BuildRequestsView
    },
    {
      path: '/assembly-items',
      name: 'assembly-items',
      component: AssemblyItemsView
    },
    {
      path: '/handover-acts',
      name: 'handover-acts',
      component: HandoverActsView
    }
  ]
})

export default router