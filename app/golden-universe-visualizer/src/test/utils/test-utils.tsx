import { ReactElement, ReactNode } from 'react';
import { render, RenderOptions, RenderResult } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { UXProvider } from '@/components/UXEnhancements/UXProvider';

/**
 * All providers used in the app for testing
 */
interface AllProvidersProps {
  children: ReactNode;
}

export const AllProviders = ({ children }: AllProvidersProps) => {
  return (
    <BrowserRouter>
      <UXProvider>{children}</UXProvider>
    </BrowserRouter>
  );
};

/**
 * Custom render function that includes all providers
 */
export const renderWithProviders = (
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
): RenderResult => {
  return render(ui, { wrapper: AllProviders, ...options });
};

/**
 * Router-only wrapper for components that only need routing
 */
export const RouterWrapper = ({ children }: { children: ReactNode }) => {
  return <BrowserRouter>{children}</BrowserRouter>;
};

/**
 * Custom render with router only
 */
export const renderWithRouter = (
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
): RenderResult => {
  return render(ui, { wrapper: RouterWrapper, ...options });
};

/**
 * Wait for async operations with timeout
 */
export const waitForAsync = (ms: number = 100): Promise<void> => {
  return new Promise((resolve) => setTimeout(resolve, ms));
};

/**
 * Create mock IntersectionObserver entry
 */
export const createMockIntersectionObserverEntry = (
  isIntersecting: boolean = true
): IntersectionObserverEntry => {
  return {
    isIntersecting,
    intersectionRatio: isIntersecting ? 1 : 0,
    boundingClientRect: {} as DOMRectReadOnly,
    intersectionRect: {} as DOMRectReadOnly,
    rootBounds: {} as DOMRectReadOnly,
    target: document.createElement('div'),
    time: Date.now(),
  };
};

/**
 * Create mock resize observer entry
 */
export const createMockResizeObserverEntry = (
  width: number = 1024,
  height: number = 768
): ResizeObserverEntry => {
  return {
    target: document.createElement('div'),
    contentRect: {
      width,
      height,
      top: 0,
      left: 0,
      bottom: height,
      right: width,
      x: 0,
      y: 0,
      toJSON: () => ({}),
    },
    borderBoxSize: [] as any,
    contentBoxSize: [] as any,
    devicePixelContentBoxSize: [] as any,
  };
};

/**
 * Mock fetch response
 */
export const mockFetch = (data: any, ok: boolean = true, status: number = 200) => {
  global.fetch = vi.fn(() =>
    Promise.resolve({
      ok,
      status,
      json: () => Promise.resolve(data),
      text: () => Promise.resolve(JSON.stringify(data)),
      blob: () => Promise.resolve(new Blob([JSON.stringify(data)])),
      arrayBuffer: () => Promise.resolve(new ArrayBuffer(0)),
      formData: () => Promise.resolve(new FormData()),
      headers: new Headers(),
      redirected: false,
      statusText: ok ? 'OK' : 'Error',
      type: 'basic' as ResponseType,
      url: '',
      clone: () => ({} as Response),
      body: null,
      bodyUsed: false,
    } as Response)
  ) as any;
};

/**
 * Reset fetch mock
 */
export const resetFetchMock = () => {
  if (global.fetch && vi.isMockFunction(global.fetch)) {
    (global.fetch as any).mockRestore();
  }
};

/**
 * Create a mock file
 */
export const createMockFile = (
  name: string = 'test.txt',
  content: string = 'test content',
  type: string = 'text/plain'
): File => {
  const blob = new Blob([content], { type });
  return new File([blob], name, { type });
};

/**
 * Trigger window resize event
 */
export const triggerWindowResize = (width: number = 1024, height: number = 768) => {
  Object.defineProperty(window, 'innerWidth', {
    writable: true,
    configurable: true,
    value: width,
  });
  Object.defineProperty(window, 'innerHeight', {
    writable: true,
    configurable: true,
    value: height,
  });
  window.dispatchEvent(new Event('resize'));
};

/**
 * Mock console methods for testing
 */
export const mockConsole = () => {
  const originalConsole = { ...console };
  console.log = vi.fn();
  console.warn = vi.fn();
  console.error = vi.fn();
  console.info = vi.fn();

  return {
    restore: () => {
      console.log = originalConsole.log;
      console.warn = originalConsole.warn;
      console.error = originalConsole.error;
      console.info = originalConsole.info;
    },
  };
};

// Re-export testing library utilities
export * from '@testing-library/react';
export { default as userEvent } from '@testing-library/user-event';
