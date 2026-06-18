<script setup>
import { ref } from 'vue'
const mensaje = ref('¡AppDietas con Tailwind CSS!')
</script>

<template>
  <div class="min-h-screen bg-slate-900 text-white flex flex-col items-center justify-center p-6">
    <div class="bg-slate-800 p-8 rounded-2xl shadow-xl border border-slate-700 text-center max-w-md">
      <h1 class="text-3xl font-bold text-emerald-400 mb-4">{{ mensaje }}</h1>
      <p class="text-slate-400 mb-6">El motor de estilos está configurado. Ya podemos olvidarnos de escribir CSS tradicional.</p>
      <button class="bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-semibold px-6 py-2 rounded-lg transition-colors">
        ¡A rodar!
      </button>
    </div>
  </div>
</template>

<style scoped>
/* Vacío. No hace falta CSS tradicional */
</style>