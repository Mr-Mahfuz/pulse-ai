<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-950 flex flex-col items-center justify-center p-4 font-sans text-center">
    <div class="mb-8 w-20 h-20 bg-blue-600 rounded-2xl flex items-center justify-center shadow-lg mx-auto">
      <svg class="w-10 h-10 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
        <path d="M12 4v16M4 12h16"/>
      </svg>
    </div>
    
    <h1 class="text-7xl font-black text-gray-900 dark:text-white tracking-tight mb-2">
      {{ error.statusCode === 404 ? '404' : error.statusCode }}
    </h1>
    <h2 class="text-2xl font-bold text-gray-700 dark:text-gray-300 mb-6">
      {{ error.statusCode === 404 ? 'Page Not Found' : 'An Error Occurred' }}
    </h2>
    
    <p class="text-gray-500 dark:text-gray-400 max-w-md mx-auto mb-10">
      {{ error.message || "We couldn't find the page you were looking for. It might have been moved or doesn't exist." }}
    </p>

    <button @click="handleError" class="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl shadow-lg shadow-blue-600/30 transition-all active:scale-95 flex items-center gap-2 mx-auto">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/></svg>
      Return to Dashboard
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  error: Object
})

const handleError = () => clearError({ redirect: '/' })

useHead({
  title: `${props.error.statusCode} - SmartTriage`,
  bodyAttrs: { class: 'bg-gray-50 dark:bg-gray-950' }
})
</script>
