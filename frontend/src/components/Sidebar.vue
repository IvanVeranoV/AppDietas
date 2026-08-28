<template>
  <aside class="sidebar-shell">
    <div class="p-6">
      <h1 class="sidebar-brand">
        <span class="text-3xl">🥗</span> AppDietas
      </h1>
    </div>

    <nav class="flex-1 px-4 space-y-2 mt-4">
      <router-link to="/" class="sidebar-link" active-class="bg-slate-800 text-emerald-400 border-l-4 border-emerald-400">
        <span>🏠</span> Inicio
      </router-link>

      <router-link to="/ingredients" class="sidebar-link" active-class="bg-slate-800 text-emerald-400 border-l-4 border-emerald-400">
        <span>🥗</span> Ingredientes
      </router-link>

      <router-link to="/recipes" class="sidebar-link" active-class="bg-slate-800 text-emerald-400 border-l-4 border-emerald-400">
        <span>🍳</span> Mis Platos
      </router-link>

      <router-link to="/calendar" class="sidebar-link" active-class="bg-slate-800 text-emerald-400 border-l-4 border-emerald-400">
        <span>📅</span> Calendario
      </router-link>
    </nav>

    <div class="sidebar-footer">
      <p class="text-slate-500">Sesión iniciada como:</p>
      <p class="font-medium text-slate-300">Usuario Demo</p>
    </div>
  </aside>
</template>