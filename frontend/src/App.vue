<script setup>
import Sidebar from './components/Sidebar.vue'
</script>

<template>
  <div class="flex min-h-screen bg-slate-950 text-slate-100">
    <Sidebar />

    <main class="flex-1 p-8 overflow-y-auto">
      <router-view></router-view>
    </main>
  </div>
</template>