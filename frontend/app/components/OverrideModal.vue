<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center animate-fade-in" @click.self="$emit('close')">
    <div class="absolute inset-0 bg-black/40 backdrop-blur-sm"></div>

    <div class="relative bg-white dark:bg-gray-900 rounded-2xl shadow-2xl w-full max-w-md mx-4 border border-gray-200 dark:border-gray-800 animate-slide-up">

      <!-- Header -->
      <div class="flex items-center justify-between px-6 py-5 border-b border-gray-100 dark:border-gray-800">
        <div>
          <h2 class="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <span class="text-orange-500">✋</span> {{ $t('override_modal.title') }}
          </h2>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-0.5">{{ $t('override_modal.subtitle') }}</p>
        </div>
        <button @click="$emit('close')" class="btn-ghost !p-2 !rounded-full">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Body -->
      <div class="p-6 space-y-5">
        <!-- Warning -->
        <div class="p-3.5 rounded-xl bg-amber-50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-900/40 text-sm text-amber-800 dark:text-amber-300">
          {{ $t('override_modal.warning') }}
        </div>

        <!-- ESI Selector -->
        <div>
          <div class="form-label mb-2">{{ $t('override_modal.select_esi') }}</div>
          <div class="grid grid-cols-5 gap-2">
            <button v-for="level in [1,2,3,4,5]" :key="level" type="button" @click="newLevel = level"
                    class="py-3 rounded-xl border-2 font-bold text-sm transition-all flex flex-col items-center gap-1"
                    :class="newLevel === level
                      ? 'scale-105 shadow-md'
                      : 'border-gray-200 dark:border-gray-700 text-gray-400 hover:border-gray-300 dark:hover:border-gray-600'"
                    :style="newLevel === level ? { borderColor: getEsiLevel(level).color, backgroundColor: `${getEsiLevel(level).color}10`, color: getEsiLevel(level).color } : {}">
              <span class="text-base">{{ getEsiLevel(level).icon }}</span>
              <span>{{ level }}</span>
            </button>
          </div>
        </div>

        <!-- Reason -->
        <div>
          <label class="form-label">{{ $t('override_modal.justification') }} <span class="text-red-500">*</span></label>
          <textarea v-model="reason" class="form-input resize-none" rows="3"></textarea>
        </div>
      </div>

      <!-- Footer -->
      <div class="flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-100 dark:border-gray-800">
        <button @click="$emit('close')" class="btn-secondary" :disabled="loading">{{ $t('override_modal.cancel') }}</button>
        <button @click="submit" class="btn-primary !bg-orange-600 hover:!bg-orange-700 dark:!bg-orange-600 dark:hover:!bg-orange-700 !text-white" :disabled="loading || !reason || !newLevel">
          <svg v-if="loading" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
          {{ $t('override_modal.confirm') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { getEsiLevel } from '~/utils/esi'

const props = defineProps({ patient: { type: Object, required: true } })
const emit = defineEmits(['close', 'overridden'])
const { overrideTriage } = useApi()

const newLevel = ref(null)
const reason = ref('')
const loading = ref(false)

const submit = async () => {
  if (!newLevel.value || !reason.value.trim()) return
  loading.value = true
  try {
    await overrideTriage(props.patient.id, newLevel.value, reason.value)
    emit('overridden')
  } catch (e) {
    console.error('Failed to override:', e)
    alert("Override failed.")
  } finally { loading.value = false }
}
</script>
