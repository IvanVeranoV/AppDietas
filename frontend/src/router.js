import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import Recipes from './views/Recipes.vue'
import CalendarWeek from './views/calendar/CalendarWeek.vue'
import Ingredients from './views/Ingredients.vue'

const routes = [
  { 
    path: '/', 
    name: 'home',
    component: Home
  },
  { 
    path: '/ingredients', 
    name: 'ingredients',
    component: Ingredients
  },
  { 
    path: '/recipes', 
    name: 'recipes',
    component: Recipes 
  },
  { 
    path: '/calendar', 
    name: 'calendar',
    component: CalendarWeek 
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router