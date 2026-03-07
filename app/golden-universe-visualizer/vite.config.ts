import { defineConfig, type Plugin } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import { visualizer } from 'rollup-plugin-visualizer'
import viteCompression from 'vite-plugin-compression'

// Custom plugin to fix CommonJS/ESM issues
function commonjsFix(): Plugin {
  return {
    name: 'commonjs-fix',
    config() {
      return {
        resolve: {
          alias: {
            'use-sync-external-store/shim/with-selector.js':
              'use-sync-external-store/shim/with-selector',
            'scheduler': 'scheduler/index.js',
            'stats.js': 'stats.js/build/stats.min.js',
            'attr-accept': 'attr-accept/dist/es/index.js',
          }
        }
      }
    },
    transform(code, id) {
      // Fix default import issues for use-sync-external-store
      if (id.includes('zustand') && code.includes('useSyncExternalStoreWithSelector')) {
        return code.replace(
          /import\s+(\w+)\s+from\s+["']use-sync-external-store\/shim\/with-selector["']/g,
          `import * as $1Temp from "use-sync-external-store/shim/with-selector";
const $1 = $1Temp.useSyncExternalStoreWithSelector || $1Temp.default || $1Temp;`
        );
      }

      // Fix scheduler default import
      if (id.includes('@react-three') && code.includes("from 'scheduler'")) {
        return code.replace(
          /import\s+(\w+)\s+from\s+['"]scheduler['"]/g,
          `import * as $1 from "scheduler"`
        );
      }

      // Fix stats.js default import
      if (id.includes('Stats') && code.includes('stats.js')) {
        return code.replace(
          /import\s+(\w+)\s+from\s+['"]stats\.js['"]/g,
          `import * as StatsModule from "stats.js";
const $1 = StatsModule.default || StatsModule;`
        );
      }

      // Fix attr-accept default import (used by react-dropzone)
      if ((id.includes('react-dropzone') || id.includes('dropzone')) && code.includes('attr-accept')) {
        return code.replace(
          /import\s+(\w+)\s+from\s+['"]attr-accept['"]/g,
          `import * as attrAcceptTemp from "attr-accept";
const $1 = attrAcceptTemp.default || attrAcceptTemp;`
        );
      }

      // Fix merge-value default import (used by leva)
      if (id.includes('leva') && code.includes('merge-value')) {
        return code.replace(
          /import\s+(\w+)\s+from\s+['"]merge-value['"]/g,
          `import * as mergeValueModule from "merge-value";
const $1 = mergeValueModule.default || mergeValueModule;`
        );
      }

      return null;
    }
  }
}

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  // Load env file based on `mode` in the current working directory.
  // const env = loadEnv(mode, process.cwd(), '')

  return {
  plugins: [
    commonjsFix(),
    react(),
    // Gzip compression for production
    viteCompression({
      algorithm: 'gzip',
      ext: '.gz',
      threshold: 10240, // Only compress files larger than 10KB
    }),
    // Brotli compression for production
    viteCompression({
      algorithm: 'brotliCompress',
      ext: '.br',
      threshold: 10240,
    }),
    // Bundle analyzer - generates stats.html
    visualizer({
      open: false,
      gzipSize: true,
      brotliSize: true,
      filename: 'dist/stats.html',
    }),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@services': path.resolve(__dirname, './src/services'),
      '@utils': path.resolve(__dirname, './src/utils'),
      '@styles': path.resolve(__dirname, './src/styles'),
      '@types': path.resolve(__dirname, './src/types'),
      '@/data': path.resolve(__dirname, './src/data'),
      // Fix for use-sync-external-store CommonJS/ESM issue
      'use-sync-external-store/shim/with-selector': path.resolve(__dirname, 'node_modules/use-sync-external-store/shim/with-selector.js'),
    },
    extensions: ['.tsx', '.ts', '.jsx', '.js', '.json'],
  },
  server: {
    port: 3000,
    open: true,
    headers: {
      'Cross-Origin-Embedder-Policy': 'require-corp',
      'Cross-Origin-Opener-Policy': 'same-origin',
    },
    proxy: {
      // Proxy API requests to the backend server
      '/api': {
        target: 'http://localhost:3001',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  worker: {
    format: 'iife', // Use IIFE format for compatibility with importScripts (Pyodide)
  },
  define: {
    '__BUILD_TIME__': JSON.stringify(new Date().toISOString()),
    '__COMMIT_SHA__': JSON.stringify(process.env.COMMIT_SHA || 'local'),
    '__APP_VERSION__': JSON.stringify(process.env.npm_package_version || '1.0.0'),
  },
  build: {
    // Target modern browsers for smaller bundle
    target: 'es2020',
    // Output directory
    outDir: 'dist',
    // Generate source maps for debugging (only in staging/dev)
    sourcemap: mode !== 'production',
    // Optimize chunk splitting
    rollupOptions: {
      output: {
        // Manual chunk splitting strategy
        manualChunks: {
          // Vendor chunks
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          'three-vendor': ['three', '@react-three/fiber', '@react-three/drei'],
          'd3-vendor': ['d3'],
          'ui-vendor': ['zustand', 'react-window'],

          // App chunks
          'visualizations': [
            './src/components/Visualizations/PhaseSpaceVisualization.tsx',
            './src/components/Visualizations/WindingNumbersVisualization.tsx',
            './src/components/Visualizations/FieldDynamicsVisualization.tsx',
            './src/components/Visualizations/MemoryEvolutionVisualization.tsx',
            './src/components/Visualizations/EpochLadderVisualization.tsx',
          ],
          'calculations': [
            './src/calculations/windingNumberCalculator.ts',
            './src/calculations/memoryIntegralCalculator.ts',
            './src/calculations/constantsCalculator.ts',
            './src/calculations/particleMassCalculator.ts',
          ],
          'theory': [
            './src/components/Theory/TheoryExplorer.tsx',
            './src/components/Theory/LawsBrowser.tsx',
            './src/components/Theory/LagrangianExplorer.tsx',
          ],
        },
        // Chunk file naming
        chunkFileNames: (chunkInfo) => {
          const facadeModuleId = chunkInfo.facadeModuleId
            ? chunkInfo.facadeModuleId.split('/').pop()
            : 'chunk';
          return `assets/js/${facadeModuleId}-[hash].js`;
        },
        entryFileNames: 'assets/js/[name]-[hash].js',
        assetFileNames: (assetInfo) => {
          const info = assetInfo.name?.split('.') || [];
          const ext = info[info.length - 1];
          if (/\.(png|jpe?g|svg|gif|tiff|bmp|ico)$/i.test(assetInfo.name || '')) {
            return `assets/images/[name]-[hash].${ext}`;
          }
          if (/\.(woff2?|eot|ttf|otf)$/i.test(assetInfo.name || '')) {
            return `assets/fonts/[name]-[hash].${ext}`;
          }
          return `assets/[ext]/[name]-[hash].${ext}`;
        },
      },
    },
    // Minify with terser for better compression
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: mode === 'production', // Remove console.log in production only
        drop_debugger: true,
        pure_funcs: mode === 'production' ? ['console.log', 'console.info', 'console.debug'] : [],
        passes: 2, // Multiple passes for better compression
      },
      mangle: {
        safari10: true,
      },
      format: {
        comments: false, // Remove all comments
      },
    },
    // Chunk size warning limit (500KB)
    chunkSizeWarningLimit: 500,
    // CSS code splitting
    cssCodeSplit: true,
    // Asset inline limit (4KB)
    assetsInlineLimit: 4096,
  },
  optimizeDeps: {
    // Pre-bundle dependencies
    include: [
      'react',
      'react-dom',
      'react-router-dom',
      'zustand',
      'zustand/middleware',
      'zustand/shallow',
      'use-sync-external-store',
      'use-sync-external-store/shim',
      'use-sync-external-store/shim/with-selector',
      'scheduler',
      'scheduler/tracing',
      'react-window',
      'idb',
      'react-dropzone',
      'attr-accept',
      'merge-value',
    ],
    // Exclude large packages from pre-bundling
    exclude: [
      'three',
      '@react-three/fiber',
      '@react-three/drei',
      'd3',
      'leva', // Exclude leva to avoid zustand compatibility issues
    ],
    esbuildOptions: {
      plugins: [
        {
          name: 'zustand-compat',
          setup(build) {
            // Intercept leva's zustand imports
            build.onLoad({ filter: /node_modules\/leva\/.*\.js$/ }, async (args) => {
              const fs = await import('fs');
              let contents = fs.readFileSync(args.path, 'utf8');

              // Replace default imports with named imports
              contents = contents.replace(
                /import\s+(\w+)\s+from\s+['"]zustand['"]/g,
                "import { create as $1 } from 'zustand'"
              );
              contents = contents.replace(
                /import\s+(\w+)\s+from\s+['"]zustand\/shallow['"]/g,
                "import { shallow as $1 } from 'zustand/shallow'"
              );

              return { contents, loader: 'js' };
            });
          },
        },
      ],
    },
  },
  // Performance optimizations
  esbuild: {
    // Remove pure annotations for better tree-shaking
    treeShaking: true,
    // Minify identifiers
    minifyIdentifiers: true,
    // Minify syntax
    minifySyntax: true,
    // Minify whitespace
    minifyWhitespace: true,
    // Legal comments
    legalComments: 'none',
  },
}
})
