/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "/app/templates/**/*.{html,js}",
    "/app/static/css/**/*.{css,js}"
  ],
  theme: {
    extend: {
      screens: {
        'xs': '425px',
      },
    },
  },
  plugins: [],
}
