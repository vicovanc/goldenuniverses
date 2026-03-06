import React from 'react';
import { useSettings } from '@/contexts/SettingsContext';
import { useTheme } from '@/hooks/useTheme';
import { useGuidedTour } from '@/hooks/useGuidedTour';
import { useAnnouncer } from '@/hooks/useAnnouncer';
import toast from 'react-hot-toast';

/**
 * Demo component showcasing all UX enhancement features
 * This component demonstrates:
 * - Settings management
 * - Theme toggling
 * - Guided tours
 * - Screen reader announcements
 * - Keyboard shortcuts
 * - Accessibility features
 */
export function UXDemo() {
  const { preferences, updatePreferences } = useSettings();
  const { theme, resolvedTheme, toggleTheme } = useTheme();
  const { startTour, hasCompletedTour } = useGuidedTour();
  const { announce } = useAnnouncer();

  const handleThemeToggle = () => {
    toggleTheme();
    announce(`Theme changed to ${resolvedTheme === 'dark' ? 'light' : 'dark'}`, 'polite');
    toast.success(`Theme changed to ${resolvedTheme === 'dark' ? 'light' : 'dark'}`);
  };

  const handleStartTour = () => {
    const demoSteps = [
      {
        element: '#ux-demo',
        intro: 'Welcome to the UX Demo! This showcases all the user experience enhancements.',
      },
      {
        element: '[data-tour="theme-toggle"]',
        intro: 'Toggle between light and dark themes here.',
        position: 'left' as const,
      },
      {
        element: '[data-tour="settings"]',
        intro: 'Open the settings panel to customize your experience.',
        position: 'left' as const,
      },
      {
        element: '[data-tour="keyboard-shortcuts"]',
        intro: 'View all available keyboard shortcuts.',
        position: 'left' as const,
      },
    ];
    startTour(demoSteps);
    announce('Starting guided tour', 'polite');
  };

  const handleToggleFeature = (feature: keyof typeof preferences) => {
    const newValue = !preferences[feature as keyof typeof preferences];
    updatePreferences({ [feature]: newValue } as any);
    announce(`${feature} ${newValue ? 'enabled' : 'disabled'}`, 'polite');
    toast.success(`${feature} ${newValue ? 'enabled' : 'disabled'}`);
  };

  return (
    <div id="ux-demo" style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
      <h2>UX Enhancements Demo</h2>
      <p>This demo showcases all the user experience features implemented in EPIC-010.</p>

      <section style={{ marginTop: '2rem' }}>
        <h3>Theme Management (GU-050)</h3>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <button onClick={handleThemeToggle} aria-label="Toggle theme">
            Toggle Theme
          </button>
          <span>
            Current: {theme} (Resolved: {resolvedTheme})
          </span>
        </div>
      </section>

      <section style={{ marginTop: '2rem' }}>
        <h3>Guided Tour (GU-048)</h3>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <button onClick={handleStartTour} aria-label="Start guided tour">
            Start Tour
          </button>
          <span>Tour completed: {hasCompletedTour ? 'Yes' : 'No'}</span>
        </div>
      </section>

      <section style={{ marginTop: '2rem' }}>
        <h3>Keyboard Shortcuts (GU-046)</h3>
        <p>Try these keyboard shortcuts:</p>
        <ul>
          <li>
            Press <kbd>?</kbd> to view all shortcuts
          </li>
          <li>
            Press <kbd>/</kbd> to focus search
          </li>
          <li>
            Press <kbd>Escape</kbd> to close modals
          </li>
          <li>
            Press <kbd>Ctrl/Cmd + T</kbd> to toggle theme
          </li>
        </ul>
      </section>

      <section style={{ marginTop: '2rem' }}>
        <h3>Accessibility Features (GU-049)</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          <label>
            <input
              type="checkbox"
              checked={preferences.screenReaderMode}
              onChange={() => handleToggleFeature('screenReaderMode')}
            />
            Screen Reader Mode
          </label>
          <label>
            <input
              type="checkbox"
              checked={preferences.keyboardNavigation}
              onChange={() => handleToggleFeature('keyboardNavigation')}
            />
            Keyboard Navigation
          </label>
          <label>
            <input
              type="checkbox"
              checked={preferences.focusIndicators}
              onChange={() => handleToggleFeature('focusIndicators')}
            />
            Enhanced Focus Indicators
          </label>
          <label>
            <input
              type="checkbox"
              checked={preferences.highContrast}
              onChange={() => handleToggleFeature('highContrast')}
            />
            High Contrast Mode
          </label>
          <label>
            <input
              type="checkbox"
              checked={preferences.reducedMotion}
              onChange={() => handleToggleFeature('reducedMotion')}
            />
            Reduce Motion
          </label>
        </div>
      </section>

      <section style={{ marginTop: '2rem' }}>
        <h3>User Preferences (GU-047)</h3>
        <p>Open Settings to customize:</p>
        <ul>
          <li>Theme and appearance</li>
          <li>Visualization quality</li>
          <li>Calculation precision</li>
          <li>Interface layout</li>
          <li>Notifications</li>
        </ul>
      </section>

      <section style={{ marginTop: '2rem' }}>
        <h3>Current Settings Summary</h3>
        <pre
          style={{
            background: 'var(--color-surface-elevated, #2a2a2a)',
            padding: '1rem',
            borderRadius: '8px',
            overflow: 'auto',
          }}
        >
          {JSON.stringify(preferences, null, 2)}
        </pre>
      </section>
    </div>
  );
}
