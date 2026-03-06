# Sidebar Component Usage Examples

## Quick Start

### 1. Replace Existing Sidebar

In your main layout component:

```tsx
// Before
import Sidebar from '@components/Sidebar/Sidebar';

// After
import { SidebarNew } from '@components/Sidebar';

function MainLayout() {
  return (
    <div className="app-layout">
      <SidebarNew />
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}
```

### 2. Complete App Integration

```tsx
// src/App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { SidebarNew } from '@components/Sidebar';
import './App.scss';

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <SidebarNew />
        <main className="app-main">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/theory/:id" element={<TheoryPage />} />
            <Route path="/derivations/:id" element={<DerivationPage />} />
            <Route path="/calculations/:id" element={<CalculationPage />} />
            <Route path="/visualizations/:id" element={<VisualizationPage />} />
            <Route path="/explanations/:id" element={<ExplanationPage />} />
            <Route path="/results/:id" element={<ResultsPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
```

### 3. App Layout Styles

```scss
// src/App.scss
.app {
  display: flex;
  height: 100vh;
  background: #0a0a0a;
  color: #e0e0e0;
}

.app-main {
  flex: 1;
  margin-left: 320px; // Width of expanded sidebar
  overflow-y: auto;
  transition: margin-left 0.3s ease;

  @media (max-width: 768px) {
    margin-left: 0; // No margin on mobile
  }
}

// When sidebar is collapsed
.sidebar-collapsed .app-main {
  margin-left: 70px;

  @media (max-width: 768px) {
    margin-left: 0;
  }
}
```

## Advanced Usage

### Custom Navigation Actions

```tsx
import { useSidebarStore, useNavigation } from '@components/Sidebar';

function MyComponent() {
  const navigate = useNavigation();
  const { addPinnedItem } = useSidebarStore();

  const handleQuickAccess = () => {
    // Navigate and pin in one action
    navigate({
      id: 'calc-electron',
      label: 'Electron Mass',
      path: '/calculations/electron-mass',
    });
    addPinnedItem('calc-electron');
  };

  return <button onClick={handleQuickAccess}>Quick Access</button>;
}
```

### Programmatic Search

```tsx
import { useSidebarStore } from '@components/Sidebar';

function SearchTrigger() {
  const { setSearchQuery } = useSidebarStore();

  return (
    <button onClick={() => setSearchQuery('electron')}>
      Find Electron
    </button>
  );
}
```

### Expand Specific Section

```tsx
import { useSidebarStore } from '@components/Sidebar';
import { useEffect } from 'react';

function TheoryPage() {
  const { toggleSection, expandedSections } = useSidebarStore();

  useEffect(() => {
    // Ensure theory section is expanded when on theory page
    if (!expandedSections.has('theory')) {
      toggleSection('theory');
    }
  }, []);

  return <div>Theory content...</div>;
}
```

### Custom Keyboard Shortcuts

```tsx
import { useSidebarStore } from '@components/Sidebar';
import { useEffect } from 'react';

function App() {
  const { setSearchQuery, expandAll } = useSidebarStore();

  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      // Cmd/Ctrl + / to focus search
      if ((e.metaKey || e.ctrlKey) && e.key === '/') {
        e.preventDefault();
        setSearchQuery('');
        document.querySelector<HTMLInputElement>('.search-input')?.focus();
      }

      // Cmd/Ctrl + E to expand all
      if ((e.metaKey || e.ctrlKey) && e.key === 'e') {
        e.preventDefault();
        expandAll();
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [setSearchQuery, expandAll]);

  return <SidebarNew />;
}
```

### Tracking Analytics

```tsx
import { useNavigation } from '@components/Sidebar';
import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

function AnalyticsWrapper() {
  const location = useLocation();

  useEffect(() => {
    // Track navigation
    console.log('User navigated to:', location.pathname);
    // Send to analytics service
    // analytics.track('page_view', { path: location.pathname });
  }, [location]);

  return <SidebarNew />;
}
```

## Customizing Navigation Data

### Adding a New Section

```typescript
// src/components/Sidebar/navigationData.ts

export const SIDEBAR_SECTIONS: SidebarSection[] = [
  // ... existing sections
  {
    id: 'resources',
    title: 'RESOURCES',
    icon: '📚',
    defaultExpanded: false,
    items: [
      {
        id: 'res-papers',
        label: 'Research Papers',
        path: '/resources/papers',
        badge: 25,
      },
      {
        id: 'res-videos',
        label: 'Video Lectures',
        path: '/resources/videos',
        icon: '🎥',
      },
    ],
  },
];
```

### Dynamic Items Loading

```tsx
import { useState, useEffect } from 'react';
import type { SidebarNavigationItem } from '@components/Sidebar';

function DynamicSidebar() {
  const [sections, setSections] = useState(SIDEBAR_SECTIONS);

  useEffect(() => {
    // Fetch dynamic items
    fetch('/api/navigation')
      .then(res => res.json())
      .then(data => {
        // Merge with static sections
        setSections([...SIDEBAR_SECTIONS, ...data.sections]);
      });
  }, []);

  return <SidebarNew sections={sections} />;
}
```

### Conditional Items

```typescript
// Show different items based on user role
const getNavItems = (userRole: string): SidebarSection[] => {
  const baseSections = SIDEBAR_SECTIONS;

  if (userRole === 'admin') {
    return [
      ...baseSections,
      {
        id: 'admin',
        title: 'ADMIN',
        icon: '⚙️',
        items: [
          { id: 'admin-users', label: 'Users', path: '/admin/users' },
          { id: 'admin-settings', label: 'Settings', path: '/admin/settings' },
        ],
      },
    ];
  }

  return baseSections;
};
```

## State Management Examples

### Syncing with URL Parameters

```tsx
import { useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useSidebarStore } from '@components/Sidebar';

function SidebarWithURLSync() {
  const [searchParams, setSearchParams] = useSearchParams();
  const { searchQuery, setSearchQuery } = useSidebarStore();

  // Sync search query with URL
  useEffect(() => {
    const query = searchParams.get('search');
    if (query && query !== searchQuery) {
      setSearchQuery(query);
    }
  }, [searchParams]);

  useEffect(() => {
    if (searchQuery) {
      setSearchParams({ search: searchQuery });
    } else {
      setSearchParams({});
    }
  }, [searchQuery]);

  return <SidebarNew />;
}
```

### Persisting Sidebar State to Backend

```tsx
import { useEffect } from 'react';
import { useSidebarStore } from '@components/Sidebar';

function SidebarWithBackendSync() {
  const { pinnedItems, recentItems } = useSidebarStore();

  // Save to backend when pinned items change
  useEffect(() => {
    const savePreferences = async () => {
      await fetch('/api/user/preferences', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pinnedItems, recentItems }),
      });
    };

    const debounceTimer = setTimeout(savePreferences, 1000);
    return () => clearTimeout(debounceTimer);
  }, [pinnedItems, recentItems]);

  return <SidebarNew />;
}
```

## Styling Customizations

### Custom Theme Colors

```scss
// Override default golden theme
.sidebar-new {
  // Blue theme
  --sidebar-primary: #4a90e2;
  --sidebar-accent: #6cb4ee;
  --sidebar-bg: linear-gradient(180deg, #1a2332 0%, #0f1419 100%);

  background: var(--sidebar-bg);
  border-right-color: var(--sidebar-primary);

  .tree-node-content.active {
    background: linear-gradient(90deg,
      rgba(74, 144, 226, 0.2) 0%,
      rgba(74, 144, 226, 0.1) 100%
    );
    border-color: var(--sidebar-primary);
  }
}
```

### Compact Mode

```scss
// Reduce padding for more compact view
.sidebar-new.compact {
  .tree-node-content {
    padding: 0.25rem 0.75rem;
  }

  .section-header {
    padding: 0.5rem 0.75rem;
  }

  .node-label {
    font-size: 0.8rem;
  }
}
```

### Custom Scrollbar

```scss
.sidebar-new {
  &::-webkit-scrollbar {
    width: 8px;
  }

  &::-webkit-scrollbar-track {
    background: linear-gradient(180deg, #1a1a1a 0%, #0a0a0a 100%);
  }

  &::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #c9a84e 0%, #8b7332 100%);
    border-radius: 4px;
    border: 2px solid #1a1a1a;

    &:hover {
      background: linear-gradient(180deg, #ffd700 0%, #c9a84e 100%);
    }
  }
}
```

## Mobile Optimization

### Touch Gestures

```tsx
import { useState, useRef } from 'react';
import { useAppStore } from '@utils/store';

function TouchSidebar() {
  const { sidebarCollapsed, toggleSidebar } = useAppStore();
  const [touchStart, setTouchStart] = useState(0);
  const sidebarRef = useRef<HTMLDivElement>(null);

  const handleTouchStart = (e: React.TouchEvent) => {
    setTouchStart(e.touches[0].clientX);
  };

  const handleTouchEnd = (e: React.TouchEvent) => {
    const touchEnd = e.changedTouches[0].clientX;
    const diff = touchStart - touchEnd;

    // Swipe left to close
    if (diff > 50 && !sidebarCollapsed) {
      toggleSidebar();
    }
  };

  return (
    <div
      ref={sidebarRef}
      onTouchStart={handleTouchStart}
      onTouchEnd={handleTouchEnd}
    >
      <SidebarNew />
    </div>
  );
}
```

## Performance Tips

### Lazy Loading Sections

```tsx
import { lazy, Suspense } from 'react';

const TheorySection = lazy(() => import('./sections/TheorySection'));
const DerivationsSection = lazy(() => import('./sections/DerivationsSection'));

function OptimizedSidebar() {
  return (
    <Suspense fallback={<div className="sidebar-loading" />}>
      <SidebarNew />
    </Suspense>
  );
}
```

### Virtual Scrolling Implementation

```tsx
import { useVirtualScroll } from '@components/Sidebar';

function VirtualizedList({ items }: { items: SidebarNavigationItem[] }) {
  const { startIndex, endIndex, offsetY, handleScroll, totalHeight } =
    useVirtualScroll(items.length, 40, 600);

  return (
    <div
      className="virtual-list"
      onScroll={handleScroll}
      style={{ height: 600, overflow: 'auto' }}
    >
      <div style={{ height: totalHeight, position: 'relative' }}>
        <div style={{ transform: `translateY(${offsetY}px)` }}>
          {items.slice(startIndex, endIndex + 1).map((item, idx) => (
            <TreeNode
              key={item.id}
              item={item}
              depth={0}
              // ... other props
            />
          ))}
        </div>
      </div>
    </div>
  );
}
```

## Testing Examples

### Unit Test

```tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { SidebarNew } from '@components/Sidebar';

describe('SidebarNew', () => {
  it('renders all main sections', () => {
    render(
      <BrowserRouter>
        <SidebarNew />
      </BrowserRouter>
    );

    expect(screen.getByText('THEORY')).toBeInTheDocument();
    expect(screen.getByText('DERIVATIONS')).toBeInTheDocument();
    expect(screen.getByText('CALCULATIONS')).toBeInTheDocument();
  });

  it('toggles section expansion', () => {
    render(
      <BrowserRouter>
        <SidebarNew />
      </BrowserRouter>
    );

    const theorySection = screen.getByText('THEORY');
    fireEvent.click(theorySection);

    // Check if content is hidden
    expect(screen.queryByText('Law 0: Foundational Symmetry')).not.toBeVisible();
  });
});
```

## Common Issues & Solutions

### Issue: Sidebar not persisting state
**Solution**: Check that Zustand persist middleware is properly configured and localStorage is available.

### Issue: Search not working
**Solution**: Verify debounce delay and check that items have searchable `label` or `tooltip` properties.

### Issue: Mobile sidebar not closing
**Solution**: Ensure media query breakpoint matches and toggleSidebar is called on navigation.

### Issue: Active state not updating
**Solution**: Check that route paths match the item path structure exactly.
