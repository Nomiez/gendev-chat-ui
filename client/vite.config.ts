import {defineConfig} from 'vite'
import preact from '@preact/preset-vite'

// https://vitejs.dev/config/
export default defineConfig({
    base: '', // Empty string leads to vite generating relative URL paths during build
    plugins: [preact()],
    server: {
        proxy: {
            // Proxy all requests to /<objectId>/api/... to http://localhost:8080/<objectId>/api/... (CORS)
            '/api': {
                target: 'http://0.0.0.0:8000',
                changeOrigin: true,
                rewrite: path => path.replace(/^\/api/, ''),
            },
        },
    },
})
