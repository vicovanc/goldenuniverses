import { useState, useEffect } from 'react';
import type { SidebarNavigationItem } from './types';

interface Derivation {
  id: number;
  number: number;
  title: string;
  name: string;
  folderName: string;
  category: string;
  pythonCount: number;
  markdownCount: number;
}

export const useDynamicDerivations = () => {
  const [derivationItems, setDerivationItems] = useState<SidebarNavigationItem[]>([]);
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
        // Fallback to static data if API fails
        console.warn('Failed to fetch derivations, using static data');
        setDerivationItems(getStaticDerivations());
        return;
      }

      const result = await response.json();
      if (result.success && result.data) {
        // Convert API data to SidebarNavigationItem format
        const items: SidebarNavigationItem[] = result.data.map((derivation: Derivation) => {
          // Format the name properly with fallback
          const nameToFormat = derivation.name || derivation.folderName || `Derivation ${derivation.number}`;
          const formattedName = nameToFormat
            .replace(/_/g, ' ')
            .toLowerCase()
            .replace(/\b\w/g, (char) => char.toUpperCase());

          // Determine badge based on content
          let badge: string | number | undefined;
          if (derivation.pythonCount > 0 && derivation.markdownCount > 0) {
            badge = `${derivation.pythonCount}+${derivation.markdownCount}`;
          } else if (derivation.pythonCount > 0) {
            badge = `PY:${derivation.pythonCount}`;
          } else if (derivation.markdownCount > 0) {
            badge = `MD:${derivation.markdownCount}`;
          }

          return {
            id: `deriv-${String(derivation.number).padStart(2, '0')}`,
            label: `${String(derivation.number).padStart(2, '0')}: ${formattedName}`,
            path: `/derivations/${derivation.id}`,
            badge,
            tooltip: derivation.title,
            icon: derivation.category === 'fundamental' ? '⭐' :
                  derivation.category === 'particles' ? '⚛️' :
                  derivation.category === 'constants' ? '🔢' : '📐',
          };
        });

        setDerivationItems(items);
      } else {
        // Fallback to static data
        setDerivationItems(getStaticDerivations());
      }
    } catch (err) {
      console.error('Error fetching derivations:', err);
      setError('Failed to load derivations');
      // Use static data as fallback
      setDerivationItems(getStaticDerivations());
    } finally {
      setLoading(false);
    }
  };

  return { derivationItems, loading, error };
};

// Static fallback data
const getStaticDerivations = (): SidebarNavigationItem[] => [
  { id: 'deriv-01', label: '01: Force Unification', path: '/derivations/1', badge: 'PDF' },
  { id: 'deriv-02', label: '02: Fundamental Constants', path: '/derivations/2', badge: 'PDF' },
  { id: 'deriv-03', label: '03: Particle Masses', path: '/derivations/3', badge: 'PDF' },
  { id: 'deriv-04', label: '04: Cosmology', path: '/derivations/4', badge: 'PDF' },
  { id: 'deriv-05', label: '05: Charge Quantization', path: '/derivations/5', badge: 'PDF' },
  { id: 'deriv-06', label: '06: Coupling Constants', path: '/derivations/6', badge: 'PDF' },
  { id: 'deriv-07', label: '07: Particle Families', path: '/derivations/7', badge: 'PDF' },
  { id: 'deriv-08', label: '08: Neutrino Masses', path: '/derivations/8', badge: 'PDF' },
  { id: 'deriv-09', label: '09: QCD Scale', path: '/derivations/9', badge: 'PDF' },
  { id: 'deriv-10', label: '10: Higgs Mechanism', path: '/derivations/10', badge: 'PDF' },
];

export default useDynamicDerivations;