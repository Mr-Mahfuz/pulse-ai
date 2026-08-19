/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    "./app/components/**/*.{js,vue,ts}",
    "./app/layouts/**/*.vue",
    "./app/pages/**/*.vue",
    "./app/plugins/**/*.{js,ts}",
    "./app.vue",
  ],
  theme: {
    extend: {
      colors: {
        esi: {
          1: 'rgba(var(--color-esi-1), <alpha-value>)',
          2: 'rgba(var(--color-esi-2), <alpha-value>)',
          3: 'rgba(var(--color-esi-3), <alpha-value>)',
          4: 'rgba(var(--color-esi-4), <alpha-value>)',
          5: 'rgba(var(--color-esi-5), <alpha-value>)',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Menlo', 'monospace'],
      },
    },
  },
  plugins: [],
}
