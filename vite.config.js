import { defineConfig } from "vite";
import { djangoVitePlugin } from "django-vite-plugin";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  server: {
    host: "0.0.0.0",
    port: 5173,
  },
  plugins: [
    vue(),
    djangoVitePlugin([
      "frontend/app.js",
    ]),
  ],
  resolve: {
    alias: {
      vue: "vue/dist/vue.esm-bundler.js",
      "@": "/frontend",
      "@views": "/frontend/views",
      "@components": "/frontend/components",
      "@constants": "/frontend/constants",
      "@svg": "/frontend/components/svg",
    },
  },
});
