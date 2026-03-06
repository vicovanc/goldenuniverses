import React, { lazy, Suspense, ComponentType } from 'react';

interface LazyLoadOptions {
  fallback?: React.ReactNode;
  delay?: number;
  preload?: boolean;
}

/**
 * Loading fallback component
 */
const DefaultLoader: React.FC = () => (
  <div className="lazy-loader">
    <div className="lazy-loader__spinner"></div>
    <p className="lazy-loader__text">Loading...</p>
  </div>
);

/**
 * Error boundary for lazy-loaded components
 */
class LazyErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean; error: Error | null }
> {
  constructor(props: { children: React.ReactNode }) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('[LazyLoad] Error loading component:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="lazy-error">
          <h2>Failed to load component</h2>
          <p>{this.state.error?.message}</p>
          <button onClick={() => window.location.reload()}>Reload Page</button>
        </div>
      );
    }

    return this.props.children;
  }
}

/**
 * Enhanced lazy loading with retry logic
 */
export function lazyLoadWithRetry<T extends ComponentType<any>>(
  importFunc: () => Promise<{ default: T }>,
  options: LazyLoadOptions = {}
): React.LazyExoticComponent<T> {
  const { delay = 0 } = options;

  return lazy(() => {
    return new Promise<{ default: T }>((resolve, reject) => {
      const attemptImport = async (retryCount = 0): Promise<void> => {
        try {
          // Add artificial delay if specified
          if (delay > 0) {
            await new Promise((r) => setTimeout(r, delay));
          }

          const module = await importFunc();
          resolve(module);
        } catch (error) {
          // Retry up to 3 times with exponential backoff
          if (retryCount < 3) {
            const backoffDelay = Math.pow(2, retryCount) * 1000;
            console.warn(
              `[LazyLoad] Retry ${retryCount + 1}/3 after ${backoffDelay}ms`,
              error
            );
            setTimeout(() => attemptImport(retryCount + 1), backoffDelay);
          } else {
            console.error('[LazyLoad] Failed after 3 retries', error);
            reject(error);
          }
        }
      };

      attemptImport();
    });
  });
}

/**
 * Wrapper component for lazy-loaded components
 */
export function LazyLoad<P extends object>(
  Component: React.LazyExoticComponent<ComponentType<P>>,
  options: LazyLoadOptions = {}
): React.FC<P> {
  const { fallback = <DefaultLoader /> } = options;

  return (props: P) => (
    <LazyErrorBoundary>
      <Suspense fallback={fallback}>{React.createElement(Component, props)}</Suspense>
    </LazyErrorBoundary>
  );
}

/**
 * Preload a lazy-loaded component
 */
export function preloadComponent<T extends ComponentType<any>>(
  LazyComponent: React.LazyExoticComponent<T>
): void {
  // Trigger the import by calling the internal _ctor
  const component = LazyComponent as any;
  if (component._ctor) {
    component._ctor();
  }
}

/**
 * HOC to add intersection observer for lazy loading
 */
export function withIntersectionObserver<P extends object>(
  Component: ComponentType<P>,
  options: IntersectionObserverInit = {}
): React.FC<P> {
  return (props: P) => {
    const [isVisible, setIsVisible] = React.useState(false);
    const ref = React.useRef<HTMLDivElement>(null);

    React.useEffect(() => {
      const observer = new IntersectionObserver(
        ([entry]) => {
          if (entry.isIntersecting) {
            setIsVisible(true);
            observer.disconnect();
          }
        },
        { threshold: 0.1, ...options }
      );

      if (ref.current) {
        observer.observe(ref.current);
      }

      return () => {
        observer.disconnect();
      };
    }, []);

    return (
      <div ref={ref}>
        {isVisible ? <Component {...props} /> : <DefaultLoader />}
      </div>
    );
  };
}
