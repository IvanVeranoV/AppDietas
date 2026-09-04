<template>
  <AppModal :show="show" :title="title" @close="$emit('close')">
    <div class="text-slate-300 whitespace-pre-line">
      <slot></slot>
    </div>

    <template #footer>
      <AppButton variant="secondary" @click="$emit('close')">Cancel</AppButton>
      <AppButton variant="primary" @click="$emit('confirm')">Confirm</AppButton>
    </template>
  </AppModal>
</template>

<script setup>
import AppButton from './AppButton.vue'
import AppModal from './AppModal.vue'

defineProps({
  show: Boolean,
  title: String
});
defineEmits(['close', 'confirm']);
</script>