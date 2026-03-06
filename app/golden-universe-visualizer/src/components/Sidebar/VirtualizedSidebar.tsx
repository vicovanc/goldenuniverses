/**
 * Virtualized Sidebar Component
 * GU-052: Uses react-window for efficient rendering of long navigation lists
 */

import { useState, useMemo, useCallback } from 'react';
import { FixedSizeList as List } from 'react-window';
import { Link, useLocation } from 'react-router-dom';
import { useAppStore } from '@utils/store';
import { NAVIGATION_ITEMS } from '@utils/constants';
import type { NavigationItem } from '@/types';
import './Sidebar.scss';

interface FlatNavigationItem extends NavigationItem {
  depth: number;
  parentExpanded: boolean;
}

const VirtualizedSidebar: React.FC = () => {
  const location = useLocation();
  const { sidebarCollapsed, toggleSidebar } = useAppStore();
  const [expandedItems, setExpandedItems] = useState<Set<string>>(new Set());

  const toggleExpanded = useCallback((id: string): void => {
    setExpandedItems(prev => {
      const newExpanded = new Set(prev);
      if (newExpanded.has(id)) {
        newExpanded.delete(id);
      } else {
        newExpanded.add(id);
      }
      return newExpanded;
    });
  }, []);

  const isActive = useCallback((path: string): boolean => {
    return location.pathname === path;
  }, [location.pathname]);

  /**
   * Flatten navigation tree for virtualization
   */
  const flattenedItems = useMemo(() => {
    const flattened: FlatNavigationItem[] = [];

    const flatten = (items: NavigationItem[], depth: number = 0, parentExpanded: boolean = true) => {
      items.forEach(item => {
        flattened.push({ ...item, depth, parentExpanded });

        if (item.children && item.children.length > 0 && expandedItems.has(item.id) && parentExpanded) {
          flatten(item.children, depth + 1, true);
        }
      });
    };

    flatten(NAVIGATION_ITEMS);
    return flattened;
  }, [expandedItems]);

  /**
   * Render a single navigation item
   */
  const Row = useCallback(({ index, style }: { index: number; style: React.CSSProperties }) => {
    const item = flattenedItems[index];
    if (!item || !item.parentExpanded) return null;

    const hasChildren = item.children && item.children.length > 0;
    const isExpanded = expandedItems.has(item.id);
    const active = isActive(item.path);

    return (
      <div
        style={{
          ...style,
          paddingLeft: `${item.depth * 16 + 12}px`,
        }}
        className={`nav-item depth-${item.depth}`}
      >
        <div className={`nav-item-content ${active ? 'active' : ''}`}>
          <Link to={item.path} className="nav-link">
            {item.icon && <span className="nav-icon">{item.icon}</span>}
            {!sidebarCollapsed && <span className="nav-label">{item.label}</span>}
          </Link>
          {hasChildren && !sidebarCollapsed && (
            <button
              className="expand-button"
              onClick={() => toggleExpanded(item.id)}
              aria-label={isExpanded ? 'Collapse' : 'Expand'}
            >
              <span className={`arrow ${isExpanded ? 'expanded' : ''}`}>▶</span>
            </button>
          )}
        </div>
      </div>
    );
  }, [flattenedItems, expandedItems, sidebarCollapsed, isActive, toggleExpanded]);

  return (
    <aside className={`sidebar ${sidebarCollapsed ? 'collapsed' : ''}`}>
      <div className="sidebar-header">
        {!sidebarCollapsed && (
          <h1 className="sidebar-title">Golden Universe</h1>
        )}
        <button
          className="collapse-button"
          onClick={toggleSidebar}
          aria-label={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          <span className="hamburger-icon">
            {sidebarCollapsed ? '☰' : '✕'}
          </span>
        </button>
      </div>
      <nav className="sidebar-nav">
        <List
          height={window.innerHeight - 80} // Subtract header height
          itemCount={flattenedItems.length}
          itemSize={48} // Height of each nav item
          width="100%"
          overscanCount={5} // Render 5 extra items for smooth scrolling
        >
          {Row}
        </List>
      </nav>
    </aside>
  );
};

export default VirtualizedSidebar;
