import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAppStore } from '@utils/store';
import { NAVIGATION_ITEMS } from '@utils/constants';
import type { NavigationItem } from '@/types';
import './MobileMenu.scss';

interface MobileMenuProps {
  isOpen: boolean;
  onClose: () => void;
}

/**
 * Full-screen mobile menu with nested navigation
 */
const MobileMenu: React.FC<MobileMenuProps> = ({ isOpen, onClose }) => {
  const location = useLocation();
  const { theme, setTheme } = useAppStore();
  const [expandedItems, setExpandedItems] = useState<Set<string>>(new Set());

  // Close menu on route change
  useEffect(() => {
    onClose();
  }, [location.pathname, onClose]);

  // Prevent body scroll when menu is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

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
    if (path === '/') {
      return location.pathname === '/';
    }
    return location.pathname.startsWith(path);
  };

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  const renderNavItem = (item: NavigationItem, depth: number = 0): React.ReactElement => {
    const hasChildren = item.children && item.children.length > 0;
    const isExpanded = expandedItems.has(item.id);
    const active = isActive(item.path);

    return (
      <div key={item.id} className={`mobile-menu__item depth-${depth}`}>
        <div className={`mobile-menu__item-content ${active ? 'active' : ''}`}>
          <Link to={item.path} className="mobile-menu__link">
            {item.icon && <span className="mobile-menu__icon">{item.icon}</span>}
            <span className="mobile-menu__label">{item.label}</span>
          </Link>
          {hasChildren && (
            <button
              className="mobile-menu__expand"
              onClick={() => toggleExpanded(item.id)}
              aria-label={isExpanded ? 'Collapse' : 'Expand'}
              aria-expanded={isExpanded}
            >
              <span className={`arrow ${isExpanded ? 'expanded' : ''}`}>▶</span>
            </button>
          )}
        </div>
        {hasChildren && isExpanded && (
          <div className="mobile-menu__children">
            {item.children?.map((child) => renderNavItem(child, depth + 1))}
          </div>
        )}
      </div>
    );
  };

  if (!isOpen) return null;

  return (
    <>
      <div className="mobile-menu-overlay" onClick={onClose} aria-hidden="true" />
      <div className={`mobile-menu ${isOpen ? 'open' : ''}`} role="dialog" aria-modal="true">
        <div className="mobile-menu__header">
          <h2 className="mobile-menu__title">Golden Universe</h2>
          <button
            className="mobile-menu__close touch-target"
            onClick={onClose}
            aria-label="Close menu"
          >
            ✕
          </button>
        </div>

        <nav className="mobile-menu__nav" role="navigation">
          {NAVIGATION_ITEMS.map((item) => renderNavItem(item))}
        </nav>

        <div className="mobile-menu__footer">
          <button
            className="mobile-menu__theme-toggle touch-target"
            onClick={toggleTheme}
            aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
          >
            <span className="theme-icon">{theme === 'dark' ? '☀️' : '🌙'}</span>
            <span className="theme-label">
              {theme === 'dark' ? 'Light Mode' : 'Dark Mode'}
            </span>
          </button>
        </div>
      </div>
    </>
  );
};

export default MobileMenu;
