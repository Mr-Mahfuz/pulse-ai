<template>
  <div class="card hover:shadow-md hover:border-gray-300 dark:hover:border-gray-700 transition-all duration-200 cursor-pointer p-4"
       :class="effectiveLevel === 1 ? 'animate-pulse-border' : ''">
    <div class="flex items-start justify-between gap-4">
      <!-- Left: Patient info -->
      <div class="flex-1 min-w-0">
        <div class="flex items-center gap-2 mb-2">
          <div class="esi-badge" :style="{ backgroundColor: `${esiInfo.color}12`, color: esiInfo.color, border: `1px solid ${esiInfo.color}30` }">
            {{ esiInfo.icon }} ESI-{{ effectiveLevel }}
          </div>
          <span v-if="patient.clinician_override"
                class="text-[10px] px-2 py-0.5 rounded-full bg-orange-50 dark:bg-orange-950/30 text-orange-600 dark:text-orange-400 border border-orange-200 dark:border-orange-900/40 font-medium">
            OVERRIDE
          </span>
          <span v-if="patient.triage_source === 'red_flag_override'"
                class="text-[10px] px-2 py-0.5 rounded-full bg-red-50 dark:bg-red-950/30 text-red-600 dark:text-red-400 border border-red-200 dark:border-red-900/40 font-bold">
            🚩 RED FLAG
          </span>
        </div>

        <h3 class="text-sm font-semibold text-gray-900 dark:text-white truncate">
          {{ patient.name }}
          <span class="text-gray-400 dark:text-gray-500 text-xs font-normal ml-1">({{ patient.age }}{{ patient.gender }})</span>
        </h3>

        <p class="text-gray-500 dark:text-gray-400 text-xs mt-1 line-clamp-1">
          {{ patient.chief_complaint }}
        </p>
      </div>

      <!-- Right: Vitals + meta -->
      <div class="flex flex-col items-end gap-2 shrink-0">
        <div v-if="patient.triage_confidence" class="text-right">
          <span class="text-[10px] text-gray-400">Confidence</span>
          <div class="flex items-center gap-1.5">
            <div class="w-14 h-1.5 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
              <div class="h-full rounded-full transition-all duration-700"
                   :class="confidenceColor"
                   :style="{ width: `${patient.triage_confidence * 100}%` }"></div>
            </div>
            <span class="text-xs font-mono font-semibold text-gray-600 dark:text-gray-300">
              {{ Math.round(patient.triage_confidence * 100) }}%
            </span>
          </div>
        </div>

        <div class="flex items-center gap-2 text-[10px] font-mono">
          <span :class="getVitalClass('heart_rate', patient.heart_rate)">HR:{{ patient.heart_rate || '—' }}</span>
          <span :class="getVitalClass('spo2', patient.spo2)">SpO₂:{{ patient.spo2 || '—' }}%</span>
        </div>

        <span class="text-[10px] text-gray-400 dark:text-gray-500">⏱ {{ formatTimeAgo(patient.arrival_time) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { getEsiLevel, getEffectiveLevel, formatTimeAgo, getVitalStatus } from '~/utils/esi'

const props = defineProps({ patient: { type: Object, required: true } })

const effectiveLevel = computed(() => getEffectiveLevel(props.patient) || 5)
const esiInfo = computed(() => getEsiLevel(effectiveLevel.value))

const confidenceColor = computed(() => {
  const conf = props.patient.triage_confidence || 0
  if (conf >= 0.8) return 'bg-emerald-500'
  if (conf >= 0.6) return 'bg-amber-500'
  return 'bg-red-500'
})

const getVitalClass = (name, value) => {
  const status = getVitalStatus(name, value)
  return {
    normal: 'text-gray-400 dark:text-gray-500',
    warning: 'text-amber-600 dark:text-amber-400 font-semibold',
    critical: 'text-red-600 dark:text-red-400 font-bold',
  }[status]
}
</script>
