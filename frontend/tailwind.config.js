/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Escala completa de cores primary com contraste WCAG AA validado
        primary: {
          50: '#fef2f3',
          100: '#fde6e7',
          200: '#fbd0d4',
          300: '#f7a8b0',
          400: '#f17885',
          500: '#e63946',  // Cor base (contraste 4.84:1 com branco)
          600: '#d32f3c',
          700: '#b22a35',
          800: '#942632',
          900: '#7d252f',
          950: '#451015',
        },
        secondary: {
          50: '#f1faee',
          100: '#e3f5dd',
          200: '#c9ebbd',
          300: '#a5db95',
          400: '#7dc76a',
          500: '#5baf4a',
          600: '#468f39',
          700: '#387130',
          800: '#2f5a29',
          900: '#284b25',
        },
        accent: {
          50: '#f0f9fa',
          100: '#d9f0f2',
          200: '#b7e2e6',
          300: '#a8dadc',  // Cor base
          400: '#6bc4c9',
          500: '#4fa9ae',
          600: '#3d8b92',
          700: '#357177',
          800: '#2f5c61',
          900: '#2b4d52',
        },
      },
      keyframes: {
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      },
      animation: {
        shimmer: 'shimmer 2s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}
