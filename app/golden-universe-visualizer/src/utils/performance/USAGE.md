# Performance Utilities Usage Guide

## Table of Contents
1. [Performance Monitoring](#performance-monitoring)
2. [Caching](#caching)
3. [Worker Pool](#worker-pool)
4. [Resource Preloading](#resource-preloading)
5. [Service Worker](#service-worker)
6. [React Hook](#react-hook)

---

## Performance Monitoring

### Basic Usage

```typescript
import { getPerformanceMonitor } from '@utils/performance';

const monitor = getPerformanceMonitor();

// Get current metrics
const metrics = monitor.getMetrics();
console.log('Bundle size:', metrics.bundleSize);
console.log('Load time:', metrics.loadTime);
console.log('FPS:', metrics.fps);

// Log formatted metrics to console
monitor.logMetrics();
```

### Subscribe to Updates

```typescript
import { getPerformanceMonitor } from '@utils/performance';

const monitor = getPerformanceMonitor();

const unsubscribe = monitor.onUpdate((metrics) => {
  console.log('FPS updated:', metrics.fps.current);

  // Check for performance issues
  if (metrics.fps.current < 30) {
    console.warn('Low FPS detected!');
  }
});

// Later, unsubscribe
unsubscribe();
```

---

## Caching

### Basic Operations

```typescript
import { getCacheManager } from '@utils/performance';

const cache = getCacheManager();

// Set a value with default TTL
await cache.set('calculations', 'electron-mass', {
  mass: 0.511,
  precision: 50
});

// Get a value
const data = await cache.get('calculations', 'electron-mass');

// Check if exists
const exists = await cache.has('calculations', 'electron-mass');

// Delete a value
await cache.delete('calculations', 'electron-mass');
```

### Advanced Caching

```typescript
import { getCacheManager, CACHE_TTL } from '@utils/performance';

const cache = getCacheManager();

// Custom TTL (1 hour)
await cache.set(
  'calculations',
  'my-key',
  data,
  3600000, // 1 hour in ms
  { source: 'api', version: '1.0' } // metadata
);

// Cache-aside pattern
const result = await cache.getOrSet(
  'calculations',
  'expensive-calc',
  async () => {
    // This only runs if cache miss
    return await performExpensiveCalculation();
  },
  CACHE_TTL.CALCULATIONS
);

// Get all cached items
const allItems = await cache.getAll('calculations');

// Clear specific store
await cache.clear('calculations');

// Clear all stores
await cache.clearAll();

// Get statistics
const stats = await cache.getStats();
console.log('Cached calculations:', stats.calculations);
```

---

## Worker Pool

### Creating a Worker Pool

```typescript
import { WorkerPool } from '@utils/performance';

// Create worker factory
const workerFactory = () => new Worker(
  new URL('./myWorker.ts', import.meta.url),
  { type: 'module' }
);

// Create pool with 4 workers
const pool = new WorkerPool(workerFactory, 4);

// Execute task
const result = await pool.execute(
  'calculate',
  { data: [1, 2, 3] },
  1 // priority (higher = more important)
);

// Get pool statistics
const stats = pool.getStats();
console.log('Busy workers:', stats.busyWorkers);
console.log('Queue length:', stats.queueLength);

// Cleanup
pool.terminate();
```

---

## Resource Preloading

### DNS Prefetch & Preconnect

```typescript
import {
  dnsPrefetch,
  preconnect,
  initializeResourceHints
} from '@utils/performance';

// Prefetch DNS for external domains
dnsPrefetch('https://cdn.jsdelivr.net');

// Preconnect to CDN (establishes connection)
preconnect('https://cdn.jsdelivr.net', true);

// Initialize all resource hints
initializeResourceHints();
```

### Module Preloading

```typescript
import {
  preloadModule,
  prefetchResource
} from '@utils/performance';

// Preload a critical module
preloadModule('/assets/js/Home-abc123.js');

// Prefetch next route
prefetchResource('/assets/js/Theory-def456.js');
```

### Lazy Loading Images

```typescript
import { lazyLoadImage } from '@utils/performance';

// In HTML
<img data-src="/path/to/image.jpg" alt="..." />

// In JavaScript
const img = document.querySelector('img[data-src]');
if (img instanceof HTMLImageElement) {
  lazyLoadImage(img);
}
```

### Web Vitals

```typescript
import { getCoreWebVitals, reportWebVitals } from '@utils/performance';

// Get and report Core Web Vitals
await getCoreWebVitals();

// Custom reporting
reportWebVitals({
  name: 'FCP',
  value: 1200,
  rating: 'good'
});
```

---

## Service Worker

### Registration

```typescript
import { registerServiceWorker } from '@utils/performance';

// Register with callbacks
registerServiceWorker({
  onSuccess: (registration) => {
    console.log('Service Worker registered:', registration);
  },
  onUpdate: (registration) => {
    console.log('New content available!');
    // Show update notification to user
  },
  onError: (error) => {
    console.error('Service Worker error:', error);
  }
});
```

### Managing Updates

```typescript
import {
  checkForUpdates,
  skipWaiting,
  unregisterServiceWorker
} from '@utils/performance';

// Check for updates manually
checkForUpdates();

// Skip waiting and activate new version
skipWaiting();

// Unregister service worker
unregisterServiceWorker();
```

---

## React Hook

### usePerformance Hook

```typescript
import { usePerformance } from '@/hooks/usePerformance';

function MyComponent() {
  const { metrics, cacheStats, clearCache, logMetrics } = usePerformance();

  if (!metrics) return <div>Loading metrics...</div>;

  return (
    <div>
      <h2>Performance Metrics</h2>

      <div>
        <h3>Bundle Size</h3>
        <p>Total: {(metrics.bundleSize.total / 1024).toFixed(2)} KB</p>
        <p>JavaScript: {(metrics.bundleSize.js / 1024).toFixed(2)} KB</p>
      </div>

      <div>
        <h3>FPS</h3>
        <p>Current: {metrics.fps.current}</p>
        <p>Average: {metrics.fps.average}</p>
      </div>

      <div>
        <h3>Cache</h3>
        <p>Calculations: {cacheStats?.calculations}</p>
        <p>Total: {cacheStats?.total}</p>
        <button onClick={() => clearCache()}>Clear All</button>
        <button onClick={() => clearCache('calculations')}>
          Clear Calculations
        </button>
      </div>

      <button onClick={logMetrics}>Log Metrics to Console</button>
    </div>
  );
}
```

---

## Complete Example: Optimized Calculation Component

```typescript
import { useState } from 'react';
import { getPythonEngineOptimized } from '@services/pythonEngine/pythonEngineOptimized';
import { usePerformance } from '@/hooks/usePerformance';

function ParticleMassCalculator() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const { cacheStats } = usePerformance();

  const calculate = async () => {
    setLoading(true);
    try {
      const engine = getPythonEngineOptimized();

      // Calculation will be cached automatically
      const mass = await engine.calculateParticleMass({
        particle: 'electron',
        epoch: 111,
        precision: 50
      });

      setResult(mass);
    } catch (error) {
      console.error('Calculation error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <button onClick={calculate} disabled={loading}>
        {loading ? 'Calculating...' : 'Calculate Electron Mass'}
      </button>

      {result && (
        <div>
          <h3>Result</h3>
          <p>Mass: {result.mass_MeV} MeV</p>
          <p>Error: {result.error_ppm} ppm</p>
        </div>
      )}

      <div>
        <small>
          Cached calculations: {cacheStats?.calculations}
        </small>
      </div>
    </div>
  );
}

export default ParticleMassCalculator;
```

---

## Best Practices

### 1. Cache Expensive Operations

```typescript
// ✅ Good: Cache the result
const result = await cache.getOrSet(
  'calculations',
  cacheKey,
  () => expensiveOperation()
);

// ❌ Bad: No caching
const result = await expensiveOperation();
```

### 2. Use Appropriate TTL

```typescript
// ✅ Good: Match TTL to data volatility
await cache.set('calculations', key, data, CACHE_TTL.CALCULATIONS); // 24h
await cache.set('visualizations', key, data, CACHE_TTL.VISUALIZATIONS); // 1h

// ❌ Bad: One size fits all
await cache.set('calculations', key, data, 60000); // Always 1 minute
```

### 3. Monitor Performance

```typescript
// ✅ Good: Monitor and react to issues
const monitor = getPerformanceMonitor();
monitor.onUpdate((metrics) => {
  if (metrics.fps.current < 30) {
    // Reduce quality or disable animations
    disableHeavyAnimations();
  }
});

// ❌ Bad: Ignore performance
// Just render everything and hope for the best
```

### 4. Preload Critical Resources

```typescript
// ✅ Good: Preload what you know you'll need
useEffect(() => {
  initializeResourceHints();
  preloadModule('/assets/js/Home-*.js');
}, []);

// ❌ Bad: Load everything on-demand
// User waits for each resource
```

### 5. Clean Up Resources

```typescript
// ✅ Good: Clean up in useEffect
useEffect(() => {
  const pool = new WorkerPool(factory, 4);

  return () => {
    pool.terminate();
  };
}, []);

// ❌ Bad: Memory leaks
const pool = new WorkerPool(factory, 4);
// Never terminated
```

---

## Performance Checklist

- [ ] Use lazy loading for routes
- [ ] Cache expensive calculations
- [ ] Virtualize long lists
- [ ] Monitor FPS for animations
- [ ] Use worker pool for heavy computation
- [ ] Preload critical resources
- [ ] Enable service worker in production
- [ ] Monitor bundle size
- [ ] Track Core Web Vitals
- [ ] Clean up resources in useEffect

---

## Debugging

### View Cache Contents

```typescript
const cache = getCacheManager();
const allCalcs = await cache.getAll('calculations');
console.log('All calculations:', allCalcs);
```

### Check Worker Status

```typescript
const pool = new WorkerPool(factory, 4);
setInterval(() => {
  console.log('Pool stats:', pool.getStats());
}, 1000);
```

### Monitor Metrics

```typescript
const monitor = getPerformanceMonitor();
monitor.logMetrics(); // Formatted console output
```

---

## Troubleshooting

### Cache not working?
1. Check IndexedDB is enabled
2. Verify store name is correct
3. Check TTL hasn't expired
4. Look for errors in console

### Workers not starting?
1. Check worker file path
2. Verify module type is correct
3. Check browser console for errors
4. Test worker in isolation

### Poor FPS?
1. Check metrics dashboard
2. Reduce particle count
3. Disable shadows/effects
4. Use LOD (Level of Detail)

---

## Additional Resources

- [Web Performance API](https://developer.mozilla.org/en-US/docs/Web/API/Performance_API)
- [IndexedDB API](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API)
- [Web Workers API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API)
- [Core Web Vitals](https://web.dev/vitals/)
