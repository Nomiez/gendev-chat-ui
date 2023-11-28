import preact from '@preact/preset-vite'
import {defineConfig, loadEnv} from 'vite'

// https://vitejs.dev/config/
export default ({mode}) => {

    process.env = Object.assign(process.env, loadEnv(mode, process.cwd(), ''));
    return defineConfig({

        base: '', // Empty string leads to vite generating relative URL paths during build
        plugins: [preact()],
        server: {
            proxy: {
                // Proxy all requests to /<objectId>/api/... to http://localhost:8080/<objectId>/api/... (CORS)
                '/api': {
                    target: process.env.VITE_PROXY_API_URL || 'server:8080',
                    changeOrigin: true,
                    rewrite: path => path.replace(/^\/api/, ''),
                },
            },
        },
    });
};
