import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.tsx'
import { registerServiceWorker, setupInstallPrompt, setupNetworkListeners } from '@/utils/pwa'
import './styles/print.scss'

// Initialize PWA features
if (import.meta.env.PROD) {
  // Register service worker in production
  registerServiceWorker().then((registration) => {
    if (registration) {
      console.log('[PWA] Service Worker registered successfully')
    }
  })

  // Setup install prompt
  setupInstallPrompt()

  // Setup network status listeners
  setupNetworkListeners(
    () => {
      console.log('[PWA] Connection restored')
    },
    () => {
      console.log('[PWA] Connection lost - app will work offline')
    }
  )
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
