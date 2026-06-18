<template>
  <aside class="w-64 bg-slate-900 h-screen text-slate-300 flex flex-col border-r border-slate-800">
    <div class="p-6">
      <h1 class="text-2xl font-bold text-emerald-400 flex items-center gap-2">
        <span class="text-3xl">🥗</span> AppDietas
      </h1>
    </div>

    <nav class="flex-1 px-4 space-y-2 mt-4">
      <router-link 
        to="/" 
        class="flex items-center gap-3 p-3 rounded-lg hover:bg-slate-800 hover:text-emerald-400 transition-colors"
        active-class="bg-slate-800 text-emerald-400 border-l-4 border-emerald-400"
      >
        <span>🏠</span> Inicio
      </router-link>

      <router-link 
        to="/recipes" 
        class="flex items-center gap-3 p-3 rounded-lg hover:bg-slate-800 hover:text-emerald-400 transition-colors"
        active-class="bg-slate-800 text-emerald-400 border-l-4 border-emerald-400"
      >
        <span>🍳</span> Mis Platos
      </router-link>

      <router-link 
        to="/calendar" 
        class="flex items-center gap-3 p-3 rounded-lg hover:bg-slate-800 hover:text-emerald-400 transition-colors"
        active-class="bg-slate-800 text-emerald-400 border-l-4 border-emerald-400"
      >
        <span>📅</span> Calendario
      </router-link>
    </nav>

    <div class="p-4 border-t border-slate-800 text-sm">
      <p class="text-slate-500">Sesión iniciada como:</p>
      <p class="font-medium text-slate-300">Usuario Demo</p>
    </div>
  </aside>
</template>