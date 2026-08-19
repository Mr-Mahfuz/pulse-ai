/**
 * ESI triage level utilities.
 */

export const ESI_LEVELS = {
  1: { name: 'Resuscitation', color: '#2563EB', bgClass: 'bg-blue-600', textClass: 'text-blue-600', badgeClass: 'esi-badge-1', borderClass: 'border-glow-1', icon: '🔵' },
  2: { name: 'Emergent', color: '#DC2626', bgClass: 'bg-red-600', textClass: 'text-red-600', badgeClass: 'esi-badge-2', borderClass: 'border-glow-2', icon: '🔴' },
  3: { name: 'Urgent', color: '#F97316', bgClass: 'bg-orange-500', textClass: 'text-orange-500', badgeClass: 'esi-badge-3', borderClass: 'border-glow-3', icon: '🟠' },
  4: { name: 'Less Urgent', color: '#65A30D', bgClass: 'bg-lime-600', textClass: 'text-lime-600', badgeClass: 'esi-badge-4', borderClass: 'border-glow-4', icon: '🟢' },
  5: { name: 'Non-Urgent', color: '#4B5563', bgClass: 'bg-gray-600', textClass: 'text-gray-600', badgeClass: 'esi-badge-5', borderClass: 'border-glow-5', icon: '⚫' },
}

export const getEsiLevel = (level) => ESI_LEVELS[level] || ESI_LEVELS[5]

export const getEffectiveLevel = (patient) => {
  return patient.clinician_override || patient.triage_level || null
}

export const formatTimeAgo = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const now = new Date()
  const diffMs = now - date
  const diffMin = Math.floor(diffMs / 60000)
  const diffHr = Math.floor(diffMin / 60)

  if (diffMin < 1) return 'just now'
  if (diffMin < 60) return `${diffMin}m ago`
  if (diffHr < 24) return `${diffHr}h ${diffMin % 60}m ago`
  return date.toLocaleDateString()
}

export const formatTimestamp = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

export const getVitalStatus = (name, value) => {
  if (value === null || value === undefined) return 'normal'
  
  const ranges = {
    heart_rate: { critical: [0, 40, 160, 300], warning: [40, 60, 100, 160] },
    systolic_bp: { critical: [0, 70, 200, 400], warning: [70, 90, 160, 200] },
    diastolic_bp: { critical: [0, 40, 120, 300], warning: [40, 60, 90, 120] },
    respiratory_rate: { critical: [0, 8, 30, 80], warning: [8, 12, 22, 30] },
    temperature: { critical: [0, 35, 39.5, 45], warning: [35, 36, 38, 39.5] },
    spo2: { critical: [0, 88, -1, -1], warning: [88, 94, -1, -1] },
    gcs_score: { critical: [0, 9, -1, -1], warning: [9, 13, -1, -1] },
  }

  const range = ranges[name]
  if (!range) return 'normal'

  const { critical, warning } = range
  
  // Check critical
  if (value <= critical[1] || (critical[2] > 0 && value >= critical[2])) return 'critical'
  // Check warning
  if (value <= warning[1] || (warning[2] > 0 && value >= warning[2])) return 'warning'
  
  return 'normal'
}

export const VITAL_LABELS = {
  heart_rate: { label: 'HR', unit: 'bpm' },
  systolic_bp: { label: 'SBP', unit: 'mmHg' },
  diastolic_bp: { label: 'DBP', unit: 'mmHg' },
  respiratory_rate: { label: 'RR', unit: '/min' },
  temperature: { label: 'Temp', unit: '°C' },
  spo2: { label: 'SpO₂', unit: '%' },
  gcs_score: { label: 'GCS', unit: '/15' },
}
