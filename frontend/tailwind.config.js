/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'medical-blue': '#4A90E2',
        'calm-green': '#7ED321',
        'warning-orange': '#F5A623',
        'emergency-red': '#D0021B',
      }
    },
  },
  plugins: [],
}
