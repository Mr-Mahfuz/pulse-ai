/**
 * API client composable for SmartTriage backend.
 */
export const useApi = () => {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase

  const fetchApi = async (path, options = {}) => {
    const url = `${baseURL}${path}`
    try {
      const response = await $fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      })
      return response
    } catch (error) {
      console.error(`API Error [${path}]:`, error)
      throw error
    }
  }

  // Patient endpoints
  const getPatients = (status) => {
    const query = status ? `?status=${status}` : ''
    return fetchApi(`/api/patients${query}`)
  }

  const getPatient = (id) => fetchApi(`/api/patients/${id}`)
  
  const createPatient = (data) => fetchApi('/api/patients', {
    method: 'POST',
    body: data,
  })

  const updatePatient = (id, data) => fetchApi(`/api/patients/${id}`, {
    method: 'PUT',
    body: data,
  })

  const deletePatient = (id) => fetchApi(`/api/patients/${id}`, {
    method: 'DELETE',
  })

  const updatePatientStatus = (id, status) => fetchApi(`/api/patients/${id}/status?status=${status}`, {
    method: 'PATCH',
  })

  // Triage endpoints
  const runTriage = (patientId) => {
    const nuxtApp = useNuxtApp()
    const lang = nuxtApp.$i18n?.locale?.value || 'en'
    return fetchApi(`/api/triage/${patientId}?language=${lang}`, { method: 'POST' })
  }

  const batchTriage = () => fetchApi('/api/triage/batch', {
    method: 'POST',
  })

  const overrideTriage = (patientId, level, reason) => fetchApi(`/api/triage/${patientId}/override`, {
    method: 'PUT',
    body: { level, reason },
  })

  const translateRationale = (patientId, language) => fetchApi(`/api/triage/${patientId}/translate`, {
    method: 'POST',
    body: { language }
  })

  // Audit endpoints
  const getAuditLog = (patientId) => fetchApi(`/api/audit/${patientId}`)
  const getAllAuditLogs = (limit = 100) => fetchApi(`/api/audit?limit=${limit}`)

  // Speech endpoint
  const parseSpeech = (transcript, language = 'en') => fetchApi('/api/parse-speech', {
    method: 'POST',
    body: { transcript, language },
  })

  return {
    getPatients,
    getPatient,
    createPatient,
    updatePatient,
    updatePatientStatus,
    deletePatient,
    runTriage,
    batchTriage,
    overrideTriage,
    translateRationale,
    getAuditLog,
    getAllAuditLogs,
    parseSpeech,
  }
}
