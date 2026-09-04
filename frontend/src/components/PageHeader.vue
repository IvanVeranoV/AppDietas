<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  subtitle: {
    type: String,
    default: ''
  }
})
</script>

<template>
  <header class="page-header">
    <div class="page-header-copy">
      <h2 class="app-page-title">{{ title }}</h2>
      <p v-if="subtitle" class="app-page-subtitle">{{ subtitle }}</p>
    </div>

    <div v-if="$slots.actions" class="page-header-actions">
      <slot name="actions" />
    </div>
  </header>
</template>
