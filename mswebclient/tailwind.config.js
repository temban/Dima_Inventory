/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#2563eb',
        'primary-600': '#1d4ed8',
        'danger': '#ef4444',
        'danger-600': '#dc2626',
        'ok': '#059669',
        'muted': '#6b7280',
        'elev-1': '#ffffff',
        'elev-2': '#ffffff',
        'bg': '#f6f7fb',
        'text': '#0b1020'
      },
      borderRadius: {
        'DEFAULT': '10px',
        'sm': '8px',
        'lg': '14px'
      },
      boxShadow: {
        'DEFAULT': '0 8px 24px rgba(16,24,40,.08)',
        'sm': '0 2px 10px rgba(16,24,40,.06)'
      }
    },
  },
  plugins: [],
}