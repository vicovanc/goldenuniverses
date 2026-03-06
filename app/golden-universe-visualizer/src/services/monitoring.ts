/**
 * Monitoring Service
 * Handles Sentry error tracking and performance monitoring
 */

import * as Sentry from '@sentry/react';
import { BrowserTracing } from '@sentry/tracing';

interface MonitoringConfig {
  dsn: string;
  environment: string;
  enabled: boolean;
  tracesSampleRate: number;
}

class MonitoringService {
  private config: MonitoringConfig;
  private initialized = false;

  constructor() {
    this.config = {
      dsn: import.meta.env.VITE_SENTRY_DSN || '',
      environment: import.meta.env.VITE_SENTRY_ENVIRONMENT || 'development',
      enabled: import.meta.env.VITE_ENABLE_SENTRY === 'true',
      tracesSampleRate: parseFloat(
        import.meta.env.VITE_SENTRY_TRACES_SAMPLE_RATE || '0.1'
      ),
    };
  }

  /**
   * Initialize Sentry
   */
  init(): void {
    if (!this.config.enabled || !this.config.dsn || this.initialized) {
      return;
    }

    Sentry.init({
      dsn: this.config.dsn,
      environment: this.config.environment,
      integrations: [
        new BrowserTracing(),
        new Sentry.Replay({
          maskAllText: true,
          blockAllMedia: true,
        }),
      ],
      tracesSampleRate: this.config.tracesSampleRate,
      replaysSessionSampleRate: 0.1,
      replaysOnErrorSampleRate: 1.0,
      beforeSend(event) {
        // Filter out non-error events in production
        if (event.level === 'info' || event.level === 'warning') {
          return null;
        }
        return event;
      },
    });

    this.initialized = true;
  }

  /**
   * Capture exception
   */
  captureException(error: Error, context?: Record<string, any>): void {
    if (!this.config.enabled || !this.initialized) {
      console.error('Error:', error, context);
      return;
    }

    Sentry.captureException(error, {
      extra: context,
    });
  }

  /**
   * Capture message
   */
  captureMessage(message: string, level: Sentry.SeverityLevel = 'info'): void {
    if (!this.config.enabled || !this.initialized) {
      console.log(message);
      return;
    }

    Sentry.captureMessage(message, level);
  }

  /**
   * Set user context
   */
  setUser(user: { id: string; email?: string; username?: string }): void {
    if (!this.config.enabled || !this.initialized) return;

    Sentry.setUser(user);
  }

  /**
   * Set custom context
   */
  setContext(name: string, context: Record<string, any>): void {
    if (!this.config.enabled || !this.initialized) return;

    Sentry.setContext(name, context);
  }

  /**
   * Add breadcrumb
   */
  addBreadcrumb(
    message: string,
    category: string,
    level: Sentry.SeverityLevel = 'info'
  ): void {
    if (!this.config.enabled || !this.initialized) return;

    Sentry.addBreadcrumb({
      message,
      category,
      level,
    });
  }

  /**
   * Start transaction
   */
  startTransaction(name: string, op: string): Sentry.Transaction | null {
    if (!this.config.enabled || !this.initialized) return null;

    return Sentry.startTransaction({
      name,
      op,
    });
  }
}

// Global monitoring instance
export const monitoring = new MonitoringService();

// Performance monitoring helper
export class PerformanceMonitor {
  private marks: Map<string, number> = new Map();

  mark(name: string): void {
    this.marks.set(name, performance.now());
  }

  measure(name: string, startMark: string): number {
    const startTime = this.marks.get(startMark);
    if (!startTime) {
      console.warn(`No mark found for: ${startMark}`);
      return 0;
    }

    const duration = performance.now() - startTime;

    // Send to monitoring
    monitoring.addBreadcrumb(
      `Performance: ${name} took ${duration.toFixed(2)}ms`,
      'performance',
      'info'
    );

    return duration;
  }

  clear(name?: string): void {
    if (name) {
      this.marks.delete(name);
    } else {
      this.marks.clear();
    }
  }
}

export const performanceMonitor = new PerformanceMonitor();
