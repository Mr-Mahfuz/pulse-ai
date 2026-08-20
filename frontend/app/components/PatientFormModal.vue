<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center animate-fade-in" @click.self="$emit('close')">
    <!-- Backdrop -->
    <div class="absolute inset-0 bg-black/40 backdrop-blur-sm"></div>

    <!-- Modal -->
    <div class="relative bg-white dark:bg-gray-900 rounded-2xl shadow-2xl w-full max-w-2xl mx-4 max-h-[90vh] flex flex-col border border-gray-200 dark:border-gray-800 animate-slide-up">

      <!-- Header -->
      <div class="flex items-center justify-between px-6 py-5 border-b border-gray-100 dark:border-gray-800 shrink-0">
        <div>
          <h2 class="text-lg font-bold text-gray-900 dark:text-white">{{ $t('patient_modal.title') }}</h2>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-0.5">{{ $t('patient_modal.subtitle') }}</p>
        </div>
        <div class="flex items-center gap-3">
          <button type="button" @click="toggleDictation" 
                  class="flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-semibold transition-all border"
                  :class="isListening 
                    ? 'bg-red-50 text-red-600 border-red-200 shadow-[0_0_15px_rgba(220,38,38,0.5)] animate-pulse' 
                    : 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50 dark:bg-gray-800 dark:text-gray-300 dark:border-gray-700 dark:hover:bg-gray-750'">
            <div class="relative">
              <svg class="w-4 h-4 relative z-10" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
              <span v-if="isListening" class="absolute inset-0 rounded-full bg-red-400 opacity-75 animate-ping"></span>
            </div>
            {{ isListening ? $t('patient_modal.listening') : (dictating ? $t('patient_modal.processing') : $t('patient_modal.dictate')) }}
          </button>
          
          <button @click="$emit('close')" class="btn-ghost !p-2 !rounded-full">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Transcript preview -->
      <div v-if="isListening || transcript" class="px-6 py-4 bg-blue-50/80 dark:bg-blue-900/20 border-b border-blue-100 dark:border-blue-800/30">
        <div class="flex items-center gap-2 mb-1">
          <div v-if="isListening" class="flex gap-1">
            <span class="w-1.5 h-1.5 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 0ms"></span>
            <span class="w-1.5 h-1.5 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 150ms"></span>
            <span class="w-1.5 h-1.5 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 300ms"></span>
          </div>
          <span class="text-xs font-bold text-blue-600 dark:text-blue-400 uppercase tracking-wider">AI Voice Parser Active</span>
        </div>
        <p class="text-sm text-blue-800 dark:text-blue-300 font-medium italic min-h-[20px]">
          "{{ transcript }}<span v-if="isListening" class="animate-pulse">_</span>"
        </p>
      </div>

      <!-- Form -->
      <form @submit.prevent="submit" class="flex-1 overflow-y-auto p-6 space-y-6">

        <!-- Quick Fill Scenarios -->
        <div class="flex flex-wrap items-center gap-2 pb-4 border-b border-gray-100 dark:border-gray-800">
          <span class="text-xs font-bold text-gray-400 uppercase tracking-wider mr-2">Auto-Fill:</span>
          <button type="button" @click="fillScenario('esi-1')" class="px-2.5 py-1 text-[10px] font-bold rounded bg-red-50 text-red-600 hover:bg-red-100 dark:bg-red-900/30 dark:text-red-400 border border-red-200 dark:border-red-800">CRITICAL (ESI-1)</button>
          <button type="button" @click="fillScenario('esi-3')" class="px-2.5 py-1 text-[10px] font-bold rounded bg-yellow-50 text-yellow-600 hover:bg-yellow-100 dark:bg-yellow-900/30 dark:text-yellow-500 border border-yellow-200 dark:border-yellow-800">URGENT (ESI-3)</button>
          <button type="button" @click="fillScenario('esi-5')" class="px-2.5 py-1 text-[10px] font-bold rounded bg-blue-50 text-blue-600 hover:bg-blue-100 dark:bg-blue-900/30 dark:text-blue-400 border border-blue-200 dark:border-blue-800">MINOR (ESI-5)</button>
        </div>

        <!-- Demographics -->
        <div>
          <div class="section-label mb-3">{{ $t('patient_modal.demographics') }}</div>
          <div class="grid grid-cols-6 gap-4">
            <div class="col-span-4">
              <label class="form-label">{{ $t('patient_modal.full_name') }} <span class="text-red-500">*</span></label>
              <input v-model="form.name" type="text" required class="form-input" />
            </div>
            <div class="col-span-1">
              <label class="form-label">{{ $t('patient_modal.age') }} <span class="text-red-500">*</span></label>
              <input v-model.number="form.age" type="number" required min="0" max="120" class="form-input" />
            </div>
            <div class="col-span-1">
              <label class="form-label">{{ $t('patient_modal.gender') }} <span class="text-red-500">*</span></label>
              <select v-model="form.gender" required class="form-input">
                <option value="" disabled>—</option>
                <option value="M">M</option>
                <option value="F">F</option>
                <option value="Other">Other</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Chief Complaint -->
        <div>
          <div class="section-label mb-3">{{ $t('patient_modal.presentation') }}</div>
          <label class="form-label">{{ $t('patient_modal.complaint') }} <span class="text-red-500">*</span></label>
          <textarea v-model="form.chief_complaint" required rows="2" class="form-input resize-none"></textarea>
        </div>

        <!-- Vitals -->
        <div>
          <div class="flex items-center justify-between mb-3">
            <div class="section-label">{{ $t('patient_modal.vitals') }} <span class="text-gray-300 dark:text-gray-600 normal-case tracking-normal">{{ $t('patient_modal.optional') }}</span></div>
            <button type="button" @click="simulateIoT" class="flex items-center gap-2 px-3 py-1 text-[10px] font-bold rounded-lg border transition-all"
                    :class="iotActive ? 'bg-emerald-50 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 border-emerald-200 dark:border-emerald-800 shadow-[0_0_10px_rgba(16,185,129,0.3)]' : 'bg-gray-50 dark:bg-gray-800 text-gray-500 border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-750'">
              <span class="w-1.5 h-1.5 rounded-full" :class="iotActive ? 'bg-emerald-500 animate-pulse' : 'bg-gray-400'"></span>
              {{ iotActive ? 'SYNCING SENSOR...' : 'CONNECT OXIMETER' }}
            </button>
          </div>
          <div class="grid grid-cols-4 gap-3">
            <div v-for="(config, key) in vitalConfig" :key="key">
              <label class="form-label !text-xs">{{ config.label }}</label>
              <div class="relative">
                <input v-model.number="form[key]" type="number" :step="['temperature', 'weight'].includes(key) ? 0.1 : 1" class="form-input font-mono pr-10 !py-2" placeholder="—" />
                <span class="absolute right-3 top-1/2 -translate-y-1/2 text-[10px] text-gray-400 font-mono">{{ config.unit }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Medical History -->
        <div>
          <label class="form-label">{{ $t('patient_modal.history') }} <span class="text-gray-400 font-normal">{{ $t('patient_modal.optional') }}</span></label>
          <textarea v-model="form.medical_history" rows="2" class="form-input resize-none"></textarea>
        </div>
      </form>

      <!-- Footer -->
      <div class="flex items-center justify-end gap-3 px-6 py-4 border-t border-gray-100 dark:border-gray-800 shrink-0">
        <button type="button" @click="$emit('close')" class="btn-secondary" :disabled="loading">{{ $t('patient_modal.cancel') }}</button>
        <button type="button" @click="submit" class="btn-primary" :disabled="loading || dictating">
          <svg v-if="loading" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
          {{ loading ? '...' : $t('patient_modal.submit') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const { createPatient, parseSpeech } = useApi()
const emit = defineEmits(['close', 'created'])

const vitalConfig = {
  heart_rate: { label: 'Heart Rate', unit: 'bpm' },
  systolic_bp: { label: 'Systolic BP', unit: 'mmHg' },
  diastolic_bp: { label: 'Diastolic BP', unit: 'mmHg' },
  respiratory_rate: { label: 'Resp. Rate', unit: '/min' },
  temperature: { label: 'Temperature', unit: '°C' },
  spo2: { label: 'SpO₂', unit: '%' },
  gcs_score: { label: 'GCS Score', unit: '/15' },
  weight: { label: 'Weight', unit: 'kg' },
  pain_scale: { label: 'Pain Scale', unit: '/10' }
}

const form = ref({
  name: '', age: null, gender: '', chief_complaint: '',
  heart_rate: null, systolic_bp: null, diastolic_bp: null,
  respiratory_rate: null, temperature: null, spo2: null, gcs_score: 15,
  weight: null, pain_scale: null,
  medical_history: ''
})

const loading = ref(false)
const iotActive = ref(false)

const fillScenario = (scenario) => {
  if (scenario === 'esi-1') {
    form.value = {
      name: 'Robert Downey', age: 62, gender: 'M', chief_complaint: 'Crushing chest pain radiating to the jaw, sweating, and severe shortness of breath.',
      heart_rate: 135, systolic_bp: 85, diastolic_bp: 50, respiratory_rate: 28,
      temperature: 36.8, spo2: 88, gcs_score: 13, weight: 88, pain_scale: 10,
      medical_history: 'Hypertension, previous myocardial infarction in 2018.'
    }
  } else if (scenario === 'esi-3') {
    form.value = {
      name: 'Emily Blunt', age: 28, gender: 'F', chief_complaint: 'High fever for 3 days and severe right lower quadrant abdominal pain.',
      heart_rate: 115, systolic_bp: 110, diastolic_bp: 70, respiratory_rate: 18,
      temperature: 39.4, spo2: 97, gcs_score: 15, weight: 62, pain_scale: 8,
      medical_history: 'None'
    }
  } else if (scenario === 'esi-5') {
    form.value = {
      name: 'Tom Holland', age: 24, gender: 'M', chief_complaint: 'Ran out of my seasonal allergy medication, need a refill prescription.',
      heart_rate: 72, systolic_bp: 120, diastolic_bp: 80, respiratory_rate: 14,
      temperature: 37.0, spo2: 99, gcs_score: 15, weight: 75, pain_scale: 0,
      medical_history: 'Seasonal allergies.'
    }
  }
}

const simulateIoT = () => {
  if (iotActive.value) return
  iotActive.value = true
  
  let cycles = 0
  const interval = setInterval(() => {
    form.value.heart_rate = Math.floor(Math.random() * (120 - 95 + 1) + 95)
    form.value.spo2 = Math.floor(Math.random() * (99 - 92 + 1) + 92)
    cycles++
    
    if (cycles > 15) {
      clearInterval(interval)
      iotActive.value = false
      form.value.heart_rate = 104
      form.value.spo2 = 96
    }
  }, 200)
}

// --- Speech Recognition Logic ---
const isListening = ref(false)
const dictating = ref(false)
const transcript = ref('')
let recognition = null

onMounted(() => {
  if (process.client) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    if (SpeechRecognition) {
      recognition = new SpeechRecognition()
      recognition.continuous = true
      recognition.interimResults = true
      
      recognition.onstart = () => {
        isListening.value = true
        transcript.value = ''
      }
      
      recognition.onresult = (event) => {
        let final = ''
        for (let i = event.resultIndex; i < event.results.length; ++i) {
          if (event.results[i].isFinal) {
            final += event.results[i][0].transcript + ' '
          }
        }
        if (final) {
          transcript.value += final
        }
      }
      
      recognition.onerror = (event) => {
        console.error('Speech recognition error', event.error)
        isListening.value = false
        dictating.value = false
      }
      
      recognition.onend = () => {
        isListening.value = false
      }
    }
  }
})

const toggleDictation = async () => {
  if (!recognition) {
    alert("Speech recognition is not supported in this browser. Please use Chrome or Edge.")
    return
  }
  
  if (isListening.value) {
    recognition.stop()
    if (transcript.value.trim()) {
      dictating.value = true
      await processSpeech(transcript.value)
    }
  } else {
    transcript.value = ''
    recognition.start()
  }
}

const processSpeech = async (text) => {
  try {
    const parsedData = await parseSpeech(text)
    
    // Merge parsed data into form, ignoring nulls
    Object.keys(parsedData).forEach(key => {
      if (parsedData[key] !== null && parsedData[key] !== undefined) {
        form.value[key] = parsedData[key]
      }
    })
  } catch (error) {
    console.error('Failed to parse speech:', error)
    if (text.trim().split(/\s+/).length < 4) {
      alert("Could not hear enough details to process. Please speak more clearly or fill the form manually.")
    } else {
      alert("Failed to parse speech with AI. Please fill the form manually.")
    }
  } finally {
    dictating.value = false
  }
}
// ------------------------------

const submit = async () => {
  if (!form.value.name || !form.value.age || !form.value.gender || !form.value.chief_complaint) {
    alert("Please fill in all required fields.")
    return
  }
  loading.value = true
  try {
    const payload = {}
    Object.keys(form.value).forEach(k => {
      if (form.value[k] !== null && form.value[k] !== '') payload[k] = form.value[k]
    })
    const newPatient = await createPatient(payload)
    emit('created', newPatient)
  } catch (e) {
    console.error('Failed to create patient:', e)
    alert("An error occurred while saving.")
  } finally { loading.value = false }
}
</script>
