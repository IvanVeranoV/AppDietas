<template>
  <div class="calendar-shell">
    <PageHeader title="Weekly Menu" />

    <div class="grid grid-cols-7 gap-2">
      <div v-for="day in ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']" :key="day"
        class="text-center font-bold p-2">
        {{ day }}
      </div>

      <div v-for="date in currentWeekDates" :key="date" class="min-h-37.5 border rounded p-2 hover:bg-gray-50">
        <div class="text-sm text-gray-500 mb-2">{{ date }}</div>

        <div v-for="menu in calendarData[date]" :key="menu.id"
          class="bg-emerald-100 text-emerald-800 text-xs p-1 mb-1 rounded">
          {{ menu.recipe_name }}
        </div>

        <AppButton variant="primary" @click="openAddMenuModal(date)">
          Add Meal
        </AppButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import PageHeader from '../../components/PageHeader.vue'
import AppButton from '../../components/AppButton.vue'

// 1. Datos de ejemplo para que la interfaz cargue
const currentWeekDates = ref(['2026-07-01', '2026-07-02', '2026-07-03', '2026-07-04', '2026-07-05', '2026-07-06', '2026-07-07'])
const calendarData = ref({
  '2026-07-01': [{ id: 1, recipe_name: 'Pasta Carbonara' }]
})

// 2. Definición de funciones que usa el template
const openAddMenuModal = (date) => {
  calendarData.value[date] ??= []
}
</script>