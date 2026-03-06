import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAppStore } from '@utils/store';
import { NAVIGATION_ITEMS } from '@utils/constants';
import type { NavigationItem } from '@/types';
import './Sidebar.scss';

const Sidebar: React.FC = () => {
  const location = useLocation();
  const { sidebarCollapsed, toggleSidebar } = useAppStore();
  const [expandedItems, setExpandedItems] = useState<Set<string>>(new Set());

  const toggleExpanded = (id: string): void => {
    const newExpanded = new Set(expandedItems);
    if (newExpanded.has(id)) {
      newExpanded.delete(id);
    } else {
      newExpanded.add(id);
    }
    setExpandedItems(newExpanded);
  };

  const isActive = (path: string): boolean => {
    // Exact match
    if (location.pathname === path) return true;

    // For derivations, check if we're on a specific derivation page
    if (path === '/derivations' && location.pathname.startsWith('/derivations/')) {
      return true;
    }

    // For other pages with sub-routes, check if the path starts with the item path
    if (path !== '/' && location.pathname.startsWith(path + '/')) {
      return true;
    }

    return false;
  };

  const renderNavItem = (item: NavigationItem, depth: number = 0): React.ReactElement => {
    const hasChildren = item.children && item.children.length > 0;
    const isExpanded = expandedItems.has(item.id);
    const active = isActive(item.path);

    return (
      <div key={item.id} className={`nav-item depth-${depth}`}>
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
        {hasChildren && isExpanded && !sidebarCollapsed && (
          <div className="nav-children">
            {item.children?.map((child) => renderNavItem(child, depth + 1))}
          </div>
        )}
      </div>
    );
  };

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
        {NAVIGATION_ITEMS.map((item) => renderNavItem(item))}
      </nav>
    </aside>
  );
};

export default Sidebar;
