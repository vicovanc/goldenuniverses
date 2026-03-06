import { useEffect, useCallback } from 'react';
import { useSettings } from '@/contexts/SettingsContext';
import introJs from 'intro.js';
import 'intro.js/introjs.css';

export interface TourStep {
  element: string;
  intro: string;
  position?: 'top' | 'right' | 'bottom' | 'left';
}

export function useGuidedTour() {
  const { preferences, updatePreferences } = useSettings();

  const startTour = useCallback(
    (steps: TourStep[]) => {
      const intro = introJs();

      intro.setOptions({
        steps: steps.map((step) => ({
          element: step.element,
          intro: step.intro,
          position: step.position || 'bottom',
        })),
        showProgress: true,
        showBullets: false,
        exitOnOverlayClick: false,
        doneLabel: 'Done',
        nextLabel: 'Next',
        prevLabel: 'Back',
        skipLabel: 'Skip',
      });

      intro.oncomplete(() => {
        updatePreferences({ hasCompletedTour: true });
      });

      intro.onexit(() => {
        updatePreferences({ hasCompletedTour: true });
      });

      intro.start();
    },
    [updatePreferences]
  );

  const resetTour = useCallback(() => {
    updatePreferences({ hasCompletedTour: false });
  }, [updatePreferences]);

  useEffect(() => {
    // Auto-start tour on first visit - DISABLED for now
    if (false && !preferences.hasCompletedTour && preferences.showHelpHints) {
      const timer = setTimeout(() => {
        const defaultSteps: TourStep[] = [
          {
            element: 'body',
            intro:
              'Welcome to Golden Universe Visualizer! This tour will guide you through the main features.',
          },
          {
            element: '[data-tour="navigation"]',
            intro: 'Use the navigation menu to explore different sections of the application.',
            position: 'right',
          },
          {
            element: '[data-tour="search"]',
            intro:
              'Use the search bar to quickly find theories, calculations, and visualizations. Press "/" or Cmd+K to focus.',
            position: 'bottom',
          },
          {
            element: '[data-tour="settings"]',
            intro:
              'Access settings to customize your experience, including theme, visualizations, and accessibility options.',
            position: 'left',
          },
          {
            element: '[data-tour="keyboard-shortcuts"]',
            intro: 'Press "?" to see all available keyboard shortcuts.',
            position: 'left',
          },
        ];

        startTour(defaultSteps);
      }, 1000);

      return () => clearTimeout(timer);
    }
  }, [preferences.hasCompletedTour, preferences.showHelpHints, startTour]);

  return {
    startTour,
    resetTour,
    hasCompletedTour: preferences.hasCompletedTour,
  };
}
