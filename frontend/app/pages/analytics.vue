<template>
  <div class="space-y-6">
    <!-- Header -->
    <div>
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white tracking-tight">{{ $t('analytics.title') }}</h1>
      <p class="text-sm text-gray-500 dark:text-gray-400 mt-0.5">{{ $t('analytics.subtitle') }}</p>
    </div>

    <!-- KPI Row -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="stat-card !bg-gradient-to-br !from-blue-600 !to-blue-700 !border-blue-500 text-white">
        <span class="stat-label !text-blue-200">{{ $t('analytics.patients_today') }}</span>
        <span class="stat-value !text-white">{{ patients.length || '—' }}</span>
        <div class="flex items-center gap-1 text-xs text-blue-200 mt-1">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/></svg>
          12% vs yesterday
        </div>
      </div>

      <div class="stat-card">
        <span class="stat-label">{{ $t('analytics.avg_wait_2') }}</span>
        <div class="flex items-baseline gap-1">
          <span class="stat-value text-orange-600 dark:text-orange-400">14</span>
          <span class="text-sm text-gray-400 font-medium">min</span>
        </div>
        <div class="flex items-center gap-1 text-xs text-emerald-600 dark:text-emerald-400 mt-1 font-medium">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6"/></svg>
          2 min improvement
        </div>
      </div>

      <div class="stat-card">
        <span class="stat-label">{{ $t('analytics.avg_wait_3') }}</span>
        <div class="flex items-baseline gap-1">
          <span class="stat-value text-amber-600 dark:text-amber-400">42</span>
          <span class="text-sm text-gray-400 font-medium">min</span>
        </div>
        <div class="flex items-center gap-1 text-xs text-red-600 dark:text-red-400 mt-1 font-medium">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/></svg>
          5 min slower
        </div>
      </div>

      <div class="stat-card">
        <span class="stat-label">{{ $t('analytics.ai_concordance') }}</span>
        <div class="flex items-baseline gap-1">
          <span class="stat-value text-gray-900 dark:text-white">92</span>
          <span class="text-sm text-gray-400 font-medium">%</span>
        </div>
        <div class="text-xs text-gray-400 dark:text-gray-500 mt-1 font-medium">Agreement with clinicians</div>
      </div>
    </div>

    <!-- Charts -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- ESI Distribution -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ $t('analytics.esi_distribution') }}</h3>
        </div>
        <div class="card-body space-y-4">
          <div v-for="level in [1,2,3,4,5]" :key="level" class="flex items-center gap-4">
            <span class="text-xs font-semibold w-14 text-gray-600 dark:text-gray-400">ESI-{{ level }}</span>
            <div class="flex-1 h-3 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
              <div class="h-full rounded-full transition-all duration-1000 ease-out"
                   :style="{ width: `${patients.length ? ((esiCounts[level] || 0) / patients.length) * 100 : 0}%`, backgroundColor: getEsiLevel(level).color }"></div>
            </div>
            <span class="text-sm font-mono font-bold w-8 text-right text-gray-700 dark:text-gray-300 tabular-nums">{{ esiCounts[level] || 0 }}</span>
          </div>
        </div>
      </div>

      <!-- Recent Overrides -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">{{ $t('analytics.recent_overrides') }}</h3>
        </div>
        <div class="card-body">
          <div v-if="overriddenPatients.length" class="space-y-3">
            <NuxtLink v-for="p in overriddenPatients.slice(0, 5)" :key="p.id" :to="`/patient/${p.id}`"
                      class="block p-3.5 rounded-xl border border-gray-100 dark:border-gray-800 hover:border-blue-200 dark:hover:border-blue-900/50 hover:bg-blue-50/30 dark:hover:bg-blue-950/10 transition-all">
              <div class="flex items-center justify-between mb-1.5">
                <span class="font-semibold text-sm text-gray-900 dark:text-white">{{ p.name }}</span>
                <span class="text-[10px] text-gray-400 dark:text-gray-500 font-mono">{{ formatTimeAgoShort(p.arrival_time) }}</span>
              </div>
              <div class="flex items-center gap-2 text-xs">
                <span class="text-gray-400 line-through">ESI-{{ p.triage_level?.level }}</span>
                <svg class="w-3 h-3 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
                <span class="font-bold text-orange-600 dark:text-orange-400">ESI-{{ p.clinician_override }}</span>
              </div>
              <p class="text-[11px] text-gray-400 dark:text-gray-500 mt-1.5 line-clamp-1">{{ p.override_reason }}</p>
            </NuxtLink>
          </div>
          <div v-else class="text-center py-14 text-gray-400 dark:text-gray-500">
            <svg class="w-10 h-10 mx-auto mb-2 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
            <p class="text-sm font-medium">{{ $t('analytics.no_overrides') }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { getEsiLevel, getEffectiveLevel } from '~/utils/esi'

const { getPatients } = useApi()
const patients = ref([])

const esiCounts = computed(() => {
  const counts = {}
  for (const p of patients.value) {
    const level = getEffectiveLevel(p)
    if (level) counts[level] = (counts[level] || 0) + 1
  }
  return counts
})

const overriddenPatients = computed(() => patients.value.filter(p => p.clinician_override))

const formatTimeAgoShort = (timestamp) => {
  if (!timestamp) return ''
  const diffMinutes = Math.floor((new Date() - new Date(timestamp + 'Z')) / 60000)
  if (diffMinutes < 60) return `${diffMinutes}m ago`
  return `${Math.floor(diffMinutes / 60)}h ago`
}

onMounted(async () => {
  try { patients.value = await getPatients() } catch (e) { console.error(e) }
})
</script>
