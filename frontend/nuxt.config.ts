export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: { enabled: true },
  modules: ["@nuxt/eslint"],
  typescript: {
    strict: true,
  },
  runtimeConfig: {
    public: {
      supabaseUrl: "",
      supabaseKey: "",
      apiBaseUrl: "http://localhost:8000",
    },
  },
});
