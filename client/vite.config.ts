import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// The dev server proxies API calls to the Express backend so the browser can
// talk to a single origin during development.
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    proxy: {
      "/api": {
        target: "http://localhost:3001",
        changeOrigin: true,
      },
    },
  },
});
