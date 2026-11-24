/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        charcoal: {
          950: '#0b0d10',
          900: '#111418',
          850: '#161a20',
          800: '#1c2128',
          750: '#232932',
          700: '#2c333f',
          600: '#3d4757',
        },
        studio: {
          purple: '#8b5cf6',
          violet: '#7c3aed',
          cyan: '#06b6d4',
          blue: '#3b82f6',
          amber: '#f59e0b',
          emerald: '#10b981',
          rose: '#f43f5e'
        }
      }
    },
  },
  plugins: [],
}
