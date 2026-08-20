<template>
  <div class="h-8 w-full relative group">
    <svg class="w-full h-full" preserveAspectRatio="none" viewBox="0 0 100 30" v-if="points.length > 1">
      <!-- Glow effect -->
      <path :d="linePath" fill="none" :stroke="color" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" class="opacity-20 blur-[2px]" />
      <!-- Main line -->
      <path :d="linePath" fill="none" :stroke="color" stroke-width="2" vector-effect="non-scaling-stroke" stroke-linecap="round" stroke-linejoin="round" />
      <circle v-for="(p, i) in points" :key="i" :cx="p.x" :cy="p.y" r="2.5" :fill="color" />
    </svg>
    <div v-else-if="points.length === 1" class="h-full w-full flex items-center justify-center">
      <div class="w-2 h-2 rounded-full" :style="{ backgroundColor: color }"></div>
      <div class="w-full h-px bg-gray-200 dark:bg-gray-800 ml-2"></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  data: { type: Array, required: true },
  color: { type: String, default: '#3B82F6' }
})

const points = computed(() => {
  if (!props.data || props.data.length === 0) return []
  
  const values = props.data.map(d => Number(d.value)).filter(v => !isNaN(v))
  if (values.length === 0) return []
  if (values.length === 1) return [{ x: 50, y: 15 }]
  
  const min = Math.min(...values)
  const max = Math.max(...values)
  
  // Add some padding to the range so points don't hit the absolute top/bottom unless needed
  const padding = (max - min) * 0.1
  const paddedMin = min - padding
  const paddedMax = max + padding
  const range = paddedMax - paddedMin === 0 ? 1 : paddedMax - paddedMin
  
  return values.map((val, i) => {
    const x = (i / (values.length - 1)) * 94 + 3 // 3 to 97
    const y = 27 - ((val - paddedMin) / range) * 24 // 3 to 27
    return { x, y, value: val }
  })
})

const linePath = computed(() => {
  if (points.value.length < 2) return ''
  return `M ${points.value.map(p => `${p.x},${p.y}`).join(' L ')}`
})
</script>
