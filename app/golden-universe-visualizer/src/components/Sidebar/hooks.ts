import { useEffect, useState, useCallback, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import type { SidebarNavigationItem } from './types';
import { useSidebarStore } from './store';

/**
 * Debounced search hook
 */
export const useDebounce = <T,>(value: T, delay: number): T => {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
};

/**
 * Keyboard navigation hook
 */
export const useKeyboardNavigation = (
  items: SidebarNavigationItem[],
  onSelect: (item: SidebarNavigationItem) => void
) => {
  const [focusedIndex, setFocusedIndex] = useState(0);
  const flattenedItems = useRef<SidebarNavigationItem[]>([]);

  // Flatten the hierarchical structure for keyboard navigation
  useEffect(() => {
    const flatten = (items: SidebarNavigationItem[]): SidebarNavigationItem[] => {
      return items.reduce<SidebarNavigationItem[]>((acc, item) => {
        acc.push(item);
        if (item.children) {
          acc.push(...flatten(item.children));
        }
        return acc;
      }, []);
    };

    flattenedItems.current = flatten(items);
  }, [items]);

  const handleKeyDown = useCallback(
    (event: KeyboardEvent) => {
      const totalItems = flattenedItems.current.length;

      switch (event.key) {
        case 'ArrowDown':
          event.preventDefault();
          setFocusedIndex((prev) => (prev + 1) % totalItems);
          break;
        case 'ArrowUp':
          event.preventDefault();
          setFocusedIndex((prev) => (prev - 1 + totalItems) % totalItems);
          break;
        case 'Enter':
          event.preventDefault();
          if (flattenedItems.current[focusedIndex]) {
            onSelect(flattenedItems.current[focusedIndex]);
          }
          break;
        case 'Home':
          event.preventDefault();
          setFocusedIndex(0);
          break;
        case 'End':
          event.preventDefault();
          setFocusedIndex(totalItems - 1);
          break;
      }
    },
    [focusedIndex, onSelect]
  );

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleKeyDown]);

  return { focusedIndex, focusedItem: flattenedItems.current[focusedIndex] };
};

/**
 * Search filtering hook
 */
export const useSearchFilter = (
  items: SidebarNavigationItem[],
  searchQuery: string
): SidebarNavigationItem[] => {
  const filterItems = useCallback(
    (items: SidebarNavigationItem[], query: string): SidebarNavigationItem[] => {
      if (!query.trim()) return items;

      const lowerQuery = query.toLowerCase();

      return items.reduce<SidebarNavigationItem[]>((acc, item) => {
        const matchesLabel = item.label.toLowerCase().includes(lowerQuery);
        const matchesTooltip = item.tooltip?.toLowerCase().includes(lowerQuery);
        const filteredChildren = item.children
          ? filterItems(item.children, query)
          : [];

        if (matchesLabel || matchesTooltip || filteredChildren.length > 0) {
          acc.push({
            ...item,
            children: filteredChildren.length > 0 ? filteredChildren : item.children,
          });
        }

        return acc;
      }, []);
    },
    []
  );

  return filterItems(items, searchQuery);
};

/**
 * Active item tracking based on current route
 */
export const useActiveItem = () => {
  const location = useLocation();
  const { setActiveItem } = useSidebarStore();

  useEffect(() => {
    // Extract item ID from pathname
    const pathSegments = location.pathname.split('/').filter(Boolean);
    const itemId = pathSegments.join('-');
    setActiveItem(itemId || null);
  }, [location.pathname, setActiveItem]);
};

/**
 * Navigation handler with recent items tracking
 */
export const useNavigation = () => {
  const navigate = useNavigate();
  const { addRecentItem } = useSidebarStore();

  const handleNavigate = useCallback(
    (item: SidebarNavigationItem) => {
      navigate(item.path);
      addRecentItem(item.id);
    },
    [navigate, addRecentItem]
  );

  return handleNavigate;
};

/**
 * Pin/Unpin items functionality
 */
export const usePinItem = () => {
  const { pinnedItems, addPinnedItem, removePinnedItem } = useSidebarStore();

  const togglePin = useCallback(
    (itemId: string) => {
      if (pinnedItems.includes(itemId)) {
        removePinnedItem(itemId);
      } else {
        addPinnedItem(itemId);
      }
    },
    [pinnedItems, addPinnedItem, removePinnedItem]
  );

  const isPinned = useCallback(
    (itemId: string) => pinnedItems.includes(itemId),
    [pinnedItems]
  );

  return { togglePin, isPinned };
};

/**
 * Tooltip positioning hook
 */
export const useTooltip = () => {
  const [tooltipData, setTooltipData] = useState<{
    content: string;
    x: number;
    y: number;
    visible: boolean;
  }>({
    content: '',
    x: 0,
    y: 0,
    visible: false,
  });

  const showTooltip = useCallback((content: string, event: React.MouseEvent) => {
    const rect = event.currentTarget.getBoundingClientRect();
    setTooltipData({
      content,
      x: rect.right + 10,
      y: rect.top,
      visible: true,
    });
  }, []);

  const hideTooltip = useCallback(() => {
    setTooltipData((prev) => ({ ...prev, visible: false }));
  }, []);

  return { tooltipData, showTooltip, hideTooltip };
};

/**
 * Virtual scrolling hook for performance with large lists
 */
export const useVirtualScroll = (
  itemCount: number,
  itemHeight: number,
  containerHeight: number,
  overscan: number = 3
) => {
  const [scrollTop, setScrollTop] = useState(0);

  const visibleStart = Math.floor(scrollTop / itemHeight);
  const visibleEnd = Math.ceil((scrollTop + containerHeight) / itemHeight);

  const startIndex = Math.max(0, visibleStart - overscan);
  const endIndex = Math.min(itemCount - 1, visibleEnd + overscan);

  const offsetY = startIndex * itemHeight;

  const handleScroll = useCallback((event: React.UIEvent<HTMLDivElement>) => {
    setScrollTop(event.currentTarget.scrollTop);
  }, []);

  return {
    startIndex,
    endIndex,
    offsetY,
    handleScroll,
    totalHeight: itemCount * itemHeight,
  };
};

/**
 * Collapse/Expand animations hook
 */
export const useCollapseAnimation = (isExpanded: boolean) => {
  const [shouldRender, setShouldRender] = useState(isExpanded);
  const [animationClass, setAnimationClass] = useState('');

  useEffect(() => {
    if (isExpanded) {
      setShouldRender(true);
      requestAnimationFrame(() => {
        setAnimationClass('expanding');
      });
    } else {
      setAnimationClass('collapsing');
      const timer = setTimeout(() => {
        setShouldRender(false);
        setAnimationClass('');
      }, 300); // Match animation duration
      return () => clearTimeout(timer);
    }
  }, [isExpanded]);

  return { shouldRender, animationClass };
};
