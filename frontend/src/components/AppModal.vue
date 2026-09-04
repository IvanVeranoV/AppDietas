<script setup>
import AppButton from './AppButton.vue'

defineProps({
  show: Boolean,
  title: {
    type: String,
    required: true
  },
  form: Boolean
})

const emit = defineEmits(['close', 'submit'])
</script>

<template>
  <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center p-4">
    <div class="modal-backdrop" @click="emit('close')"></div>

    <div class="modal-shell-alt animate-in fade-in zoom-in-95 duration-200">
      <component
        :is="form ? 'form' : 'div'"
        @submit.prevent="form && emit('submit')">
        <div class="modal-header">
          <h3 class="text-xl font-bold text-slate-100">{{ title }}</h3>
          <AppButton variant="icon" @click="emit('close')">✕</AppButton>
        </div>

        <div class="p-6 max-h-[65vh] overflow-y-auto">
          <slot />
        </div>

        <div class="modal-footer">
          <slot name="footer">
            <AppButton variant="secondary" @click="emit('close')">Cancel</AppButton>
          </slot>
        </div>
      </component>
    </div>
  </div>
</template>
