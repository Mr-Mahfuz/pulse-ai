<template>
  <div :class="[colorMode, 'min-h-screen font-sans']">
    <!-- Sidebar -->
    <aside class="fixed inset-y-0 left-0 w-64 z-30 flex flex-col bg-white dark:bg-gray-950 border-r border-gray-200 dark:border-gray-800 print:hidden">
      <!-- Logo -->
      <div class="h-16 flex items-center gap-3 px-6 border-b border-gray-100 dark:border-gray-800 shrink-0">
        <div class="w-9 h-9 rounded-xl bg-blue-600 flex items-center justify-center shadow-sm">
          <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
            <path d="M12 4v16M4 12h16"/>
          </svg>
        </div>
        <div>
          <span class="text-base font-bold text-gray-900 dark:text-white tracking-tight">SmartTriage</span>
          <span class="text-[10px] font-medium text-blue-600 dark:text-blue-400 ml-1 uppercase tracking-wider">AI</span>
        </div>
      </div>

      <!-- Navigation -->
      <!-- Sidebar Content -->
      <div class="flex-1 overflow-y-auto px-4 py-4 space-y-6">
        <!-- Main Menu -->
        <div class="space-y-1.5">
          <div class="px-3 mb-2 text-xs font-bold text-gray-400 dark:text-gray-500 tracking-wider">{{ $t('nav.main_menu') }}</div>
          
          <NuxtLink to="/" class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold transition-all text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20">
            <div class="p-1.5 rounded-lg bg-blue-100 dark:bg-blue-800/50 text-blue-600 dark:text-blue-400">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
            </div>
            {{ $t('nav.triage_queue') }}
          </NuxtLink>

          <NuxtLink to="/analytics" class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold transition-all text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800/50">
            <div class="p-1.5 rounded-lg bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
            </div>
            {{ $t('nav.analytics') }}
          </NuxtLink>
        </div>

        <!-- System -->
        <div class="space-y-1.5">
          <div class="px-3 mb-2 text-xs font-bold text-gray-400 dark:text-gray-500 tracking-wider">{{ $t('nav.system') }}</div>
          
          <NuxtLink to="/monitor" class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold transition-all text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800/50">
            <div class="p-1.5 rounded-lg bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
            </div>
            Public Monitor
          </NuxtLink>
          
          <button class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold transition-all text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800/50">
            <div class="p-1.5 rounded-lg bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
            </div>
            {{ $t('nav.staff_directory') }}
          </button>
          
          <button class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold transition-all text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800/50">
            <div class="p-1.5 rounded-lg bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
            </div>
            {{ $t('nav.settings') }}
          </button>
        </div>
      </div>

      <!-- Bottom Actions -->
      <div class="px-6 pb-6 pt-4 space-y-2">

        <!-- User -->
        <div class="flex items-center gap-3 px-3 py-2.5">
          <div class="w-8 h-8 rounded-full bg-gradient-to-br from-emerald-500 to-emerald-700 flex items-center justify-center text-white text-xs font-bold shadow-sm">NA</div>
          <div class="flex-1 min-w-0">
            <div class="text-sm font-semibold text-gray-900 dark:text-white truncate">Nurse Akter</div>
            <div class="text-[11px] text-gray-400 dark:text-gray-500">Triage Desk (ED)</div>
          </div>
        </div>
      </div>
    </aside>

    <!-- Main Area -->
    <div class="pl-64 print:pl-0 flex flex-col min-h-screen bg-transparent print:bg-white">
      <!-- Top Bar -->
      <header class="h-14 bg-white/80 dark:bg-gray-950/80 backdrop-blur-xl border-b border-gray-200/60 dark:border-gray-800/60 sticky top-0 z-20 grid grid-cols-3 items-center px-8 print:hidden">
        <!-- Left: Unit Info -->
        <div class="flex items-center gap-2 text-sm text-gray-400 dark:text-gray-500">
          <span>ER Department</span>
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
          <span class="font-medium text-gray-700 dark:text-gray-300">Triage Unit A</span>
        </div>

        <!-- Center: Clock -->
        <div class="flex items-center justify-center">
          <div class="text-xs font-mono font-medium text-gray-500 dark:text-gray-400 tabular-nums bg-gray-50 dark:bg-gray-900/50 px-3 py-1.5 rounded-full border border-gray-100 dark:border-gray-800">
            {{ currentTime }}
          </div>
        </div>

        <!-- Right: Controls & Status -->
        <div class="flex items-center justify-end gap-5">
          <!-- Language Toggle -->
          <button @click="$i18n.setLocale($i18n.locale === 'en' ? 'bn' : 'en')" class="flex items-center gap-1.5 text-xs font-bold text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors" title="Toggle Language">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            {{ $i18n.locale === 'en' ? 'EN' : 'BN' }}
          </button>

          <!-- Theme Toggle -->
          <button @click="toggleTheme" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors" title="Toggle Theme">
            <svg v-if="colorMode.value === 'dark'" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
            <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/></svg>
          </button>

          <div class="h-4 w-px bg-gray-200 dark:bg-gray-800"></div>

          <!-- Status -->
          <div class="flex items-center gap-2">
            <span class="relative flex h-2 w-2">
              <span v-if="isOnline" class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2" :class="isOnline ? 'bg-emerald-500' : 'bg-red-500'"></span>
            </span>
            <span class="text-[11px] font-medium uppercase tracking-wider" :class="isOnline ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-500'">
              {{ isOnline ? 'Connected' : 'Offline' }}
            </span>
          </div>
        </div>
      </header>

      <!-- Page -->
      <main class="flex-1 p-6 lg:p-8 print:p-0 print:m-0">
        <div class="max-w-[1400px] mx-auto print:max-w-none">
          <NuxtPage />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
const colorMode = useCookie('colorMode', { default: () => 'light' })
const isOnline = ref(false)
const currentTime = ref('')
let healthCheckInterval = null
let clockInterval = null

const toggleTheme = () => {
  colorMode.value = colorMode.value === 'light' ? 'dark' : 'light'
  if (process.client) {
    document.documentElement.classList.toggle('dark', colorMode.value === 'dark')
  }
}

const updateClock = () => {
  currentTime.value = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true })
}

useHead({
  htmlAttrs: { class: computed(() => colorMode.value) },
  bodyAttrs: { class: 'bg-gray-50 dark:bg-gray-950' },
})

const checkHealth = async () => {
  try {
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase || 'http://localhost:8000'
    const res = await fetch(`${apiBase}/api/health`)
    isOnline.value = res.ok
  } catch { isOnline.value = false }
}

onMounted(() => {
  if (process.client && colorMode.value === 'dark') {
    document.documentElement.classList.add('dark')
  }
  checkHealth()
  healthCheckInterval = setInterval(checkHealth, 10000)
  updateClock()
  clockInterval = setInterval(updateClock, 1000)
})

onUnmounted(() => {
  if (healthCheckInterval) clearInterval(healthCheckInterval)
  if (clockInterval) clearInterval(clockInterval)
})
</script>

<style scoped>
.nav-link {
  @apply flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-lg transition-all duration-150
         text-gray-500 dark:text-gray-400
         hover:text-gray-900 dark:hover:text-white
         hover:bg-gray-100 dark:hover:bg-gray-800/60;
}
.nav-link.router-link-active {
  @apply bg-blue-50 dark:bg-blue-950/40 text-blue-700 dark:text-blue-400 font-semibold;
}
.nav-link.router-link-active .nav-icon {
  @apply text-blue-600 dark:text-blue-400;
}
.nav-icon {
  @apply w-8 h-8 flex items-center justify-center rounded-lg bg-gray-50 dark:bg-gray-800/50 
         text-gray-400 dark:text-gray-500 transition-colors shrink-0;
}
.nav-link:hover .nav-icon {
  @apply bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300;
}
.nav-link.router-link-active .nav-icon {
  @apply bg-blue-100 dark:bg-blue-900/40 text-blue-600 dark:text-blue-400;
}
</style>
