import axios from 'axios'

const API_RECIPES_URL = import.meta.env.VITE_API_RECIPES_URL
const API_INGREDIENTS_URL = import.meta.env.VITE_API_INGREDIENTS_URL

export const getRecipes = () => axios.get(API_RECIPES_URL)

export const getIngredients = () => axios.get(API_INGREDIENTS_URL)

export const createRecipe = (payload) => axios.post(API_RECIPES_URL, payload)

export const updateRecipe = (recipeId, payload) =>
  axios.patch(`${API_RECIPES_URL}/${recipeId}`, payload)

export const deleteRecipe = (recipeId) =>
  axios.delete(`${API_RECIPES_URL}/${recipeId}`)
