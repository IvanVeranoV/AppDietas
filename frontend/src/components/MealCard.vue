<template>
  <div class="meal-card">
    <div class="flex justify-between items-start mb-1">
      <span class="meal-card-type">{{ mealType }}</span>
      <span class="meal-card-badge">
        Keto
      </span>
    </div>
    <h3 class="meal-card-title">{{ title }}</h3>
    <p class="meal-card-calories">{{ calories }} kcal</p>
  </div>
</template>

<script setup>
defineProps({
    title: String,
    calories: Number,
    mealType: String, // 'Breakfast', 'Lunch', 'Dinner'
    tags: {
        type: Array,
        default: () => []
    }
})
</script>