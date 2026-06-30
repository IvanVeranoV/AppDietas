<template>
  <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <div class="absolute inset-0 bg-slate-950/80 backdrop-blur-sm" @click="$emit('close')"></div>
    <div class="relative bg-slate-900 border border-slate-700 w-full max-w-lg rounded-2xl shadow-2xl p-6">
      <h3 class="text-xl font-bold text-white mb-4">{{ title }}</h3>
      <div class="text-slate-300 mb-6 whitespace-pre-line">
        <slot></slot>
      </div>
      <div class="flex justify-end gap-3">
        <button @click="$emit('close')" class="px-4 py-2 text-slate-400 hover:text-white transition">Cancel</button>
        <button @click="$emit('confirm')"
          class="bg-emerald-500 hover:bg-slate-950 font-bold px-5 py-2 rounded-lg transition">Confirm</button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps(['show', 'title']);
defineEmits(['close', 'confirm']);
</script>