import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import {
  PHI,
  fibonacci,
  fibonacciRatio,
  formatNumber,
  goldenRectangle,
  debounce,
  throttle,
  isValidNumber,
  clamp,
  lerp,
} from '../helpers';

describe('helpers', () => {
  describe('PHI constant', () => {
    it('should equal the golden ratio', () => {
      expect(PHI).toBeCloseTo(1.618033988749895, 10);
    });

    it('should satisfy the golden ratio equation', () => {
      // φ² = φ + 1
      expect(PHI * PHI).toBeCloseTo(PHI + 1, 10);
    });
  });

  describe('fibonacci', () => {
    it('should return 0 for n=0', () => {
      expect(fibonacci(0)).toBe(0);
    });

    it('should return 1 for n=1', () => {
      expect(fibonacci(1)).toBe(1);
    });

    it('should calculate correct Fibonacci numbers', () => {
      expect(fibonacci(2)).toBe(1);
      expect(fibonacci(3)).toBe(2);
      expect(fibonacci(4)).toBe(3);
      expect(fibonacci(5)).toBe(5);
      expect(fibonacci(6)).toBe(8);
      expect(fibonacci(7)).toBe(13);
      expect(fibonacci(10)).toBe(55);
    });
  });

  describe('fibonacciRatio', () => {
    it('should return 0 for n <= 1', () => {
      expect(fibonacciRatio(0)).toBe(0);
      expect(fibonacciRatio(1)).toBe(0);
    });

    it('should approach golden ratio for large n', () => {
      // As n increases, the ratio approaches φ
      const ratio = fibonacciRatio(20);
      expect(ratio).toBeCloseTo(PHI, 5);
    });

    it('should calculate ratios correctly', () => {
      expect(fibonacciRatio(2)).toBe(1);
      expect(fibonacciRatio(3)).toBe(2);
      expect(fibonacciRatio(4)).toBeCloseTo(1.5, 10);
    });
  });

  describe('formatNumber', () => {
    it('should format to 2 decimals by default', () => {
      expect(formatNumber(3.14159)).toBe('3.14');
      expect(formatNumber(1.618033)).toBe('1.62');
    });

    it('should format to specified decimals', () => {
      expect(formatNumber(PHI, 5)).toBe('1.61803');
      expect(formatNumber(PHI, 10)).toBe('1.6180339887');
    });

    it('should handle integers', () => {
      expect(formatNumber(42)).toBe('42.00');
      expect(formatNumber(42, 0)).toBe('42');
    });
  });

  describe('goldenRectangle', () => {
    it('should calculate golden rectangle dimensions', () => {
      const rect = goldenRectangle(100);
      expect(rect.width).toBe(100);
      expect(rect.height).toBeCloseTo(61.803398875, 5);
    });

    it('should maintain golden ratio', () => {
      const rect = goldenRectangle(1000);
      expect(rect.width / rect.height).toBeCloseTo(PHI, 10);
    });
  });

  describe('debounce', () => {
    beforeEach(() => {
      vi.useFakeTimers();
    });

    afterEach(() => {
      vi.restoreAllMocks();
    });

    it('should debounce function calls', () => {
      const mockFn = vi.fn();
      const debouncedFn = debounce(mockFn, 100);

      debouncedFn();
      debouncedFn();
      debouncedFn();

      expect(mockFn).not.toHaveBeenCalled();

      vi.advanceTimersByTime(100);

      expect(mockFn).toHaveBeenCalledTimes(1);
    });

    it('should pass arguments correctly', () => {
      const mockFn = vi.fn();
      const debouncedFn = debounce(mockFn, 100);

      debouncedFn('test', 123);
      vi.advanceTimersByTime(100);

      expect(mockFn).toHaveBeenCalledWith('test', 123);
    });

    it('should reset timer on subsequent calls', () => {
      const mockFn = vi.fn();
      const debouncedFn = debounce(mockFn, 100);

      debouncedFn();
      vi.advanceTimersByTime(50);
      debouncedFn();
      vi.advanceTimersByTime(50);

      expect(mockFn).not.toHaveBeenCalled();

      vi.advanceTimersByTime(50);
      expect(mockFn).toHaveBeenCalledTimes(1);
    });
  });

  describe('throttle', () => {
    beforeEach(() => {
      vi.useFakeTimers();
    });

    afterEach(() => {
      vi.restoreAllMocks();
    });

    it('should throttle function calls', () => {
      const mockFn = vi.fn();
      const throttledFn = throttle(mockFn, 100);

      throttledFn();
      throttledFn();
      throttledFn();

      expect(mockFn).toHaveBeenCalledTimes(1);

      vi.advanceTimersByTime(100);
      throttledFn();

      expect(mockFn).toHaveBeenCalledTimes(2);
    });

    it('should pass arguments correctly', () => {
      const mockFn = vi.fn();
      const throttledFn = throttle(mockFn, 100);

      throttledFn('test', 456);

      expect(mockFn).toHaveBeenCalledWith('test', 456);
    });
  });

  describe('isValidNumber', () => {
    it('should return true for valid numbers', () => {
      expect(isValidNumber(0)).toBe(true);
      expect(isValidNumber(42)).toBe(true);
      expect(isValidNumber(-10)).toBe(true);
      expect(isValidNumber(3.14)).toBe(true);
      expect(isValidNumber(PHI)).toBe(true);
    });

    it('should return false for invalid values', () => {
      expect(isValidNumber(NaN)).toBe(false);
      expect(isValidNumber(Infinity)).toBe(false);
      expect(isValidNumber(-Infinity)).toBe(false);
      expect(isValidNumber('42')).toBe(false);
      expect(isValidNumber(null)).toBe(false);
      expect(isValidNumber(undefined)).toBe(false);
      expect(isValidNumber({})).toBe(false);
    });
  });

  describe('clamp', () => {
    it('should clamp value between min and max', () => {
      expect(clamp(5, 0, 10)).toBe(5);
      expect(clamp(-5, 0, 10)).toBe(0);
      expect(clamp(15, 0, 10)).toBe(10);
    });

    it('should handle edge cases', () => {
      expect(clamp(0, 0, 10)).toBe(0);
      expect(clamp(10, 0, 10)).toBe(10);
    });

    it('should work with negative ranges', () => {
      expect(clamp(-5, -10, 0)).toBe(-5);
      expect(clamp(-15, -10, 0)).toBe(-10);
      expect(clamp(5, -10, 0)).toBe(0);
    });
  });

  describe('lerp', () => {
    it('should interpolate between two values', () => {
      expect(lerp(0, 10, 0)).toBe(0);
      expect(lerp(0, 10, 0.5)).toBe(5);
      expect(lerp(0, 10, 1)).toBe(10);
    });

    it('should work with negative values', () => {
      expect(lerp(-10, 10, 0.5)).toBe(0);
      expect(lerp(-10, 10, 0.25)).toBe(-5);
      expect(lerp(-10, 10, 0.75)).toBe(5);
    });

    it('should extrapolate outside 0-1 range', () => {
      expect(lerp(0, 10, 1.5)).toBe(15);
      expect(lerp(0, 10, -0.5)).toBe(-5);
    });
  });
});
