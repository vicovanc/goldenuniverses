import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './BottomNav.scss';

export interface BottomNavItem {
  id: string;
  label: string;
  path: string;
  icon: string;
}

interface BottomNavProps {
  items?: BottomNavItem[];
  className?: string;
}

const DEFAULT_NAV_ITEMS: BottomNavItem[] = [
  {
    id: 'home',
    label: 'Home',
    path: '/',
    icon: '◈',
  },
  {
    id: 'theory',
    label: 'Theory',
    path: '/theory',
    icon: '◉',
  },
  {
    id: 'calculations',
    label: 'Calculate',
    path: '/calculations',
    icon: '◐',
  },
  {
    id: 'visualizations',
    label: 'Visualize',
    path: '/visualizations',
    icon: '◳',
  },
];

/**
 * Bottom navigation component for mobile devices
 * Provides easy access to main app sections with touch-friendly targets
 */
const BottomNav: React.FC<BottomNavProps> = ({
  items = DEFAULT_NAV_ITEMS,
  className = '',
}) => {
  const location = useLocation();

  const isActive = (path: string): boolean => {
    if (path === '/') {
      return location.pathname === '/';
    }
    return location.pathname.startsWith(path);
  };

  return (
    <nav className={`bottom-nav ${className}`} role="navigation" aria-label="Main navigation">
      <div className="bottom-nav__container">
        {items.map((item) => {
          const active = isActive(item.path);
          return (
            <Link
              key={item.id}
              to={item.path}
              className={`bottom-nav__item ${active ? 'active' : ''}`}
              aria-current={active ? 'page' : undefined}
            >
              <span className="bottom-nav__icon" role="img" aria-hidden="true">
                {item.icon}
              </span>
              <span className="bottom-nav__label">{item.label}</span>
              {active && <span className="bottom-nav__indicator" aria-hidden="true" />}
            </Link>
          );
        })}
      </div>
    </nav>
  );
};

export default BottomNav;
