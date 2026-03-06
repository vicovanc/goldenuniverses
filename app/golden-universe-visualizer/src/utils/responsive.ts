/**
 * Responsive utility functions and constants
 */

// Breakpoint values (in pixels)
export const BREAKPOINTS = {
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
  '2xl': 1536,
} as const;

// Touch target minimum size (for accessibility)
export const TOUCH_TARGET_SIZE = {
  min: 48, // px - WCAG 2.1 AA standard
  recommended: 56, // px - Material Design recommendation
} as const;

/**
 * Check if device is likely mobile based on screen width
 */
export function isMobileDevice(): boolean {
  if (typeof window === 'undefined') return false;
  return window.innerWidth < BREAKPOINTS.sm;
}

/**
 * Check if device is likely tablet based on screen width
 */
export function isTabletDevice(): boolean {
  if (typeof window === 'undefined') return false;
  return window.innerWidth >= BREAKPOINTS.sm && window.innerWidth < BREAKPOINTS.lg;
}

/**
 * Check if device is likely desktop based on screen width
 */
export function isDesktopDevice(): boolean {
  if (typeof window === 'undefined') return false;
  return window.innerWidth >= BREAKPOINTS.lg;
}

/**
 * Check if device supports touch
 */
export function isTouchDevice(): boolean {
  if (typeof window === 'undefined') return false;
  return (
    'ontouchstart' in window ||
    navigator.maxTouchPoints > 0 ||
    (navigator as any).msMaxTouchPoints > 0
  );
}

/**
 * Get viewport dimensions
 */
export function getViewportDimensions() {
  if (typeof window === 'undefined') {
    return { width: 0, height: 0 };
  }
  return {
    width: window.innerWidth,
    height: window.innerHeight,
  };
}

/**
 * Debounce function for resize events
 */
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout | null = null;

  return function executedFunction(...args: Parameters<T>) {
    const later = () => {
      timeout = null;
      func(...args);
    };

    if (timeout) {
      clearTimeout(timeout);
    }
    timeout = setTimeout(later, wait);
  };
}

/**
 * Throttle function for scroll/touch events
 */
export function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean;

  return function executedFunction(...args: Parameters<T>) {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

/**
 * Calculate responsive font size
 */
export function getResponsiveFontSize(
  baseSizePx: number,
  minSizePx: number = baseSizePx * 0.75,
  maxSizePx: number = baseSizePx * 1.25
): string {
  return `clamp(${minSizePx}px, ${baseSizePx}px + 0.5vw, ${maxSizePx}px)`;
}

/**
 * Calculate responsive spacing
 */
export function getResponsiveSpacing(baseRem: number): string {
  return `clamp(${baseRem * 0.5}rem, ${baseRem}rem, ${baseRem * 1.5}rem)`;
}
