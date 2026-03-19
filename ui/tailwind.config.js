/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans:    ['Inter', 'system-ui', 'sans-serif'],
        display: ['"Playfair Display"', 'Georgia', 'serif'],
      },
      colors: {
        riceblue: {
          50:  '#f2f4f8',
          100: '#e5eaef',
          200: '#c0cddb',
          300: '#99b0c7',
          400: '#4d75a0',
          500: '#003b7a',
          600: '#00356e',
          700: '#00205B',
          800: '#001a49',
          900: '#00153c',
          950: '#000b1e',
        },
        ricewhite: {
          50:  '#ffffff',
          100: '#fcfcfc',
          200: '#f5f5f5',
          300: '#e5e5e5',
          400: '#d4d4d4',
          500: '#a3a3a3',
        },
        gold: {
          light: '#F0E0B0',
          DEFAULT: '#C8A96E',
          dark: '#9A7A44',
        },
      },
    },
  },
  plugins: [],
}
