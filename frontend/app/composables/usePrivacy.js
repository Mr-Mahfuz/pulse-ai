import { useState } from '#imports'

export const usePrivacy = () => {
  const privacyMode = useState('privacyMode', () => false)

  const maskName = (name) => {
    if (!privacyMode.value || !name) return name
    const parts = name.split(' ')
    return parts.map(p => p.charAt(0) + '*'.repeat(Math.max(1, p.length - 1))).join(' ')
  }

  const maskMRN = (id) => {
    if (!privacyMode.value || !id) return id
    return id.split('-')[0].charAt(0) + '***'
  }

  return { privacyMode, maskName, maskMRN }
}
