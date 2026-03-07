/**
 * Monitoring Service
 * Handles Sentry error tracking and performance monitoring
 * Note: Sentry is optional - if not installed, monitoring will be disabled
 */

// Sentry types (will be null if @sentry packages are not installed)
type SentryModule = any;
type SeverityLevel = 'fatal' | 'error' | 'warning' | 'log' | 'info' | 'debug';
type Transaction = any;

interface MonitoringConfig {
  dsn: string;
  environment: string;
  enabled: boolean;
  tracesSampleRate: number;
}

class MonitoringService {
  private config: MonitoringConfig;
  private initialized = false;
  private Sentry: SentryModule | null = null;
  private BrowserTracing: any | null = null;

  constructor() {
    this.config = {
      dsn: import.meta.env.VITE_SENTRY_DSN || '',
      environment: import.meta.env.VITE_SENTRY_ENVIRONMENT || 'development',
      enabled: import.meta.env.VITE_ENABLE_SENTRY === 'true',
      tracesSampleRate: parseFloat(
        import.meta.env.VITE_SENTRY_TRACES_SAMPLE_RATE || '0.1'
      ),
    };
    this.loadSentry();
  }

  /**
   * Dynamically load Sentry if available
   */
  private async loadSentry(): Promise<void> {
    if (!this.config.enabled) return;

    try {
      // @ts-ignore - Optional dependency
      const sentryModule = await import('@sentry/react');
      // @ts-ignore - Optional dependency
      const tracingModule = await import('@sentry/tracing');
      this.Sentry = sentryModule;
      this.BrowserTracing = tracingModule.BrowserTracing;
    } catch (error) {
      console.warn('Sentry packages not installed. Monitoring disabled.');
      this.config.enabled = false;
    }
  }

  /**
   * Initialize Sentry
   */
  async init(): Promise<void> {
    if (!this.config.enabled || !this.config.dsn || this.initialized) {
      return;
    }

    // Wait for Sentry to load
    if (!this.Sentry || !this.BrowserTracing) {
      await this.loadSentry();
    }

    if (!this.Sentry || !this.BrowserTracing) {
      console.warn('Cannot initialize Sentry - modules not available');
      return;
    }

    this.Sentry.init({
      dsn: this.config.dsn,
      environment: this.config.environment,
      integrations: [
        new this.BrowserTracing(),
        new this.Sentry.Replay({
          maskAllText: true,
          blockAllMedia: true,
        }),
      ],
      tracesSampleRate: this.config.tracesSampleRate,
      replaysSessionSampleRate: 0.1,
      replaysOnErrorSampleRate: 1.0,
      beforeSend(event: any) {
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
    if (!this.config.enabled || !this.initialized || !this.Sentry) {
      console.error('Error:', error, context);
      return;
    }

    this.Sentry.captureException(error, {
      extra: context,
    });
  }

  /**
   * Capture message
   */
  captureMessage(message: string, level: SeverityLevel = 'info'): void {
    if (!this.config.enabled || !this.initialized || !this.Sentry) {
      console.log(message);
      return;
    }

    this.Sentry.captureMessage(message, level);
  }

  /**
   * Set user context
   */
  setUser(user: { id: string; email?: string; username?: string }): void {
    if (!this.config.enabled || !this.initialized || !this.Sentry) return;

    this.Sentry.setUser(user);
  }

  /**
   * Set custom context
   */
  setContext(name: string, context: Record<string, any>): void {
    if (!this.config.enabled || !this.initialized || !this.Sentry) return;

    this.Sentry.setContext(name, context);
  }

  /**
   * Add breadcrumb
   */
  addBreadcrumb(
    message: string,
    category: string,
    level: SeverityLevel = 'info'
  ): void {
    if (!this.config.enabled || !this.initialized || !this.Sentry) return;

    this.Sentry.addBreadcrumb({
      message,
      category,
      level,
    });
  }

  /**
   * Start transaction
   */
  startTransaction(name: string, op: string): Transaction | null {
    if (!this.config.enabled || !this.initialized || !this.Sentry) return null;

    return this.Sentry.startTransaction({
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
