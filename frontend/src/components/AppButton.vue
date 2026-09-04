<script setup>
defineProps({
  variant: {
    type: String,
    default: 'primary'
  },
  type: {
    type: String,
    default: 'button'
  }
})
</script>

<template>
  <button
    v-bind="$attrs"
    :type="type"
    class="app-button"
    :class="`app-button-${variant}`">
    <slot />
  </button>
</template>
