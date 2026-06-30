<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <div>
        <h2 class="text-3xl font-bold text-emerald-400">My Recipes</h2>
        <p class="text-slate-400">Manage your culinary creations and view preparation steps.</p>
      </div>
      <button v-if="recipes.length > 0 && !isLoading && !hasServerError" @click="openCreateModal"
        class="bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold px-4 py-2.5 rounded-lg transition-colors flex items-center gap-2 text-sm shadow-lg shadow-emerald-500/10">
        ➕ Add New Recipe
      </button>
    </div>

    <div v-if="isLoading" class="text-center py-12 bg-slate-900 rounded-xl border border-slate-800">
      <p class="text-emerald-400 font-medium animate-pulse text-lg">⏳ Connecting to server...</p>
    </div>

    <div v-else-if="hasServerError" class="text-center py-12 bg-rose-950/20 rounded-xl border border-rose-800/50 p-6">
      <span class="text-4xl">⚠️</span>
      <h3 class="text-xl font-bold text-rose-400 mt-2">Unable to retrieve data from the server</h3>
      <button @click="fetchRecipes"
        class="mt-4 bg-rose-500 hover:bg-rose-600 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors">
        Retry connection
      </button>
    </div>

    <div v-else-if="recipes.length === 0" class="text-center py-12 bg-slate-900 rounded-xl border border-slate-800 p-6">
      <span class="text-4xl">🍳</span>
      <h3 class="text-xl font-bold text-slate-200 mt-2">No recipes created yet</h3>
      <p class="text-slate-400 mt-1 mb-6">Ready to start planning your diet?</p>
      <button @click="openCreateModal"
        class="bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-semibold px-4 py-2 rounded-lg transition-colors">
        ➕ Create your first recipe
      </button>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="recipe in recipes" :key="recipe.id"
        class="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden flex flex-col justify-between group hover:border-slate-700 transition-all duration-300">
        <div class="relative h-48 bg-slate-950 overflow-hidden">
          <img
            :src="`https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=600&q=80&sig=${recipe.id}`"
            :alt="recipe.name"
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 opacity-90 group-hover:opacity-100" />
          <div class="absolute inset-0 bg-gradient-to-t from-slate-900 via-transparent to-transparent"></div>
        </div>
        <div class="p-5 flex-grow flex flex-col justify-between">
          <h3 class="text-xl font-bold text-slate-100 mb-4 line-clamp-2 min-h-[3.5rem] flex items-center">
            {{ recipe.name }}
          </h3>
          <button @click="openInstructions(recipe)"
            class="w-full bg-slate-800 hover:bg-emerald-500 hover:text-slate-950 text-emerald-400 font-semibold py-2.5 px-4 rounded-lg transition-all duration-300 flex items-center justify-center gap-2 border border-slate-700">
            📖 View Instructions
          </button>
        </div>
      </div>
    </div>

    <div v-if="isViewModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div @click="closeViewModal" class="absolute inset-0 bg-slate-950/75 backdrop-blur-sm"></div>

      <div
        class="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-xl overflow-hidden shadow-2xl relative z-10 animate-in fade-in zoom-in-95 duration-200">
        <div class="p-6 border-b border-slate-800 flex justify-between items-start bg-slate-950/40">
          <h3 class="text-2xl font-bold text-slate-100 pr-4">{{ selectedRecipe?.name }}</h3>
          <button @click="closeViewModal"
            class="text-slate-400 hover:text-slate-200 bg-slate-800/50 hover:bg-slate-800 p-1.5 rounded-lg">✕</button>
        </div>

        <div class="p-6 max-h-[65vh] overflow-y-auto space-y-6">

          <div class="space-y-2">
            <h4 class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Required Ingredients</h4>

            <div v-if="selectedRecipe?.ingredients && selectedRecipe.ingredients.length > 0"
              class="grid grid-cols-1 sm:grid-cols-2 gap-2">
              <div v-for="item in selectedRecipe.ingredients" :key="item.ingredient_id"
                class="flex justify-between items-center bg-slate-950/40 border border-slate-800/80 px-4 py-2.5 rounded-xl text-sm">
                <span class="text-slate-300 font-medium">
                  {{ingredientsCatalog.find(ing => ing.id === item.ingredient_id)?.name || `Ingredient
                  #${item.ingredient_id}`}}
                </span>
                <span
                  class="text-emerald-400 font-bold bg-emerald-950/30 border border-emerald-900/30 px-2 py-0.5 rounded-md text-xs">
                  x{{ item.quantity }}
                </span>
              </div>
            </div>

            <div v-else class="text-xs text-slate-500 italic bg-slate-950/20 p-3 rounded-xl border border-slate-800/50">
              No ingredients listed for this recipe.
            </div>
          </div>

          <div class="space-y-2">
            <h4 class="text-xs font-bold text-emerald-400 uppercase tracking-wider">Preparation Steps</h4>
            <p
              class="text-slate-300 leading-relaxed whitespace-pre-line text-sm bg-slate-950/20 p-4 rounded-xl border border-slate-800/50">
              {{ selectedRecipe?.instructions }}
            </p>
            <div class="p-4 text-right flex justify-end gap-2">
              <button @click="openEditModal(recipe)" class="text-emerald-400 hover:text-emerald-300">Edit</button>
              <button @click="initiateDelete(recipe)" class="text-red-400 hover:text-red-300">Delete</button>
            </div>

            <Modal :show="isModalOpen" :title="modalTitle" @close="isModalOpen = false" @confirm="handleConfirm">
              <p class="whitespace-pre-line">{{ modalMessage }}</p>
            </Modal>
          </div>

        </div>

        <div class="p-4 bg-slate-950/40 border-t border-slate-800 flex justify-end">
          <button @click="closeViewModal"
            class="bg-slate-800 hover:bg-slate-700 text-slate-200 px-5 py-2 rounded-lg text-sm font-medium">Close</button>
        </div>
      </div>
    </div>

    <div v-if="isCreateModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div @click="!isSubmitting && closeCreateModal()" class="absolute inset-0 bg-slate-950/75 backdrop-blur-sm"></div>

      <div
        class="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-lg overflow-hidden shadow-2xl relative z-10 animate-in fade-in zoom-in-95 duration-200">
        <div class="p-6 border-b border-slate-800 flex justify-between items-center bg-slate-950/40">
          <h3 class="text-xl font-bold text-slate-100">Create New Recipe</h3>
          <button :disabled="isSubmitting" @click="closeCreateModal"
            class="text-slate-400 hover:text-slate-200 bg-slate-800/50 hover:bg-slate-800 p-1.5 rounded-lg disabled:opacity-50">✕</button>
        </div>

        <form @submit.prevent="handleCreateRecipe">
          <div class="p-6 space-y-5 max-h-[65vh] overflow-y-auto">

            <div class="space-y-2">
              <label for="recipe-name" class="text-xs font-bold text-slate-400 uppercase tracking-wider">Recipe Name
                *</label>
              <input id="recipe-name" v-model="newRecipeName" type="text" required
                placeholder="e.g., Grilled Salmon with Asparagus"
                class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-slate-200 placeholder-slate-600 focus:outline-none focus:border-emerald-500 transition-colors text-sm"
                :disabled="isSubmitting" />
            </div>

            <div class="space-y-2">
              <label for="recipe-steps" class="text-xs font-bold text-slate-400 uppercase tracking-wider">Preparation
                Instructions</label>
              <textarea id="recipe-steps" v-model="newRecipeInstructions" rows="4"
                placeholder="Describe the step-by-step cooking method..."
                class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-slate-200 placeholder-slate-600 focus:outline-none focus:border-emerald-500 transition-colors text-sm resize-none"
                :disabled="isSubmitting"></textarea>
            </div>

            <div class="space-y-3 pt-2 border-t border-slate-800/60">
              <div class="flex justify-between items-center">
                <div class="text-xs font-bold text-slate-400 uppercase tracking-wider">Ingredients & Quantities</div>
                <button type="button" @click="addIngredientRow"
                  class="text-xs bg-slate-800 hover:bg-slate-700 text-emerald-400 font-semibold px-2.5 py-1 rounded-lg border border-slate-700 transition-colors">
                  ➕ Add Ingredient
                </button>
              </div>

              <div v-for="(row, index) in recipeIngredientsForm" :key="index"
                class="flex gap-2 items-center animate-in fade-in slide-in-from-top-1 duration-150">

                <label :for="`ingredient-${index}`" class="sr-only">Ingredient</label>
                <select :id="`ingredient-${index}`" v-model="row.ingredient_id"
                  class="flex-grow bg-slate-950 border border-slate-800 rounded-xl px-3 py-2.5 text-slate-200 text-sm focus:outline-none focus:border-emerald-500"
                  required>
                  <option value="" disabled selected>Select an ingredient...</option>
                  <option v-for="ing in ingredientsCatalog" :key="ing.id" :value="ing.id"
                    :disabled="recipeIngredientsForm.some(item => item.ingredient_id === ing.id && item.ingredient_id !== row.ingredient_id)">
                    {{ ing.name }} {{ ing.is_fresh ? '🌿' : '' }}
                  </option>
                </select>

                <label :for="`quantity-${index}`" class="sr-only">Quantity</label>
                <input :id="`quantity-${index}`" v-model="row.quantity" type="number" min="1" required placeholder="Qty"
                  class="w-20 bg-slate-950 border border-slate-800 rounded-xl px-3 py-2.5 text-slate-200 text-sm text-center focus:outline-none focus:border-emerald-500" />

                <button type="button" @click="removeIngredientRow(index)" :disabled="recipeIngredientsForm.length === 1"
                  class="p-2.5 text-rose-500 hover:bg-rose-950/30 rounded-xl border border-transparent hover:border-rose-900/50 disabled:opacity-30 disabled:hover:bg-transparent transition-colors"
                  title="Remove ingredient">
                  ✕
                </button>
              </div>
            </div>

          </div>

          <div class="p-4 bg-slate-950/40 border-t border-slate-800 flex justify-end gap-3">
            <button type="button" :disabled="isSubmitting" @click="closeCreateModal"
              class="bg-slate-800 hover:bg-slate-700 text-slate-300 px-4 py-2 rounded-lg text-sm font-medium transition-colors">
              Cancel
            </button>
            <button type="submit" :disabled="isSubmitting || !newRecipeName.trim()"
              class="bg-emerald-500 hover:bg-emerald-600 disabled:bg-slate-800 text-slate-950 disabled:text-slate-600 font-bold px-5 py-2 rounded-lg text-sm transition-all duration-200">
              {{ isSubmitting ? 'Saving...' : 'Save Recipe' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const API_RECIPES_URL = import.meta.env.VITE_API_RECIPES_URL
const API_INGREDIENTS_URL = import.meta.env.VITE_API_INGREDIENTS_URL

const recipes = ref([])
const isLoading = ref(true)
const hasServerError = ref(false)

const isViewModalOpen = ref(false)
const selectedRecipe = ref(null)

const isCreateModalOpen = ref(false)
const newRecipeName = ref('')
const newRecipeInstructions = ref('')
const isSubmitting = ref(false)

const ingredientsCatalog = ref([])
const hasLoadedIngredients = ref(false)

const isModalOpen = ref(false)
const modalTitle = ref('')
const modalMessage = ref('')
const recipeIdToDelete = ref(null)

const normalizeRecipe = (recipe) => ({
  id: recipe.id,
  name: recipe.name,
  instructions: recipe.instructions && recipe.instructions.trim() !== ""
    ? recipe.instructions
    : 'No preparation steps provided for this recipe yet.'
})

const recipeIngredientsForm = ref([
  { ingredient_id: '', quantity: 1 }
])

const fetchRecipes = async () => {
  try {
    hasServerError.value = false
    isLoading.value = true
    const response = await axios.get(`${API_RECIPES_URL}`)
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

const fetchIngredientsIfNeeded = async () => {
  // Si ya los tenemos cargados, no molestamos al servidor
  if (hasLoadedIngredients.value) return

  try {
    const response = await axios.get(`${API_INGREDIENTS_URL}`)
    ingredientsCatalog.value = response.data
    hasLoadedIngredients.value = true
  } catch (error) {
    console.error('Failed to fetch ingredients catalog:', error)
  }
}

const openInstructions = (recipe) => {
  selectedRecipe.value = recipe
  isViewModalOpen.value = true
}
const closeViewModal = () => {
  isViewModalOpen.value = false
  selectedRecipe.value = null
}

const openCreateModal = async () => {
  isCreateModalOpen.value = true
  await fetchIngredientsIfNeeded()
}

const addIngredientRow = () => {
  recipeIngredientsForm.value.push({ ingredient_id: '', quantity: 1 })
}

const removeIngredientRow = (index) => {
  recipeIngredientsForm.value.splice(index, 1)
}

const initiateDelete = (recipe) => {
  recipeIdToDelete.value = recipe.id
  modalTitle.value = "Confirmar eliminación"
  modalMessage.value = `¿Estás seguro de que quieres eliminar la receta "${recipe.name}"?`
  isModalOpen.value = true
}

const handleConfirm = async () => {
  try {
    // Asegúrate de apuntar a la ruta correcta de recetas
    await axios.delete(`http://127.0.0.1:8000/recipes/${recipeIdToDelete.value}`)
    await fetchRecipes() // Refresca tu lista de recetas
    isModalOpen.value = false
  } catch (error) {
    modalTitle.value = "Error"
    modalMessage.value = "No se pudo eliminar la receta. Verifica que no esté en uso."
    // Si tienes lógica de 409 para recetas, agrégala aquí también
  }
}

const closeCreateModal = () => {
  isCreateModalOpen.value = false
  newRecipeName.value = ''
  newRecipeInstructions.value = ''
  recipeIngredientsForm.value = [{ ingredient_id: '', quantity: 1 }]
}

const handleCreateRecipe = async () => {
  if (!newRecipeName.value.trim()) return

  try {
    isSubmitting.value = true

    // Filtramos las filas de ingredientes por si el usuario dejó algún selector en blanco
    const validIngredients = recipeIngredientsForm.value
      .filter(item => item.ingredient_id !== '')
      .map(item => ({
        ingredient_id: Number(item.ingredient_id),
        quantity: Number(item.quantity)
      }))

    // Construimos el payload plano y anidado
    const payload = {
      name: newRecipeName.value.trim(),
      instructions: newRecipeInstructions.value.trim(),
      ingredients: validIngredients // <--- ¡Aquí viaja tu lista relacional!
    }

    const response = await axios.post(API_RECIPES_URL, payload)

    if (response.status === 201) {
      recipes.value.push(normalizeRecipe(response.data))
      closeCreateModal()
      // Reseteamos el formulario de ingredientes a su estado inicial
      recipeIngredientsForm.value = [{ ingredient_id: '', quantity: 1 }]
    }
  } catch (error) {
    console.error('Error creating the recipe:', error)
    alert('Could not save the recipe with its ingredients.')
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  fetchRecipes()
})
</script>