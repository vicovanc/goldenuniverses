/**
 * Performance Utilities
 * Central export for all performance-related functionality
 */

export { getPerformanceMonitor, PerformanceMonitor } from './metrics';
export type { PerformanceMetrics } from './metrics';

export { getCacheManager, CacheManager, CACHE_TTL } from './cache';
export type { CacheEntry } from './cache';

export { WorkerPool } from './workerPool';
export type { WorkerTask, WorkerInstance } from './workerPool';

export {
  preloadModule,
  prefetchResource,
  dnsPrefetch,
  preconnect,
  initializeResourceHints,
  getCoreWebVitals,
  reportWebVitals,
  lazyLoadImage,
} from './preload';
export type { WebVitalsMetric } from './preload';

export {
  register as registerServiceWorker,
  unregister as unregisterServiceWorker,
  checkForUpdates,
  skipWaiting,
} from './serviceWorker';
export type { ServiceWorkerConfig } from './serviceWorker';
