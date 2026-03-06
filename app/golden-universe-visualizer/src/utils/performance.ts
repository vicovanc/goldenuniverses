/**
 * Performance optimization utilities
 */

/**
 * Measure component render time
 */
export function measureRenderTime(componentName: string, callback: () => void): void {
  const startTime = performance.now();
  callback();
  const endTime = performance.now();
  console.log(`[Performance] ${componentName} rendered in ${endTime - startTime}ms`);
}

/**
 * Detect slow frame rates
 */
export function detectSlowFrames(threshold: number = 16.67): void {
  let lastTime = performance.now();
  let frameCount = 0;
  let slowFrames = 0;

  function checkFrame() {
    const currentTime = performance.now();
    const frameTime = currentTime - lastTime;
    lastTime = currentTime;
    frameCount++;

    if (frameTime > threshold) {
      slowFrames++;
    }

    if (frameCount % 60 === 0) {
      const slowFramePercentage = (slowFrames / frameCount) * 100;
      if (slowFramePercentage > 10) {
        console.warn(
          `[Performance] ${slowFramePercentage.toFixed(2)}% slow frames detected`
        );
      }
    }

    requestAnimationFrame(checkFrame);
  }

  requestAnimationFrame(checkFrame);
}

/**
 * Monitor memory usage (Chrome only)
 */
export function monitorMemory(): void {
  if ('memory' in performance) {
    const memory = (performance as any).memory;
    const usedMemoryMB = memory.usedJSHeapSize / 1048576;
    const totalMemoryMB = memory.totalJSHeapSize / 1048576;
    const limitMemoryMB = memory.jsHeapSizeLimit / 1048576;

    console.log('[Performance] Memory usage:', {
      used: `${usedMemoryMB.toFixed(2)} MB`,
      total: `${totalMemoryMB.toFixed(2)} MB`,
      limit: `${limitMemoryMB.toFixed(2)} MB`,
      percentage: `${((usedMemoryMB / limitMemoryMB) * 100).toFixed(2)}%`,
    });

    // Warning if memory usage is high
    if (usedMemoryMB / limitMemoryMB > 0.9) {
      console.warn('[Performance] High memory usage detected!');
    }
  }
}

/**
 * Get connection info
 */
export function getConnectionInfo(): {
  effectiveType: string;
  downlink: number;
  rtt: number;
  saveData: boolean;
} | null {
  const connection =
    (navigator as any).connection ||
    (navigator as any).mozConnection ||
    (navigator as any).webkitConnection;

  if (connection) {
    return {
      effectiveType: connection.effectiveType || 'unknown',
      downlink: connection.downlink || 0,
      rtt: connection.rtt || 0,
      saveData: connection.saveData || false,
    };
  }

  return null;
}

/**
 * Check if user is on slow connection
 */
export function isSlowConnection(): boolean {
  const connection = getConnectionInfo();
  if (!connection) return false;

  return (
    connection.effectiveType === '2g' ||
    connection.effectiveType === 'slow-2g' ||
    connection.saveData
  );
}

/**
 * Resource hints for preloading
 */
export function preloadResource(url: string, as: string = 'fetch'): void {
  const link = document.createElement('link');
  link.rel = 'preload';
  link.as = as;
  link.href = url;
  document.head.appendChild(link);
}

/**
 * Prefetch resource for future navigation
 */
export function prefetchResource(url: string): void {
  const link = document.createElement('link');
  link.rel = 'prefetch';
  link.href = url;
  document.head.appendChild(link);
}

/**
 * DNS prefetch for external domains
 */
export function dnsPrefetch(domain: string): void {
  const link = document.createElement('link');
  link.rel = 'dns-prefetch';
  link.href = domain;
  document.head.appendChild(link);
}

/**
 * Optimize images based on device capabilities
 */
export function getOptimalImageSize(): 'small' | 'medium' | 'large' {
  const width = window.innerWidth;
  const dpr = window.devicePixelRatio || 1;

  if (width < 640 || dpr <= 1) {
    return 'small';
  } else if (width < 1024 || dpr <= 2) {
    return 'medium';
  }
  return 'large';
}

/**
 * Check if reduced motion is preferred
 */
export function prefersReducedMotion(): boolean {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

/**
 * Debounce function for resize/scroll
 */
export function debounceRAF<T extends (...args: any[]) => any>(
  callback: T
): (...args: Parameters<T>) => void {
  let rafId: number | null = null;

  return function (...args: Parameters<T>) {
    if (rafId !== null) {
      cancelAnimationFrame(rafId);
    }

    rafId = requestAnimationFrame(() => {
      callback(...args);
      rafId = null;
    });
  };
}

/**
 * Idle callback wrapper
 */
export function runWhenIdle(callback: () => void, options?: IdleRequestOptions): number {
  if ('requestIdleCallback' in window) {
    return window.requestIdleCallback(callback, options);
  }
  // Fallback for browsers that don't support requestIdleCallback
  return setTimeout(callback, 1) as any;
}

/**
 * Cancel idle callback
 */
export function cancelIdle(id: number): void {
  if ('cancelIdleCallback' in window) {
    window.cancelIdleCallback(id);
  } else {
    clearTimeout(id);
  }
}

/**
 * Batch DOM updates
 */
export function batchUpdates(updates: Array<() => void>): void {
  requestAnimationFrame(() => {
    updates.forEach((update) => update());
  });
}

/**
 * Virtual scrolling helper
 */
export function calculateVisibleRange(
  scrollTop: number,
  containerHeight: number,
  itemHeight: number,
  totalItems: number,
  overscan: number = 3
): { start: number; end: number } {
  const start = Math.max(0, Math.floor(scrollTop / itemHeight) - overscan);
  const visibleItems = Math.ceil(containerHeight / itemHeight);
  const end = Math.min(totalItems, start + visibleItems + overscan * 2);

  return { start, end };
}

/**
 * Check device memory (Chrome only)
 */
export function getDeviceMemory(): number | undefined {
  return (navigator as any).deviceMemory;
}

/**
 * Check hardware concurrency
 */
export function getHardwareConcurrency(): number {
  return navigator.hardwareConcurrency || 4;
}

/**
 * Adaptive loading strategy
 */
export function getLoadingStrategy(): {
  shouldLazyLoad: boolean;
  shouldPreload: boolean;
  imageQuality: 'low' | 'medium' | 'high';
  enableAnimations: boolean;
} {
  const isSlowNet = isSlowConnection();
  const deviceMemory = getDeviceMemory() || 4;
  const reducedMotion = prefersReducedMotion();

  return {
    shouldLazyLoad: isSlowNet || deviceMemory < 4,
    shouldPreload: !isSlowNet && deviceMemory >= 4,
    imageQuality: isSlowNet ? 'low' : deviceMemory >= 8 ? 'high' : 'medium',
    enableAnimations: !reducedMotion && !isSlowNet,
  };
}

/**
 * Report web vitals
 */
export function reportWebVitals(metric: any): void {
  console.log('[Web Vitals]', metric);

  // Send to analytics service
  if (window.gtag) {
    window.gtag('event', metric.name, {
      value: Math.round(metric.value),
      metric_id: metric.id,
      metric_value: metric.value,
      metric_delta: metric.delta,
    });
  }
}

declare global {
  interface Window {
    gtag?: (...args: any[]) => void;
  }
}
