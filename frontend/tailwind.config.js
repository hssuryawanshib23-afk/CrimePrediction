/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#172033',
        muted: '#657086',
        panel: '#ffffff',
        line: '#e7ebf2',
        riskLow: '#1f9d62',
        riskMedium: '#d99a16',
        riskHigh: '#c24135'
      },
      boxShadow: {
        soft: '0 14px 40px rgba(24, 39, 75, 0.08)'
      }
    }
  },
  plugins: []
};

