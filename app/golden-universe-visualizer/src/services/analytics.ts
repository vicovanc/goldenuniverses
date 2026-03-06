/**
 * Analytics Service
 * Handles Google Analytics tracking and custom events
 */

interface AnalyticsConfig {
  trackingId: string;
  enabled: boolean;
}

class AnalyticsService {
  private config: AnalyticsConfig;
  private initialized = false;

  constructor() {
    this.config = {
      trackingId: import.meta.env.VITE_GOOGLE_ANALYTICS_ID || '',
      enabled: import.meta.env.VITE_ENABLE_ANALYTICS === 'true',
    };
  }

  /**
   * Initialize Google Analytics
   */
  init(): void {
    if (!this.config.enabled || !this.config.trackingId || this.initialized) {
      return;
    }

    // Load Google Analytics script
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${this.config.trackingId}`;
    document.head.appendChild(script);

    // Initialize gtag
    window.dataLayer = window.dataLayer || [];
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    function gtag(...args: any[]) {
      window.dataLayer.push(args);
    }
    gtag('js', new Date());
    gtag('config', this.config.trackingId, {
      send_page_view: false, // We'll send page views manually
    });

    this.initialized = true;
  }

  /**
   * Track page view
   */
  trackPageView(path: string, title?: string): void {
    if (!this.config.enabled || !this.initialized) return;

    if (window.gtag) {
      window.gtag('event', 'page_view', {
        page_path: path,
        page_title: title || document.title,
      });
    }
  }

  /**
   * Track custom event
   */
  trackEvent(
    category: string,
    action: string,
    label?: string,
    value?: number
  ): void {
    if (!this.config.enabled || !this.initialized) return;

    if (window.gtag) {
      window.gtag('event', action, {
        event_category: category,
        event_label: label,
        value: value,
      });
    }
  }

  /**
   * Track visualization interaction
   */
  trackVisualization(name: string, action: string): void {
    this.trackEvent('Visualization', action, name);
  }

  /**
   * Track calculation
   */
  trackCalculation(type: string, duration: number): void {
    this.trackEvent('Calculation', 'execute', type, duration);
  }

  /**
   * Track search
   */
  trackSearch(query: string, resultsCount: number): void {
    this.trackEvent('Search', 'query', query, resultsCount);
  }

  /**
   * Track error
   */
  trackError(error: string, fatal: boolean = false): void {
    this.trackEvent('Error', fatal ? 'fatal' : 'non-fatal', error);
  }

  /**
   * Track timing
   */
  trackTiming(category: string, variable: string, value: number): void {
    if (!this.config.enabled || !this.initialized) return;

    if (window.gtag) {
      window.gtag('event', 'timing_complete', {
        name: variable,
        value: value,
        event_category: category,
      });
    }
  }
}

// Global analytics instance
export const analytics = new AnalyticsService();

// Extend Window interface
declare global {
  interface Window {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    dataLayer: any[];
    gtag?: (...args: any[]) => void;
  }
}
