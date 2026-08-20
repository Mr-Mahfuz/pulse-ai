<template>
  <div class="min-h-screen bg-gray-950 text-white p-8">
    <!-- Header -->
    <div class="flex items-center justify-between mb-10 pb-6 border-b border-gray-800">
      <div class="flex items-center gap-4">
        <div class="w-16 h-16 bg-blue-600 rounded-2xl flex items-center justify-center">
          <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/></svg>
        </div>
        <div>
          <h1 class="text-4xl font-black tracking-tight">SmartTriage <span class="text-blue-500 text-3xl">AI</span></h1>
          <p class="text-xl text-gray-400 mt-1">ED Waiting Room Status</p>
        </div>
      </div>
      <div class="text-right">
        <div class="text-4xl font-bold font-mono">{{ currentTime }}</div>
        <div class="text-lg text-emerald-400 font-semibold mt-2 animate-pulse flex items-center gap-2 justify-end">
          <span class="w-3 h-3 rounded-full bg-emerald-500"></span> Live Queue Updates
        </div>
      </div>
    </div>

    <!-- Active Callouts (ESI-1/2) -->
    <div v-if="criticalPatients.length > 0" class="mb-10">
      <h2 class="text-xl font-bold text-gray-400 uppercase tracking-widest mb-4">Please Proceed Immediately</h2>
      <div class="grid grid-cols-2 gap-6">
        <div v-for="patient in criticalPatients.slice(0, 4)" :key="patient.id" 
             class="bg-red-900/30 border-2 border-red-500/50 rounded-2xl p-6 flex items-center justify-between shadow-[0_0_30px_rgba(220,38,38,0.2)]">
          <div>
            <div class="text-3xl font-black text-white mb-2">{{ maskName(patient.name) }}</div>
            <div class="text-lg text-red-200">{{ patient.age }}y • {{ patient.gender }}</div>
          </div>
          <div class="text-center bg-red-600 px-6 py-3 rounded-xl font-black text-2xl uppercase tracking-wider animate-pulse">
            Triage Desk A
          </div>
        </div>
      </div>
    </div>

    <!-- Main Queue -->
    <div>
      <h2 class="text-xl font-bold text-gray-400 uppercase tracking-widest mb-4">Current Queue</h2>
      
      <div class="grid grid-cols-12 gap-4 text-sm font-bold text-gray-500 uppercase tracking-wider px-6 mb-2">
        <div class="col-span-1">Priority</div>
        <div class="col-span-4">Patient Name</div>
        <div class="col-span-4">Symptoms</div>
        <div class="col-span-3 text-right">Est. Wait</div>
      </div>

      <div class="space-y-4">
        <div v-for="(patient, idx) in standardPatients.slice(0, 10)" :key="patient.id"
             class="grid grid-cols-12 gap-4 items-center bg-gray-900 border border-gray-800 rounded-2xl p-6 transition-all"
             :class="idx === 0 ? 'bg-gray-800 border-gray-700 shadow-lg' : ''">
          
          <!-- Priority Badge -->
          <div class="col-span-1">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center font-black text-xl"
                 :class="getPriorityClass(getEffectiveLevel(patient))">
              {{ getEffectiveLevel(patient) || '?' }}
            </div>
          </div>
          
          <!-- Patient -->
          <div class="col-span-4">
            <div class="text-2xl font-bold text-white">{{ maskName(patient.name) }}</div>
            <div class="text-gray-400">{{ patient.age }}y</div>
          </div>
          
          <!-- Symptoms -->
          <div class="col-span-4">
            <div class="text-lg text-gray-300 truncate pr-4">{{ patient.chief_complaint }}</div>
          </div>
          
          <!-- Wait Time -->
          <div class="col-span-3 text-right">
            <div class="text-3xl font-mono font-bold" :class="idx < 3 ? 'text-amber-400' : 'text-gray-300'">
              {{ getEstimatedWait(patient, idx) }}
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="standardPatients.length > 10" class="text-center text-gray-500 mt-8 font-semibold text-lg">
      + {{ standardPatients.length - 10 }} more patients waiting
    </div>
  </div>
</template>

<script setup>
import { getEffectiveLevel } from '~/utils/esi'

definePageMeta({ layout: false })

const { getPatients } = useApi()

// ALWAYS FORCE PRIVACY MODE ON PUBLIC MONITOR
const maskName = (name) => {
  if (!name) return name
  const parts = name.split(' ')
  return parts.map(p => p.charAt(0) + '*'.repeat(Math.max(1, p.length - 1))).join(' ')
}

const patients = ref([])
let interval = null
let timeInterval = null
const currentTime = ref('')

const activePatients = computed(() => patients.value.filter(p => p.status === 'waiting'))

// Sort by severity then wait time
const sortedPatients = computed(() => {
  return [...activePatients.value].sort((a, b) => {
    const levelA = getEffectiveLevel(a) || 99
    const levelB = getEffectiveLevel(b) || 99
    if (levelA !== levelB) return levelA - levelB
    return new Date(a.arrival_time) - new Date(b.arrival_time)
  })
})

const criticalPatients = computed(() => sortedPatients.value.filter(p => getEffectiveLevel(p) <= 2))
const standardPatients = computed(() => sortedPatients.value.filter(p => getEffectiveLevel(p) > 2))

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true })
}

const fetchPatients = async () => {
  try {
    patients.value = await getPatients()
  } catch (e) {
    console.error(e)
  }
}

const getPriorityClass = (level) => {
  if (level === 1) return 'bg-red-500 text-white'
  if (level === 2) return 'bg-orange-500 text-white'
  if (level === 3) return 'bg-yellow-500 text-yellow-900'
  if (level === 4) return 'bg-green-500 text-white'
  if (level === 5) return 'bg-blue-500 text-white'
  return 'bg-gray-700 text-gray-300'
}

const getEstimatedWait = (patient, idx) => {
  // Simple deterministic visual estimation for the board
  const level = getEffectiveLevel(patient)
  if (level <= 2) return 'NOW'
  const minutes = Math.max(10, idx * (level === 3 ? 15 : 10))
  return `~${minutes}m`
}

onMounted(() => {
  updateTime()
  timeInterval = setInterval(updateTime, 1000)
  
  fetchPatients()
  interval = setInterval(fetchPatients, 5000) // Fast refresh for monitor
})

onUnmounted(() => {
  if (interval) clearInterval(interval)
  if (timeInterval) clearInterval(timeInterval)
})
</script>
