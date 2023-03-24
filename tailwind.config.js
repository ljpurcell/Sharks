/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/base.html",
    "./app/templates/index.html",
    "./app/templates/*.html",
    "./app/templates/**/*.html",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
