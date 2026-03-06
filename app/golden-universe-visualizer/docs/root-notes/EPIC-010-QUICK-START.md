# EPIC-010: UX Enhancements - Quick Start Guide

## For Developers

### Installation & Setup

The UX enhancements are already integrated. No additional setup needed!

### Using the Features

#### 1. Access User Settings

```tsx
import { useSettings } from '@/contexts/SettingsContext';

function MyComponent() {
  const { preferences, updatePreferences } = useSettings();

  // Read a preference
  const isDarkTheme = preferences.theme === 'dark';

  // Update a preference
  updatePreferences({ fontSize: 'large' });

  // Export settings
  const json = exportSettings();

  // Import settings
  importSettings(jsonString);

  // Reset to defaults
  resetPreferences();
}
```

#### 2. Add Keyboard Shortcuts

```tsx
import { useKeyboardShortcuts } from '@/hooks/useKeyboardShortcuts';

function MyComponent() {
  const shortcuts = [
    {
      key: 's',
      ctrlKey: true,
      description: 'Save document',
      action: handleSave,
      category: 'general',
    },
    {
      key: 'p',
      description: 'Print',
      action: handlePrint,
      category: 'general',
    }
  ];

  useKeyboardShortcuts(shortcuts);
}
```

#### 3. Manage Theme

```tsx
import { useTheme } from '@/hooks/useTheme';

function MyComponent() {
  const { theme, resolvedTheme, toggleTheme, setTheme } = useTheme();

  // Toggle between light and dark
  toggleTheme();

  // Set specific theme
  setTheme('dark'); // 'light' | 'dark' | 'system'

  // Check current theme
  console.log(theme); // User preference
  console.log(resolvedTheme); // Actual applied theme
}
```

#### 4. Start a Guided Tour

```tsx
import { useGuidedTour } from '@/hooks/useGuidedTour';

function MyComponent() {
  const { startTour } = useGuidedTour();

  const handleStartTour = () => {
    startTour([
      {
        element: '#feature-1',
        intro: 'This is feature 1',
        position: 'bottom',
      },
      {
        element: '#feature-2',
        intro: 'This is feature 2',
        position: 'right',
      },
    ]);
  };
}
```

#### 5. Show Tooltips

```tsx
import { useTooltip } from '@/hooks/useTooltip';

function MyComponent() {
  const { show, hide } = useTooltip();
  const buttonRef = useRef<HTMLButtonElement>(null);

  return (
    <button
      ref={buttonRef}
      onMouseEnter={() => show('Click to save', buttonRef.current!)}
      onMouseLeave={hide}
    >
      Save
    </button>
  );
}
```

#### 6. Screen Reader Announcements

```tsx
import { useAnnouncer } from '@/hooks/useAnnouncer';

function MyComponent() {
  const { announce } = useAnnouncer();

  const handleSave = async () => {
    await saveData();
    announce('Data saved successfully', 'polite');
  };

  const handleError = () => {
    announce('Error occurred!', 'assertive');
  };
}
```

#### 7. Focus Management

```tsx
import { useFocusManagement } from '@/hooks/useFocusManagement';

function Modal({ isOpen }) {
  const { trapFocus } = useFocusManagement();
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen && modalRef.current) {
      return trapFocus(modalRef.current);
    }
  }, [isOpen, trapFocus]);

  return <div ref={modalRef}>...</div>;
}
```

## For Users

### Keyboard Shortcuts

Press `?` to see all shortcuts, or use these common ones:

- **`/`** - Focus search
- **`Cmd/Ctrl + K`** - Open search
- **`Cmd/Ctrl + T`** - Toggle theme
- **`Escape`** - Close modals
- **`Alt + 1-4`** - Navigate to sections
- **`H`** - Go to home

### Settings Panel

Click the settings icon (⚙️) in the header to customize:

- **Theme:** Light, Dark, or System
- **Font Size:** Small, Medium, or Large
- **Accessibility:** High contrast, reduced motion, focus indicators
- **Visualizations:** Quality, animations, grid
- **Calculations:** Precision, auto-calculate
- **Notifications:** Duration and enable/disable

### Theme Toggle

Click the sun/moon icon to switch between light and dark themes.
- The "Auto" badge means it follows your system preference

### Guided Tour

On your first visit, a guided tour will automatically start.
- You can restart it anytime from Settings → "Reset Tour"

## Common Patterns

### Conditional Rendering Based on Preferences

```tsx
const { preferences } = useSettings();

{preferences.showTooltips && <Tooltip content="..." />}
{preferences.enableAnimations && <AnimatedComponent />}
```

### Theme-Aware Styling

```tsx
// In your component
<div className="my-component">
  Content
</div>

// In your SCSS
.my-component {
  background: var(--color-surface);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
}

[data-theme='light'] .my-component {
  // Light theme overrides
}
```

### Accessibility Attributes

```tsx
<button
  aria-label="Close modal"
  aria-describedby="modal-description"
  data-tour="close-button"
>
  ×
</button>
```

### Tour Integration Points

Add `data-tour` attributes to elements you want to highlight:

```tsx
<div data-tour="feature-name">
  Feature content
</div>
```

## Testing Your Implementation

### Manual Testing

1. **Keyboard Navigation**
   ```
   - Press Tab to navigate
   - Press ? to open shortcuts
   - Press / to focus search
   - Press Escape to close modals
   ```

2. **Theme Testing**
   ```
   - Toggle theme manually
   - Change system theme (should auto-update if set to system)
   - Check all components render correctly in both themes
   ```

3. **Settings Testing**
   ```
   - Change each setting and verify it applies
   - Export settings and verify JSON
   - Import settings from file
   - Reset to defaults
   ```

4. **Accessibility Testing**
   ```
   - Tab through all interactive elements
   - Use skip links (Tab from page load)
   - Enable screen reader and verify announcements
   - Enable high contrast and verify readability
   ```

### Debug Mode

Check localStorage in browser DevTools:

```javascript
// View current settings
localStorage.getItem('golden-universe-preferences')

// View storage
localStorage.getItem('golden-universe-storage')

// Clear all (for testing)
localStorage.clear()
```

## Troubleshooting

### Shortcuts Not Working

1. Check if keyboard navigation is enabled in settings
2. Verify you're not in an input field
3. Check browser console for errors

### Theme Not Changing

1. Clear localStorage and reload
2. Check if browser supports matchMedia (for system theme)
3. Verify CSS variables are defined

### Tour Not Starting

1. Check if `hasCompletedTour` is false in settings
2. Verify elements with `data-tour` attributes exist
3. Check browser console for Intro.js errors

### Settings Not Persisting

1. Check if localStorage is enabled in browser
2. Verify no localStorage quota exceeded errors
3. Check browser console for errors

## Best Practices

### Do's ✅

- Use provided hooks for all UX features
- Add `data-tour` attributes to key features
- Use CSS variables for theming
- Add ARIA labels to all interactive elements
- Test with keyboard only
- Test with screen reader
- Respect user's reduced motion preference

### Don'ts ❌

- Don't bypass the settings context
- Don't hardcode theme colors
- Don't trap focus without escape
- Don't override user's accessibility preferences
- Don't add keyboard shortcuts that conflict with browser/OS
- Don't forget to announce dynamic content changes

## Need Help?

1. Check the full documentation: `src/components/UXEnhancements/README.md`
2. View implementation details: `EPIC-010-IMPLEMENTATION.md`
3. See all files: `EPIC-010-FILES.md`
4. Run the demo: Import and render `<UXDemo />` component

## Quick Links

- **Settings Context:** `/src/contexts/SettingsContext.tsx`
- **Keyboard Context:** `/src/contexts/KeyboardShortcutsContext.tsx`
- **All Hooks:** `/src/hooks/index.ts`
- **Main Provider:** `/src/components/UXEnhancements/UXProvider.tsx`
- **Demo Component:** `/src/components/UXEnhancements/UXDemo.tsx`

---

**Version:** 1.0.0
**Last Updated:** February 25, 2026
**Status:** Production Ready ✅
