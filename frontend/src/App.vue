<script setup>
import Sidebar from './components/Sidebar.vue'
</script>

<template>
  <div class="flex h-screen overflow-hidden bg-slate-950 text-slate-100">
    <Sidebar />

    <main class="flex-1 min-w-0 p-8 overflow-hidden">
      <router-view v-slot="{ Component }">
        <component :is="Component" class="route-content" />
      </router-view>
    </main>
  </div>
</template>