/**
 * Performance Metrics Collection
 * Tracks bundle size, load time, memory usage, and FPS
 */

export interface PerformanceMetrics {
  bundleSize: {
    total: number;
    js: number;
    css: number;
    chunks: Array<{ name: string; size: number }>;
  };
  loadTime: {
    domContentLoaded: number;
    loadComplete: number;
    firstContentfulPaint: number;
    largestContentfulPaint: number;
    timeToInteractive: number;
  };
  memory: {
    used: number;
    total: number;
    limit: number;
  };
  fps: {
    current: number;
    average: number;
    min: number;
    max: number;
  };
  timestamp: number;
}

class PerformanceMonitor {
  private fpsHistory: number[] = [];
  private fpsFrameCount = 0;
  private fpsLastTime = performance.now();
  private rafId: number | null = null;
  private listeners: Set<(metrics: PerformanceMetrics) => void> = new Set();

  constructor() {
    if (typeof window !== 'undefined') {
      this.startFPSMonitoring();
    }
  }

  /**
   * Get current performance metrics
   */
  getMetrics(): PerformanceMetrics {
    const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
    const paint = performance.getEntriesByType('paint');

    // Calculate bundle size from performance entries
    const resources = performance.getEntriesByType('resource') as PerformanceResourceTiming[];
    const jsResources = resources.filter(r => r.name.endsWith('.js'));
    const cssResources = resources.filter(r => r.name.endsWith('.css'));

    const bundleSize = {
      js: jsResources.reduce((sum, r) => sum + (r.transferSize || 0), 0),
      css: cssResources.reduce((sum, r) => sum + (r.transferSize || 0), 0),
      total: resources.reduce((sum, r) => sum + (r.transferSize || 0), 0),
      chunks: jsResources.map(r => ({
        name: r.name.split('/').pop() || 'unknown',
        size: r.transferSize || 0,
      })),
    };

    // Get paint timings
    const fcp = paint.find(p => p.name === 'first-contentful-paint');
    const lcp = this.getLargestContentfulPaint();

    const loadTime = {
      domContentLoaded: navigation?.domContentLoadedEventEnd - navigation?.domContentLoadedEventStart || 0,
      loadComplete: navigation?.loadEventEnd - navigation?.loadEventStart || 0,
      firstContentfulPaint: fcp?.startTime || 0,
      largestContentfulPaint: lcp || 0,
      timeToInteractive: this.getTimeToInteractive(),
    };

    // Get memory usage (Chrome only)
    const memory = this.getMemoryUsage();

    // Get FPS stats
    const fps = this.getFPSStats();

    return {
      bundleSize,
      loadTime,
      memory,
      fps,
      timestamp: Date.now(),
    };
  }

  /**
   * Get Largest Contentful Paint
   */
  private getLargestContentfulPaint(): number {
    try {
      const lcpEntries = performance.getEntriesByType('largest-contentful-paint');
      if (lcpEntries.length > 0) {
        return lcpEntries[lcpEntries.length - 1].startTime;
      }
    } catch (e) {
      // LCP not supported
    }
    return 0;
  }

  /**
   * Get Time to Interactive (approximation)
   */
  private getTimeToInteractive(): number {
    const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
    return navigation?.domInteractive - navigation?.fetchStart || 0;
  }

  /**
   * Get memory usage (Chrome only)
   */
  private getMemoryUsage(): PerformanceMetrics['memory'] {
    if ('memory' in performance && (performance as any).memory) {
      const mem = (performance as any).memory;
      return {
        used: mem.usedJSHeapSize,
        total: mem.totalJSHeapSize,
        limit: mem.jsHeapSizeLimit,
      };
    }
    return { used: 0, total: 0, limit: 0 };
  }

  /**
   * Start FPS monitoring
   */
  private startFPSMonitoring(): void {
    const measureFPS = (currentTime: number) => {
      this.fpsFrameCount++;
      const delta = currentTime - this.fpsLastTime;

      if (delta >= 1000) {
        const fps = Math.round((this.fpsFrameCount * 1000) / delta);
        this.fpsHistory.push(fps);

        // Keep only last 60 samples
        if (this.fpsHistory.length > 60) {
          this.fpsHistory.shift();
        }

        this.fpsFrameCount = 0;
        this.fpsLastTime = currentTime;

        // Notify listeners
        this.notifyListeners();
      }

      this.rafId = requestAnimationFrame(measureFPS);
    };

    this.rafId = requestAnimationFrame(measureFPS);
  }

  /**
   * Get FPS statistics
   */
  private getFPSStats(): PerformanceMetrics['fps'] {
    if (this.fpsHistory.length === 0) {
      return { current: 60, average: 60, min: 60, max: 60 };
    }

    const current = this.fpsHistory[this.fpsHistory.length - 1] || 60;
    const average = Math.round(
      this.fpsHistory.reduce((sum, fps) => sum + fps, 0) / this.fpsHistory.length
    );
    const min = Math.min(...this.fpsHistory);
    const max = Math.max(...this.fpsHistory);

    return { current, average, min, max };
  }

  /**
   * Subscribe to metrics updates
   */
  onUpdate(listener: (metrics: PerformanceMetrics) => void): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  /**
   * Notify all listeners
   */
  private notifyListeners(): void {
    const metrics = this.getMetrics();
    this.listeners.forEach(listener => listener(metrics));
  }

  /**
   * Stop FPS monitoring
   */
  stopFPSMonitoring(): void {
    if (this.rafId !== null) {
      cancelAnimationFrame(this.rafId);
      this.rafId = null;
    }
  }

  /**
   * Log metrics to console
   */
  logMetrics(): void {
    const metrics = this.getMetrics();
    console.group('Performance Metrics');
    console.log('Bundle Size:', {
      total: `${(metrics.bundleSize.total / 1024).toFixed(2)} KB`,
      js: `${(metrics.bundleSize.js / 1024).toFixed(2)} KB`,
      css: `${(metrics.bundleSize.css / 1024).toFixed(2)} KB`,
    });
    console.log('Load Time:', {
      domContentLoaded: `${metrics.loadTime.domContentLoaded.toFixed(2)} ms`,
      loadComplete: `${metrics.loadTime.loadComplete.toFixed(2)} ms`,
      firstContentfulPaint: `${metrics.loadTime.firstContentfulPaint.toFixed(2)} ms`,
      largestContentfulPaint: `${metrics.loadTime.largestContentfulPaint.toFixed(2)} ms`,
    });
    console.log('Memory:', {
      used: `${(metrics.memory.used / 1024 / 1024).toFixed(2)} MB`,
      total: `${(metrics.memory.total / 1024 / 1024).toFixed(2)} MB`,
    });
    console.log('FPS:', metrics.fps);
    console.groupEnd();
  }
}

// Singleton instance
let monitorInstance: PerformanceMonitor | null = null;

export function getPerformanceMonitor(): PerformanceMonitor {
  if (!monitorInstance) {
    monitorInstance = new PerformanceMonitor();
  }
  return monitorInstance;
}

export { PerformanceMonitor };
