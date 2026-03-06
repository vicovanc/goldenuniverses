import React, { useCallback, useState, useRef, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import type { TreeNodeProps } from './types';
import { useCollapseAnimation } from './hooks';
import { useSidebarStore } from './store';

const TreeNode: React.FC<TreeNodeProps> = ({
  item,
  depth,
  isExpanded,
  isActive,
  isPinned,
  onToggle,
  onNavigate,
  onPin,
  searchQuery,
}) => {
  const location = useLocation();
  const { expandedItems, pinnedItems } = useSidebarStore();
  const hasChildren = item.children && item.children.length > 0;
  const [showTooltip, setShowTooltip] = useState(false);
  const [tooltipPosition, setTooltipPosition] = useState({ x: 0, y: 0 });
  const nodeRef = useRef<HTMLDivElement>(null);
  const { shouldRender, animationClass } = useCollapseAnimation(isExpanded);

  const handleClick = useCallback(
    (event: React.MouseEvent) => {
      event.preventDefault();

      // Always navigate if the item has a path
      if (item.path) {
        onNavigate(item);
      }

      // Also expand/collapse if it has children
      if (hasChildren) {
        onToggle(item.id);
      }
    },
    [hasChildren, item, onToggle, onNavigate]
  );

  const handleToggle = useCallback(
    (event: React.MouseEvent) => {
      event.stopPropagation();
      onToggle(item.id);
    },
    [item.id, onToggle]
  );

  const handlePin = useCallback(
    (event: React.MouseEvent) => {
      event.stopPropagation();
      event.preventDefault();
      onPin(item.id);
    },
    [item.id, onPin]
  );

  const handleMouseEnter = useCallback((event: React.MouseEvent) => {
    const rect = event.currentTarget.getBoundingClientRect();
    setTooltipPosition({
      x: rect.right + 10,
      y: rect.top,
    });
    setShowTooltip(true);
  }, []);

  const handleMouseLeave = useCallback(() => {
    setShowTooltip(false);
  }, []);

  // Highlight search matches
  const highlightText = useCallback(
    (text: string, query: string) => {
      if (!query.trim()) return text;

      const parts = text.split(new RegExp(`(${query})`, 'gi'));
      return parts.map((part, index) =>
        part.toLowerCase() === query.toLowerCase() ? (
          <mark key={index} className="search-highlight">
            {part}
          </mark>
        ) : (
          part
        )
      );
    },
    []
  );

  // Auto-expand if search matches child
  useEffect(() => {
    if (searchQuery && hasChildren && !isExpanded) {
      const searchInChildren = (items: typeof item.children): boolean => {
        if (!items) return false;
        return items.some(
          (child) =>
            child.label.toLowerCase().includes(searchQuery.toLowerCase()) ||
            searchInChildren(child.children)
        );
      };

      if (searchInChildren(item.children)) {
        onToggle(item.id);
      }
    }
  }, [searchQuery, hasChildren, isExpanded, item.children, item.id, onToggle]);

  const paddingLeft = `${depth * 1.5 + 1}rem`;

  return (
    <div className={`tree-node depth-${depth}`} ref={nodeRef}>
      <div
        className={`tree-node-content ${isActive ? 'active' : ''} ${
          isPinned ? 'pinned' : ''
        }`}
        onClick={handleClick}
        onMouseEnter={item.tooltip ? handleMouseEnter : undefined}
        onMouseLeave={item.tooltip ? handleMouseLeave : undefined}
        style={{ paddingLeft }}
        role="button"
        tabIndex={0}
        aria-expanded={hasChildren ? isExpanded : undefined}
        aria-label={item.label}
      >
        {hasChildren && (
          <button
            className={`expand-toggle ${isExpanded ? 'expanded' : ''}`}
            onClick={handleToggle}
            aria-label={isExpanded ? 'Collapse' : 'Expand'}
            type="button"
          >
            <span className="arrow">▶</span>
          </button>
        )}

        <div className="node-main">
          {item.icon && <span className="node-icon">{item.icon}</span>}
          <span className="node-label">
            {searchQuery
              ? highlightText(item.label, searchQuery)
              : item.label}
          </span>
        </div>

        <div className="node-actions">
          {item.badge && (
            <span
              className={`node-badge ${
                typeof item.badge === 'number' ? 'count' : 'status'
              }`}
            >
              {item.badge}
            </span>
          )}

          <button
            className={`pin-button ${isPinned ? 'active' : ''}`}
            onClick={handlePin}
            aria-label={isPinned ? 'Unpin' : 'Pin'}
            type="button"
            title={isPinned ? 'Unpin item' : 'Pin item'}
          >
            {isPinned ? '◉' : '○'}
          </button>
        </div>
      </div>

      {hasChildren && shouldRender && (
        <div className={`tree-node-children ${animationClass}`}>
          {item.children?.map((child) => {
            // Determine if this child is active based on its path
            const currentPath = location.pathname;
            const isChildActive = currentPath === child.path;
            const isChildExpanded = expandedItems.has(child.id);
            const isChildPinned = pinnedItems.includes(child.id);

            return (
              <TreeNode
                key={child.id}
                item={child}
                depth={depth + 1}
                isExpanded={isChildExpanded}
                isActive={isChildActive}
                isPinned={isChildPinned}
                onToggle={onToggle}
                onNavigate={onNavigate}
                onPin={onPin}
                searchQuery={searchQuery}
              />
            );
          })}
        </div>
      )}

      {showTooltip && item.tooltip && (
        <div
          className="tree-node-tooltip"
          style={{
            left: `${tooltipPosition.x}px`,
            top: `${tooltipPosition.y}px`,
          }}
        >
          {item.tooltip}
        </div>
      )}
    </div>
  );
};

export default TreeNode;
