<template>
  <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <div class="modal-overlay" @click="$emit('close')"></div>
    <div class="modal-shell">
      <h3 class="text-xl font-bold text-white mb-4">{{ title }}</h3>
      <div class="text-slate-300 mb-6 whitespace-pre-line">
        <slot></slot>
      </div>
      <div class="flex justify-end gap-3">
        <button type="button" @click="$emit('close')" class="px-4 py-2 text-slate-400 hover:text-white transition">Cancel</button>
        <button type="button" @click="$emit('confirm')" class="btn-primary px-5 py-2">Confirm</button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  show: Boolean,
  title: String
});
defineEmits(['close', 'confirm']);
</script>