import path from "path"
import react from "@vitejs/plugin-react-swc"
import { defineConfig } from "vite"
import tailwindcss from 'tailwindcss'
import { viteStaticCopy } from 'vite-plugin-static-copy'

export default defineConfig({
  plugins: [
    react(),
    viteStaticCopy({
      targets: [
        {
          src: path.resolve(__dirname, '../simulation_results.json'),
          dest: '.'
        }
      ]
    })
  ],
  base: '/election2024/webapp/',  // Add this line
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  css: {
    postcss: {
      plugins: [tailwindcss],
    },
  },
  build: {
    outDir: '../docs/webapp',
    emptyOutDir: true,
  },
})