import React, { useState, useEffect } from 'react';
import type { SidebarNavigationItem } from './types';

interface Derivation {
  id: number;
  number: number;
  title: string;
  name: string;
  folderName: string;
  category: string;
}

interface DynamicDerivationsProps {
  onItemsLoaded: (items: SidebarNavigationItem[]) => void;
}

export const DynamicDerivations: React.FC<DynamicDerivationsProps> = ({ onItemsLoaded }) => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDerivations();
  }, []);

  const fetchDerivations = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch('/api/derivations');
      if (!response.ok) {
        throw new Error('Failed to fetch derivations');
      }

      const result = await response.json();
      if (result.success && result.data) {
        // Convert API data to SidebarNavigationItem format
        const items: SidebarNavigationItem[] = result.data.map((derivation: Derivation) => ({
          id: `deriv-${derivation.id}`,
          label: `${String(derivation.number).padStart(2, '0')}: ${derivation.name}`,
          path: `/derivations/${derivation.id}`,
          badge: derivation.category === 'fundamental' ? '⭐' : undefined,
          tooltip: derivation.title,
        }));

        onItemsLoaded(items);
      } else {
        throw new Error('Invalid response format');
      }
    } catch (err) {
      console.error('Error fetching derivations:', err);
      setError('Failed to load derivations');
      // Return empty items on error
      onItemsLoaded([]);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="sidebar-loading">Loading derivations...</div>;
  }

  if (error) {
    return <div className="sidebar-error">{error}</div>;
  }

  return null;
};

export default DynamicDerivations;