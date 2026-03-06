import { useEffect, useCallback, useRef } from 'react';
import { useSettings } from '@/contexts/SettingsContext';

export function useFocusManagement() {
  const { preferences } = useSettings();
  const focusableElements = useRef<HTMLElement[]>([]);

  const getFocusableElements = useCallback(() => {
    const selector = [
      'a[href]',
      'button:not([disabled])',
      'textarea:not([disabled])',
      'input:not([disabled])',
      'select:not([disabled])',
      '[tabindex]:not([tabindex="-1"])',
    ].join(',');

    return Array.from(document.querySelectorAll<HTMLElement>(selector)).filter(
      (el) => !el.hasAttribute('aria-hidden')
    );
  }, []);

  const trapFocus = useCallback(
    (container: HTMLElement) => {
      const focusable = container.querySelectorAll<HTMLElement>(
        'a[href], button:not([disabled]), textarea:not([disabled]), input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])'
      );

      if (focusable.length === 0) return;

      const firstFocusable = focusable[0];
      const lastFocusable = focusable[focusable.length - 1];

      const handleKeyDown = (e: KeyboardEvent) => {
        if (e.key !== 'Tab') return;

        if (e.shiftKey) {
          if (document.activeElement === firstFocusable) {
            e.preventDefault();
            lastFocusable.focus();
          }
        } else {
          if (document.activeElement === lastFocusable) {
            e.preventDefault();
            firstFocusable.focus();
          }
        }
      };

      container.addEventListener('keydown', handleKeyDown);
      firstFocusable.focus();

      return () => {
        container.removeEventListener('keydown', handleKeyDown);
      };
    },
    []
  );

  const restoreFocus = useCallback(() => {
    const lastFocused = document.activeElement as HTMLElement;
    return () => {
      if (lastFocused && lastFocused.focus) {
        lastFocused.focus();
      }
    };
  }, []);

  useEffect(() => {
    if (!preferences.keyboardNavigation) return;

    focusableElements.current = getFocusableElements();

    const handleKeyDown = (e: KeyboardEvent) => {
      // Skip if typing in input
      const target = e.target as HTMLElement;
      if (
        target.tagName === 'INPUT' ||
        target.tagName === 'TEXTAREA' ||
        target.isContentEditable
      ) {
        return;
      }

      // Handle arrow key navigation
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        const currentIndex = focusableElements.current.indexOf(
          document.activeElement as HTMLElement
        );
        if (currentIndex === -1) return;

        e.preventDefault();
        let nextIndex: number;

        if (e.key === 'ArrowDown') {
          nextIndex = (currentIndex + 1) % focusableElements.current.length;
        } else {
          nextIndex =
            currentIndex === 0
              ? focusableElements.current.length - 1
              : currentIndex - 1;
        }

        focusableElements.current[nextIndex]?.focus();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [preferences.keyboardNavigation, getFocusableElements]);

  return {
    trapFocus,
    restoreFocus,
    getFocusableElements,
  };
}
