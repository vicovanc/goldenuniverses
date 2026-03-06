/**
 * Resource Preloading Utilities
 * Optimize loading of critical resources
 */

/**
 * Preload a JavaScript module
 */
export function preloadModule(modulePath: string): void {
  const link = document.createElement('link');
  link.rel = 'modulepreload';
  link.href = modulePath;
  document.head.appendChild(link);
}

/**
 * Prefetch a resource for future navigation
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
 * Preconnect to external origins
 */
export function preconnect(origin: string, crossorigin: boolean = false): void {
  const link = document.createElement('link');
  link.rel = 'preconnect';
  link.href = origin;
  if (crossorigin) {
    link.crossOrigin = 'anonymous';
  }
  document.head.appendChild(link);
}

/**
 * Preload critical routes
 */
export function preloadCriticalRoutes(): void {
  // Preload the most commonly accessed routes
  const criticalRoutes = [
    '/assets/js/Home-*.js',
    '/assets/js/Theory-*.js',
    '/assets/js/Visualizations-*.js',
  ];

  // This would need to be called after build with actual filenames
  // For now, we'll use modulepreload which Vite handles automatically
}

/**
 * Lazy load images with Intersection Observer
 */
export function lazyLoadImage(img: HTMLImageElement): void {
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const image = entry.target as HTMLImageElement;
          const src = image.dataset.src;
          if (src) {
            image.src = src;
            observer.unobserve(image);
          }
        }
      });
    });

    observer.observe(img);
  } else {
    // Fallback for browsers without Intersection Observer
    const src = img.dataset.src;
    if (src) {
      img.src = src;
    }
  }
}

/**
 * Initialize resource hints for CDNs and external services
 */
export function initializeResourceHints(): void {
  // DNS prefetch for Pyodide CDN
  dnsPrefetch('https://cdn.jsdelivr.net');

  // Preconnect to CDN
  preconnect('https://cdn.jsdelivr.net', true);
}

/**
 * Report Web Vitals to analytics
 */
export interface WebVitalsMetric {
  name: 'CLS' | 'FID' | 'FCP' | 'LCP' | 'TTFB';
  value: number;
  rating: 'good' | 'needs-improvement' | 'poor';
}

export function reportWebVitals(metric: WebVitalsMetric): void {
  // Log to console in development
  if (import.meta.env.DEV) {
    console.log(`[Web Vitals] ${metric.name}:`, {
      value: metric.value.toFixed(2),
      rating: metric.rating,
    });
  }

  // In production, send to analytics
  // Example: sendToAnalytics(metric);
}

/**
 * Get Core Web Vitals
 */
export async function getCoreWebVitals(): Promise<void> {
  // This would integrate with web-vitals library in a real implementation
  // For now, we use Performance API

  const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
  const paint = performance.getEntriesByType('paint');

  // First Contentful Paint
  const fcp = paint.find(p => p.name === 'first-contentful-paint');
  if (fcp) {
    reportWebVitals({
      name: 'FCP',
      value: fcp.startTime,
      rating: fcp.startTime < 1800 ? 'good' : fcp.startTime < 3000 ? 'needs-improvement' : 'poor',
    });
  }

  // Largest Contentful Paint
  const lcpEntries = performance.getEntriesByType('largest-contentful-paint');
  if (lcpEntries.length > 0) {
    const lcp = lcpEntries[lcpEntries.length - 1];
    reportWebVitals({
      name: 'LCP',
      value: lcp.startTime,
      rating: lcp.startTime < 2500 ? 'good' : lcp.startTime < 4000 ? 'needs-improvement' : 'poor',
    });
  }

  // Time to First Byte
  if (navigation) {
    const ttfb = navigation.responseStart - navigation.requestStart;
    reportWebVitals({
      name: 'TTFB',
      value: ttfb,
      rating: ttfb < 800 ? 'good' : ttfb < 1800 ? 'needs-improvement' : 'poor',
    });
  }
}
