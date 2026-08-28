<template>
  <div class="calendar-shell">
    <div class="flex justify-between items-center mb-8">
      <h2 class="text-2xl font-bold text-white">Weekly Menu</h2>
      <button type="button" class="calendar-header-button">
        + New Recipe
      </button>
    </div>

    <div class="w-full flex flex-col gap-2">
      <div class="grid grid-cols-[100px_repeat(7,1fr)] gap-4 mb-4">
        <div></div>
        <div v-for="day in weekDays" :key="day.date" class="text-center">
          <p class="text-[10px] font-bold text-gray-400 uppercase tracking-wider">{{ day.name }}</p>
          <p class="text-lg font-bold text-white">{{ day.dateNumber }}</p>
        </div>
      </div>

      <div v-for="type in ['Breakfast', 'Lunch', 'Dinner']" :key="type" class="grid grid-cols-[100px_repeat(7,1fr)] gap-4 items-center mb-2">
        <div class="font-bold text-gray-400 text-xs tracking-widest uppercase text-right pr-4">
          {{ type }}
        </div>

        <div v-for="day in weekDays" :key="day.date + type" class="calendar-cell">
          <MealCard
            v-if="findMeal(day.date, type)"
            :title="findMeal(day.date, type).title"
            :calories="findMeal(day.date, type).calories"
            :mealType="type"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import MealCard from '../../components/MealCard.vue'

// Datos de ejemplo simulando tu base de datos
const weekDays = [
  { name: 'Mon', date: '2026-07-21', dateNumber: 21 },
  { name: 'Tue', date: '2026-07-22', dateNumber: 22 },
  { name: 'Wed', date: '2026-07-23', dateNumber: 23 },
  // ... añadir el resto
]

const meals = [
  { date: '2026-07-21', type: 'Breakfast', title: 'Avocado Toast', calories: 320 }
]

const findMeal = (date, type) => meals.find(m => m.date === date && m.type === type)
</script>