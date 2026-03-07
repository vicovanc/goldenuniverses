import { useState, useCallback, useRef, useEffect } from 'react';
import { useSettings } from '@/contexts/SettingsContext';

export interface TooltipPosition {
  top: number;
  left: number;
}

export function useTooltip() {
  const { preferences } = useSettings();
  const [isVisible, setIsVisible] = useState(false);
  const [content, setContent] = useState<string>('');
  const [position, setPosition] = useState<TooltipPosition>({ top: 0, left: 0 });
  const timeoutRef = useRef<number>();

  const show = useCallback(
    (tooltipContent: string, element: HTMLElement) => {
      if (!preferences.showTooltips) return;

      const rect = element.getBoundingClientRect();
      setContent(tooltipContent);
      setPosition({
        top: rect.top - 40,
        left: rect.left + rect.width / 2,
      });

      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }

      timeoutRef.current = setTimeout(() => {
        setIsVisible(true);
      }, 500);
    },
    [preferences.showTooltips]
  );

  const hide = useCallback(() => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    setIsVisible(false);
  }, []);

  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  return {
    isVisible,
    content,
    position,
    show,
    hide,
    enabled: preferences.showTooltips,
  };
}
