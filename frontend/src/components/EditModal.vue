<template>
  <AppModal :show="show" :title="title" form @close="close" @submit="confirm">
    <slot></slot>

    <template #footer>
      <AppButton variant="secondary" @click="close">
        Cancel
      </AppButton>
      <AppButton type="submit" variant="primary">
        {{ confirmText }}
      </AppButton>
    </template>
  </AppModal>
</template>

<script setup>
import AppButton from './AppButton.vue'
import AppModal from './AppModal.vue'

defineProps({
  show: Boolean,
  title: String,
  confirmText: {
    type: String,
    default: 'Save Changes'
  }
})

const emit = defineEmits(['close', 'confirm'])

const close = () => emit('close')
const confirm = () => emit('confirm')
</script>
