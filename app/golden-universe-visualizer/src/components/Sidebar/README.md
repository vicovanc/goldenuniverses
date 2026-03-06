# ContextLoom-Style Sidebar Navigation

A comprehensive, feature-rich sidebar navigation component for the Golden Universe application, inspired by ContextLoom's modern interface design.

## Features

### Core Features
- **Hierarchical Tree Structure**: Six main sections (Theory, Derivations, Calculations, Visualizations, Explanations, Results)
- **Expandable/Collapsible Sections**: Smooth animations with multiple depth levels
- **Search Functionality**: Debounced search with highlighting and auto-expansion
- **Active Item Highlighting**: Visual feedback for current route
- **Badge Indicators**: Count and status badges for items
- **Icons/Emojis**: Visual identifiers for sections and items
- **Pinned Items**: Quick access to favorite items
- **Keyboard Navigation**: Arrow keys, Enter, Home, End support
- **Responsive Design**: Mobile-friendly with slide-in behavior

### Advanced Features
- **State Persistence**: Uses Zustand with localStorage persistence
- **Virtual Scrolling**: Performance optimization for long lists (hooks provided)
- **Tooltip System**: Hover tooltips with preview information
- **Loading States**: Async content loading support
- **Recent Items Tracking**: Automatically tracks navigation history
- **Keyboard Shortcuts**:
  - `Cmd/Ctrl + K`: Focus search
  - `Cmd/Ctrl + Shift + E`: Expand all
  - `Cmd/Ctrl + Shift + C`: Collapse all
  - `Arrow Up/Down`: Navigate items
  - `Enter`: Select item
  - `Escape`: Clear search

## Component Structure

```
Sidebar/
├── SidebarNew.tsx          # Main sidebar component
├── SidebarNew.scss         # Complete styling
├── TreeNode.tsx            # Recursive tree node component
├── SearchBar.tsx           # Search input with debouncing
├── store.ts                # Zustand state management
├── hooks.ts                # Custom hooks for functionality
├── navigationData.ts       # Hierarchical navigation data
├── types.ts                # TypeScript type definitions
├── index.ts                # Public exports
└── README.md               # This file
```

## Usage

### Basic Usage

```tsx
import { SidebarNew } from '@components/Sidebar';

function App() {
  return (
    <div className="app">
      <SidebarNew />
      <main>{/* Your content */}</main>
    </div>
  );
}
```

### Using with React Router

The component is already integrated with React Router. Make sure your app has the router setup:

```tsx
import { BrowserRouter } from 'react-router-dom';
import { SidebarNew } from '@components/Sidebar';

function App() {
  return (
    <BrowserRouter>
      <SidebarNew />
      {/* Routes */}
    </BrowserRouter>
  );
}
```

### Customizing Navigation Data

Modify `navigationData.ts` to add/remove sections or items:

```typescript
export const SIDEBAR_SECTIONS: SidebarSection[] = [
  {
    id: 'my-section',
    title: 'MY SECTION',
    icon: '🎯',
    defaultExpanded: true,
    items: [
      {
        id: 'my-item',
        label: 'My Item',
        path: '/my-path',
        icon: '📄',
        badge: 'NEW',
        tooltip: 'Description of my item',
        children: [/* nested items */],
      },
    ],
  },
];
```

## Navigation Data Structure

### Sections (6 Total)

#### 1. THEORY (📚)
- Law 0: Foundational Symmetry
- Laws 1-10: Core Principles (collapsible with 10 children)
- Laws 11-20: Field Dynamics (collapsible with 10 children)
- Laws 21-30: Gravitational Theory (collapsible with 10 children)
- Laws 31-38: Advanced Topics (collapsible with 8 children)
- Lagrangian Structure
- Field Equations
- Symmetry Breaking

#### 2. DERIVATIONS (🧪)
- 41 derivation folders (01_FORCE_UNIFICATION through 41_HAMILTONIAN)
- Each marked with 'PDF' badge

#### 3. CALCULATIONS (💫)
- Quick Calculate
- Particle Masses (10 sub-items: electron, muon, tau, quarks, neutrinos)
- Newton's G
- Fine Structure α
- Coupling Constants (3 sub-items: electromagnetic, strong, weak)

#### 4. VISUALIZATIONS (📊)
- Winding Numbers
- Phase Space
- Memory Evolution
- Epoch Ladder
- Field Configurations
- Symmetry Breaking

#### 5. EXPLANATIONS (📝)
- What is the Electron?
- What is Gravity?
- Consciousness
- Nature of Time
- Origin of Mass
- Electric Charge

#### 6. RESULTS (📈)
- Precision Table (NEW badge)
- Comparison Charts
- Key Achievements (count badge: 15)
- Predictions (TESTABLE badge)

## State Management

### Zustand Store

```typescript
import { useSidebarStore } from '@components/Sidebar';

function MyComponent() {
  const {
    expandedSections,
    expandedItems,
    searchQuery,
    pinnedItems,
    toggleSection,
    toggleItem,
    setSearchQuery,
    addPinnedItem,
    removePinnedItem,
  } = useSidebarStore();

  // Use the state...
}
```

### Persisted State
- `expandedSections`: Set of expanded section IDs
- `expandedItems`: Set of expanded item IDs
- `pinnedItems`: Array of pinned item IDs
- `recentItems`: Array of recently visited item IDs (last 10)

## Custom Hooks

### useDebounce
```typescript
const debouncedValue = useDebounce(searchQuery, 300);
```

### useSearchFilter
```typescript
const filteredItems = useSearchFilter(items, searchQuery);
```

### useNavigation
```typescript
const handleNavigate = useNavigation();
handleNavigate(item); // Navigates and tracks in recent items
```

### usePinItem
```typescript
const { togglePin, isPinned } = usePinItem();
togglePin(itemId);
const pinned = isPinned(itemId);
```

### useVirtualScroll
```typescript
const { startIndex, endIndex, offsetY, handleScroll, totalHeight } =
  useVirtualScroll(itemCount, itemHeight, containerHeight, overscan);
```

## Styling

The sidebar uses a dark theme with golden accents:

### Color Palette
- **Primary Gold**: `#c9a84e`
- **Accent Gold**: `#ffd700`
- **Background Dark**: `#1a1a1a` to `#0f0f0f` (gradient)
- **Text**: `#e0e0e0`
- **Border**: `rgba(201, 168, 78, 0.2)`

### Key CSS Classes
- `.sidebar-new`: Main container
- `.sidebar-new.collapsed`: Collapsed state (70px width)
- `.nav-section`: Section container
- `.tree-node`: Individual tree node
- `.tree-node-content.active`: Active item
- `.search-highlight`: Search result highlight

## Animations

All animations use smooth transitions:
- **Expand/Collapse**: 0.3s ease
- **Hover Effects**: 0.15s ease
- **Slide Down**: 0.3s ease-out
- **Tooltip Fade**: 0.15s ease-out

## Responsive Behavior

### Desktop (> 768px)
- Fixed sidebar, always visible
- Width: 320px (expanded), 70px (collapsed)

### Mobile (≤ 768px)
- Slide-in sidebar
- Hidden by default
- Full overlay when opened
- Auto-closes on navigation

## Accessibility

- ARIA labels on all interactive elements
- Keyboard navigation support
- Focus management
- Screen reader friendly
- High contrast mode compatible

## Performance Optimizations

1. **Debounced Search**: 300ms delay prevents excessive filtering
2. **Virtual Scrolling**: Hooks provided for large lists
3. **Memoized Filtering**: useMemo for expensive operations
4. **Lazy Expansion**: Only render expanded children
5. **CSS Animations**: Hardware-accelerated transforms

## Integration Notes

### Required Dependencies
- `react` ^19.2.0
- `react-router-dom` ^6.30.3
- `zustand` ^5.0.11
- `sass` ^1.97.3

### Path Aliases (tsconfig.json)
```json
{
  "compilerOptions": {
    "paths": {
      "@components/*": ["./src/components/*"],
      "@utils/*": ["./src/utils/*"],
      "@/*": ["./src/*"]
    }
  }
}
```

### App Store Integration
The sidebar uses both:
- `useAppStore()` from `@utils/store` for global app state (collapsed state, theme)
- `useSidebarStore()` from local store for sidebar-specific state

## Future Enhancements

Potential improvements:
1. Drag-and-drop reordering
2. Custom section colors
3. Icon customization
4. Export/import sidebar configuration
5. Multi-select for bulk operations
6. Breadcrumb navigation
7. Recent searches
8. Smart suggestions

## License

Part of the Golden Universe Visualizer project.
