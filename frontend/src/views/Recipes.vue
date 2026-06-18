<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_ENDPOINT = 'http://127.0.0.1:8000/recipes'

const recipes = ref([])
const isLoading = ref(true)
const hasServerError = ref(false)

// Estados para el Modal de Instrucciones
const isModalOpen = ref(false)
const selectedRecipe = ref(null)

const normalizeRecipe = (recipe) => ({
  id: recipe.id,
  name: recipe.name,
  // Si no hay instrucciones en la BD, ponemos un texto amigable por defecto
  instructions: recipe.instructions && recipe.instructions.trim() !== "" 
    ? recipe.instructions 
    : 'No preparation steps provided for this recipe yet.'
})

const fetchRecipes = async () => {
  try {
    hasServerError.value = false
    isLoading.value = true

    const response = await axios.get(API_ENDPOINT)
    recipes.value = Array.isArray(response.data)
      ? response.data.map(normalizeRecipe)
      : []
  } catch (error) {
    console.error('Failed to fetch recipes:', error)
    hasServerError.value = true
  } finally {
    isLoading.value = false
  }
}

// Funciones para controlar el flujo del Modal
const openInstructions = (recipe) => {
  selectedRecipe.value = recipe
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
  selectedRecipe.value = null
}

onMounted(() => {
  fetchRecipes()
})
</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <div>
        <h2 class="text-3xl font-bold text-emerald-400">My Recipes</h2>
        <p class="text-slate-400">Manage your culinary creations and view preparation steps.</p>
      </div>
    </div>

    <div v-if="isLoading" class="text-center py-12 bg-slate-900 rounded-xl border border-slate-800">
      <p class="text-emerald-400 font-medium animate-pulse text-lg">⏳ Connecting to server...</p>
    </div>

    <div v-else-if="hasServerError" class="text-center py-12 bg-rose-950/20 rounded-xl border border-rose-800/50 p-6">
      <span class="text-4xl">⚠️</span>
      <h3 class="text-xl font-bold text-rose-400 mt-2">Unable to retrieve data from the server</h3>
      <p class="text-slate-400 mt-1 mb-4">Please verify that your Python container is running.</p>
      <button @click="fetchRecipes" class="bg-rose-500 hover:bg-rose-600 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors">
        Retry connection
      </button>
    </div>

    <div v-else-if="recipes.length === 0" class="text-center py-12 bg-slate-900 rounded-xl border border-slate-800 p-6">
      <span class="text-4xl">🍳</span>
      <h3 class="text-xl font-bold text-slate-200 mt-2">No recipes created yet</h3>
      <p class="text-slate-400 mt-1 mb-6">Ready to start planning your diet?</p>
      <button class="bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-semibold px-4 py-2 rounded-lg transition-colors">
        ➕ Create your first recipe
      </button>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="recipe in recipes" :key="recipe.id" class="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden flex flex-col justify-between group hover:border-slate-700 transition-all duration-300">
        
        <div class="relative h-48 bg-slate-950 overflow-hidden">
          <img 
            :src="`https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=600&q=80&sig=${recipe.id}`" 
            :alt="recipe.name"
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 opacity-90 group-hover:opacity-100"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-slate-900 via-transparent to-transparent"></div>
        </div>

        <div class="p-5 flex-grow flex flex-col justify-between">
          <h3 class="text-xl font-bold text-slate-100 mb-4 line-clamp-2 min-h-[3.5rem] flex items-center">
            {{ recipe.name }}
          </h3>
          
          <button 
            @click="openInstructions(recipe)"
            class="w-full bg-slate-800 hover:bg-emerald-500 hover:text-slate-950 text-emerald-400 font-semibold py-2.5 px-4 rounded-lg transition-all duration-300 flex items-center justify-center gap-2 border border-slate-700 group-hover:border-transparent"
          >
            📖 View Instructions
          </button>
        </div>
      </div>
    </div>

    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div @click="closeModal" class="absolute inset-0 bg-slate-950/75 backdrop-blur-sm transition-opacity"></div>

      <div class="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-lg overflow-hidden shadow-2xl relative z-10 transform transition-all animate-in fade-in zoom-in-95 duration-200">
        <div class="p-6 border-b border-slate-800 flex justify-between items-start bg-slate-950/40">
          <h3 class="text-2xl font-bold text-slate-100 pr-4">{{ selectedRecipe?.name }}</h3>
          <button 
            @click="closeModal" 
            class="text-slate-400 hover:text-slate-200 bg-slate-800/50 hover:bg-slate-800 p-1.5 rounded-lg transition-colors"
          >
            ✕
          </button>
        </div>

        <div class="p-6 max-h-[60vh] overflow-y-auto space-y-4">
          <h4 class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Preparation Steps</h4>
          <p class="text-slate-300 leading-relaxed whitespace-pre-line text-sm bg-slate-950/20 p-4 rounded-xl border border-slate-800/50">
            {{ selectedRecipe?.instructions }}
          </p>
        </div>

        <div class="p-4 bg-slate-950/40 border-t border-slate-800 flex justify-end">
          <button 
            @click="closeModal" 
            class="bg-slate-800 hover:bg-slate-700 text-slate-200 px-5 py-2 rounded-lg font-medium transition-colors text-sm"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>