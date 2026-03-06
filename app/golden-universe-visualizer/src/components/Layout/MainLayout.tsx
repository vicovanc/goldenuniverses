import { Outlet } from 'react-router-dom';
import { useAppStore } from '@utils/store';
import SidebarNew from '@components/Sidebar/SidebarNew';
import { PerformanceDashboard } from '@components/Performance';
import './MainLayout.scss';

const MainLayout: React.FC = () => {
  const { sidebarCollapsed, loading, error } = useAppStore();

  return (
    <div className="main-layout">
      <SidebarNew />
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
      {/* Performance monitoring dashboard - only in development */}
      {import.meta.env.DEV && <PerformanceDashboard />}
    </div>
  );
};

export default MainLayout;
