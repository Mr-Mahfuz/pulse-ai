<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between print:hidden">
      <div class="flex items-center gap-4">
        <NuxtLink to="/" class="btn-ghost !p-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18"/></svg>
        </NuxtLink>
        <div v-if="patient">
          <h1 class="text-2xl font-bold text-gray-900 dark:text-white tracking-tight">{{ maskName(patient.name) }}</h1>
          <div class="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400 mt-0.5">
            <span>{{ patient.age }}y · {{ patient.gender === 'M' ? 'Male' : patient.gender === 'F' ? 'Female' : patient.gender }}</span>
            <span class="w-1 h-1 rounded-full bg-gray-300 dark:bg-gray-600"></span>
            <span class="font-mono text-xs">MRN: {{ maskMRN(patient.id) }}</span>
            <span class="w-1 h-1 rounded-full bg-gray-300 dark:bg-gray-600"></span>
            <span>{{ formatTimeAgo(patient.arrival_time) }}</span>
          </div>
        </div>
      </div>

      <!-- ESI Badge + Actions -->
      <div class="flex items-center gap-3" v-if="patient && patient.triage_level">
        <button v-if="patient.status === 'waiting'" @click="clearPatient" :disabled="clearing" class="btn-primary !bg-emerald-600 hover:!bg-emerald-700 !border-emerald-700 print:hidden mr-2">
          <svg v-if="clearing" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
          Clear Patient
        </button>
        <button v-else-if="patient.status === 'discharged'" @click="restorePatient" :disabled="clearing" class="btn-primary !bg-blue-600 hover:!bg-blue-700 !border-blue-700 print:hidden mr-2">
          <svg v-if="clearing" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6"/></svg>
          Restore Patient
        </button>
        <button @click="printReport" class="btn-secondary print:hidden">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path stroke-linecap="round" stroke-linejoin="round" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"/></svg>
          {{ $t('patient_detail.print') }}
        </button>
        <div class="esi-badge text-sm !py-2 !px-4 !rounded-xl font-bold"
             :style="{ backgroundColor: `${esiInfo.color}15`, borderColor: `${esiInfo.color}40`, color: esiInfo.color, border: `1.5px solid ${esiInfo.color}40` }">
          {{ esiInfo.icon }} ESI-{{ effectiveLevel }} · {{ $t(`dashboard.esi_${effectiveLevel}`) }}
        </div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="card p-16 flex flex-col items-center justify-center gap-3 text-gray-400">
      <svg class="animate-spin h-7 w-7 text-blue-500" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
      <span class="text-sm">{{ $t('patient_detail.loading') }}</span>
    </div>

    <!-- Content Grid -->
    <div v-else-if="patient" class="grid grid-cols-1 lg:grid-cols-3 gap-6 print:block print:text-black">

      <!-- Print Letterhead (Hidden on screen) -->
      <div class="hidden print:block mb-8 border-b-2 border-gray-900 pb-4">
        <div class="flex items-center gap-4">
          <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center text-blue-700 font-bold text-2xl">🏥</div>
          <div>
            <h1 class="text-3xl font-black text-black tracking-tight">Dhaka Medical College Hospital</h1>
            <p class="text-sm text-gray-700 font-medium">100 Secretariat Road, Dhaka 1000 | Emergency Dept: +880-2-55165088</p>
            <div class="flex items-center justify-between mt-2">
              <p class="text-sm text-black font-bold uppercase tracking-wider">Official Triage Assessment Report</p>
              <p class="text-sm text-black font-medium">Assigned Physician: ___________________________</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Column 1: Patient Info -->
      <div class="space-y-6 print:space-y-4 print:mb-6">
        <!-- Clinical Presentation -->
        <div class="card shadow-xl backdrop-blur-xl bg-white/80 dark:bg-gray-900/80 border border-gray-200/50 dark:border-gray-800/50 print:shadow-none print:border-gray-300 print:bg-transparent print:break-inside-avoid">
          <div class="card-header border-b border-gray-100 dark:border-gray-800/50">
            <h2 class="card-title flex items-center gap-2">
              <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
              {{ $t('patient_detail.presentation') }}
            </h2>
          </div>
          <div class="card-body space-y-5">
            <div>
              <div class="section-label mb-1.5">Chief Complaint</div>
              <p class="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">{{ patient.chief_complaint || 'Not provided' }}</p>
            </div>
            <div>
              <div class="section-label mb-1.5">Medical History</div>
              <p class="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">{{ patient.medical_history || 'None reported' }}</p>
            </div>
          </div>
        </div>

        <!-- Vitals -->
        <div class="card shadow-xl backdrop-blur-xl bg-white/80 dark:bg-gray-900/80 border border-gray-200/50 dark:border-gray-800/50 print:shadow-none print:border-gray-300 print:bg-transparent print:break-inside-avoid">
          <div class="card-header flex items-center justify-between border-b border-gray-100 dark:border-gray-800/50 print:border-gray-300">
            <h2 class="card-title flex items-center gap-2">
              <svg class="w-4 h-4 text-rose-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
              {{ $t('patient_detail.vitals') }}
            </h2>
            <button v-if="vitalsChanged" @click="saveVitalsAndRetriage" :disabled="saving" class="btn-primary !py-1.5 !px-3 !text-xs print:hidden">
              <svg v-if="saving" class="animate-spin h-3 w-3" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
              {{ $t('patient_detail.save') }}
            </button>
          </div>
          <div class="card-body">
            <div class="grid grid-cols-2 gap-3">
              <div v-for="(vital, key) in vitalFields" :key="key">
                <div class="section-label mb-1">{{ vital.label }} <span class="text-gray-300 dark:text-gray-600">{{ vital.unit }}</span></div>
                <input v-model.number="editableVitals[key]" type="number" :step="['temperature', 'weight'].includes(key) ? 0.1 : 1"
                       class="form-input font-mono text-sm !py-2"
                       :class="getVitalInputClass(key, editableVitals[key])" />
                <div class="mt-2 opacity-60 hover:opacity-100 transition-opacity" v-if="getVitalHistory(key).length > 1">
                  <VitalSparkline :data="getVitalHistory(key)" :color="getSparklineColor(key)" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Column 2: AI Assessment -->
      <div class="space-y-6 print:space-y-4 print:mb-6">
        <div class="card shadow-xl backdrop-blur-xl bg-white/90 dark:bg-gray-900/90 border border-gray-200/50 dark:border-gray-800/50 print:shadow-none print:border-gray-300 print:bg-transparent print:break-inside-avoid" :class="effectiveLevel === 1 ? 'animate-pulse-border ring-1 ring-red-200 dark:ring-red-900/50 print:ring-0 print:animate-none' : ''">
          <div class="card-header flex items-center justify-between border-b border-gray-100 dark:border-gray-800/50 print:border-gray-300">
            <h2 class="card-title flex items-center gap-2">
              <svg class="w-4 h-4 text-violet-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
              {{ $t('patient_detail.ai_assessment') }}
            </h2>
            <div class="flex gap-2 print:hidden">
              <button @click="handleRetriage" :disabled="triaging" class="btn-ghost !text-xs">
                <svg v-if="triaging" class="animate-spin h-3 w-3" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
                {{ $t('patient_detail.rerun') }}
              </button>
              <button @click="showOverrideModal = true" class="btn-ghost !text-xs !text-orange-600 dark:!text-orange-400 hover:!bg-orange-50 dark:hover:!bg-orange-950/30">{{ $t('patient_detail.override') }}</button>
            </div>
          </div>

          <div class="card-body space-y-5" v-if="patient.triage_level">
            <!-- Override Banner -->
            <div v-if="patient.clinician_override" class="p-4 rounded-xl bg-orange-50 dark:bg-orange-950/20 border border-orange-200 dark:border-orange-900/40">
              <div class="flex items-center gap-2 text-sm font-semibold text-orange-700 dark:text-orange-400 mb-1">
                <span>✋</span> {{ $t('patient_detail.override_active') }}
              </div>
              <p class="text-sm text-orange-600/80 dark:text-orange-300/70">ESI-{{ patient.clinician_override }} — {{ patient.override_reason }}</p>
            </div>

            <!-- Red Flags -->
            <div v-if="patient.triage_red_flags?.length">
              <div class="section-label text-red-500 dark:text-red-400 mb-2">🚩 {{ $t('patient_detail.red_flags') }}</div>
              <div class="flex flex-wrap gap-1.5">
                <span v-for="flag in patient.triage_red_flags" :key="flag"
                      class="text-xs px-2.5 py-1 rounded-lg bg-red-50 dark:bg-red-950/30 text-red-700 dark:text-red-400 font-medium border border-red-100 dark:border-red-900/40">
                  {{ flag }}
                </span>
              </div>
            </div>

            <!-- ML Probabilities -->
            <div v-if="patient.triage_probabilities" class="print:hidden">
              <div class="section-label mb-3">{{ $t('patient_detail.ml_probability') }}</div>
              <div class="space-y-2.5">
                <div v-for="level in [1,2,3,4,5]" :key="level" class="flex items-center gap-3">
                  <span class="text-xs font-mono w-10 text-gray-500 dark:text-gray-400 shrink-0">ESI-{{ level }}</span>
                  <div class="flex-1 h-2.5 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
                    <div class="h-full rounded-full transition-all duration-700"
                         :style="{ width: `${(patient.triage_probabilities[`ESI-${level}`] || 0) * 100}%`, backgroundColor: getEsiLevel(level).color }"></div>
                  </div>
                  <span class="text-xs font-mono w-10 text-right font-semibold tabular-nums" :style="{ color: getEsiLevel(level).color }">
                    {{ Math.round((patient.triage_probabilities[`ESI-${level}`] || 0) * 100) }}%
                  </span>
                </div>
              </div>
            </div>

            <!-- Rationale -->
            <div v-if="patient.triage_rationale" class="pt-4 border-t border-gray-100 dark:border-gray-800">
              <div class="flex items-center justify-between mb-2">
                <div class="section-label">{{ $t('patient_detail.clinical_rationale') }}</div>
                <div class="flex items-center gap-1 bg-gray-100 dark:bg-gray-800 p-0.5 rounded-lg print:hidden">
                  <button @click="translate('en')" :class="activeLang === 'en' ? 'bg-white dark:bg-gray-700 shadow-sm text-gray-900 dark:text-white' : 'text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'" class="px-2.5 py-1 text-[10px] font-bold rounded-md transition-all">EN</button>
                  <button @click="translate('bn')" :class="activeLang === 'bn' ? 'bg-white dark:bg-gray-700 shadow-sm text-gray-900 dark:text-white' : 'text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'" class="px-2.5 py-1 text-[10px] font-bold rounded-md transition-all">BN</button>
                </div>
              </div>
              <div class="relative text-sm text-gray-600 dark:text-gray-300 leading-relaxed bg-gray-50 dark:bg-gray-800/50 p-4 rounded-xl border border-gray-100 dark:border-gray-800 italic transition-colors">
                <div v-if="translating" class="absolute inset-0 bg-white/50 dark:bg-gray-900/50 flex items-center justify-center backdrop-blur-[1px] rounded-xl z-10">
                  <svg class="animate-spin h-5 w-5 text-blue-500" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
                </div>
                "{{ patient.triage_rationale }}"
              </div>
            </div>
          </div>

          <div v-else class="card-body text-center py-12">
            <div class="text-gray-400 dark:text-gray-500 mb-4">
              <svg class="w-12 h-12 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1"><path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
              <p class="text-sm font-medium">{{ $t('patient_detail.not_triaged') }}</p>
            </div>
            <button @click="handleRetriage" :disabled="triaging" class="btn-primary print:hidden">
              <svg v-if="triaging" class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
              {{ $t('patient_detail.run_ai') }}
            </button>
          </div>
        </div>
      </div>

      <!-- Column 3: Audit Trail -->
      <div class="space-y-6 print:hidden">
        <div class="card h-full flex flex-col shadow-xl backdrop-blur-xl bg-white/80 dark:bg-gray-900/80 border border-gray-200/50 dark:border-gray-800/50 print:shadow-none print:border-gray-300 print:bg-transparent print:break-inside-avoid print:block">
          <div class="card-header border-b border-gray-100 dark:border-gray-800/50 print:border-gray-300">
            <h2 class="card-title flex items-center gap-2">
              <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              {{ $t('patient_detail.audit_trail') }}
            </h2>
          </div>
          <div class="card-body flex-1 overflow-y-auto max-h-[600px] print:max-h-none print:overflow-visible">
            <div v-if="auditLogs.length" class="space-y-4">
              <div v-for="(log, i) in auditLogs" :key="log.id" class="relative pl-6">
                <!-- Timeline -->
                <div v-if="i !== auditLogs.length - 1" class="absolute left-[9px] top-5 bottom-[-16px] w-px bg-gray-100 dark:bg-gray-800"></div>
                <div class="absolute left-0 top-1.5 w-[18px] h-[18px] rounded-full border-[2.5px] border-white dark:border-gray-900"
                     :class="getAuditDotClass(log.action)"></div>

                <div>
                  <div class="text-[10px] font-mono text-gray-400 dark:text-gray-500 tabular-nums">{{ formatTimestamp(log.timestamp) }}</div>
                  <div class="text-sm font-semibold text-gray-800 dark:text-gray-200 mt-0.5">{{ $t(`audit.${log.action}`) }}</div>
                  <div v-if="log.new_value" class="text-xs text-gray-500 dark:text-gray-400 mt-1 leading-relaxed">{{ formatAuditValue(log) }}</div>
                  <div class="text-[10px] text-gray-400 dark:text-gray-500 uppercase tracking-wider mt-1 font-medium">{{ log.actor }}</div>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-10 text-gray-400 dark:text-gray-500">
              <svg class="w-8 h-8 mx-auto mb-2 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
              <p class="text-sm">{{ $t('patient_detail.no_audit') }}</p>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- Physician Notes (Print Only) -->
    <div class="hidden print:block mt-8 border-t-2 border-gray-200 pt-8 break-inside-avoid">
      <h2 class="text-lg font-bold text-black uppercase tracking-wider mb-6">Physician Notes & Orders</h2>
      <div class="space-y-10">
        <div class="border-b border-gray-400 w-full h-8"></div>
        <div class="border-b border-gray-400 w-full h-8"></div>
        <div class="border-b border-gray-400 w-full h-8"></div>
        <div class="border-b border-gray-400 w-full h-8"></div>
        <div class="border-b border-gray-400 w-full h-8"></div>
        <div class="border-b border-gray-400 w-full h-8"></div>
        <div class="border-b border-gray-400 w-full h-8"></div>
        <div class="border-b border-gray-400 w-full h-8"></div>
        <div class="border-b border-gray-400 w-full h-8"></div>
      </div>
      <div class="mt-16 flex justify-between px-10">
        <div class="border-t-2 border-gray-800 pt-2 w-64 text-center text-sm font-bold uppercase tracking-wider text-black">Physician Signature / ID</div>
        <div class="border-t-2 border-gray-800 pt-2 w-48 text-center text-sm font-bold uppercase tracking-wider text-black">Date & Time</div>
      </div>
    </div>

    <!-- Override Modal -->
    <OverrideModal v-if="showOverrideModal" :patient="patient" @close="showOverrideModal = false" @overridden="onOverridden" />
  </div>
</template>

<script setup>
import { getEsiLevel, getEffectiveLevel, formatTimeAgo, formatTimestamp, getVitalStatus, VITAL_LABELS } from '~/utils/esi'
import { usePrivacy } from '~/composables/usePrivacy'

const route = useRoute()
const { getPatient, updatePatient, runTriage, getAuditLog, updatePatientStatus, translateRationale } = useApi()
const { maskName, maskMRN } = usePrivacy()

const patient = ref(null)
const auditLogs = ref([])
const loading = ref(true)
const triaging = ref(false)
const saving = ref(false)
const clearing = ref(false)
const showOverrideModal = ref(false)
const editableVitals = ref({})
const translating = ref(false)
const activeLang = ref('en')

const vitalFields = VITAL_LABELS

const effectiveLevel = computed(() => patient.value ? (getEffectiveLevel(patient.value) || 5) : 5)
const esiInfo = computed(() => getEsiLevel(effectiveLevel.value))

const vitalsChanged = computed(() => {
  if (!patient.value) return false
  return Object.keys(vitalFields).some(key => editableVitals.value[key] !== patient.value[key])
})

const fetchPatient = async () => {
  try {
    patient.value = await getPatient(route.params.id)
    Object.keys(vitalFields).forEach(key => { editableVitals.value[key] = patient.value[key] })
  } catch (e) { console.error('Failed to fetch patient:', e) }
}

const fetchAudit = async () => {
  try { auditLogs.value = await getAuditLog(route.params.id) } catch (e) { console.error(e) }
}

const handleRetriage = async () => {
  triaging.value = true
  try { await runTriage(route.params.id); await fetchPatient(); await fetchAudit() } catch (e) { console.error(e) }
  finally { triaging.value = false }
}

const saveVitalsAndRetriage = async () => {
  saving.value = true
  try { await updatePatient(route.params.id, editableVitals.value); await runTriage(route.params.id); await fetchPatient(); await fetchAudit() } catch (e) { console.error(e) }
  finally { saving.value = false }
}

const onOverridden = async () => {
  showOverrideModal.value = false
  await fetchPatient(); await fetchAudit()
}

const clearPatient = async () => {
  if (!confirm('Are you sure you want to clear this patient from the triage queue?')) return
  clearing.value = true
  try {
    await updatePatientStatus(route.params.id, 'discharged')
    useRouter().push('/')
  } catch (e) {
    console.error('Failed to discharge patient', e)
  } finally {
    clearing.value = false
  }
}

const restorePatient = async () => {
  clearing.value = true
  try {
    await updatePatientStatus(route.params.id, 'waiting')
    useRouter().push('/')
  } catch (e) {
    console.error('Failed to restore patient', e)
  } finally {
    clearing.value = false
  }
}

const translate = async (lang) => {
  if (lang === activeLang.value) return
  translating.value = true
  try {
    const res = await translateRationale(route.params.id, lang)
    patient.value.triage_rationale = res.rationale
    activeLang.value = lang
  } catch (e) {
    console.error(e)
    alert("Translation failed")
  } finally {
    translating.value = false
  }
}

const getVitalInputClass = (name, value) => {
  const status = getVitalStatus(name, value)
  return {
    normal: '',
    warning: '!border-amber-400 !text-amber-700 dark:!text-amber-400 !bg-amber-50 dark:!bg-amber-950/20',
    critical: '!border-red-400 !text-red-700 dark:!text-red-400 !bg-red-50 dark:!bg-red-950/20',
  }[status]
}

const getVitalHistory = (key) => {
  if (!patient.value || patient.value[key] === null || patient.value[key] === undefined) return []
  const history = []
  history.unshift({ value: patient.value[key], time: new Date() })
  for (const log of auditLogs.value) {
    if (log.action === 'patient_updated' && log.old_value && log.old_value[key] !== undefined) {
      history.unshift({ value: log.old_value[key], time: new Date(log.timestamp) })
    }
  }
  return history
}

const getSparklineColor = (key) => {
  if (!patient.value) return '#3B82F6'
  const status = getVitalStatus(key, patient.value[key])
  if (status === 'critical') return '#DC2626' // red-600
  if (status === 'warning') return '#D97706' // amber-600
  return '#3B82F6' // blue-500
}

const getAuditDotClass = (action) => ({
  triage_computed: 'bg-blue-500',
  clinician_override: 'bg-orange-500',
  patient_registered: 'bg-emerald-500',
  patient_updated: 'bg-amber-500',
}[action] || 'bg-gray-300 dark:bg-gray-600')

const formatAuditValue = (log) => {
  if (!log.new_value) return ''
  if (log.action === 'triage_computed') return `Assigned ESI-${log.new_value.level} (${Math.round((log.new_value.confidence || 0) * 100)}% conf, via ${log.new_value.source})`
  if (log.action === 'clinician_override') return `Changed to ESI-${log.new_value.clinician_override}. Reason: "${log.new_value.reason}"`
  if (log.action === 'patient_updated') return 'Modified clinical vitals data'
  return ''
}

const printReport = () => { if (process.client) window.print() }

onMounted(async () => { await fetchPatient(); await fetchAudit(); loading.value = false })
</script>
