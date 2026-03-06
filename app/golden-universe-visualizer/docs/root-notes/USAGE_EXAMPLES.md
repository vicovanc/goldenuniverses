# Usage Examples - Modern Redesign

## How to Use the Redesigned SCSS

### 1. Visualizations

#### Using the Common Visualization Styles
```scss
// In any visualization SCSS file
@import '../../styles/design-system.scss';
@import './visualizations-common';

.my-visualization {
  @extend .visualization-container;

  // Add custom styles
  .custom-element {
    color: $text-primary;
  }
}
```

#### Adding a Legend
```tsx
// In your React component
<div className="viz-legend">
  <h3>Legend Title</h3>
  <div className="legend-item">
    <div className="color-indicator" style={{ background: '#5E3AEE' }} />
    <span className="item-label">Particle Type</span>
    <span className="item-type">Primary</span>
  </div>
  {/* More legend items */}
</div>
```

#### Adding Control Panel
```tsx
<div className="viz-controls">
  <h4>Settings</h4>
  <div className="control-group">
    <label>Speed</label>
    <input type="range" min="0" max="100" />
  </div>
  <div className="control-group">
    <button className="active">Play</button>
  </div>
</div>
```

#### Adding Loading State
```tsx
{loading ? (
  <div className="viz-loading">
    <div className="spinner" />
    <p>Loading visualization...</p>
  </div>
) : (
  <canvas ref={canvasRef} />
)}
```

### 2. Results Dashboard

#### Using the Redesigned Results Styles
```tsx
// Import the new styles in ResultsDashboard.tsx
import './Results-redesigned.scss';
// OR keep using Results.scss and merge the styles

// The class names remain the same:
<div className="results-dashboard">
  <div className="dashboard-header">
    {/* Header content */}
  </div>

  <div className="stats-banner">
    <div className="stat-item highlight">
      <span className="stat-value">42</span>
      <span className="stat-label">Predictions</span>
    </div>
  </div>
</div>
```

#### Navigation Tabs
```tsx
<div className="dashboard-nav">
  <button className="nav-tab active">Overview</button>
  <button className="nav-tab">Charts</button>
  <button className="nav-tab">Tables</button>
</div>
```

#### Category Badges
```tsx
<span className="category-badge leptons">Leptons</span>
<span className="category-badge quarks">Quarks</span>
<span className="category-badge bosons">Bosons</span>
<span className="category-badge constants">Constants</span>
```

#### Precision Badges
```tsx
<span className="precision-badge excellent">Excellent</span>
<span className="precision-badge very-good">Very Good</span>
<span className="precision-badge good">Good</span>
<span className="precision-badge fair">Fair</span>
<span className="precision-badge poor">Poor</span>
```

### 3. Documentation Viewer

#### Using TheoryDocViewer Styles
```tsx
// Import in TheoryDocViewer.tsx
import './TheoryDocViewer.scss';

// Component structure:
<div className="theory-doc-viewer">
  <div className="doc-controls">
    <div className="search-box">
      <input
        type="text"
        className="doc-search-input"
        placeholder="Search in document..."
      />
      {searchResults.length > 0 && (
        <div className="search-results-count">
          {searchResults.length} sections found
        </div>
      )}
    </div>

    <div className="doc-actions">
      <button className="doc-action-button">
        <svg>...</svg>
        Print
      </button>
    </div>
  </div>

  <div className="doc-layout">
    <div className="doc-sidebar">
      <div className="doc-toc">
        <h3>Table of Contents</h3>
        <ul className="toc-list">
          <li className="toc-item level-1 active">
            <button className="toc-link">Section 1</button>
          </li>
        </ul>
      </div>
    </div>

    <div className="doc-main">
      <div className="doc-content">
        {/* Markdown content renders here */}
      </div>
    </div>
  </div>
</div>
```

### 4. Loading States (Skeletons)

#### Card Skeleton
```tsx
import { CardSkeleton } from '@/components/Common/Skeleton';

{loading ? <CardSkeleton /> : <ActualCard />}
```

#### List Skeleton
```tsx
import { ListSkeleton } from '@/components/Common/Skeleton';

{loading ? <ListSkeleton count={5} /> : <ActualList />}
```

#### Table Skeleton
```tsx
import { TableSkeleton } from '@/components/Common/Skeleton';

{loading ? <TableSkeleton rows={10} cols={5} /> : <ActualTable />}
```

#### Custom Skeleton
```tsx
import { Skeleton } from '@/components/Common/Skeleton';

<Skeleton width="60%" height={24} variant="rounded" animation="wave" />
<Skeleton width="100%" height={16} animation="pulse" />
```

#### Visualization Skeleton
```tsx
{loading ? (
  <div className="viz-skeleton">
    <div className="viz-skeleton-content">
      <div className="viz-skeleton-spinner" />
      <p>Preparing visualization...</p>
    </div>
  </div>
) : (
  <ActualVisualization />
)}
```

#### Dashboard Skeleton
```tsx
{loading ? (
  <div className="dashboard-skeleton">
    <div className="dashboard-skeleton-header">
      <Skeleton width="40%" height={40} />
      <Skeleton width="20%" height={40} />
    </div>

    <div className="dashboard-skeleton-stats">
      {[1,2,3,4,5].map(i => (
        <div key={i} className="stat-skeleton">
          <Skeleton width="80%" height={60} />
          <Skeleton width="60%" height={20} />
        </div>
      ))}
    </div>

    <div className="dashboard-skeleton-content">
      <Skeleton width="100%" height={400} />
    </div>
  </div>
) : (
  <ActualDashboard />
)}
```

## Common Patterns

### Glassmorphic Card
```tsx
// Any component
<div className="my-card" style={{
  background: 'rgba(255, 255, 255, 0.05)',
  backdropFilter: 'blur(20px)',
  border: '1px solid rgba(255, 255, 255, 0.1)',
  borderRadius: '12px',
  padding: '24px',
  boxShadow: '0 10px 15px rgba(0, 0, 0, 0.15)'
}}>
  {/* Content */}
</div>

// Or using SCSS mixin
.my-card {
  @include glass-card;
  // Add custom styles
}
```

### Gradient Text
```tsx
<h1 style={{
  background: 'linear-gradient(135deg, #5E3AEE 0%, #3B82F6 100%)',
  WebkitBackgroundClip: 'text',
  WebkitTextFillColor: 'transparent',
  backgroundClip: 'text'
}}>
  Gradient Header
</h1>

// Or using SCSS
.gradient-heading {
  @include gradient-text($gradient-primary);
}
```

### Animated Button
```tsx
<button
  className="my-button"
  style={{
    transition: 'all 200ms cubic-bezier(0.4, 0, 0.2, 1)',
  }}
  onMouseEnter={(e) => {
    e.currentTarget.style.transform = 'translateY(-2px)';
    e.currentTarget.style.boxShadow = '0 8px 16px rgba(94, 58, 238, 0.3)';
  }}
  onMouseLeave={(e) => {
    e.currentTarget.style.transform = 'translateY(0)';
    e.currentTarget.style.boxShadow = 'none';
  }}
>
  Hover Me
</button>

// Or using SCSS
.my-button {
  @include button-base;
  transition: all $transition-base;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(94, 58, 238, 0.3);
  }
}
```

### Staggered Animation
```tsx
// In JSX
{items.map((item, index) => (
  <div
    key={item.id}
    className="animated-item"
    style={{
      animation: 'fadeInUp 0.5s ease-out backwards',
      animationDelay: `${index * 0.1}s`
    }}
  >
    {item.content}
  </div>
))}

// Or using SCSS
.animated-item {
  animation: fadeInUp 0.5s $ease-out backwards;

  @for $i from 1 through 10 {
    &:nth-child(#{$i}) {
      animation-delay: #{$i * 0.1}s;
    }
  }
}
```

## Design System Variables

### Using Colors
```scss
// In your SCSS files
.my-element {
  background: $bg-primary;      // #0A0A0B
  color: $text-primary;          // rgba(255, 255, 255, 0.95)
  border-color: $card-border;    // rgba(255, 255, 255, 0.08)
}

// Brand colors
.brand-element {
  background: $brand-primary;    // #5E3AEE
  background: $brand-secondary;  // #3B82F6
  background: $brand-accent;     // #F59E0B
}

// Gradients
.gradient-element {
  background: $gradient-primary; // Purple gradient
  background: $gradient-accent;  // Gold gradient
}
```

### Using Spacing
```scss
.spaced-element {
  padding: $space-6;           // 24px
  margin-bottom: $space-8;     // 32px
  gap: $space-4;               // 16px
}
```

### Using Typography
```scss
.text-element {
  font-size: $text-xl;         // 1.25rem
  font-weight: $font-semibold; // 600
  line-height: $leading-relaxed; // 1.75
  font-family: $font-family-primary; // Inter
}
```

### Using Shadows and Effects
```scss
.elevated-card {
  box-shadow: $shadow-xl;
  border-radius: $radius-lg;

  &:hover {
    box-shadow: $shadow-2xl, 0 0 40px rgba(94, 58, 238, 0.2);
  }
}
```

## Animation Timing

### Common Durations
```scss
// Fast interactions (hover, focus)
transition: all $transition-fast;  // 150ms

// Normal interactions (state changes)
transition: all $transition-base;  // 200ms

// Slow interactions (complex animations)
transition: all $transition-slow;  // 300ms

// Extra slow (page transitions)
transition: all $transition-slower; // 500ms
```

### Easing Functions
```scss
// Smooth ease-out (recommended for most cases)
transition: all 300ms $ease-out;

// Smooth ease-in-out (for reversible animations)
transition: all 300ms $ease-in-out;
```

## Responsive Design

### Breakpoints
```scss
// Mobile first approach
.responsive-element {
  // Mobile styles (default)
  width: 100%;

  // Tablet and up
  @media (min-width: $breakpoint-md) {
    width: 50%;
  }

  // Desktop and up
  @media (min-width: $breakpoint-lg) {
    width: 33.333%;
  }

  // Wide screen
  @media (min-width: $breakpoint-xl) {
    width: 25%;
  }
}
```

## Accessibility

### Focus States
```scss
.interactive-element {
  &:focus {
    outline: 2px solid $brand-primary;
    outline-offset: 2px;
  }

  &:focus-visible {
    box-shadow: 0 0 0 3px rgba(94, 58, 238, 0.3);
  }
}
```

### Reduced Motion
```scss
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Pro Tips

1. **Always use design system variables** instead of hard-coded values
2. **Use mixins** for common patterns (@include glass-card)
3. **Leverage CSS Grid** for modern layouts
4. **Use transform and opacity** for performant animations
5. **Add loading states** to all data-driven components
6. **Test responsiveness** at all breakpoints
7. **Maintain color contrast** for accessibility
8. **Use semantic HTML** with proper ARIA attributes
9. **Keep animations subtle** - less is more
10. **Profile performance** with DevTools if animations feel slow

---

Happy coding! The redesigned interface provides a solid foundation for a beautiful, modern application.
