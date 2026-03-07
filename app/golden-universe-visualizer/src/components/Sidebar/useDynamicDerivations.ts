import { useState, useEffect } from 'react';
import type { SidebarNavigationItem } from './types';
import { fetchDerivations } from '@/services/derivationsService';

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
    loadDerivationsData();
  }, []);

  const loadDerivationsData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Use the service to fetch from static JSON
      const derivationFolders = await fetchDerivations();

      if (derivationFolders && derivationFolders.length > 0) {
        // Convert folder data to SidebarNavigationItem format
        const items: SidebarNavigationItem[] = derivationFolders.map((folder, index) => {
          const derivationNumber = index + 1;

          // Format the name from folder name
          const nameToFormat = folder.displayName || folder.folderName || `Derivation ${derivationNumber}`;
          const formattedName = nameToFormat
            .replace(/_/g, ' ')
            .replace(/-/g, ' ')
            .toLowerCase()
            .replace(/\b\w/g, (char) => char.toUpperCase());

          // Count files for badge
          const pythonCount = folder.pythonScripts?.length || 0;
          const markdownCount = folder.markdownFiles?.length || 0;

          let badge: string | number | undefined;
          if (pythonCount > 0 && markdownCount > 0) {
            badge = `${pythonCount}+${markdownCount}`;
          } else if (pythonCount > 0) {
            badge = `PY:${pythonCount}`;
          } else if (markdownCount > 0) {
            badge = `MD:${markdownCount}`;
          }

          // Determine icon based on folder name patterns
          let icon = '📐';
          const folderLower = folder.folderName.toLowerCase();
          if (folderLower.includes('force') || folderLower.includes('unification')) {
            icon = '⭐';
          } else if (folderLower.includes('particle') || folderLower.includes('masses')) {
            icon = '⚛️';
          } else if (folderLower.includes('constant') || folderLower.includes('alpha')) {
            icon = '🔢';
          }

          return {
            id: `deriv-${String(derivationNumber).padStart(2, '0')}`,
            label: `${String(derivationNumber).padStart(2, '0')}: ${formattedName}`,
            path: `/derivations/${derivationNumber}`,
            badge,
            tooltip: formattedName,
            icon,
          };
        });

        setDerivationItems(items);
      } else {
        // Fallback to static data if no derivations found
        console.warn('No derivations found, using static fallback');
        setDerivationItems(getStaticDerivations());
      }
    } catch (err) {
      console.error('Error loading derivations:', err);
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