import React, { useRef } from 'react';
import { useSettings } from '@/contexts/SettingsContext';
import toast from 'react-hot-toast';
import './SettingsPanel.scss';

interface SettingsPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

export function SettingsPanel({ isOpen, onClose }: SettingsPanelProps) {
  const { preferences, updatePreferences, resetPreferences, exportSettings, importSettings } =
    useSettings();
  const fileInputRef = useRef<HTMLInputElement>(null);

  if (!isOpen) return null;

  const handleExport = () => {
    const settingsJson = exportSettings();
    const blob = new Blob([settingsJson], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `golden-universe-settings-${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    toast.success('Settings exported');
  };

  const handleImport = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      const content = event.target?.result as string;
      importSettings(content);
    };
    reader.readAsText(file);
  };

  const handleBackdropClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div
      className="settings-panel-backdrop"
      onClick={handleBackdropClick}
      role="dialog"
      aria-modal="true"
      aria-labelledby="settings-panel-title"
    >
      <div className="settings-panel">
        <div className="settings-header">
          <h2 id="settings-panel-title">Settings</h2>
          <button
            className="close-button"
            onClick={onClose}
            aria-label="Close settings panel"
          >
            ×
          </button>
        </div>

        <div className="settings-content">
          {/* Appearance Section */}
          <section className="settings-section">
            <h3>Appearance</h3>
            <div className="setting-item">
              <label htmlFor="theme-select">Theme</label>
              <select
                id="theme-select"
                value={preferences.theme}
                onChange={(e) =>
                  updatePreferences({ theme: e.target.value as 'light' | 'dark' | 'system' })
                }
              >
                <option value="light">Light</option>
                <option value="dark">Dark</option>
                <option value="system">System</option>
              </select>
            </div>
            <div className="setting-item">
              <label htmlFor="font-size-select">Font Size</label>
              <select
                id="font-size-select"
                value={preferences.fontSize}
                onChange={(e) =>
                  updatePreferences({ fontSize: e.target.value as 'small' | 'medium' | 'large' })
                }
              >
                <option value="small">Small</option>
                <option value="medium">Medium</option>
                <option value="large">Large</option>
              </select>
            </div>
            <div className="setting-item">
              <label htmlFor="high-contrast">
                <input
                  type="checkbox"
                  id="high-contrast"
                  checked={preferences.highContrast}
                  onChange={(e) => updatePreferences({ highContrast: e.target.checked })}
                />
                <span>High Contrast</span>
              </label>
            </div>
            <div className="setting-item">
              <label htmlFor="reduced-motion">
                <input
                  type="checkbox"
                  id="reduced-motion"
                  checked={preferences.reducedMotion}
                  onChange={(e) => updatePreferences({ reducedMotion: e.target.checked })}
                />
                <span>Reduce Motion</span>
              </label>
            </div>
          </section>

          {/* Visualization Section */}
          <section className="settings-section">
            <h3>Visualization</h3>
            <div className="setting-item">
              <label htmlFor="quality-select">Quality</label>
              <select
                id="quality-select"
                value={preferences.visualizationQuality}
                onChange={(e) =>
                  updatePreferences({
                    visualizationQuality: e.target.value as 'low' | 'medium' | 'high',
                  })
                }
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </select>
            </div>
            <div className="setting-item">
              <label htmlFor="enable-animations">
                <input
                  type="checkbox"
                  id="enable-animations"
                  checked={preferences.enableAnimations}
                  onChange={(e) => updatePreferences({ enableAnimations: e.target.checked })}
                />
                <span>Enable Animations</span>
              </label>
            </div>
            <div className="setting-item">
              <label htmlFor="show-grid">
                <input
                  type="checkbox"
                  id="show-grid"
                  checked={preferences.showGrid}
                  onChange={(e) => updatePreferences({ showGrid: e.target.checked })}
                />
                <span>Show Grid</span>
              </label>
            </div>
          </section>

          {/* Calculations Section */}
          <section className="settings-section">
            <h3>Calculations</h3>
            <div className="setting-item">
              <label htmlFor="auto-calculate">
                <input
                  type="checkbox"
                  id="auto-calculate"
                  checked={preferences.autoCalculate}
                  onChange={(e) => updatePreferences({ autoCalculate: e.target.checked })}
                />
                <span>Auto Calculate</span>
              </label>
            </div>
            <div className="setting-item">
              <label htmlFor="precision-digits">
                Precision Digits: {preferences.precisionDigits}
              </label>
              <input
                type="range"
                id="precision-digits"
                min="5"
                max="20"
                value={preferences.precisionDigits}
                onChange={(e) => updatePreferences({ precisionDigits: parseInt(e.target.value) })}
              />
            </div>
            <div className="setting-item">
              <label htmlFor="show-intermediate-steps">
                <input
                  type="checkbox"
                  id="show-intermediate-steps"
                  checked={preferences.showIntermediateSteps}
                  onChange={(e) =>
                    updatePreferences({ showIntermediateSteps: e.target.checked })
                  }
                />
                <span>Show Intermediate Steps</span>
              </label>
            </div>
          </section>

          {/* Interface Section */}
          <section className="settings-section">
            <h3>Interface</h3>
            <div className="setting-item">
              <label htmlFor="sidebar-position-select">Sidebar Position</label>
              <select
                id="sidebar-position-select"
                value={preferences.sidebarPosition}
                onChange={(e) =>
                  updatePreferences({ sidebarPosition: e.target.value as 'left' | 'right' })
                }
              >
                <option value="left">Left</option>
                <option value="right">Right</option>
              </select>
            </div>
            <div className="setting-item">
              <label htmlFor="compact-mode">
                <input
                  type="checkbox"
                  id="compact-mode"
                  checked={preferences.compactMode}
                  onChange={(e) => updatePreferences({ compactMode: e.target.checked })}
                />
                <span>Compact Mode</span>
              </label>
            </div>
            <div className="setting-item">
              <label htmlFor="show-tooltips">
                <input
                  type="checkbox"
                  id="show-tooltips"
                  checked={preferences.showTooltips}
                  onChange={(e) => updatePreferences({ showTooltips: e.target.checked })}
                />
                <span>Show Tooltips</span>
              </label>
            </div>
          </section>

          {/* Accessibility Section */}
          <section className="settings-section">
            <h3>Accessibility</h3>
            <div className="setting-item">
              <label htmlFor="screen-reader-mode">
                <input
                  type="checkbox"
                  id="screen-reader-mode"
                  checked={preferences.screenReaderMode}
                  onChange={(e) => updatePreferences({ screenReaderMode: e.target.checked })}
                />
                <span>Screen Reader Mode</span>
              </label>
            </div>
            <div className="setting-item">
              <label htmlFor="keyboard-navigation">
                <input
                  type="checkbox"
                  id="keyboard-navigation"
                  checked={preferences.keyboardNavigation}
                  onChange={(e) => updatePreferences({ keyboardNavigation: e.target.checked })}
                />
                <span>Keyboard Navigation</span>
              </label>
            </div>
            <div className="setting-item">
              <label htmlFor="focus-indicators">
                <input
                  type="checkbox"
                  id="focus-indicators"
                  checked={preferences.focusIndicators}
                  onChange={(e) => updatePreferences({ focusIndicators: e.target.checked })}
                />
                <span>Enhanced Focus Indicators</span>
              </label>
            </div>
          </section>

          {/* Notifications Section */}
          <section className="settings-section">
            <h3>Notifications</h3>
            <div className="setting-item">
              <label htmlFor="enable-notifications">
                <input
                  type="checkbox"
                  id="enable-notifications"
                  checked={preferences.enableNotifications}
                  onChange={(e) => updatePreferences({ enableNotifications: e.target.checked })}
                />
                <span>Enable Notifications</span>
              </label>
            </div>
            <div className="setting-item">
              <label htmlFor="notification-duration">
                Duration: {preferences.notificationDuration / 1000}s
              </label>
              <input
                type="range"
                id="notification-duration"
                min="1000"
                max="10000"
                step="1000"
                value={preferences.notificationDuration}
                onChange={(e) =>
                  updatePreferences({ notificationDuration: parseInt(e.target.value) })
                }
              />
            </div>
          </section>

          {/* Tour & Help Section */}
          <section className="settings-section">
            <h3>Help & Tour</h3>
            <div className="setting-item">
              <label htmlFor="show-help-hints">
                <input
                  type="checkbox"
                  id="show-help-hints"
                  checked={preferences.showHelpHints}
                  onChange={(e) => updatePreferences({ showHelpHints: e.target.checked })}
                />
                <span>Show Help Hints</span>
              </label>
            </div>
            <div className="setting-item">
              <button
                className="secondary-button"
                onClick={() => updatePreferences({ hasCompletedTour: false })}
              >
                Reset Tour
              </button>
            </div>
          </section>
        </div>

        <div className="settings-footer">
          <div className="button-group">
            <button className="secondary-button" onClick={handleExport}>
              Export Settings
            </button>
            <button className="secondary-button" onClick={handleImport}>
              Import Settings
            </button>
            <input
              ref={fileInputRef}
              type="file"
              accept=".json"
              style={{ display: 'none' }}
              onChange={handleFileChange}
            />
          </div>
          <div className="button-group">
            <button className="danger-button" onClick={resetPreferences}>
              Reset to Defaults
            </button>
            <button className="primary-button" onClick={onClose}>
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
