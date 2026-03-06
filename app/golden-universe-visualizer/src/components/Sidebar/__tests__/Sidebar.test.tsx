import { describe, it, expect, vi, beforeEach } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { renderWithProviders } from '@/test/utils/test-utils';
import Sidebar from '../Sidebar';
import { useAppStore } from '@utils/store';

// Mock the store
vi.mock('@utils/store', () => ({
  useAppStore: vi.fn(),
}));

// Mock constants
vi.mock('@utils/constants', () => ({
  NAVIGATION_ITEMS: [
    {
      id: 'home',
      label: 'Home',
      path: '/',
      icon: '🏠',
    },
    {
      id: 'theory',
      label: 'Theory',
      path: '/theory',
      icon: '📚',
      children: [
        {
          id: 'fundamentals',
          label: 'Fundamentals',
          path: '/theory/fundamentals',
        },
        {
          id: 'equations',
          label: 'Equations',
          path: '/theory/equations',
        },
      ],
    },
    {
      id: 'calculations',
      label: 'Calculations',
      path: '/calculations',
      icon: '🧮',
    },
  ],
}));

describe('Sidebar', () => {
  const mockToggleSidebar = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    (useAppStore as any).mockReturnValue({
      sidebarCollapsed: false,
      toggleSidebar: mockToggleSidebar,
    });
  });

  describe('Rendering', () => {
    it('should render sidebar with title', () => {
      renderWithProviders(<Sidebar />);
      expect(screen.getByText('Golden Universe')).toBeInTheDocument();
    });

    it('should render navigation items', () => {
      renderWithProviders(<Sidebar />);
      expect(screen.getByText('Home')).toBeInTheDocument();
      expect(screen.getByText('Theory')).toBeInTheDocument();
      expect(screen.getByText('Calculations')).toBeInTheDocument();
    });

    it('should render collapse button', () => {
      renderWithProviders(<Sidebar />);
      const collapseButton = screen.getByLabelText('Collapse sidebar');
      expect(collapseButton).toBeInTheDocument();
    });

    it('should hide title when collapsed', () => {
      (useAppStore as any).mockReturnValue({
        sidebarCollapsed: true,
        toggleSidebar: mockToggleSidebar,
      });

      renderWithProviders(<Sidebar />);
      expect(screen.queryByText('Golden Universe')).not.toBeInTheDocument();
    });
  });

  describe('Navigation', () => {
    it('should highlight active navigation item', () => {
      renderWithProviders(<Sidebar />);
      const homeLink = screen.getByText('Home').closest('.nav-item-content');
      expect(homeLink).toHaveClass('active');
    });

    it('should navigate when clicking on item', async () => {
      const user = userEvent.setup();
      renderWithProviders(<Sidebar />);

      const theoryLink = screen.getByText('Theory');
      await user.click(theoryLink);

      // Navigation happens via react-router-dom Link
      expect(theoryLink.closest('a')).toHaveAttribute('href', '/theory');
    });

    it('should render navigation icons', () => {
      renderWithProviders(<Sidebar />);
      const icons = screen.getAllByClassName('nav-icon');
      expect(icons.length).toBeGreaterThan(0);
    });
  });

  describe('Expandable Items', () => {
    it('should not show children initially', () => {
      renderWithProviders(<Sidebar />);
      expect(screen.queryByText('Fundamentals')).not.toBeInTheDocument();
      expect(screen.queryByText('Equations')).not.toBeInTheDocument();
    });

    it('should show expand button for items with children', () => {
      renderWithProviders(<Sidebar />);
      const theoryItem = screen.getByText('Theory').closest('.nav-item');
      const expandButton = theoryItem?.querySelector('.expand-button');
      expect(expandButton).toBeInTheDocument();
    });

    it('should expand children when clicking expand button', async () => {
      const user = userEvent.setup();
      renderWithProviders(<Sidebar />);

      const theoryItem = screen.getByText('Theory').closest('.nav-item');
      const expandButton = theoryItem?.querySelector('.expand-button');

      if (expandButton) {
        await user.click(expandButton as Element);
        await waitFor(() => {
          expect(screen.getByText('Fundamentals')).toBeInTheDocument();
          expect(screen.getByText('Equations')).toBeInTheDocument();
        });
      }
    });

    it('should collapse children when clicking expand button again', async () => {
      const user = userEvent.setup();
      renderWithProviders(<Sidebar />);

      const theoryItem = screen.getByText('Theory').closest('.nav-item');
      const expandButton = theoryItem?.querySelector('.expand-button');

      if (expandButton) {
        // Expand
        await user.click(expandButton as Element);
        await waitFor(() => {
          expect(screen.getByText('Fundamentals')).toBeInTheDocument();
        });

        // Collapse
        await user.click(expandButton as Element);
        await waitFor(() => {
          expect(screen.queryByText('Fundamentals')).not.toBeInTheDocument();
        });
      }
    });

    it('should not show expand button when collapsed', () => {
      (useAppStore as any).mockReturnValue({
        sidebarCollapsed: true,
        toggleSidebar: mockToggleSidebar,
      });

      renderWithProviders(<Sidebar />);
      const expandButtons = screen.queryAllByClassName('expand-button');
      expect(expandButtons.length).toBe(0);
    });
  });

  describe('Collapse/Expand Functionality', () => {
    it('should call toggleSidebar when clicking collapse button', async () => {
      const user = userEvent.setup();
      renderWithProviders(<Sidebar />);

      const collapseButton = screen.getByLabelText('Collapse sidebar');
      await user.click(collapseButton);

      expect(mockToggleSidebar).toHaveBeenCalledTimes(1);
    });

    it('should show expand icon when collapsed', () => {
      (useAppStore as any).mockReturnValue({
        sidebarCollapsed: true,
        toggleSidebar: mockToggleSidebar,
      });

      renderWithProviders(<Sidebar />);
      const expandButton = screen.getByLabelText('Expand sidebar');
      expect(expandButton.textContent).toContain('☰');
    });

    it('should show collapse icon when expanded', () => {
      renderWithProviders(<Sidebar />);
      const collapseButton = screen.getByLabelText('Collapse sidebar');
      expect(collapseButton.textContent).toContain('✕');
    });

    it('should have collapsed class when collapsed', () => {
      (useAppStore as any).mockReturnValue({
        sidebarCollapsed: true,
        toggleSidebar: mockToggleSidebar,
      });

      const { container } = renderWithProviders(<Sidebar />);
      const sidebar = container.querySelector('.sidebar');
      expect(sidebar).toHaveClass('collapsed');
    });
  });

  describe('Accessibility', () => {
    it('should have proper ARIA labels', () => {
      renderWithProviders(<Sidebar />);
      expect(screen.getByLabelText('Collapse sidebar')).toBeInTheDocument();
    });

    it('should have proper ARIA labels for expand buttons', async () => {
      const user = userEvent.setup();
      renderWithProviders(<Sidebar />);

      const theoryItem = screen.getByText('Theory').closest('.nav-item');
      const expandButton = theoryItem?.querySelector('.expand-button');

      expect(expandButton).toHaveAttribute('aria-label', 'Expand');

      if (expandButton) {
        await user.click(expandButton as Element);
        await waitFor(() => {
          expect(expandButton).toHaveAttribute('aria-label', 'Collapse');
        });
      }
    });

    it('should be keyboard navigable', async () => {
      const user = userEvent.setup();
      renderWithProviders(<Sidebar />);

      const collapseButton = screen.getByLabelText('Collapse sidebar');
      collapseButton.focus();

      expect(collapseButton).toHaveFocus();

      await user.keyboard('{Enter}');
      expect(mockToggleSidebar).toHaveBeenCalled();
    });
  });
});
