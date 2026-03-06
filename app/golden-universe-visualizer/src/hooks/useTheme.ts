import { useEffect, useState, useCallback } from 'react';
import { useSettings } from '@/contexts/SettingsContext';

type ResolvedTheme = 'light' | 'dark';

export function useTheme() {
  const { preferences, updatePreferences } = useSettings();
  const [resolvedTheme, setResolvedTheme] = useState<ResolvedTheme>('dark');

  const getSystemTheme = useCallback((): ResolvedTheme => {
    if (typeof window === 'undefined') return 'dark';
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }, []);

  const resolveTheme = useCallback((): ResolvedTheme => {
    if (preferences.theme === 'system') {
      return getSystemTheme();
    }
    return preferences.theme;
  }, [preferences.theme, getSystemTheme]);

  useEffect(() => {
    const newResolvedTheme = resolveTheme();
    setResolvedTheme(newResolvedTheme);

    // Apply theme to document
    document.documentElement.setAttribute('data-theme', newResolvedTheme);
    document.documentElement.classList.remove('light', 'dark');
    document.documentElement.classList.add(newResolvedTheme);
  }, [resolveTheme]);

  useEffect(() => {
    if (preferences.theme !== 'system') return;

    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = () => {
      const newTheme = getSystemTheme();
      setResolvedTheme(newTheme);
      document.documentElement.setAttribute('data-theme', newTheme);
      document.documentElement.classList.remove('light', 'dark');
      document.documentElement.classList.add(newTheme);
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [preferences.theme, getSystemTheme]);

  const toggleTheme = useCallback(() => {
    const currentResolved = resolveTheme();
    const newTheme = currentResolved === 'dark' ? 'light' : 'dark';
    updatePreferences({ theme: newTheme });
  }, [resolveTheme, updatePreferences]);

  const setTheme = useCallback(
    (theme: 'light' | 'dark' | 'system') => {
      updatePreferences({ theme });
    },
    [updatePreferences]
  );

  return {
    theme: preferences.theme,
    resolvedTheme,
    toggleTheme,
    setTheme,
  };
}
