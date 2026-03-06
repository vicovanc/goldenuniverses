import React, { ReactNode, useEffect } from 'react';
import { Toaster } from 'react-hot-toast';
import { KeyboardShortcutsProvider } from '@/contexts/KeyboardShortcutsContext';
import { SettingsProvider, useSettings } from '@/contexts/SettingsContext';
import { SkipLinks } from '@/components/Accessibility/SkipLinks';
import { useKeyboardShortcuts } from '@/hooks/useKeyboardShortcuts';
import { useKeyboardShortcutsContext } from '@/contexts/KeyboardShortcutsContext';
import { useTheme } from '@/hooks/useTheme';
import { useGuidedTour } from '@/hooks/useGuidedTour';
import { useAnnouncer } from '@/hooks/useAnnouncer';
import type { KeyboardShortcut } from '@/types/keyboard';
import { useNavigate } from 'react-router-dom';

function UXEnhancementsInner({ children }: { children: ReactNode }) {
  const { preferences } = useSettings();
  const { toggleShortcutsModal, registerShortcut } = useKeyboardShortcutsContext();
  const { toggleTheme } = useTheme();
  const { startTour } = useGuidedTour();
  const { announce } = useAnnouncer();
  const navigate = useNavigate();

  // Apply accessibility preferences to document
  useEffect(() => {
    const root = document.documentElement;

    // Font size
    root.setAttribute('data-font-size', preferences.fontSize);

    // High contrast
    root.setAttribute('data-high-contrast', preferences.highContrast.toString());

    // Reduced motion
    root.setAttribute('data-reduced-motion', preferences.reducedMotion.toString());

    // Focus indicators
    root.setAttribute('data-focus-indicators', preferences.focusIndicators.toString());

    // Track mouse usage for focus indicators
    let isUsingMouse = false;
    const handleMouseDown = () => {
      isUsingMouse = true;
      document.body.classList.add('using-mouse');
    };
    const handleKeyDown = () => {
      isUsingMouse = false;
      document.body.classList.remove('using-mouse');
    };

    document.addEventListener('mousedown', handleMouseDown);
    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('mousedown', handleMouseDown);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [preferences]);

  // Register global keyboard shortcuts
  const shortcuts: KeyboardShortcut[] = [
    {
      key: '?',
      shiftKey: true,
      description: 'Show keyboard shortcuts',
      action: toggleShortcutsModal,
      category: 'general',
    },
    {
      key: 'Escape',
      description: 'Close modal or dialog',
      action: () => {
        // This will be handled by individual modals
        announce('Dialog closed', 'polite');
      },
      category: 'general',
    },
    {
      key: 't',
      ctrlKey: true,
      description: 'Toggle theme',
      action: () => {
        toggleTheme();
        announce('Theme toggled', 'polite');
      },
      category: 'ui',
    },
    {
      key: 'k',
      metaKey: true,
      description: 'Open search',
      action: () => {
        const searchInput = document.querySelector<HTMLInputElement>('[data-tour="search"]');
        if (searchInput) {
          searchInput.focus();
          announce('Search opened', 'polite');
        }
      },
      category: 'search',
    },
    {
      key: '/',
      description: 'Focus search',
      action: () => {
        const searchInput = document.querySelector<HTMLInputElement>('[data-tour="search"]');
        if (searchInput) {
          searchInput.focus();
          announce('Search focused', 'polite');
        }
      },
      category: 'search',
    },
    {
      key: 'h',
      description: 'Go to home',
      action: () => {
        navigate('/');
        announce('Navigated to home', 'polite');
      },
      category: 'navigation',
    },
    {
      key: '1',
      altKey: true,
      description: 'Go to Theory',
      action: () => {
        navigate('/theory');
        announce('Navigated to theory section', 'polite');
      },
      category: 'navigation',
    },
    {
      key: '2',
      altKey: true,
      description: 'Go to Derivations',
      action: () => {
        navigate('/derivations');
        announce('Navigated to derivations section', 'polite');
      },
      category: 'navigation',
    },
    {
      key: '3',
      altKey: true,
      description: 'Go to Calculations',
      action: () => {
        navigate('/calculations');
        announce('Navigated to calculations section', 'polite');
      },
      category: 'navigation',
    },
    {
      key: '4',
      altKey: true,
      description: 'Go to Visualizations',
      action: () => {
        navigate('/visualizations');
        announce('Navigated to visualizations section', 'polite');
      },
      category: 'navigation',
    },
  ];

  useKeyboardShortcuts(shortcuts, {
    enabled: preferences.keyboardNavigation,
  });

  // Register shortcuts with context for display
  useEffect(() => {
    shortcuts.forEach((shortcut) => registerShortcut(shortcut));
  }, [registerShortcut]);

  return (
    <>
      <SkipLinks />
      {children}
      <Toaster
        position="top-right"
        toastOptions={{
          duration: preferences.notificationDuration,
          style: {
            background: 'var(--color-surface-elevated, #2a2a2a)',
            color: 'var(--color-text-primary, #fff)',
            border: '1px solid var(--color-border, #444)',
          },
        }}
      />
    </>
  );
}

export function UXProvider({ children }: { children: ReactNode }) {
  return (
    <SettingsProvider>
      <KeyboardShortcutsProvider>
        <UXEnhancementsInner>{children}</UXEnhancementsInner>
      </KeyboardShortcutsProvider>
    </SettingsProvider>
  );
}
