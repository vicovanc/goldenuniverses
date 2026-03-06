import React, { useState } from 'react';
import { useAppStore } from '@utils/store';
import MobileMenu from './MobileMenu';
import './MobileHeader.scss';

interface MobileHeaderProps {
  title?: string;
  className?: string;
}

/**
 * Mobile header with hamburger menu and branding
 */
const MobileHeader: React.FC<MobileHeaderProps> = ({
  title = 'Golden Universe',
  className = '',
}) => {
  const [menuOpen, setMenuOpen] = useState(false);
  const { theme } = useAppStore();

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
  };

  return (
    <>
      <header className={`mobile-header ${className}`} data-theme={theme}>
        <button
          className="mobile-header__menu-button touch-target"
          onClick={toggleMenu}
          aria-label="Open menu"
          aria-expanded={menuOpen}
        >
          <span className="hamburger">
            <span className="hamburger__line"></span>
            <span className="hamburger__line"></span>
            <span className="hamburger__line"></span>
          </span>
        </button>

        <h1 className="mobile-header__title">{title}</h1>

        <div className="mobile-header__actions">
          {/* Placeholder for future actions like search, notifications, etc. */}
        </div>
      </header>

      <MobileMenu isOpen={menuOpen} onClose={() => setMenuOpen(false)} />
    </>
  );
};

export default MobileHeader;
