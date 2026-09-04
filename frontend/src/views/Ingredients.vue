<template>
    <div class="inventory-shell">
        <div class="page-header">
            <h2 class="app-page-title">Ingredient Inventory</h2>
            <button type="button" @click="openCreateModal" class="btn-primary px-4 py-2">
                + New Ingredient
            </button>
        </div>

        <table class="inventory-table">
            <thead class="bg-slate-950 text-slate-400 text-left">
                <tr>
                    <th class="p-4">Name</th>
                    <th class="p-4">Type</th>
                    <th class="p-4">Category</th>
                    <th class="p-4 text-right">Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="ing in ingredients" :key="ing.id" class="border-t border-slate-800 hover:bg-slate-800/50">
                    <td class="p-4 font-semibold">{{ ing.name }}</td>
                    <td class="p-4">{{ ing.is_fresh ? '🌿 Fresh' : '📦 Pantry' }}</td>
                    <td class="p-4">
                        {{categories.find(cat => cat.id === ing.category_id)?.name || 'Uncategorized'}}
                    </td>
                    <td class="p-4 text-right flex justify-end gap-2">
                        <button type="button" @click="openEditModal(ing)" class="btn-link text-sm">Edit</button>
                        <button type="button" @click="initiateDelete(ing)" class="btn-danger text-sm">Delete</button>
                    </td>
                </tr>
            </tbody>
        </table>

        <Modal :show="isModalOpen" :title="modalTitle" @close="isModalOpen = false" @confirm="handleConfirm">
            <form v-if="!isDeleteMode" @submit.prevent="saveIngredient" class="space-y-4">
                <div>
                    <label for="ingredient-name" class="block text-xs font-bold text-slate-400 uppercase">Name</label>
                    <input id="ingredient-name" v-model="newIngredient.name" type="text" required
                        class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 mt-1" />
                </div>
                <label for="ingredient-fresh" class="flex items-center gap-2 text-sm">
                    <input id="ingredient-fresh" v-model="newIngredient.is_fresh" type="checkbox" /> Is this ingredient fresh? (🌿)
                </label>
                <div>
                    <label for="ingredient-category" class="block text-xs font-bold text-slate-400 uppercase">Category</label>
                    <select id="ingredient-category" v-model="newIngredient.category_id" required
                        class="w-full bg-slate-950 border border-slate-800 rounded-lg p-2 mt-1">
                        <option :value="null" disabled>Select a category...</option>
                        <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
                    </select>
                </div>
            </form>

            <p v-else class="whitespace-pre-line">{{ modalMessage }}</p>
        </Modal>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Modal from '../components/Modal.vue'

const API_INGREDIENTS_URL = import.meta.env.VITE_API_INGREDIENTS_URL
const API_CATEGORIES_URL = import.meta.env.VITE_API_CATEGORIES_URL

const ingredients = ref([])
const categories = ref([])

// Estado del Modal
const isModalOpen = ref(false)
const isDeleteMode = ref(false)
const modalTitle = ref('')
const modalMessage = ref('')
const ingredientIdToDelete = ref(null)

const newIngredient = ref({ name: '', is_fresh: false, category_id: null })

const fetchIngredients = async () => {
    const res = await axios.get(API_INGREDIENTS_URL)
    ingredients.value = res.data
}

const fetchCategories = async () => {
    const res = await axios.get(API_CATEGORIES_URL)
    categories.value = res.data
}

// Lógica de Crear/Editar
const openCreateModal = () => {
    newIngredient.value = { name: '', is_fresh: false, category_id: null }
    modalTitle.value = 'New Ingredient'
    isDeleteMode.value = false
    isModalOpen.value = true
}

const openEditModal = (ing) => {
    newIngredient.value = { ...ing }
    modalTitle.value = 'Edit Ingredient'
    isDeleteMode.value = false
    isModalOpen.value = true
}

const saveIngredient = async () => {
    if (newIngredient.value.id) {
        await axios.put(`${API_INGREDIENTS_URL}/${newIngredient.value.id}`, newIngredient.value)
    } else {
        await axios.post(API_INGREDIENTS_URL, newIngredient.value)
    }
    await fetchIngredients()
    isModalOpen.value = false
}

// Lógica de Borrado
const initiateDelete = (ing) => {
    ingredientIdToDelete.value = ing.id
    modalTitle.value = "Confirmar eliminación"
    modalMessage.value = `¿Estás seguro de que quieres eliminar "${ing.name}"?`
    isDeleteMode.value = true
    isModalOpen.value = true
}

const handleConfirm = async () => {
    if (!isDeleteMode.value) {
        // Si estamos creando/editando, llamamos a save
        await saveIngredient()
    } else {
        // Si estamos borrando
        try {
            await axios.delete(`${API_INGREDIENTS_URL}/${ingredientIdToDelete.value}`)
            await fetchIngredients()
            isModalOpen.value = false
        } catch (error) {
            if (error.response?.status === 409) {
                modalTitle.value = "Conflicto de dependencias"
                modalMessage.value = `No se puede borrar. Está siendo utilizado en:\n• ${error.response.data.recipes.join('\n• ')}`
            } else {
                modalTitle.value = "Error"
                modalMessage.value = "No se pudo borrar el ingrediente."
                isModalOpen.value = true
                isModalOpen.value = false
            }
        }
    }
}

onMounted(() => {
    fetchIngredients()
    fetchCategories()
})
</script>