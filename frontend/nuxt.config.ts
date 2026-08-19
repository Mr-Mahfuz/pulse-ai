// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },

  css: ['~/assets/css/main.css'],

  modules: [
    '@nuxtjs/tailwindcss',
    '@nuxtjs/google-fonts',
    '@nuxtjs/i18n'
  ],

  i18n: {
    locales: [
      { code: 'en', iso: 'en-US', file: 'en.json', name: 'English' },
      { code: 'bn', iso: 'bn-BD', file: 'bn.json', name: 'বাংলা' }
    ],
    defaultLocale: 'en',
    lazy: true,
    langDir: './locales',
    strategy: 'no_prefix'
  },

  googleFonts: {
    families: {
      Inter: [300, 400, 500, 600, 700, 800],
      'JetBrains Mono': [400, 500, 600],
    },
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE || 'http://localhost:8000',
    },
  },

  app: {
    head: {
      title: 'SmartTriage — AI Emergency Patient Prioritization',
      meta: [
        { name: 'description', content: 'AI-powered emergency department triage assistant that uses a three-layer AI architecture to prioritize patients in real-time.' },
        { name: 'theme-color', content: '#0f172a' },
      ],
      link: [
        { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' },
      ],
    },
  },
})
