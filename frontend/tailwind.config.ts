import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          50: "#f4f7fb",
          100: "#e9eef8",
          200: "#cad7ec",
          300: "#9db4db",
          400: "#6f8ac9",
          500: "#4766af",
          600: "#36508f",
          700: "#2c4072",
          800: "#26355d",
          900: "#242f4e"
        },
        accent: {
          400: "#2ec4b6",
          500: "#1fb3a6",
          600: "#189184"
        }
      },
      fontFamily: {
        heading: ["Poppins", "Segoe UI", "sans-serif"],
        body: ["Manrope", "Segoe UI", "sans-serif"]
      },
      boxShadow: {
        glass: "0 20px 60px -20px rgba(20, 32, 68, 0.35)"
      }
    }
  },
  plugins: []
};

export default config;
