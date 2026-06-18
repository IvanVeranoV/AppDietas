import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import Recipes from './views/Recipes.vue'
import Calendar from './views/Calendar.vue'

const routes = [
  { 
    path: '/', 
    name: 'home',
    component: Home
  },
  { 
    path: '/recipes', 
    name: 'recipes',
    component: Recipes 
  },
  { 
    path: '/calendar', 
    name: 'calendar',
    component: Calendar 
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router