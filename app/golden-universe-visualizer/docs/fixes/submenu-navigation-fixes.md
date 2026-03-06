# Submenu Navigation Fixes Checklist

## Investigation Date: February 28, 2026

## Problem Summary
The submenu navigation in the Golden Universe Visualizer app is not working. Clicking on submenu items doesn't navigate to the appropriate pages. The issue affects the entire sidebar navigation system across all pages.

## Root Causes Identified

### 1. ❌ **Critical Logic Bug in TreeNode Component**
**Location:** `src/components/Sidebar/TreeNode.tsx`, lines 26-36
**Issue:** Parent items with children only toggle expansion, never navigate
**Status:** NEEDS FIX

### 2. ❌ **Missing Auto-Expand Logic**
**Location:** `src/components/Sidebar/SidebarNew.tsx`
**Issue:** Parent sections don't auto-expand when visiting child routes
**Status:** NEEDS FIX

### 3. ❌ **Inconsistent Navigation Data**
**Location:** Multiple files using different data structures
**Issue:** Two separate navigation data sources causing confusion
**Status:** NEEDS FIX

### 4. ❌ **Event Handling Conflicts**
**Location:** `src/components/Sidebar/TreeNode.tsx`
**Issue:** Click event propagation issues between parent and child elements
**Status:** NEEDS FIX

### 5. ❌ **No Active State Persistence**
**Location:** Navigation state management
**Issue:** Expanded states are lost on page refresh
**Status:** NEEDS FIX

---

## Fixes Checklist

### Priority 1: Critical Fixes (Do First)

#### ✅ Fix 1: Update TreeNode Click Handler
**File:** `src/components/Sidebar/TreeNode.tsx`
**Lines to Change:** 26-36

**Current Code (BROKEN):**
```tsx
const handleClick = useCallback(
  (event: React.MouseEvent) => {
    event.preventDefault();
    if (hasChildren) {
      onToggle(item.id);  // Only toggles, never navigates
    } else {
      onNavigate(item);
    }
  },
  [hasChildren, item, onToggle, onNavigate]
);
```

**Fixed Code:**
```tsx
const handleClick = useCallback(
  (event: React.MouseEvent) => {
    event.preventDefault();

    // Always navigate if the item has a path
    if (item.path) {
      onNavigate(item);
    }

    // Also expand if it has children
    if (hasChildren) {
      onToggle(item.id);
    }
  },
  [hasChildren, item, onToggle, onNavigate]
);
```

---

#### ✅ Fix 2: Implement Auto-Expand for Active Routes
**File:** `src/components/Sidebar/SidebarNew.tsx`
**Add after line 50 (in component body):**

```tsx
// Auto-expand parent items when their children are active
useEffect(() => {
  const currentPath = location.pathname;

  // Find all parent items that should be expanded
  const itemsToExpand: string[] = [];

  const checkForActiveChild = (items: NavigationItem[]) => {
    items.forEach(item => {
      if (item.children) {
        const hasActiveChild = item.children.some(child =>
          child.path === currentPath ||
          (child.children && checkForActiveChild([child]))
        );

        if (hasActiveChild || item.path === currentPath) {
          itemsToExpand.push(item.id);
        }

        // Recursively check nested children
        checkForActiveChild(item.children);
      }
    });

    return false;
  };

  SIDEBAR_SECTIONS.forEach(section => {
    if (section.items) {
      checkForActiveChild(section.items);
    }
  });

  // Expand all parent items
  itemsToExpand.forEach(id => {
    if (!expandedItems.includes(id)) {
      toggleExpanded(id);
    }
  });
}, [location.pathname]);
```

---

### Priority 2: Enhanced Fixes

#### ✅ Fix 3: Separate Click Areas for Expand vs Navigate
**File:** `src/components/Sidebar/TreeNode.tsx`
**Replace lines 108-163 with:**

```tsx
<div className={nodeClasses}>
  <div className="tree-node-content">
    {/* Expand/Collapse button - separate click area */}
    {hasChildren && (
      <button
        className="expand-toggle"
        onClick={handleToggle}
        aria-label={isExpanded ? 'Collapse' : 'Expand'}
      >
        <svg className="expand-icon" viewBox="0 0 20 20">
          <path d={isExpanded ? 'M5 8l5 5 5-5' : 'M8 5l5 5-5 5'} />
        </svg>
      </button>
    )}

    {/* Clickable area for navigation */}
    <div
      className="node-main"
      onClick={handleClick}
      style={{ cursor: item.path ? 'pointer' : 'default' }}
    >
      {item.icon && (
        <span className="node-icon" role="img" aria-label={item.label}>
          {item.icon}
        </span>
      )}
      <span className="node-label">{item.label}</span>
    </div>

    <div className="node-actions">
      {item.badge && (
        <span className={`node-badge ${item.badgeVariant || ''}`}>
          {item.badge}
        </span>
      )}
      {onPin && (
        <button
          className={`pin-button ${isPinned ? 'pinned' : ''}`}
          onClick={handlePin}
          aria-label={isPinned ? 'Unpin' : 'Pin'}
        >
          📌
        </button>
      )}
    </div>
  </div>

  {/* Children rendering remains the same */}
  {hasChildren && isExpanded && (
    <div className="tree-children">
      {item.children?.map((child) => (
        <TreeNode
          key={child.id}
          item={child}
          depth={depth + 1}
          onNavigate={onNavigate}
          onToggle={onToggle}
          expandedItems={expandedItems}
          onPin={onPin}
          pinnedItems={pinnedItems}
        />
      ))}
    </div>
  )}
</div>
```

---

#### ✅ Fix 4: Consolidate Navigation Data
**Action Required:** Choose one source of truth

**Option A (Recommended):** Use `SIDEBAR_SECTIONS` everywhere
1. Update `MobileMenu.tsx` to use `SIDEBAR_SECTIONS` from `navigationData.ts`
2. Update `BottomNav.tsx` to use `SIDEBAR_SECTIONS`
3. Delete `NAVIGATION_ITEMS` from `constants.ts`

**Option B:** Sync both data structures
1. Update `NAVIGATION_ITEMS` in `constants.ts` to match `SIDEBAR_SECTIONS` structure
2. Keep both but ensure they're always in sync

---

### Priority 3: State Management Fixes

#### ✅ Fix 5: Persist Expanded State in Local Storage
**File:** `src/components/Sidebar/store.ts`
**Add to the store:**

```tsx
// Add to the store interface
interface SidebarStore {
  // ... existing properties
  loadExpandedFromStorage: () => void;
  saveExpandedToStorage: (items: string[]) => void;
}

// In the store implementation
loadExpandedFromStorage: () => {
  const saved = localStorage.getItem('sidebar-expanded-items');
  if (saved) {
    set({ expandedItems: JSON.parse(saved) });
  }
},

saveExpandedToStorage: (items) => {
  localStorage.setItem('sidebar-expanded-items', JSON.stringify(items));
},

// Update toggleExpanded to save state
toggleExpanded: (id) =>
  set((state) => {
    const newExpanded = state.expandedItems.includes(id)
      ? state.expandedItems.filter((item) => item !== id)
      : [...state.expandedItems, id];

    // Save to localStorage
    localStorage.setItem('sidebar-expanded-items', JSON.stringify(newExpanded));

    return { expandedItems: newExpanded };
  }),
```

---

### Priority 4: Visual Feedback

#### ✅ Fix 6: Add Active State Styling
**File:** `src/components/Sidebar/TreeNode.tsx`
**Add active state detection:**

```tsx
// Add after line 20
const isActive = location.pathname === item.path;

// Update nodeClasses
const nodeClasses = clsx('tree-node', {
  'is-expanded': isExpanded,
  'has-children': hasChildren,
  'is-pinned': isPinned,
  'is-active': isActive,  // Add this
  [`depth-${depth}`]: true,
});
```

**File:** `src/components/Sidebar/TreeNode.scss`
**Add styling:**

```scss
.tree-node {
  &.is-active {
    > .tree-node-content {
      background: rgba(212, 175, 55, 0.1);
      border-left: 3px solid var(--color-gold);

      .node-label {
        color: var(--color-gold);
        font-weight: 600;
      }
    }
  }
}
```

---

## Testing Checklist

After implementing fixes, test the following:

### Navigation Tests
- [ ] Click parent item with children → navigates AND expands
- [ ] Click expand button → only expands/collapses
- [ ] Click child item → navigates to child page
- [ ] Parent stays expanded when navigating to child
- [ ] Active item is highlighted
- [ ] Refresh page → expanded states persist
- [ ] Deep navigation works (3+ levels)

### Cross-Page Tests
- [ ] Test on Theory page with laws submenu
- [ ] Test on Derivations page with epochs submenu
- [ ] Test on Calculations page with nested items
- [ ] Test on Visualizations page
- [ ] Test on Explanations page with new theory papers section

### Mobile Tests
- [ ] Mobile menu shows all submenu items
- [ ] Touch events work properly
- [ ] Hamburger menu toggle works
- [ ] Bottom navigation reflects current page

---

## Files to Modify

1. **src/components/Sidebar/TreeNode.tsx** - Fix click handlers
2. **src/components/Sidebar/SidebarNew.tsx** - Add auto-expand logic
3. **src/components/Sidebar/store.ts** - Add persistence
4. **src/components/Sidebar/TreeNode.scss** - Add active styles
5. **src/components/Navigation/MobileMenu.tsx** - Update data source
6. **src/utils/constants.ts** - Clean up navigation data

---

## Implementation Order

1. **First:** Fix TreeNode click handler (Fix 1)
2. **Second:** Add auto-expand logic (Fix 2)
3. **Third:** Add active state styling (Fix 6)
4. **Fourth:** Separate click areas (Fix 3)
5. **Fifth:** Add state persistence (Fix 5)
6. **Last:** Consolidate navigation data (Fix 4)

---

## Verification Steps

1. Run `npm run dev`
2. Open http://localhost:3000
3. Navigate to `/explanations/consciousness`
4. Verify:
   - "Explanations" parent is expanded
   - "Consciousness" item is highlighted
   - Can click "Explanations" to go to main page
   - Can click expand button to collapse without navigating
5. Refresh page
6. Verify expanded state persists
7. Test all items in the testing checklist

---

## Notes

- The main issue was in the TreeNode component's handleClick function
- Parent items need dual functionality: navigate AND expand
- State persistence improves UX significantly
- Mobile navigation needs the same fixes applied
- Consider adding breadcrumbs for better navigation context

---

## Status: READY FOR IMPLEMENTATION

Generated: February 28, 2026
Priority: CRITICAL - Users cannot navigate the application properly
Impact: Affects all pages and all users
Estimated Time: 2-3 hours for all fixes