export interface SidebarNavigationItem {
  id: string;
  label: string;
  icon?: string;
  path: string;
  badge?: number | string;
  tooltip?: string;
  children?: SidebarNavigationItem[];
  isPinned?: boolean;
  isNew?: boolean;
  metadata?: {
    count?: number;
    status?: 'complete' | 'in-progress' | 'pending';
    preview?: string;
  };
}

export interface SidebarSection {
  id: string;
  title: string;
  icon: string;
  items: SidebarNavigationItem[];
  collapsible?: boolean;
  defaultExpanded?: boolean;
}

export interface SidebarState {
  expandedSections: Set<string>;
  expandedItems: Set<string>;
  searchQuery: string;
  pinnedItems: string[];
  recentItems: string[];
  activeItemId: string | null;
}

export interface SidebarStore extends SidebarState {
  toggleSection: (sectionId: string) => void;
  toggleItem: (itemId: string) => void;
  setSearchQuery: (query: string) => void;
  addPinnedItem: (itemId: string) => void;
  removePinnedItem: (itemId: string) => void;
  addRecentItem: (itemId: string) => void;
  setActiveItem: (itemId: string | null) => void;
  expandAll: () => void;
  collapseAll: () => void;
  reset: () => void;
}

export interface TreeNodeProps {
  item: SidebarNavigationItem;
  depth: number;
  isExpanded: boolean;
  isActive: boolean;
  isPinned: boolean;
  onToggle: (id: string) => void;
  onNavigate: (item: SidebarNavigationItem) => void;
  onPin: (id: string) => void;
  searchQuery?: string;
}

export interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  onClear?: () => void;
}

export interface VirtualScrollProps {
  items: SidebarNavigationItem[];
  itemHeight: number;
  containerHeight: number;
  overscan?: number;
  renderItem: (item: SidebarNavigationItem, index: number) => React.ReactNode;
}
