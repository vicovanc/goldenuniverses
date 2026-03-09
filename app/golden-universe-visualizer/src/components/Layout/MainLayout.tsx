import { Outlet } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { useAppStore } from '@utils/store';
import SidebarNew from '@components/Sidebar/SidebarNew';
import { PerformanceDashboard } from '@components/Performance';
import './MainLayout.scss';

const MainLayout: React.FC = () => {
  const { sidebarCollapsed, loading, error, toggleSidebar } = useAppStore();
  const [isMobile, setIsMobile] = useState(false);

  // Detect mobile
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth <= 768);
    };

    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  // Handle backdrop click on mobile
  const handleBackdropClick = () => {
    if (!sidebarCollapsed && window.innerWidth <= 768) {
      toggleSidebar();
    }
  };

  return (
    <div className="main-layout">
      <SidebarNew />

      {/* Mobile backdrop */}
      <div
        className={`sidebar-backdrop ${!sidebarCollapsed ? 'active' : ''}`}
        onClick={handleBackdropClick}
        aria-hidden="true"
      />

      <main className={`main-content ${sidebarCollapsed ? 'expanded' : ''}`}>
        {loading && (
          <div className="loading-overlay">
            <div className="spinner"></div>
            <p>Loading...</p>
          </div>
        )}
        {error && (
          <div className="error-banner">
            <span className="error-icon">⚠</span>
            <span className="error-message">{error}</span>
            <button
              className="error-close"
              onClick={() => useAppStore.getState().setError(null)}
              aria-label="Dismiss error"
            >
              ✕
            </button>
          </div>
        )}
        <div className="content-wrapper">
          <Outlet />
        </div>
      </main>

      {/* Mobile menu toggle button */}
      {isMobile && sidebarCollapsed && (
        <button
          className="mobile-menu-toggle"
          onClick={toggleSidebar}
          aria-label="Open menu"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 12h18M3 6h18M3 18h18" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          </svg>
        </button>
      )}

      {/* Performance monitoring dashboard - disabled */}
      {/* {import.meta.env.DEV && <PerformanceDashboard />} */}
    </div>
  );
};

export default MainLayout;
