/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.{html,js}"],
  theme: {
    extend: {
      fontFamily: {
        playfair: ['"Playfair Display"', "serif"],
        sans: ['"DM Sans"', "Inter", "sans-serif"],
      },
      ringWidth: {
        3: "3.58px", // Adds a 3-pixel ring width
      },
      colors: {
        bgGreen: "#EFFFF8",
        primaryText: "#1A7348",
        primary: "#2DAB6F",
        primaryLight: "#34BF7D",
        primaryLightest: "#4FE79F",
        txt: "#2E2E2E",
        bgImg: "#C6EBDB",
        slide: "#CEF5E4",
      },
    },
  },
  plugins: [],
};
