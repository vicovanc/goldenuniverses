import React, { createContext, useContext, useCallback, ReactNode } from 'react';
import { useLocalStorage } from '@/hooks/useLocalStorage';
import type { UserPreferences, SettingsContextValue } from '@/types/settings';
import { DEFAULT_PREFERENCES } from '@/types/settings';
import toast from 'react-hot-toast';

const SettingsContext = createContext<SettingsContextValue | undefined>(undefined);

export function SettingsProvider({ children }: { children: ReactNode }) {
  const [preferences, setPreferences] = useLocalStorage<UserPreferences>(
    'golden-universe-preferences',
    DEFAULT_PREFERENCES
  );

  const updatePreferences = useCallback(
    (updates: Partial<UserPreferences>) => {
      setPreferences((prev) => ({
        ...prev,
        ...updates,
      }));
    },
    [setPreferences]
  );

  const resetPreferences = useCallback(() => {
    setPreferences(DEFAULT_PREFERENCES);
    toast.success('Settings reset to defaults');
  }, [setPreferences]);

  const exportSettings = useCallback(() => {
    return JSON.stringify(preferences, null, 2);
  }, [preferences]);

  const importSettings = useCallback(
    (json: string): boolean => {
      try {
        const imported = JSON.parse(json) as UserPreferences;

        // Validate that imported settings have the right structure
        const requiredKeys = Object.keys(DEFAULT_PREFERENCES);
        const hasAllKeys = requiredKeys.every((key) => key in imported);

        if (!hasAllKeys) {
          toast.error('Invalid settings file');
          return false;
        }

        setPreferences(imported);
        toast.success('Settings imported successfully');
        return true;
      } catch (error) {
        toast.error('Failed to import settings');
        console.error('Import settings error:', error);
        return false;
      }
    },
    [setPreferences]
  );

  const value: SettingsContextValue = {
    preferences,
    updatePreferences,
    resetPreferences,
    exportSettings,
    importSettings,
  };

  return <SettingsContext.Provider value={value}>{children}</SettingsContext.Provider>;
}

export function useSettings() {
  const context = useContext(SettingsContext);
  if (!context) {
    throw new Error('useSettings must be used within SettingsProvider');
  }
  return context;
}
