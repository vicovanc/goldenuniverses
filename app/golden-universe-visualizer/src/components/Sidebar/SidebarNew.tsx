import React, { useMemo, useCallback, useEffect } from 'react';
import { useLocation, Link } from 'react-router-dom';
import { useAppStore } from '@utils/store';
import { useSidebarStore } from './store';
import { SIDEBAR_SECTIONS } from './navigationData';
// Removed dynamic derivations - using static link instead
import SearchBar from './SearchBar';
import TreeNode from './TreeNode';
import {
  useDebounce,
  useSearchFilter,
  useNavigation,
  usePinItem,
} from './hooks';
import type { SidebarNavigationItem } from './types';
import './SidebarNew.scss';

const SidebarNew: React.FC = () => {
  const location = useLocation();
  const { sidebarCollapsed, toggleSidebar } = useAppStore();
  const {
    expandedSections,
    expandedItems,
    searchQuery,
    pinnedItems,
    setSearchQuery,
    toggleSection,
    toggleItem,
    expandAll,
    collapseAll,
  } = useSidebarStore();

  const handleNavigate = useNavigation();
  const { togglePin, isPinned } = usePinItem();

  // Debounce search query for performance
  const debouncedSearchQuery = useDebounce(searchQuery, 300);

  // Use static sections directly (no dynamic derivations anymore)
  const sectionsWithDynamicData = SIDEBAR_SECTIONS;

  // Get pinned items for quick access
  const pinnedItemsList = useMemo(() => {
    const allItems: SidebarNavigationItem[] = [];

    const collectItems = (items: SidebarNavigationItem[]) => {
      items.forEach((item) => {
        allItems.push(item);
        if (item.children) {
          collectItems(item.children);
        }
      });
    };

    sectionsWithDynamicData.forEach((section) => {
      collectItems(section.items);
    });

    return allItems.filter((item) => pinnedItems.includes(item.id));
  }, [pinnedItems, sectionsWithDynamicData]);

  // Determine active item based on current path
  const activeItemId = useMemo(() => {
    const pathSegments = location.pathname.split('/').filter(Boolean);
    return pathSegments.join('-') || 'home';
  }, [location.pathname]);

  // Handle search clear
  const handleSearchClear = useCallback(() => {
    setSearchQuery('');
  }, [setSearchQuery]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      // Expand all: Ctrl/Cmd + Shift + E
      if ((event.ctrlKey || event.metaKey) && event.shiftKey && event.key === 'e') {
        event.preventDefault();
        expandAll();
      }
      // Collapse all: Ctrl/Cmd + Shift + C
      if ((event.ctrlKey || event.metaKey) && event.shiftKey && event.key === 'c') {
        event.preventDefault();
        collapseAll();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [expandAll, collapseAll]);

  // Mobile: Close sidebar on navigation
  useEffect(() => {
    if (window.innerWidth < 768) {
      if (!sidebarCollapsed) {
        toggleSidebar();
      }
    }
  }, [location.pathname]); // Don't include toggleSidebar to avoid loops

  return (
    <aside className={`sidebar-new ${sidebarCollapsed ? 'collapsed' : ''}`}>
      {/* Header */}
      <div className="sidebar-header">
        {!sidebarCollapsed && (
          <Link to="/" className="sidebar-branding">
            <img src="/logo.svg" alt="Golden Universe" className="brand-logo" />
            <h1 className="brand-title">Golden Universe</h1>
          </Link>
        )}
        <button
          className="toggle-button"
          onClick={toggleSidebar}
          aria-label={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          title={sidebarCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
            {sidebarCollapsed ? (
              <path d="M2 4h12M2 8h12M2 12h12" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            ) : (
              <path d="M4 4l8 8M12 4l-8 8" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            )}
          </svg>
        </button>
      </div>

      {/* Search Bar */}
      {!sidebarCollapsed && (
        <div className="sidebar-search">
          <SearchBar
            value={searchQuery}
            onChange={setSearchQuery}
            placeholder="Search navigation..."
            onClear={handleSearchClear}
          />
        </div>
      )}

      {/* Action Buttons */}
      {!sidebarCollapsed && (
        <div className="sidebar-actions">
          <button
            className="action-button"
            onClick={expandAll}
            title="Expand all sections (⌘⇧E)"
          >
            Expand All
          </button>
          <button
            className="action-button"
            onClick={collapseAll}
            title="Collapse all sections (⌘⇧C)"
          >
            Collapse All
          </button>
        </div>
      )}

      {/* Navigation Content */}
      <nav className="sidebar-nav" role="navigation" aria-label="Main navigation">
        {/* Pinned Items Section */}
        {!sidebarCollapsed && pinnedItemsList.length > 0 && (
          <div className="nav-section pinned-section">
            <div className="section-header">
              <span className="section-icon">
                <svg width="14" height="14" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M9.5 1L11 2.5L9.5 4L12 6.5L7.5 11L6 9.5L4 11.5L3 15L6.5 14L8.5 12L7 10.5L11.5 6L14 8.5L15.5 7L14 5.5L15.5 4L14 2.5L12.5 4L11 2.5L9.5 1Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </span>
              <h2 className="section-title">PINNED</h2>
              <span className="section-count">{pinnedItemsList.length}</span>
            </div>
            <div className="section-content">
              {pinnedItemsList.map((item) => (
                <TreeNode
                  key={item.id}
                  item={item}
                  depth={0}
                  isExpanded={expandedItems.has(item.id)}
                  isActive={activeItemId === item.id}
                  isPinned={true}
                  onToggle={toggleItem}
                  onNavigate={handleNavigate}
                  onPin={togglePin}
                  searchQuery={debouncedSearchQuery}
                />
              ))}
            </div>
            <div className="section-divider" />
          </div>
        )}

        {/* Main Navigation Sections */}
        {sectionsWithDynamicData.map((section) => {
          const isExpanded = expandedSections.has(section.id);
          const filteredItems = useSearchFilter(section.items, debouncedSearchQuery);

          // Hide empty sections when searching
          if (debouncedSearchQuery && filteredItems.length === 0) {
            return null;
          }

          return (
            <div
              key={section.id}
              className={`nav-section ${isExpanded ? 'expanded' : 'collapsed'}`}
            >
              <button
                className="section-header"
                onClick={() => toggleSection(section.id)}
                aria-expanded={isExpanded}
                aria-label={`${section.title} section`}
              >
                <span className="section-icon">{section.icon}</span>
                {!sidebarCollapsed && (
                  <>
                    <h2 className="section-title">{section.title}</h2>
                    <span className="section-count">{filteredItems.length}</span>
                    <span className={`section-arrow ${isExpanded ? 'expanded' : ''}`}>
                      ▶
                    </span>
                  </>
                )}
              </button>

              {isExpanded && !sidebarCollapsed && (
                <div className="section-content">
                  {filteredItems.map((item) => (
                    <TreeNode
                      key={item.id}
                      item={item}
                      depth={0}
                      isExpanded={expandedItems.has(item.id)}
                      isActive={activeItemId === item.id}
                      isPinned={isPinned(item.id)}
                      onToggle={toggleItem}
                      onNavigate={handleNavigate}
                      onPin={togglePin}
                      searchQuery={debouncedSearchQuery}
                    />
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </nav>

      {/* Footer */}
      {!sidebarCollapsed && (
        <div className="sidebar-footer">
          <div className="footer-stats">
            <div className="stat-item">
              <svg className="stat-icon" width="14" height="14" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 2h10a1 1 0 011 1v10a1 1 0 01-1 1H3a1 1 0 01-1-1V3a1 1 0 011-1z" stroke="currentColor" strokeWidth="1.5"/>
                <path d="M6 6h4M6 9h4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
              </svg>
              <span className="stat-value">39</span>
              <span className="stat-label">Laws</span>
            </div>
            <div className="stat-item">
              <svg className="stat-icon" width="14" height="14" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="8" cy="8" r="6" stroke="currentColor" strokeWidth="1.5"/>
                <path d="M8 5v3l2 2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
              </svg>
              <span className="stat-value">45</span>
              <span className="stat-label">Deriv</span>
            </div>
          </div>
          <div className="footer-version">v1.0.0</div>
        </div>
      )}
    </aside>
  );
};

export default SidebarNew;
