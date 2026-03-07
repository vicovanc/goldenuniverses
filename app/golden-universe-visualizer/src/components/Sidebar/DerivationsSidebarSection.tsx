/**
 * DerivationsSidebarSection - Dynamic derivations loading for sidebar
 * Fetches derivation list from API and provides navigation items
 */

import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import type { SidebarNavigationItem } from './types';

interface Derivation {
  id: number;
  number: number;
  title: string;
  name: string;
  description: string;
  category: 'fundamental' | 'particles' | 'constants' | 'advanced';
  folderName: string;
}

interface DerivationsSidebarSectionProps {
  defaultExpanded?: boolean;
  onItemClick?: (derivationId: string) => void;
}

export const DerivationsSidebarSection: React.FC<DerivationsSidebarSectionProps> = ({
  defaultExpanded = true,
  onItemClick
}) => {
  const location = useLocation();
  const navigate = useNavigate();
  const [derivations, setDerivations] = useState<Derivation[]>([]);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState(defaultExpanded);

  // Fetch derivations from the API
  useEffect(() => {
    fetchDerivations();
  }, []);

  const fetchDerivations = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/derivations');
      if (!response.ok) {
        console.error('Failed to fetch derivations');
        return;
      }

      const result = await response.json();
      if (result.success && result.data) {
        setDerivations(result.data);
      }
    } catch (err) {
      console.error('Error fetching derivations:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDerivationClick = (derivationId: string) => {
    navigate(`/derivations/${derivationId}`);
    if (onItemClick) {
      onItemClick(derivationId);
    }
  };

  const isActive = (path: string): boolean => {
    return location.pathname === path;
  };

  const isDerivationActive = (derivationId: number): boolean => {
    return location.pathname === `/derivations/${derivationId}`;
  };

  const toggleExpanded = () => {
    setExpanded(!expanded);
  };

  // Group derivations by category
  const categorizedDerivations = React.useMemo(() => {
    const grouped: Record<string, Derivation[]> = {
      fundamental: [],
      particles: [],
      constants: [],
      advanced: []
    };

    derivations.forEach(d => {
      if (grouped[d.category]) {
        grouped[d.category].push(d);
      }
    });

    return grouped;
  }, [derivations]);

  const categoryLabels = {
    fundamental: 'Fundamental Laws',
    particles: 'Particle Masses',
    constants: 'Physical Constants',
    advanced: 'Advanced Topics'
  };

  return (
    <div className="sidebar-section">
      <div className="section-header" onClick={toggleExpanded}>
        <span className="section-icon">◈</span>
        <h3 className="section-title">DERIVATIONS</h3>
        <button className="expand-toggle" aria-label={expanded ? 'Collapse' : 'Expand'}>
          <span className={`arrow ${expanded ? 'expanded' : ''}`}>▶</span>
        </button>
      </div>

      {expanded && (
        <div className="section-content">
          {loading ? (
            <div className="loading-message">Loading derivations...</div>
          ) : derivations.length === 0 ? (
            <div className="empty-message">No derivations available</div>
          ) : (
            <>
              {/* Main derivations link */}
              <div
                className={`sidebar-item ${isActive('/derivations') ? 'active' : ''}`}
                onClick={() => navigate('/derivations')}
              >
                <span className="item-icon">◎</span>
                <span className="item-label">All Derivations</span>
                <span className="item-badge">{derivations.length}</span>
              </div>

              {/* Categorized derivations */}
              {Object.entries(categorizedDerivations).map(([category, items]) => {
                if (items.length === 0) return null;

                return (
                  <div key={category} className="category-group">
                    <div className="category-header">
                      <span className="category-label">{categoryLabels[category as keyof typeof categoryLabels]}</span>
                      <span className="category-count">{items.length}</span>
                    </div>
                    <div className="category-items">
                      {items.map(derivation => (
                        <div
                          key={derivation.id}
                          className={`sidebar-item sub-item ${isDerivationActive(derivation.id) ? 'active' : ''}`}
                          onClick={() => handleDerivationClick(derivation.id.toString())}
                          title={derivation.description}
                        >
                          <span className="item-number">#{derivation.number}</span>
                          <span className="item-label">
                            {derivation.title || `Law ${derivation.number}: ${derivation.name}`}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                );
              })}
            </>
          )}
        </div>
      )}
    </div>
  );
};