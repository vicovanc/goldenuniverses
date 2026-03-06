import React, { useState } from 'react';
import { ThemeToggle } from '@/components/Theme/ThemeToggle';
import { SettingsPanel } from '@/components/Settings/SettingsPanel';
import { KeyboardShortcutsModal } from '@/components/Keyboard/KeyboardShortcutsModal';
import { useKeyboardShortcutsContext } from '@/contexts/KeyboardShortcutsContext';
import './AppHeader.scss';

export function AppHeader() {
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const { toggleShortcutsModal } = useKeyboardShortcutsContext();

  return (
    <>
      <header className="app-header" role="banner">
        <div className="header-content">
          <div className="header-left">
            <h1 className="app-title">Golden Universe Theory</h1>
            <span className="header-subtitle">φ = (1 + √5) / 2</span>
          </div>

          <div className="header-right">
            <button
              className="header-button"
              onClick={() => setIsSettingsOpen(true)}
              aria-label="Open settings"
              data-tour="settings"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <circle cx="12" cy="12" r="3" />
                <path d="M12 1v6m0 6v6m4.22-13.22l-4.24 4.24m8.24 0l-4.24 4.24m4.24 4.24l-4.24-4.24m0 8.48l-4.24-4.24M19 12h-6m-6 0H1" />
              </svg>
            </button>
            <button
              className="header-button"
              onClick={toggleShortcutsModal}
              aria-label="Show keyboard shortcuts"
              data-tour="keyboard-shortcuts"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <rect x="2" y="4" width="20" height="16" rx="2" />
                <path d="M6 8h.01M10 8h.01M14 8h.01M18 8h.01M8 12h8M6 16h12" />
              </svg>
            </button>
            <ThemeToggle />
          </div>
        </div>
      </header>

      <SettingsPanel isOpen={isSettingsOpen} onClose={() => setIsSettingsOpen(false)} />
      <KeyboardShortcutsModal />
    </>
  );
}
