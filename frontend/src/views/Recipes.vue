<template>
  <div class="recipe-view flex h-full min-h-0 flex-col">
    <div class="page-header">
      <div>
        <h2 class="app-page-title">My Recipes</h2>
        <p class="app-page-subtitle">Manage your culinary creations and view preparation steps.</p>
      </div>
      <button type="button" v-if="recipes.length > 0 && !isLoading && !hasServerError" @click="openCreateModal"
        class="btn-primary px-4 py-2.5 flex items-center gap-2 text-sm shadow-lg shadow-emerald-500/10">
        ➕ Add New Recipe
      </button>
    </div>

    <div class="recipe-scroll-panel min-h-0 flex-1 overflow-y-auto">
      <div v-if="isLoading" class="text-center py-12 app-surface">
        <p class="text-emerald-400 font-medium animate-pulse text-lg">⏳ Connecting to server...</p>
      </div>

      <div v-else-if="hasServerError" class="text-center py-12 bg-rose-950/20 rounded-xl border border-rose-800/50 p-6">
      <span class="text-4xl">⚠️</span>
      <h3 class="text-xl font-bold text-rose-400 mt-2">Unable to retrieve data from the server</h3>
      <button type="button" @click="fetchRecipes"
        class="mt-4 bg-rose-500 hover:bg-rose-600 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-colors">
        Retry connection
      </button>
    </div>

      <div v-else-if="recipes.length === 0" class="text-center py-12 app-surface p-6">
      <span class="text-4xl">🍳</span>
      <h3 class="text-xl font-bold text-slate-200 mt-2">No recipes created yet</h3>
      <p class="text-slate-400 mt-1 mb-6">Ready to start planning your diet?</p>
      <button type="button" @click="openCreateModal"
        class="btn-primary-sm px-4 py-2">
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
          <div class="absolute inset-0 bg-linear-to-t from-slate-900 via-transparent to-transparent"></div>
        </div>
        <div class="p-5 grow flex flex-col justify-between">
          <h3 class="text-xl font-bold text-slate-100 mb-4 line-clamp-2 min-h-14 flex items-center">
            {{ recipe.name }}
          </h3>
          <button type="button" @click="openInstructions(recipe)"
            class="w-full bg-slate-800 hover:bg-emerald-500 hover:text-slate-950 text-emerald-400 font-semibold py-2.5 px-4 rounded-lg transition-all duration-300 flex items-center justify-center gap-2 border border-slate-700">
            📖 View Instructions
          </button>
        </div>
      </div>
      </div>
    </div>

    <div v-if="isViewModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div @click="closeViewModal" class="modal-backdrop"></div>

      <div class="modal-window-lg animate-in fade-in zoom-in-95 duration-200">
        <div class="p-6 border-b border-slate-800 flex justify-between items-start bg-slate-950/40">
          <h3 class="text-2xl font-bold text-slate-100 pr-4">{{ selectedRecipe?.name }}</h3>
          <button type="button" @click="closeViewModal" class="btn-icon">✕</button>
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
              <button type="button" @click="openEditModal(selectedRecipe)" class="btn-link">Edit</button>
              <button type="button" @click="initiateDelete(selectedRecipe)" class="btn-danger">Delete</button>
            </div>

            <EditModal :show="isEditModalOpen" title="Edit Recipe" @close="isEditModalOpen = false" @confirm="handleUpdate">
              <div class="space-y-4">
                <div class="space-y-2">
                  <label for="edit-recipe-name" class="text-xs font-bold text-slate-400 uppercase">Recipe Name</label>
                  <input id="edit-recipe-name" v-model="newRecipe.name" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-slate-200 text-sm focus:outline-none focus:border-emerald-500" />
                </div>
                <div class="space-y-2">
                  <label for="edit-recipe-instructions" class="text-xs font-bold text-slate-400 uppercase">Instructions</label>
                  <textarea id="edit-recipe-instructions" v-model="newRecipe.instructions" rows="4" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 text-slate-200 text-sm focus:outline-none focus:border-emerald-500"></textarea>
                </div>
              </div>
            </EditModal>

            <Modal :show="isModalOpen" :title="modalTitle" @close="isModalOpen = false" @confirm="handleConfirm">
              <p class="whitespace-pre-line">{{ modalMessage }}</p>
            </Modal>
          </div>

        </div>

        <div class="p-4 bg-slate-950/40 border-t border-slate-800 flex justify-end">
          <button type="button" @click="closeViewModal" class="btn-secondary px-5 py-2 text-sm">Close</button>
        </div>
      </div>
    </div>

    <div v-if="isCreateModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div @click="!isSubmitting && closeCreateModal()" class="modal-backdrop"></div>

      <div class="modal-window animate-in fade-in zoom-in-95 duration-200">
        <div class="p-6 border-b border-slate-800 flex justify-between items-center bg-slate-950/40">
          <h3 class="text-xl font-bold text-slate-100">Create New Recipe</h3>
          <button type="button" :disabled="isSubmitting" @click="closeCreateModal" class="btn-icon disabled:opacity-50">✕</button>
        </div>

        <form @submit.prevent="handleCreateRecipe">
          <div class="p-6 space-y-5 max-h-[65vh] overflow-y-auto">

            <div class="space-y-2">
              <label for="recipe-name" class="form-label">Recipe Name
                *</label>
              <input id="recipe-name" v-model="newRecipeName" type="text" required
                placeholder="e.g., Grilled Salmon with Asparagus"
                class="app-input"
                :disabled="isSubmitting" />
            </div>

            <div class="space-y-2">
              <label for="recipe-steps" class="form-label">Preparation
                Instructions</label>
              <textarea id="recipe-steps" v-model="newRecipeInstructions" rows="4"
                placeholder="Describe the step-by-step cooking method..."
                class="app-input resize-none"
                :disabled="isSubmitting"></textarea>
            </div>

            <div class="space-y-3 pt-2 border-t border-slate-800/60">
              <div class="flex justify-between items-center">
                <div class="form-label">Ingredients & Quantities</div>
                <button type="button" @click="addIngredientRow"
                  class="text-xs bg-slate-800 hover:bg-slate-700 text-emerald-400 font-semibold px-2.5 py-1 rounded-lg border border-slate-700 transition-colors">
                  ➕ Add Ingredient
                </button>
              </div>

              <div v-for="(row, index) in recipeIngredientsForm" :key="index"
                class="flex gap-2 items-center animate-in fade-in slide-in-from-top-1 duration-150">

                <label :for="`ingredient-${index}`" class="sr-only">Ingredient</label>
                <select :id="`ingredient-${index}`" v-model="row.ingredient_id"
                  class="grow bg-slate-950 border border-slate-800 rounded-xl px-3 py-2.5 text-slate-200 text-sm focus:outline-none focus:border-emerald-500"
                  required>
                  <option value="" disabled>Select an ingredient...</option>
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
            <button type="button" :disabled="isSubmitting" @click="closeCreateModal" class="btn-secondary px-4 py-2 text-sm">
              Cancel
            </button>
            <button type="submit" :disabled="isSubmitting || !newRecipeName.trim()"
              class="btn-primary px-5 py-2 text-sm disabled:bg-slate-800 disabled:text-slate-600">
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
import Modal from '../components/Modal.vue'
import EditModal from '../components/EditModal.vue'

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

const newRecipe = ref({ name: '', instructions: '' }) // O los campos que tenga tu receta

const isDeleteMode = ref(false)

const isModalOpen = ref(false)
const modalTitle = ref('')
const modalMessage = ref('')
const recipeIdToDelete = ref(null)

const normalizeRecipe = (recipe) => ({
  id: recipe.id,
  name: recipe.name,
  instructions: recipe.instructions && recipe.instructions.trim() !== ""
    ? recipe.instructions
    : 'No preparation steps provided for this recipe yet.',
  ingredients: Array.isArray(recipe.ingredients)
    ? recipe.ingredients.map(item => ({
        ingredient_id: item.ingredient_id,
        quantity: item.quantity
      })) : 'No preparation steps provided for this recipe yet.'
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

const openInstructions = async (recipe) => {
  await fetchIngredientsIfNeeded()
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

const isEditModalOpen = ref(false)

const openEditModal = (recipe) => {
  // Clonamos la receta para editarla de forma segura
  newRecipe.value = { ...recipe }
  isEditModalOpen.value = true
} 

const handleUpdate = async () => {
  try {
    const response = await axios.patch(`${API_RECIPES_URL}/${newRecipe.value.id}`, newRecipe.value)
    
    // Actualizamos la lista de recetas
    await fetchRecipes()
    
    // Refrescamos la receta seleccionada con la respuesta del servidor
    selectedRecipe.value = normalizeRecipe(response.data)
    
    isEditModalOpen.value = false
  } catch (error) {
    console.error("Error updating recipe:", error)
  }
} 

const handleConfirm = async () => {
  try {
    // Asegúrate de apuntar a la ruta correcta de recetas
    await axios.delete(`${API_RECIPES_URL}/${recipeIdToDelete.value}`)
    await fetchRecipes() // Refresca tu lista de recetas
    isModalOpen.value = false
    closeViewModal()
    } catch (error) {
    console.error("Error deleting recipe:", error)
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
    modalTitle.value = 'Error'
    modalMessage.value = 'Could not save the recipe with its ingredients.'
    isModalOpen.value = true
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  fetchRecipes()
})
</script>