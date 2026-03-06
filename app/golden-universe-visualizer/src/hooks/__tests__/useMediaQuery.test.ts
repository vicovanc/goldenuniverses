import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import {
  useMediaQuery,
  useIsMobile,
  useIsTablet,
  useIsDesktop,
  useIsMobileOrTablet,
  useBreakpoint,
  useResponsiveValue,
} from '../useMediaQuery';

describe('useMediaQuery', () => {
  let matchMediaMock: any;

  beforeEach(() => {
    matchMediaMock = vi.fn().mockImplementation((query: string) => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    }));

    window.matchMedia = matchMediaMock;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('useMediaQuery', () => {
    it('should return false initially when query does not match', () => {
      matchMediaMock.mockImplementation(() => ({
        matches: false,
        media: '(max-width: 639px)',
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
      }));

      const { result } = renderHook(() => useMediaQuery('(max-width: 639px)'));
      expect(result.current).toBe(false);
    });

    it('should return true when query matches', () => {
      matchMediaMock.mockImplementation(() => ({
        matches: true,
        media: '(max-width: 639px)',
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
      }));

      const { result } = renderHook(() => useMediaQuery('(max-width: 639px)'));
      expect(result.current).toBe(true);
    });

    it('should update when media query changes', () => {
      let changeHandler: ((event: any) => void) | null = null;

      matchMediaMock.mockImplementation(() => ({
        matches: false,
        media: '(max-width: 639px)',
        addEventListener: vi.fn((event, handler) => {
          if (event === 'change') {
            changeHandler = handler;
          }
        }),
        removeEventListener: vi.fn(),
      }));

      const { result } = renderHook(() => useMediaQuery('(max-width: 639px)'));
      expect(result.current).toBe(false);

      // Simulate media query change
      act(() => {
        if (changeHandler) {
          changeHandler({ matches: true });
        }
      });

      expect(result.current).toBe(true);
    });

    it('should cleanup event listener on unmount', () => {
      const removeEventListener = vi.fn();
      matchMediaMock.mockImplementation(() => ({
        matches: false,
        media: '(max-width: 639px)',
        addEventListener: vi.fn(),
        removeEventListener,
      }));

      const { unmount } = renderHook(() => useMediaQuery('(max-width: 639px)'));
      unmount();

      expect(removeEventListener).toHaveBeenCalledWith('change', expect.any(Function));
    });

    it('should update when query changes', () => {
      matchMediaMock.mockImplementation((query: string) => ({
        matches: query === '(max-width: 639px)',
        media: query,
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
      }));

      const { result, rerender } = renderHook(({ query }) => useMediaQuery(query), {
        initialProps: { query: '(max-width: 639px)' },
      });

      expect(result.current).toBe(true);

      rerender({ query: '(min-width: 1024px)' });
      expect(result.current).toBe(false);
    });
  });

  describe('Breakpoint hooks', () => {
    it('useIsMobile should return true for mobile width', () => {
      matchMediaMock.mockImplementation((query: string) => ({
        matches: query === '(max-width: 639px)',
        media: query,
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
      }));

      const { result } = renderHook(() => useIsMobile());
      expect(result.current).toBe(true);
    });

    it('useIsTablet should return true for tablet width', () => {
      matchMediaMock.mockImplementation((query: string) => ({
        matches: query === '(min-width: 640px) and (max-width: 1023px)',
        media: query,
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
      }));

      const { result } = renderHook(() => useIsTablet());
      expect(result.current).toBe(true);
    });

    it('useIsDesktop should return true for desktop width', () => {
      matchMediaMock.mockImplementation((query: string) => ({
        matches: query === '(min-width: 1024px)',
        media: query,
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
      }));

      const { result } = renderHook(() => useIsDesktop());
      expect(result.current).toBe(true);
    });

    it('useIsMobileOrTablet should return true for mobile or tablet', () => {
      matchMediaMock.mockImplementation((query: string) => ({
        matches: query === '(max-width: 1023px)',
        media: query,
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
      }));

      const { result } = renderHook(() => useIsMobileOrTablet());
      expect(result.current).toBe(true);
    });
  });

  describe('useBreakpoint', () => {
    it('should return "mobile" for mobile width', () => {
      matchMediaMock.mockImplementation((query: string) => ({
        matches: query === '(max-width: 639px)',
        media: query,
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
      }));

      const { result } = renderHook(() => useBreakpoint());
      expect(result.current).toBe('mobile');
    });

    it('should return "tablet" for tablet width', () => {
      matchMediaMock.mockImplementation((query: string) => ({
        matches: query === '(min-width: 640px) and (max-width: 1023px)',
        media: query,
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
      }));

      const { result } = renderHook(() => useBreakpoint());
      expect(result.current).toBe('tablet');
    });

    it('should return "desktop" for desktop width', () => {
      matchMediaMock.mockImplementation((query: string) => ({
        matches: query === '(min-width: 1024px)' || query.includes('min-width: 1024px'),
        media: query,
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
      }));

      const { result } = renderHook(() => useBreakpoint());
      expect(result.current).toBe('desktop');
    });
  });

  describe('useResponsiveValue', () => {
    it('should return mobile value on mobile', () => {
      matchMediaMock.mockImplementation((query: string) => ({
        matches: query === '(max-width: 639px)',
        media: query,
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
      }));

      const { result } = renderHook(() =>
        useResponsiveValue({
          mobile: 'mobile-value',
          tablet: 'tablet-value',
          desktop: 'desktop-value',
        })
      );

      expect(result.current).toBe('mobile-value');
    });

    it('should return tablet value on tablet', () => {
      matchMediaMock.mockImplementation((query: string) => ({
        matches: query === '(min-width: 640px) and (max-width: 1023px)',
        media: query,
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
      }));

      const { result } = renderHook(() =>
        useResponsiveValue({
          mobile: 'mobile-value',
          tablet: 'tablet-value',
          desktop: 'desktop-value',
        })
      );

      expect(result.current).toBe('tablet-value');
    });

    it('should return desktop value on desktop', () => {
      matchMediaMock.mockImplementation((query: string) => ({
        matches: query === '(min-width: 1024px)' || query.includes('min-width: 1024px'),
        media: query,
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
      }));

      const { result } = renderHook(() =>
        useResponsiveValue({
          mobile: 'mobile-value',
          tablet: 'tablet-value',
          desktop: 'desktop-value',
        })
      );

      expect(result.current).toBe('desktop-value');
    });

    it('should fallback to desktop value when mobile/tablet not provided', () => {
      matchMediaMock.mockImplementation((query: string) => ({
        matches: query === '(max-width: 639px)',
        media: query,
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
      }));

      const { result } = renderHook(() =>
        useResponsiveValue({
          desktop: 'desktop-value',
        })
      );

      expect(result.current).toBe('desktop-value');
    });
  });
});
