<template>
  <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <div @click="close" class="modal-backdrop"></div>

    <div class="modal-shell-alt animate-in fade-in zoom-in-95 duration-200">
      <div class="modal-header">
        <h3 class="text-xl font-bold text-slate-100">{{ title }}</h3>
        <button type="button" @click="close" class="btn-icon">✕</button>
      </div>

      <form @submit.prevent="confirm">
        <div class="p-6 space-y-5 max-h-[65vh] overflow-y-auto">
          <slot></slot>
        </div>

        <div class="modal-footer">
          <button type="button" @click="close" class="btn-secondary px-4 py-2 text-sm">
            Cancel
          </button>
          <button type="submit" class="btn-primary px-5 py-2 text-sm">
            {{ confirmText }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
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
