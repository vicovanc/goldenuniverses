import { useEffect, useState, useRef } from 'react';
import {
  getConnectionInfo,
  isSlowConnection,
  prefersReducedMotion,
  getLoadingStrategy,
} from '@/utils/performance';

/**
 * Hook to monitor and adapt to connection quality
 */
export function useConnectionQuality() {
  const [connectionInfo, setConnectionInfo] = useState(getConnectionInfo());
  const [isSlow, setIsSlow] = useState(isSlowConnection());

  useEffect(() => {
    const updateConnectionInfo = () => {
      setConnectionInfo(getConnectionInfo());
      setIsSlow(isSlowConnection());
    };

    const connection =
      (navigator as any).connection ||
      (navigator as any).mozConnection ||
      (navigator as any).webkitConnection;

    if (connection) {
      connection.addEventListener('change', updateConnectionInfo);
      return () => {
        connection.removeEventListener('change', updateConnectionInfo);
      };
    }
  }, []);

  return { connectionInfo, isSlow };
}

/**
 * Hook to detect if user prefers reduced motion
 */
export function useReducedMotion(): boolean {
  const [reducedMotion, setReducedMotion] = useState(prefersReducedMotion());

  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    const handler = (event: MediaQueryListEvent) => {
      setReducedMotion(event.matches);
    };

    mediaQuery.addEventListener('change', handler);
    return () => {
      mediaQuery.removeEventListener('change', handler);
    };
  }, []);

  return reducedMotion;
}

/**
 * Hook to get adaptive loading strategy
 */
export function useAdaptiveLoading() {
  const { isSlow } = useConnectionQuality();
  const reducedMotion = useReducedMotion();
  const [strategy] = useState(() => getLoadingStrategy());

  return {
    ...strategy,
    isSlow,
    reducedMotion,
  };
}

/**
 * Hook to measure component render performance
 */
export function useRenderTime(componentName: string) {
  const renderCount = useRef(0);

  useEffect(() => {
    renderCount.current++;
  });

  const startTime = useRef(performance.now());

  useEffect(() => {
    const endTime = performance.now();
    const renderTime = endTime - startTime.current;
    console.log(
      `[Performance] ${componentName} render #${renderCount.current}: ${renderTime.toFixed(2)}ms`
    );
    startTime.current = endTime;
  });
}

/**
 * Hook to detect visibility and pause updates when hidden
 */
export function usePageVisibility() {
  const [isVisible, setIsVisible] = useState(!document.hidden);

  useEffect(() => {
    const handleVisibilityChange = () => {
      setIsVisible(!document.hidden);
    };

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, []);

  return isVisible;
}

/**
 * Hook for idle callback
 */
export function useIdleCallback(callback: () => void, options?: IdleRequestOptions) {
  useEffect(() => {
    if ('requestIdleCallback' in window) {
      const id = window.requestIdleCallback(callback, options);
      return () => {
        window.cancelIdleCallback(id);
      };
    } else {
      const timeout = setTimeout(callback, 1);
      return () => {
        clearTimeout(timeout);
      };
    }
  }, [callback, options]);
}

/**
 * Hook to track intersection and lazy load
 */
export function useIntersectionObserver(
  elementRef: React.RefObject<Element>,
  options?: IntersectionObserverInit
): boolean {
  const [isIntersecting, setIsIntersecting] = useState(false);

  useEffect(() => {
    const element = elementRef.current;
    if (!element) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        setIsIntersecting(entry.isIntersecting);
      },
      { threshold: 0.1, ...options }
    );

    observer.observe(element);

    return () => {
      observer.disconnect();
    };
  }, [elementRef, options]);

  return isIntersecting;
}

/**
 * Hook to prefetch data/resources
 */
export function usePrefetch<T>(
  fetcher: () => Promise<T>,
  enabled: boolean = true
): { data: T | null; loading: boolean; error: Error | null } {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    if (!enabled) return;

    let cancelled = false;

    const prefetch = async () => {
      setLoading(true);
      try {
        const result = await fetcher();
        if (!cancelled) {
          setData(result);
          setError(null);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err as Error);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };

    // Use requestIdleCallback if available
    if ('requestIdleCallback' in window) {
      const id = window.requestIdleCallback(() => prefetch());
      return () => {
        cancelled = true;
        window.cancelIdleCallback(id);
      };
    } else {
      prefetch();
      return () => {
        cancelled = true;
      };
    }
  }, [fetcher, enabled]);

  return { data, loading, error };
}

/**
 * Hook to batch state updates
 */
export function useBatchedState<T>(initialValue: T): [T, (value: T) => void] {
  const [state, setState] = useState(initialValue);
  const rafIdRef = useRef<number | null>(null);
  const nextValueRef = useRef<T>(initialValue);

  const setBatchedState = (value: T) => {
    nextValueRef.current = value;

    if (rafIdRef.current !== null) {
      return;
    }

    rafIdRef.current = requestAnimationFrame(() => {
      setState(nextValueRef.current);
      rafIdRef.current = null;
    });
  };

  useEffect(() => {
    return () => {
      if (rafIdRef.current !== null) {
        cancelAnimationFrame(rafIdRef.current);
      }
    };
  }, []);

  return [state, setBatchedState];
}
