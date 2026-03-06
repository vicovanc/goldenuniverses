# Mobile Features - Quick Reference Guide

## Responsive Hooks

```typescript
import { useIsMobile, useIsTablet, useIsDesktop, useBreakpoint } from '@/hooks';

// Basic checks
const isMobile = useIsMobile();        // < 640px
const isTablet = useIsTablet();        // 640px - 1023px
const isDesktop = useIsDesktop();      // ≥ 1024px

// Get current breakpoint
const breakpoint = useBreakpoint();    // 'mobile' | 'tablet' | 'desktop'

// Responsive values
const columns = useResponsiveValue({
  mobile: 1,
  tablet: 2,
  desktop: 4
});
```

## Touch Gestures

```tsx
import TouchControls from '@components/Visualizations/TouchControls';

<TouchControls
  onPinch={(scale) => zoom(scale)}
  onRotate={(angle) => rotate(angle)}
  onPan={(dx, dy) => pan(dx, dy)}
  onSwipe={(dir) => navigate(dir)}
  onDoubleTap={() => reset()}
  onLongPress={() => showMenu()}
>
  {children}
</TouchControls>
```

## Mobile Navigation

```tsx
import { BottomNav, MobileMenu, MobileHeader } from '@components/Navigation';

// Bottom navigation (auto-shown on mobile)
<BottomNav items={navItems} />

// Mobile header (auto-shown on mobile)
<MobileHeader title="App Name" />

// Full-screen menu
<MobileMenu isOpen={open} onClose={() => setOpen(false)} />
```

## PWA Functions

```typescript
import {
  registerServiceWorker,
  promptInstall,
  isAppInstalled,
  checkForUpdates,
  setupNetworkListeners
} from '@/utils/pwa';

// Register service worker
registerServiceWorker();

// Setup install prompt
setupInstallPrompt();

// Prompt user to install
const result = await promptInstall(); // 'accepted' | 'dismissed' | 'unavailable'

// Check if installed
if (isAppInstalled()) {
  console.log('Running as installed PWA');
}

// Check for updates
const hasUpdate = await checkForUpdates();

// Listen for network changes
setupNetworkListeners(
  () => console.log('Online'),
  () => console.log('Offline')
);
```

## Lazy Loading

```typescript
import { lazyLoadWithRetry, LazyLoad } from '@/utils/lazyLoad';

// Create lazy component
const MyComponent = LazyLoad(
  lazyLoadWithRetry(() => import('./MyComponent'))
);

// Use it
<MyComponent prop="value" />
```

## Performance Hooks

```typescript
import {
  useAdaptiveLoading,
  useConnectionQuality,
  useReducedMotion
} from '@/hooks';

// Adaptive loading
const {
  shouldLazyLoad,
  imageQuality,
  enableAnimations
} = useAdaptiveLoading();

// Connection quality
const { isSlow } = useConnectionQuality();

// Reduced motion preference
const reducedMotion = useReducedMotion();
```

## SCSS Mixins

```scss
@import '@styles/responsive.scss';

.my-component {
  padding: 1rem;

  @include mobile {
    padding: 0.5rem;
  }

  @include tablet {
    padding: 0.75rem;
  }

  @include desktop {
    padding: 1.5rem;
  }

  @include from-lg {
    max-width: 1200px;
  }

  @include until-md {
    width: 100%;
  }
}
```

## Responsive Classes

```html
<!-- Visibility -->
<div className="hide-on-mobile">Desktop only</div>
<div className="show-on-mobile">Mobile only</div>
<div className="hide-on-tablet">Not on tablet</div>

<!-- Touch targets -->
<button className="touch-target">Click me</button>
<button className="touch-target-large">Large target</button>

<!-- Safe areas -->
<div className="safe-area-top">Notch safe</div>
<div className="safe-area-bottom">Home indicator safe</div>

<!-- Mobile utilities -->
<div className="mobile-card">Card content</div>
<button className="mobile-button">Button</button>
<div className="mobile-list-item">List item</div>
```

## Performance Utilities

```typescript
import {
  isSlowConnection,
  getConnectionInfo,
  prefersReducedMotion,
  preloadResource,
  runWhenIdle
} from '@/utils/performance';

// Check connection
if (isSlowConnection()) {
  // Load lighter version
}

// Get connection details
const info = getConnectionInfo();
console.log(info.effectiveType); // '4g', '3g', '2g', etc.

// Check motion preference
if (prefersReducedMotion()) {
  // Disable animations
}

// Preload resources
preloadResource('/api/data', 'fetch');

// Run on idle
runWhenIdle(() => {
  // Non-critical work
});
```

## Layout Components

```tsx
import MobileLayout from '@components/Layout/MobileLayout';
import ResponsiveLayout from '@components/Layout/ResponsiveLayout';

// Mobile-optimized layout (includes bottom nav, mobile header)
<MobileLayout>
  <YourContent />
</MobileLayout>

// Generic responsive layout
<ResponsiveLayout
  sidebar={<Sidebar />}
  header={<Header />}
  footer={<Footer />}
  bottomNav={<BottomNav />}
>
  <YourContent />
</ResponsiveLayout>
```

## Breakpoint Values

```typescript
// JavaScript
const BREAKPOINTS = {
  sm: 640,   // Mobile
  md: 768,   // Tablet
  lg: 1024,  // Desktop
  xl: 1280,  // Large desktop
  '2xl': 1536 // Extra large
};

// Touch targets
const TOUCH_TARGET_SIZE = {
  min: 48,         // WCAG minimum
  recommended: 56  // Material Design
};
```

## Testing Commands

```bash
# Development
npm run dev

# Build production
npm run build

# Preview production build
npm run preview

# Test with network throttling
# Chrome DevTools > Network > Throttling > Slow 3G

# Test PWA
# Chrome DevTools > Application > Service Workers
# Chrome DevTools > Lighthouse > Run PWA audit
```

## Common Patterns

### Responsive Image Loading
```tsx
const imageSize = getOptimalImageSize(); // 'small' | 'medium' | 'large'
const imageSrc = `/images/photo-${imageSize}.jpg`;
```

### Conditional Rendering
```tsx
const isMobile = useIsMobile();

return (
  <>
    {isMobile ? <MobileView /> : <DesktopView />}
  </>
);
```

### Adaptive Features
```tsx
const { isSlow, enableAnimations } = useAdaptiveLoading();

return (
  <motion.div
    animate={enableAnimations ? { scale: 1.2 } : {}}
    transition={isSlow ? { duration: 0 } : { duration: 0.3 }}
  >
    Content
  </motion.div>
);
```

### Safe Area Handling
```scss
.mobile-header {
  padding-top: env(safe-area-inset-top);
  padding-bottom: env(safe-area-inset-bottom);
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
}
```

## Important Notes

1. **Touch Targets:** Minimum 48px × 48px (WCAG 2.1 AA)
2. **Font Sizes:** Minimum 16px on mobile to prevent zoom
3. **Viewport:** Use `viewport-fit=cover` for notched devices
4. **Service Worker:** Only registers in production
5. **Lazy Loading:** Uses retry logic (3 attempts with backoff)
6. **Performance:** Monitor Web Vitals in production
7. **Offline:** Service worker handles offline gracefully
8. **Icons:** Generate PWA icons in multiple sizes (72px to 512px)

## Browser DevTools

### Mobile Testing
- Chrome: Ctrl+Shift+M (Windows) / Cmd+Shift+M (Mac)
- Device emulation
- Touch simulation
- Network throttling

### PWA Testing
- Application tab > Manifest
- Application tab > Service Workers
- Lighthouse > PWA audit
- Application tab > Storage > Clear storage

### Performance Testing
- Performance tab > Record
- Memory tab > Take snapshot
- Network tab > Throttling
- Lighthouse > Performance audit
