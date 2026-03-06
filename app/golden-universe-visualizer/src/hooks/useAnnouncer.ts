import { useEffect, useRef, useCallback } from 'react';
import { useSettings } from '@/contexts/SettingsContext';

type AnnouncementPriority = 'polite' | 'assertive';

export function useAnnouncer() {
  const { preferences } = useSettings();
  const politeRef = useRef<HTMLDivElement | null>(null);
  const assertiveRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    // Create screen reader announcement containers
    if (!politeRef.current) {
      politeRef.current = document.createElement('div');
      politeRef.current.setAttribute('role', 'status');
      politeRef.current.setAttribute('aria-live', 'polite');
      politeRef.current.setAttribute('aria-atomic', 'true');
      politeRef.current.className = 'sr-only';
      document.body.appendChild(politeRef.current);
    }

    if (!assertiveRef.current) {
      assertiveRef.current = document.createElement('div');
      assertiveRef.current.setAttribute('role', 'alert');
      assertiveRef.current.setAttribute('aria-live', 'assertive');
      assertiveRef.current.setAttribute('aria-atomic', 'true');
      assertiveRef.current.className = 'sr-only';
      document.body.appendChild(assertiveRef.current);
    }

    return () => {
      if (politeRef.current) {
        document.body.removeChild(politeRef.current);
        politeRef.current = null;
      }
      if (assertiveRef.current) {
        document.body.removeChild(assertiveRef.current);
        assertiveRef.current = null;
      }
    };
  }, []);

  const announce = useCallback(
    (message: string, priority: AnnouncementPriority = 'polite') => {
      if (!preferences.screenReaderMode) return;

      const container = priority === 'assertive' ? assertiveRef.current : politeRef.current;
      if (!container) return;

      // Clear existing message
      container.textContent = '';

      // Set new message after a brief delay to ensure screen readers catch the change
      setTimeout(() => {
        if (container) {
          container.textContent = message;
        }
      }, 100);
    },
    [preferences.screenReaderMode]
  );

  return { announce };
}
