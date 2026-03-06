# User Experience Enhancements - EPIC-010

This module implements comprehensive UX enhancements for the Golden Universe Visualizer application, including keyboard shortcuts, user preferences, guided tours, accessibility features, and theme management.

## Features Implemented

### GU-046: Keyboard Shortcuts System

A comprehensive keyboard navigation system with contextual shortcuts.

**Key Features:**
- Global keyboard shortcut management
- Context-aware shortcut handling
- Visual shortcut reference modal (press `?`)
- Platform-specific key display (Mac/Windows)
- Automatic conflict detection

**Available Shortcuts:**
- `?` - Show keyboard shortcuts modal
- `/` - Focus search bar
- `Cmd/Ctrl + K` - Open search
- `Cmd/Ctrl + T` - Toggle theme
- `Escape` - Close modals/dialogs
- `Alt + 1-4` - Navigate to sections
- `H` - Go to home
- Arrow keys - Navigate focusable elements

**Usage:**
```tsx
import { useKeyboardShortcuts } from '@/hooks/useKeyboardShortcuts';

const shortcuts = [
  {
    key: 's',
    ctrlKey: true,
    description: 'Save document',
    action: handleSave,
    category: 'general',
  },
];

useKeyboardShortcuts(shortcuts);
```

### GU-047: User Preferences & Settings

Persistent user preferences with localStorage synchronization.

**Preference Categories:**
- **Appearance**: Theme, font size, high contrast, reduced motion
- **Visualization**: Quality, animations, grid display
- **Calculations**: Auto-calculate, precision, intermediate steps
- **Interface**: Sidebar position, compact mode, tooltips
- **Accessibility**: Screen reader, keyboard navigation, focus indicators
- **Notifications**: Enable/disable, duration
- **Tour & Help**: Tour completion, help hints

**Features:**
- Settings panel with organized sections
- Export/import settings as JSON
- Reset to defaults
- Real-time preference application
- Cross-tab synchronization

**Usage:**
```tsx
import { useSettings } from '@/contexts/SettingsContext';

const { preferences, updatePreferences } = useSettings();

// Update a preference
updatePreferences({ theme: 'dark' });

// Export settings
const json = exportSettings();

// Reset to defaults
resetPreferences();
```

### GU-048: Tooltips & Guided Tours

Interactive onboarding and contextual help system.

**Features:**
- Intro.js integration for guided tours
- Custom tooltip system
- Auto-start tour for first-time users
- Tour reset capability
- Configurable tour steps

**Tour Steps:**
1. Welcome message
2. Navigation overview
3. Search functionality
4. Settings access
5. Keyboard shortcuts

**Usage:**
```tsx
import { useGuidedTour } from '@/hooks/useGuidedTour';

const { startTour, resetTour } = useGuidedTour();

// Start custom tour
startTour([
  {
    element: '#feature',
    intro: 'This is a great feature!',
    position: 'bottom',
  },
]);
```

### GU-049: Accessibility Improvements

WCAG 2.1 AA compliant accessibility features.

**Features:**
- Skip links for keyboard navigation
- Screen reader announcements
- Focus management and trapping
- ARIA labels and live regions
- Enhanced focus indicators
- High contrast mode support
- Minimum touch target sizes (44x44px)

**Accessibility Hooks:**

**Focus Management:**
```tsx
import { useFocusManagement } from '@/hooks/useFocusManagement';

const { trapFocus, restoreFocus } = useFocusManagement();

// Trap focus within modal
useEffect(() => {
  if (isOpen) {
    return trapFocus(modalRef.current);
  }
}, [isOpen]);
```

**Screen Reader Announcements:**
```tsx
import { useAnnouncer } from '@/hooks/useAnnouncer';

const { announce } = useAnnouncer();

// Announce changes
announce('Settings saved successfully', 'polite');
announce('Error occurred!', 'assertive');
```

### GU-050: Dark/Light Theme Toggle

Advanced theme system with system preference detection.

**Features:**
- Three theme modes: light, dark, system
- System preference detection and sync
- Smooth theme transitions
- CSS variable-based theming
- Persistent theme preference
- Visual theme toggle button

**Theme Management:**
```tsx
import { useTheme } from '@/hooks/useTheme';

const { theme, resolvedTheme, toggleTheme, setTheme } = useTheme();

// Toggle between light/dark
toggleTheme();

// Set specific theme
setTheme('system'); // 'light' | 'dark' | 'system'

// Get current resolved theme
console.log(resolvedTheme); // 'light' | 'dark'
```

## Components

### Core Components

#### `UXProvider`
Main provider component that wraps the entire application with UX enhancements.

```tsx
<UXProvider>
  <App />
</UXProvider>
```

#### `AppHeader`
Application header with theme toggle, settings, and shortcuts access.

#### `SettingsPanel`
Comprehensive settings modal with all user preferences organized by category.

#### `KeyboardShortcutsModal`
Visual reference for all available keyboard shortcuts, grouped by category.

#### `ThemeToggle`
Animated theme toggle button with system preference indicator.

#### `SkipLinks`
Accessibility skip links for keyboard navigation to main content areas.

### Utility Components

#### `Tooltip`
Custom tooltip component for contextual help.

## Contexts

### `SettingsContext`
Manages user preferences with localStorage persistence.

**Methods:**
- `updatePreferences(updates)` - Update one or more preferences
- `resetPreferences()` - Reset all preferences to defaults
- `exportSettings()` - Export settings as JSON string
- `importSettings(json)` - Import settings from JSON

### `KeyboardShortcutsContext`
Manages keyboard shortcuts registration and display.

**Methods:**
- `registerShortcut(shortcut)` - Register a new shortcut
- `unregisterShortcut(key)` - Remove a shortcut
- `toggleShortcutsModal()` - Show/hide shortcuts reference

## Hooks

### Core Hooks

- `useKeyboardShortcuts(shortcuts, options)` - Register keyboard shortcuts
- `useSettings()` - Access user preferences
- `useTheme()` - Theme management
- `useGuidedTour()` - Guided tour functionality
- `useTooltip()` - Tooltip management
- `useFocusManagement()` - Focus trap and restoration
- `useAnnouncer()` - Screen reader announcements
- `useLocalStorage(key, defaultValue)` - Persistent state

## Styling

### CSS Variables

All components use CSS custom properties for theming:

```css
/* Dark theme */
--color-primary: #ffd700;
--color-text-primary: #ffffff;
--color-text-secondary: #999999;
--color-surface: #1e1e1e;
--color-surface-elevated: #2a2a2a;
--color-border: #444444;
--color-hover: rgba(255, 255, 255, 0.1);

/* Light theme */
[data-theme='light'] {
  --color-primary: #d4af37;
  --color-text-primary: #1a1a1a;
  --color-surface: #ffffff;
  /* ... */
}
```

### Data Attributes

Settings are applied via data attributes on the root element:

- `data-theme` - Current theme (light/dark)
- `data-font-size` - Font size (small/medium/large)
- `data-high-contrast` - High contrast mode (true/false)
- `data-reduced-motion` - Reduced motion (true/false)
- `data-focus-indicators` - Enhanced focus (true/false)

## Browser Support

- Modern browsers with ES2022 support
- CSS Grid and Flexbox
- CSS Custom Properties
- Local Storage API
- matchMedia API for system preferences

## Accessibility Standards

Complies with WCAG 2.1 Level AA:

- ✅ Keyboard Navigation (2.1.1)
- ✅ No Keyboard Trap (2.1.2)
- ✅ Focus Visible (2.4.7)
- ✅ Focus Order (2.4.3)
- ✅ Bypass Blocks (2.4.1)
- ✅ Page Titled (2.4.2)
- ✅ Link Purpose (2.4.4)
- ✅ Multiple Ways (2.4.5)
- ✅ Headings and Labels (2.4.6)
- ✅ Contrast Minimum (1.4.3)
- ✅ Resize Text (1.4.4)
- ✅ Target Size (2.5.5)
- ✅ Label in Name (2.5.3)

## Testing

### Manual Testing Checklist

- [ ] All keyboard shortcuts work as expected
- [ ] Settings persist across page reloads
- [ ] Theme changes apply immediately
- [ ] System theme preference is detected
- [ ] Guided tour completes successfully
- [ ] Skip links are accessible with Tab key
- [ ] Screen reader announcements work
- [ ] Focus trap works in modals
- [ ] High contrast mode is readable
- [ ] Reduced motion disables animations
- [ ] Export/import settings works
- [ ] Cross-tab synchronization works
- [ ] All interactive elements are keyboard accessible
- [ ] Touch targets meet minimum size (44x44px)

### Keyboard Testing

1. Press `Tab` to navigate through all interactive elements
2. Press `?` to open shortcuts modal
3. Press `Escape` to close modal
4. Press `/` to focus search
5. Press `Alt + 1-4` to navigate sections
6. Press `Ctrl/Cmd + T` to toggle theme

### Screen Reader Testing

1. Enable screen reader (NVDA, JAWS, VoiceOver)
2. Navigate with screen reader shortcuts
3. Verify skip links are announced
4. Verify form labels are read correctly
5. Verify state changes are announced

## Performance Considerations

- Lazy loading of tour library (Intro.js)
- Debounced localStorage writes
- Memoized keyboard event handlers
- CSS containment for modals
- Reduced motion respects user preferences

## Future Enhancements

Potential improvements for future versions:

- Custom keyboard shortcut configuration
- Settings profiles
- Advanced tour authoring
- A11y audit tool integration
- Voice navigation
- Gesture support for mobile
- Multi-language support
- Settings cloud sync
