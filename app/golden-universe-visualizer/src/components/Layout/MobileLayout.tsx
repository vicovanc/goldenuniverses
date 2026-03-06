import React from 'react';
import { Outlet } from 'react-router-dom';
import { useAppStore } from '@utils/store';
import { useIsMobileOrTablet } from '@/hooks/useMediaQuery';
import Sidebar from '@components/Sidebar/Sidebar';
import BottomNav from '@components/Navigation/BottomNav';
import MobileHeader from '@components/Navigation/MobileHeader';
import InstallPrompt from '@components/PWA/InstallPrompt';
import './MobileLayout.scss';

/**
 * Mobile-optimized layout that switches between desktop and mobile views
 */
const MobileLayout: React.FC = () => {
  const { sidebarCollapsed, loading, error, setError } = useAppStore();
  const isMobileOrTablet = useIsMobileOrTablet();

  return (
    <div className="mobile-layout" data-mobile={isMobileOrTablet}>
      {/* Mobile Header - only shown on mobile/tablet */}
      {isMobileOrTablet && <MobileHeader />}

      {/* Desktop Sidebar - only shown on desktop */}
      {!isMobileOrTablet && <Sidebar />}

      {/* Main Content */}
      <main
        className={`mobile-layout__content ${
          !isMobileOrTablet && sidebarCollapsed ? 'expanded' : ''
        }`}
      >
        {loading && (
          <div className="mobile-layout__loading">
            <div className="spinner"></div>
            <p>Loading...</p>
          </div>
        )}

        {error && (
          <div className="mobile-layout__error">
            <span className="error-icon">⚠</span>
            <span className="error-message">{error}</span>
            <button
              className="error-close"
              onClick={() => setError(null)}
              aria-label="Dismiss error"
            >
              ✕
            </button>
          </div>
        )}

        <div className="mobile-layout__wrapper">
          <Outlet />
        </div>
      </main>

      {/* Bottom Navigation - only shown on mobile/tablet */}
      {isMobileOrTablet && <BottomNav />}

      {/* PWA Install Prompt */}
      <InstallPrompt />
    </div>
  );
};

export default MobileLayout;
