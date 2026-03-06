import React, { ReactNode } from 'react';
import { useIsMobileOrTablet } from '@/hooks/useMediaQuery';
import './ResponsiveLayout.scss';

interface ResponsiveLayoutProps {
  children: ReactNode;
  sidebar?: ReactNode;
  header?: ReactNode;
  footer?: ReactNode;
  bottomNav?: ReactNode;
  className?: string;
}

/**
 * Responsive layout component that adapts to different screen sizes
 */
const ResponsiveLayout: React.FC<ResponsiveLayoutProps> = ({
  children,
  sidebar,
  header,
  footer,
  bottomNav,
  className = '',
}) => {
  const isMobileOrTablet = useIsMobileOrTablet();

  return (
    <div className={`responsive-layout ${className}`}>
      {header && <header className="responsive-layout__header">{header}</header>}

      <div className="responsive-layout__body">
        {sidebar && !isMobileOrTablet && (
          <aside className="responsive-layout__sidebar">{sidebar}</aside>
        )}

        <main className="responsive-layout__main">{children}</main>
      </div>

      {footer && <footer className="responsive-layout__footer">{footer}</footer>}

      {bottomNav && isMobileOrTablet && (
        <nav className="responsive-layout__bottom-nav">{bottomNav}</nav>
      )}
    </div>
  );
};

export default ResponsiveLayout;
