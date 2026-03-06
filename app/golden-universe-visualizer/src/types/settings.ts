export interface UserPreferences {
  // Appearance
  theme: 'light' | 'dark' | 'system';
  fontSize: 'small' | 'medium' | 'large';
  reducedMotion: boolean;
  highContrast: boolean;

  // Visualization
  visualizationQuality: 'low' | 'medium' | 'high';
  enableAnimations: boolean;
  showGrid: boolean;

  // Calculations
  autoCalculate: boolean;
  precisionDigits: number;
  showIntermediateSteps: boolean;

  // Interface
  sidebarPosition: 'left' | 'right';
  compactMode: boolean;
  showTooltips: boolean;

  // Accessibility
  screenReaderMode: boolean;
  keyboardNavigation: boolean;
  focusIndicators: boolean;

  // Notifications
  enableNotifications: boolean;
  notificationDuration: number;

  // Tour & Help
  hasCompletedTour: boolean;
  showHelpHints: boolean;
}

export const DEFAULT_PREFERENCES: UserPreferences = {
  theme: 'dark',
  fontSize: 'medium',
  reducedMotion: false,
  highContrast: false,
  visualizationQuality: 'high',
  enableAnimations: true,
  showGrid: true,
  autoCalculate: true,
  precisionDigits: 10,
  showIntermediateSteps: true,
  sidebarPosition: 'left',
  compactMode: false,
  showTooltips: true,
  screenReaderMode: false,
  keyboardNavigation: true,
  focusIndicators: true,
  enableNotifications: true,
  notificationDuration: 3000,
  hasCompletedTour: false,
  showHelpHints: true,
};

export interface SettingsContextValue {
  preferences: UserPreferences;
  updatePreferences: (updates: Partial<UserPreferences>) => void;
  resetPreferences: () => void;
  exportSettings: () => string;
  importSettings: (json: string) => boolean;
}
