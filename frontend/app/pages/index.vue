<template>
  <div class="space-y-6">
    <!-- Critical Alert Banner -->
    <div v-if="criticalAlertPatient" class="fixed top-4 left-1/2 -translate-x-1/2 z-50 w-full max-w-3xl px-4 animate-slide-down">
      <div class="bg-red-600 text-white rounded-2xl shadow-[0_0_40px_rgba(220,38,38,0.6)] border-2 border-red-400 p-4 flex items-center justify-between cursor-pointer hover:bg-red-700 transition-colors" @click="navigateTo(`/patient/${criticalAlertPatient.id}`)">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center shrink-0">
            <span class="text-2xl animate-bounce">🚨</span>
          </div>
          <div>
            <h3 class="font-black text-lg uppercase tracking-wider animate-pulse">Critical Patient Arrived (ESI-1)</h3>
            <p class="text-red-100 text-sm font-medium">{{ criticalAlertPatient.name }} • {{ criticalAlertPatient.age }}y • {{ criticalAlertPatient.chief_complaint }}</p>
          </div>
        </div>
        <div class="bg-white text-red-700 font-bold px-4 py-2 rounded-lg text-sm shrink-0 shadow-sm">
          Triage Now
        </div>
      </div>
    </div>

    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold tracking-tight" :class="mciMode ? 'text-red-600 dark:text-red-500' : 'text-gray-900 dark:text-white'">
          {{ mciMode ? $t('dashboard.mci_title') : $t('dashboard.title') }}
        </h1>
        <p class="text-sm text-gray-500 dark:text-gray-400 mt-0.5">
          {{ mciMode ? $t('dashboard.mci_subtitle') : $t('dashboard.subtitle') }}
        </p>
      </div>
      <div class="flex items-center gap-3">
        <!-- MCI Toggle -->
        <button @click="mciMode = !mciMode" 
                class="px-3 py-1.5 rounded-lg text-sm font-bold transition-colors border"
                :class="mciMode ? 'bg-red-600 text-white border-red-700 animate-pulse' : 'bg-white dark:bg-gray-800 text-red-500 border-red-200 dark:border-red-900/50 hover:bg-red-50 dark:hover:bg-red-900/30'">
          {{ $t('dashboard.mci_mode') }}
        </button>
        <!-- Privacy Toggle -->
        <button @click="privacyMode = !privacyMode" class="btn-ghost !p-2" :class="privacyMode ? 'text-emerald-500 bg-emerald-50 dark:bg-emerald-900/30' : ''" :title="privacyMode ? 'Disable Privacy Mode' : 'Enable Privacy Mode'">
          <svg v-if="privacyMode" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
          <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path stroke-linecap="round" stroke-linejoin="round" d="M8 11V7a4 4 0 118 0m-4 8v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2z"/></svg>
        </button>
        <button @click="fetchPatients" class="btn-ghost !p-2" title="Refresh">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
        </button>
        <button @click="showAnalyticsModal = true" class="btn-ghost !p-2" title="System Analytics">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.8"><path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
        </button>
        <button @click="showAddModal = true" class="btn-primary">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/></svg>
          {{ $t('dashboard.register') }}
        </button>
      </div>
    </div>

    <!-- Summary Stats (Standard) -->
    <div v-if="!mciMode" class="grid grid-cols-2 md:grid-cols-6 gap-3">
      <div class="stat-card !bg-gray-900 !border-gray-800 flex flex-col justify-center shadow-lg backdrop-blur-xl bg-opacity-80">
        <span class="text-[10px] font-bold text-gray-400 tracking-wider mb-1">{{ $t('dashboard.in_queue') }}</span>
        <span class="text-3xl font-bold text-white">{{ activePatients.length }}</span>
      </div>
      <div v-for="level in [1,2,3,4,5]" :key="level" class="stat-card relative overflow-hidden backdrop-blur-lg bg-white/70 dark:bg-gray-900/70 border border-white/20 dark:border-gray-800/50 shadow-sm">
        <div class="absolute top-0 left-0 w-full h-1.5" :style="{ backgroundColor: getEsiLevel(level).color }"></div>
        <span class="text-[10px] font-bold text-gray-500 dark:text-gray-400 tracking-wider mb-1">ESI-{{ level }}</span>
        <span class="text-3xl font-bold text-gray-900 dark:text-white mb-1" :style="{ color: getEsiLevel(level).color }">
          {{ getCountByLevel(level) }}
        </span>
        <span class="text-[10px] text-gray-400 truncate">{{ $t(`dashboard.esi_${level}`) }}</span>
      </div>
    </div>

    <!-- Summary Stats (MCI) -->
    <div v-else class="grid grid-cols-3 gap-3">
      <div class="stat-card bg-red-500 text-white relative overflow-hidden flex flex-col justify-center py-6 shadow-red-500/20 shadow-lg">
        <span class="text-[12px] font-bold tracking-widest mb-1 opacity-80">{{ $t('dashboard.mci_immediate') }}</span>
        <span class="text-4xl font-black">{{ getMciCount('IMMEDIATE') }}</span>
      </div>
      <div class="stat-card bg-yellow-500 text-white relative overflow-hidden flex flex-col justify-center py-6 shadow-yellow-500/20 shadow-lg">
        <span class="text-[12px] font-bold tracking-widest mb-1 opacity-80">{{ $t('dashboard.mci_delayed') }}</span>
        <span class="text-4xl font-black">{{ getMciCount('DELAYED') }}</span>
      </div>
      <div class="stat-card bg-green-500 text-white relative overflow-hidden flex flex-col justify-center py-6 shadow-green-500/20 shadow-lg">
        <span class="text-[12px] font-bold tracking-widest mb-1 opacity-80">{{ $t('dashboard.mci_minor') }}</span>
        <span class="text-4xl font-black">{{ getMciCount('MINOR') }}</span>
      </div>
    </div>

    <!-- Dual Queue Tabs -->
    <div v-if="!mciMode" class="flex gap-4 border-b border-gray-200 dark:border-gray-800">
      <button @click="activeTab = 'main'" 
              class="px-4 py-3 text-sm font-bold border-b-2 transition-colors flex items-center gap-2"
              :class="activeTab === 'main' ? 'border-blue-500 text-blue-600 dark:text-blue-400' : 'border-transparent text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'">
        {{ $t('dashboard.main_ed') }}
        <span class="px-2 py-0.5 rounded-full text-xs" :class="activeTab === 'main' ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30' : 'bg-gray-100 text-gray-500 dark:bg-gray-800'">{{ mainQueueCount }}</span>
      </button>
      <button @click="activeTab = 'fast'" 
              class="px-4 py-3 text-sm font-bold border-b-2 transition-colors flex items-center gap-2"
              :class="activeTab === 'fast' ? 'border-green-500 text-green-600 dark:text-green-400' : 'border-transparent text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'">
        {{ $t('dashboard.fast_track') }}
        <span class="px-2 py-0.5 rounded-full text-xs" :class="activeTab === 'fast' ? 'bg-green-100 text-green-700 dark:bg-green-900/30' : 'bg-gray-100 text-gray-500 dark:bg-gray-800'">{{ fastQueueCount }}</span>
      </button>
      <button @click="activeTab = 'history'" 
              class="px-4 py-3 text-sm font-bold border-b-2 transition-colors flex items-center gap-2 ml-auto"
              :class="activeTab === 'history' ? 'border-gray-500 text-gray-700 dark:text-gray-300' : 'border-transparent text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'">
        History (Cleared)
      </button>
    </div>

    <!-- Patient Table -->
    <div class="card flex flex-col shadow-xl backdrop-blur-xl bg-white/80 dark:bg-gray-900/80 border border-gray-200/50 dark:border-gray-800/50">
      <div class="card-header flex flex-wrap items-center justify-between gap-4 border-b border-gray-100 dark:border-gray-800 pb-4">
        <h2 class="text-sm font-bold text-gray-900 dark:text-white flex items-center gap-2">
          {{ mciMode ? $t('dashboard.start_triage_list') : $t('dashboard.title') }}
        </h2>
        <div class="relative w-full md:w-64">
          <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          <input v-model="searchQuery" type="text" :placeholder="$t('dashboard.search')" class="form-input pl-9 !py-1.5 !text-sm w-full bg-white/50 dark:bg-gray-900/50" />
        </div>
      </div>

      <!-- Table -->
      <div v-if="!mciMode" class="overflow-x-auto min-h-[400px] pb-4">
        <table class="w-full text-left border-collapse min-w-[900px]">
          <thead>
            <tr class="border-b border-gray-100 dark:border-gray-800 text-[10px] font-bold text-gray-400 dark:text-gray-500 tracking-wider uppercase">
              <th class="px-4 py-3 font-semibold w-px whitespace-nowrap">{{ $t('dashboard.priority') }}</th>
              <th class="px-4 py-3 font-semibold w-px whitespace-nowrap">{{ $t('dashboard.wait') }}</th>
              <th class="px-4 py-3 font-semibold w-px whitespace-nowrap">{{ $t('dashboard.est_time') }}</th>
              <th class="px-4 py-3 font-semibold w-48">{{ $t('dashboard.patient') }}</th>
              <th class="px-4 py-3 font-semibold w-auto">{{ $t('dashboard.complaint') }}</th>
              <th class="px-4 py-3 font-semibold w-px whitespace-nowrap">{{ $t('dashboard.vitals') }}</th>
              <th class="px-4 py-3 font-semibold text-right w-px whitespace-nowrap">{{ $t('dashboard.ai_conf') }}</th>
            </tr>
          </thead>
          <!-- Loading -->
          <tbody v-if="loading && !patients.length">
            <tr>
              <td colspan="7" class="!py-16 text-center text-gray-400 text-sm">
                <div class="flex flex-col items-center gap-3">
                  <svg class="animate-spin h-6 w-6" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
                  {{ $t('dashboard.loading') }}
                </div>
              </td>
            </tr>
          </tbody>
          <!-- Data -->
          <tbody class="text-sm">
            <tr v-for="patient in displayPatients" :key="patient.id" 
                @click="navigateTo(`/patient/${patient.id}`)"
                class="border-b border-gray-50 dark:border-gray-800/50 hover:bg-gray-50/50 dark:hover:bg-gray-800/40 cursor-pointer transition-all group"
                :class="getRowClass(patient)">
              <!-- Priority Badge -->
              <td class="px-4 py-4 whitespace-nowrap">
                <div v-if="!mciMode" class="esi-badge text-xs px-2 shadow-sm" :style="{ backgroundColor: `${getEsiLevel(getEffectiveLevel(patient)).color}15`, color: getEsiLevel(getEffectiveLevel(patient)).color, border: `1px solid ${getEsiLevel(getEffectiveLevel(patient)).color}30` }">
                  {{ getEsiLevel(getEffectiveLevel(patient)).icon }} ESI-{{ getEffectiveLevel(patient) }}
                </div>
                <div v-else class="esi-badge text-xs px-2 font-bold text-white shadow-sm" :class="getMciColor(getEffectiveLevel(patient)).bg">
                  {{ getMciColor(getEffectiveLevel(patient)).label }}
                </div>
                <!-- SLA Breach Flag -->
                <div v-if="isSlaBreached(patient) && !mciMode" class="mt-1.5 flex items-center gap-1 text-[9px] font-bold text-red-600 dark:text-red-400 uppercase tracking-wider animate-pulse">
                  <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
                  SLA Breach
                </div>
              </td>
              <!-- Wait -->
              <td class="px-4 py-4 whitespace-nowrap">
                <span class="text-xs font-mono font-medium" :class="getMinutesInQueue(patient.arrival_time) > 120 ? 'text-orange-600 dark:text-orange-400' : 'text-gray-500 dark:text-gray-400'">
                  {{ formatTimeAgoShort(patient.arrival_time) }}
                </span>
              </td>
              <!-- Est Time -->
              <td class="px-4 py-4 whitespace-nowrap">
                <span v-if="!mciMode" class="text-xs font-mono text-gray-500 dark:text-gray-400 px-2 py-0.5 rounded bg-gray-100 dark:bg-gray-800">
                  {{ getEstimatedWait(patient) }}
                </span>
                <span v-else class="text-xs font-mono text-gray-400">—</span>
              </td>
              <!-- Patient -->
              <td class="px-4 py-4 whitespace-nowrap">
                <div class="font-semibold text-gray-900 dark:text-white text-sm">{{ maskName(patient.name) }}</div>
                <div class="text-xs text-gray-500 mt-0.5">{{ patient.age }}y · {{ patient.gender }}</div>
              </td>
              <!-- Complaint -->
              <td class="px-4 py-4 truncate">
                <p class="text-gray-600 dark:text-gray-300 truncate text-xs" :title="patient.chief_complaint">{{ patient.chief_complaint }}</p>
                <div v-if="patient.triage_source === 'red_flag_override'" class="mt-1 flex">
                  <span class="text-[8px] px-1.5 py-0.5 rounded bg-red-50 dark:bg-red-950/30 text-red-600 dark:text-red-400 border border-red-200 dark:border-red-900/40 font-bold tracking-wider uppercase">🚩 {{ $t('dashboard.red_flag') }}</span>
                </div>
              </td>
              <!-- Vitals -->
              <td class="px-4 py-4 whitespace-nowrap">
                <div class="flex gap-1.5">
                  <span v-if="patient.heart_rate" class="text-[10px] font-mono px-1.5 py-0.5 rounded"
                        :class="patient.heart_rate > 100 || patient.heart_rate < 50 ? 'bg-red-50 dark:bg-red-950/30 text-red-600 dark:text-red-400 font-semibold' : 'text-gray-500'">
                    HR:{{ patient.heart_rate }}
                  </span>
                  <span v-if="patient.spo2" class="text-[10px] font-mono px-1.5 py-0.5 rounded"
                        :class="patient.spo2 < 95 ? 'bg-red-50 dark:bg-red-950/30 text-red-600 dark:text-red-400 font-semibold' : 'text-gray-500'">
                    SpO₂:{{ patient.spo2 }}
                  </span>
                  <span v-if="patient.temperature" class="text-[10px] font-mono px-1.5 py-0.5 rounded"
                        :class="patient.temperature >= 38.5 ? 'bg-orange-50 dark:bg-orange-950/30 text-orange-600 dark:text-orange-400 font-semibold' : 'text-gray-500'">
                    T:{{ patient.temperature }}°
                  </span>
                </div>
                <!-- Re-triage Alert -->
                <div v-if="needsReTriage(patient)" class="mt-1.5 text-[9px] font-bold text-orange-600 dark:text-orange-400 uppercase tracking-wider">
                  ⚠️ Re-triage Required
                </div>
              </td>
              <!-- Confidence -->
              <td class="text-right px-4 py-4 whitespace-nowrap">
                <div v-if="patient.triage_source === 'red_flag_override'" class="flex items-center justify-end">
                  <span class="text-[10px] px-2 py-0.5 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 font-bold uppercase tracking-wider">
                    Safety Rule
                  </span>
                </div>
                <div v-else-if="patient.triage_confidence" class="flex items-center justify-end gap-2.5">
                  <div class="w-14 h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                    <div class="h-full rounded-full transition-all duration-500"
                         :class="patient.triage_confidence >= 0.8 ? 'bg-emerald-500' : patient.triage_confidence >= 0.6 ? 'bg-amber-500' : 'bg-red-500'"
                         :style="{ width: `${patient.triage_confidence * 100}%` }"></div>
                  </div>
                  <span class="text-xs font-mono font-semibold text-gray-600 dark:text-gray-300 tabular-nums">
                    {{ Math.round(patient.triage_confidence * 100) }}%
                  </span>
                </div>
                <span v-else class="text-xs text-gray-300 dark:text-gray-600">—</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- MCI Card Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-6 min-h-[400px]">
        <div v-for="patient in displayPatients" :key="patient.id" class="rounded-2xl border-4 overflow-hidden flex flex-col shadow-xl transition-transform hover:scale-[1.02] cursor-pointer"
             :class="getMciColor(getEffectiveLevel(patient)).cardBorder"
             @click="navigateTo(`/patient/${patient.id}`)">
          <div class="p-4 text-center font-black tracking-widest text-xl text-white" :class="getMciColor(getEffectiveLevel(patient)).bg">
            {{ getMciColor(getEffectiveLevel(patient)).label }}
          </div>
          <div class="p-6 bg-white dark:bg-gray-900 flex-1 flex flex-col">
            <h3 class="font-bold text-2xl mb-1 text-gray-900 dark:text-white">{{ maskName(patient.name) }}</h3>
            <div class="text-sm text-gray-500 mb-4">{{ patient.age }}y • {{ patient.gender }}</div>
            <p class="text-gray-700 dark:text-gray-300 font-medium mb-6 line-clamp-3 flex-1">
              "{{ patient.chief_complaint }}"
            </p>
            <button class="w-full py-3 rounded-xl font-bold text-lg uppercase tracking-wider transition-colors"
                    :class="getMciColor(getEffectiveLevel(patient)).btnClass"
                    @click.stop="navigateTo(`/patient/${patient.id}`)">
              View & Admit
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <Teleport to="body">
      <PatientFormModal v-if="showAddModal" @close="showAddModal = false" @created="onPatientCreated" />
    </Teleport>

    <!-- Enrolling Spinner -->
    <Teleport to="body">
      <div v-if="isEnrolling" class="fixed inset-0 z-[60] flex items-center justify-center bg-black/40 backdrop-blur-sm animate-fade-in">
        <div class="bg-white dark:bg-gray-900 rounded-2xl p-8 shadow-2xl flex flex-col items-center gap-4 border border-gray-200 dark:border-gray-800 animate-slide-up">
          <svg class="animate-spin h-10 w-10 text-blue-500" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/></svg>
          <div class="text-center">
            <h2 class="text-lg font-bold text-gray-900 dark:text-white">Enrolling Patient...</h2>
            <p class="text-sm text-gray-500 mt-1">Running AI Triage Assessment</p>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Analytics Modal -->
    <Teleport to="body">
      <div v-if="showAnalyticsModal" class="fixed inset-0 z-[60] flex items-center justify-center animate-fade-in" @click.self="showAnalyticsModal = false">
        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm"></div>
        <div class="relative bg-white dark:bg-gray-900 rounded-2xl shadow-2xl w-full max-w-lg mx-4 p-6 border border-gray-200 dark:border-gray-800 animate-slide-up">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
              <svg class="w-5 h-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
              System & Token Analytics
            </h2>
            <button @click="showAnalyticsModal = false" class="btn-ghost !p-2 !rounded-full">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
            </button>
          </div>

          <div class="grid grid-cols-2 gap-4 mb-6">
            <div class="p-4 rounded-xl bg-blue-50 dark:bg-blue-950/20 border border-blue-100 dark:border-blue-900/30">
              <div class="text-[10px] font-bold text-blue-500 tracking-wider uppercase mb-1">Total Triages</div>
              <div class="text-3xl font-black text-blue-700 dark:text-blue-400">{{ patients.length }}</div>
            </div>
            <div class="p-4 rounded-xl bg-emerald-50 dark:bg-emerald-950/20 border border-emerald-100 dark:border-emerald-900/30">
              <div class="text-[10px] font-bold text-emerald-500 tracking-wider uppercase mb-1">Rules Bypasses</div>
              <div class="text-3xl font-black text-emerald-700 dark:text-emerald-400">{{ rulesBypasses }}</div>
              <div class="text-[9px] text-emerald-600 mt-1">Saved {{ rulesBypasses * 350 }} LLM Tokens</div>
            </div>
          </div>

          <div class="space-y-3">
            <div class="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-800 border border-gray-100 dark:border-gray-700">
              <span class="text-sm font-semibold text-gray-600 dark:text-gray-300">Total LLM Tokens Used</span>
              <span class="font-mono font-bold text-gray-900 dark:text-white">{{ (patients.length - rulesBypasses) * 350 }}</span>
            </div>
            <div class="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-800 border border-gray-100 dark:border-gray-700">
              <span class="text-sm font-semibold text-gray-600 dark:text-gray-300">Estimated API Cost</span>
              <span class="font-mono font-bold text-gray-900 dark:text-white">${{ (((patients.length - rulesBypasses) * 350) / 1000000 * 0.075).toFixed(4) }}</span>
            </div>
            <div class="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-800 border border-gray-100 dark:border-gray-700">
              <span class="text-sm font-semibold text-gray-600 dark:text-gray-300">Avg. Latency (Rules)</span>
              <span class="font-mono font-bold text-emerald-600 dark:text-emerald-400">&lt; 5ms</span>
            </div>
            <div class="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-800 border border-gray-100 dark:border-gray-700">
              <span class="text-sm font-semibold text-gray-600 dark:text-gray-300">Avg. Latency (LLM)</span>
              <span class="font-mono font-bold text-blue-600 dark:text-blue-400">~ 850ms</span>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { getEsiLevel, getEffectiveLevel } from '~/utils/esi'
import { usePrivacy } from '~/composables/usePrivacy'

const { getPatients, runTriage } = useApi()
const { privacyMode, maskName } = usePrivacy()

const patients = ref([])
const loading = ref(true)
const showAddModal = ref(false)
const showAnalyticsModal = ref(false)
const isEnrolling = ref(false)
const searchQuery = ref('')
const mciMode = useState('mciMode', () => false)
const activeTab = ref('main') // 'main' or 'fast'
let refreshInterval = null
const previousEsi1Ids = ref(new Set())
const criticalAlertPatient = ref(null)

const activePatients = computed(() => patients.value.filter(p => p.status === 'waiting'))
const rulesBypasses = computed(() => patients.value.filter(p => p.triage_source === 'rules_engine' || p.triage_source === 'red_flag_override').length)

const esiCounts = computed(() => {
  const counts = {}
  for (const p of activePatients.value) {
    const level = getEffectiveLevel(p)
    if (level) counts[level] = (counts[level] || 0) + 1
  }
  return counts
})

const getCountByLevel = (level) => esiCounts.value[level] || 0

// MCI Logic
const getMciColor = (level) => {
  if (level <= 1) return { bg: 'bg-red-600', label: 'IMMEDIATE', cardBorder: 'border-red-600', btnClass: 'bg-red-100 text-red-700 hover:bg-red-200 dark:bg-red-900/30 dark:text-red-400 dark:hover:bg-red-900/50' }
  if (level <= 3) return { bg: 'bg-yellow-500 text-yellow-950', label: 'DELAYED', cardBorder: 'border-yellow-500', btnClass: 'bg-yellow-100 text-yellow-800 hover:bg-yellow-200 dark:bg-yellow-900/30 dark:text-yellow-500 dark:hover:bg-yellow-900/50' }
  return { bg: 'bg-green-500 text-green-950', label: 'MINOR', cardBorder: 'border-green-500', btnClass: 'bg-green-100 text-green-800 hover:bg-green-200 dark:bg-green-900/30 dark:text-green-500 dark:hover:bg-green-900/50' }
}
const getMciCount = (cat) => {
  if (cat === 'IMMEDIATE') return getCountByLevel(1)
  if (cat === 'DELAYED') return getCountByLevel(2) + getCountByLevel(3)
  if (cat === 'MINOR') return getCountByLevel(4) + getCountByLevel(5)
  return 0
}

const getMinutesInQueue = (timestamp) => {
  if (!timestamp) return 0
  return Math.floor((new Date() - new Date(timestamp + 'Z')) / 60000)
}

const formatTimeAgoShort = (timestamp) => {
  const diffMinutes = getMinutesInQueue(timestamp)
  if (diffMinutes < 1) return 'now'
  if (diffMinutes < 60) return `${diffMinutes}m`
  const hours = Math.floor(diffMinutes / 60)
  return `${hours}h ${diffMinutes % 60}m`
}

// SLA & Re-Triage Rules
const isSlaBreached = (patient) => {
  if (patient.status === 'discharged') return false
  const level = getEffectiveLevel(patient)
  const minutes = getMinutesInQueue(patient.arrival_time)
  if (level === 2 && minutes > 15) return true
  if (level === 3 && minutes > 60) return true
  if (level === 4 && minutes > 120) return true
  if (level === 5 && minutes > 240) return true
  return false
}

const needsReTriage = (patient) => {
  if (patient.status === 'discharged') return false
  const level = getEffectiveLevel(patient)
  const minutes = getMinutesInQueue(patient.arrival_time)
  // Alert if ESI 4/5 waits > 120 mins (to prevent orphaned queue deterioration)
  return (level === 4 || level === 5) && minutes > 120
}

const getRowClass = (patient) => {
  if (mciMode.value) return ''
  if (isSlaBreached(patient)) return 'bg-red-50/50 dark:bg-red-900/10'
  if (needsReTriage(patient)) return 'bg-orange-50/30 dark:bg-orange-900/10'
  return ''
}

// Queue Processing & Estimates
const filteredPatients = computed(() => {
  let list = activeTab.value === 'history' 
    ? patients.value.filter(p => p.status === 'discharged')
    : activePatients.value

  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(p => p.name?.toLowerCase().includes(q) || p.chief_complaint?.toLowerCase().includes(q))
  }
  return list
})

// Completely sort patients: SLA Breached first, then ESI Level, then Time
const sortedPatients = computed(() => {
  return [...filteredPatients.value].sort((a, b) => {
    if (!mciMode.value) {
      const slaA = isSlaBreached(a) ? -1 : 1
      const slaB = isSlaBreached(b) ? -1 : 1
      if (slaA !== slaB) return slaA - slaB // SLA breaches float to top in normal mode
    }
    
    const levelA = getEffectiveLevel(a) || 99
    const levelB = getEffectiveLevel(b) || 99
    if (levelA !== levelB) return levelA - levelB // Sort by ESI
    
    return new Date(a.arrival_time) - new Date(b.arrival_time) // Sort by time
  })
})

// Tab logic
const mainQueueCount = computed(() => activePatients.value.filter(p => getEffectiveLevel(p) <= 3).length)
const fastQueueCount = computed(() => activePatients.value.filter(p => getEffectiveLevel(p) > 3).length)

const displayPatients = computed(() => {
  if (mciMode.value) return sortedPatients.value // In MCI, see all
  if (activeTab.value === 'history') return sortedPatients.value
  return sortedPatients.value.filter(p => {
    const level = getEffectiveLevel(p)
    if (activeTab.value === 'main') return level <= 3
    return level > 3
  })
})

const getEstimatedWait = (patient) => {
  const level = getEffectiveLevel(patient)
  if (level <= 2) return 'Imm'
  
  // Find index in their respective queue
  const queue = level <= 3 ? 
    sortedPatients.value.filter(p => getEffectiveLevel(p) <= 3) : 
    sortedPatients.value.filter(p => getEffectiveLevel(p) > 3)
    
  const index = queue.findIndex(p => p.id === patient.id)
  
  if (level === 3) return `~${Math.max(15, index * 15)}m` // Main ED throughput (15m per critical)
  return `~${Math.max(10, index * 10)}m` // Fast track throughput (10m per minor)
}

const fetchPatients = async () => {
  try {
    const data = await getPatients()
    
    // Check for new ESI-1 patients
    if (previousEsi1Ids.value.size > 0) { // Don't alert on initial load
      const currentEsi1 = data.filter(p => p.status === 'waiting' && getEffectiveLevel(p) === 1)
      for (const p of currentEsi1) {
        if (!previousEsi1Ids.value.has(p.id)) {
          criticalAlertPatient.value = p
          setTimeout(() => { criticalAlertPatient.value = null }, 8000)
          break // Just show one alert at a time
        }
      }
    }
    
    // Update tracking set
    const newSet = new Set()
    data.filter(p => p.status === 'waiting' && getEffectiveLevel(p) === 1).forEach(p => newSet.add(p.id))
    previousEsi1Ids.value = newSet
    
    patients.value = data
  } catch (e) {
    console.error('Failed to fetch patients:', e)
  } finally {
    loading.value = false
  }
}

const onPatientCreated = async (patient) => {
  showAddModal.value = false
  isEnrolling.value = true
  try { await runTriage(patient.id) } catch (e) { console.error('Triage failed:', e) }
  isEnrolling.value = false
  navigateTo(`/patient/${patient.id}`)
}

onMounted(() => {
  fetchPatients()
  refreshInterval = setInterval(() => { fetchPatients() }, 10000)
})

onUnmounted(() => {
  if (refreshInterval) clearInterval(refreshInterval)
})
</script>
