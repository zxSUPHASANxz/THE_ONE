/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './templates/**/*.html',
        './users/templates/**/*.html',
        './chatbot/templates/**/*.html',
        './booking/templates/**/*.html',
        './mechanics/templates/**/*.html',
        './static/js/**/*.js',
    ],
    theme: {
        extend: {
            colors: {
                primary: {
                    50: '#fff1f2',
                    100: '#ffe4e6',
                    200: '#fecdd3',
                    300: '#fda4af',
                    400: '#fb7185',
                    500: '#f43f5e',
                    600: '#e11d48',
                    700: '#be123c', // Deep Red
                    800: '#9f1239',
                    900: '#881337',
                    950: '#4c0519',
                },
                gold: {
                    50: '#fffbeb',
                    100: '#fef3c7',
                    200: '#fde68a',
                    300: '#fcd34d',
                    400: '#fbbf24',
                    500: '#f59e0b',
                    600: '#d97706',
                    700: '#b45309',
                    800: '#92400e',
                    900: '#78350f',
                    950: '#451a03',
                },
                luxury: {
                    red: '#720e1e',
                    gold: '#d4af37',
                    black: '#1a1a1a',
                    white: '#f9f9f9',
                }
            },
            fontFamily: {
                sans: ['Inter', 'Kanit', 'sans-serif'],
                thai: ['Kanit', 'sans-serif'],
            },
            animation: {
                'fade-in': 'fadeIn 0.8s ease-out forwards',
                'slide-up': 'slideUp 0.8s ease-out forwards',
                'slide-down': 'slideDown 0.5s ease-out forwards',
                'scale-up': 'scaleUp 0.5s ease-out forwards',
                'bounce-slow': 'bounce 3s infinite',
                'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'glow': 'glow 3s ease-in-out infinite',
                'float': 'float 6s ease-in-out infinite',
            },
            keyframes: {
                fadeIn: {
                    '0%': { opacity: '0' },
                    '100%': { opacity: '1' },
                },
                slideUp: {
                    '0%': { opacity: '0', transform: 'translateY(20px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
                slideDown: {
                    '0%': { opacity: '0', transform: 'translateY(-20px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
                scaleUp: {
                    '0%': { opacity: '0', transform: 'scale(0.9)' },
                    '100%': { opacity: '1', transform: 'scale(1)' },
                },
                glow: {
                    '0%, 100%': { boxShadow: '0 0 5px rgba(212, 175, 55, 0.2)' },
                    '50%': { boxShadow: '0 0 20px rgba(212, 175, 55, 0.6)' },
                },
                float: {
                    '0%, 100%': { transform: 'translateY(0)' },
                    '50%': { transform: 'translateY(-10px)' },
                }
            },
            backgroundImage: {
                'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
                'hero-pattern': "url('/static/images/pattern.svg')",
            }
        },
    },
    plugins: [],
}