/**
 * DerivationsBrowser - Browse derivation folders dynamically
 * Shows step-by-step mathematical derivations organized by topic
 * Fetches the list from the server which reads the actual filesystem
 */

import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { DerivationViewerNew } from './DerivationViewerNew';
import './DerivationsBrowser.scss';

interface Derivation {
  id: number;
  number: number;
  title: string;
  name: string;
  description: string;
  category: 'fundamental' | 'particles' | 'constants' | 'advanced';
  folderName: string;
  folder_path: string;
  pythonCount: number;
  markdownCount: number;
  totalFiles: number;
  files: {
    python: string[];
    markdown: string[];
    all: string[];
  };
}

export const DerivationsBrowser: React.FC = () => {
  const { derivationId } = useParams<{ derivationId?: string }>();
  const navigate = useNavigate();
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedDerivation, setSelectedDerivation] = useState<Derivation | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [derivations, setDerivations] = useState<Derivation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch derivations from the server
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
        console.log('Derivations from API:', result.data);
        console.log('First derivation title:', result.data[0]?.title);
        setDerivations(result.data);
      } else {
        throw new Error('Invalid response format');
      }
    } catch (err) {
      console.error('Error fetching derivations:', err);
      setError('Failed to load derivations. Please try refreshing the page.');
    } finally {
      setLoading(false);
    }
  };

  // Update selected derivation when URL changes
  useEffect(() => {
    if (!derivations.length) return; // Wait for derivations to load

    if (derivationId) {
      // When we have a specific derivation ID in the URL
      const derivation = derivations.find(d => d.id.toString() === derivationId);
      if (derivation) {
        setSelectedDerivation(derivation);
        // Scroll to top when derivation changes via URL (sidebar navigation)
        window.scrollTo({ top: 0, behavior: 'smooth' });

        // Also scroll the selected card into view in the derivations list
        setTimeout(() => {
          const selectedCard = document.querySelector('.derivation-card.selected');
          if (selectedCard) {
            selectedCard.scrollIntoView({
              behavior: 'smooth',
              block: 'center',
              inline: 'nearest'
            });
          }
        }, 100); // Small delay to ensure DOM is updated
      }
    }
  }, [derivationId, derivations]);

  // Auto-select first derivation only on initial mount if no derivation is selected
  useEffect(() => {
    if (derivations.length > 0 && !derivationId && !selectedDerivation) {
      const firstDerivation = derivations[0];
      setSelectedDerivation(firstDerivation);
      navigate(`/derivations/${firstDerivation.id}`, { replace: true });
    }
  }, [derivations.length]); // Only run when derivations are first loaded

  // Calculate categories dynamically from fetched derivations
  const categories = React.useMemo(() => {
    const cats = [
      { id: 'all', name: 'All Derivations', count: derivations.length }
    ];

    const categoryMap: Record<string, number> = {
      fundamental: 0,
      particles: 0,
      constants: 0,
      advanced: 0
    };

    derivations.forEach(d => {
      if (categoryMap[d.category] !== undefined) {
        categoryMap[d.category]++;
      }
    });

    if (categoryMap.fundamental > 0) {
      cats.push({ id: 'fundamental', name: 'Fundamental Laws', count: categoryMap.fundamental });
    }
    if (categoryMap.particles > 0) {
      cats.push({ id: 'particles', name: 'Particle Masses', count: categoryMap.particles });
    }
    if (categoryMap.constants > 0) {
      cats.push({ id: 'constants', name: 'Physical Constants', count: categoryMap.constants });
    }
    if (categoryMap.advanced > 0) {
      cats.push({ id: 'advanced', name: 'Advanced Topics', count: categoryMap.advanced });
    }

    return cats;
  }, [derivations]);

  const filteredDerivations = derivations.filter(d => {
    const matchesCategory = selectedCategory === 'all' || d.category === selectedCategory;
    const matchesSearch = searchTerm === '' ||
      (d.title || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
      (d.description || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
      (d.folderName || '').toLowerCase().includes(searchTerm.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const getDifficultyFromFiles = (pythonCount: number, markdownCount: number): string => {
    const totalFiles = pythonCount + markdownCount;
    if (totalFiles <= 2) return 'basic';
    if (totalFiles <= 5) return 'intermediate';
    return 'advanced';
  };

  const getDifficultyColor = (pythonCount: number, markdownCount: number) => {
    const difficulty = getDifficultyFromFiles(pythonCount, markdownCount);
    switch (difficulty) {
      case 'basic': return 'green';
      case 'intermediate': return 'purple';
      case 'advanced': return 'violet';
      default: return 'gray';
    }
  };

  const handleDerivationClick = (derivation: Derivation) => {
    // Scroll to top of the page
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Set the selected derivation and navigate
    setSelectedDerivation(derivation);
    navigate(`/derivations/${derivation.id}`);
  };

  const handleCloseDerivation = () => {
    setSelectedDerivation(null);
    navigate('/derivations');
  };

  if (loading) {
    return (
      <div className="derivations-browser">
        <div className="browser-header">
          <h1>Derivations Browser</h1>
          <p className="subtitle">Loading derivations from filesystem...</p>
        </div>
        <div className="loading-spinner">
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="derivations-browser">
        <div className="browser-header">
          <h1>Derivations Browser</h1>
          <p className="subtitle error">{error}</p>
        </div>
        <button onClick={fetchDerivations} className="retry-button">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="derivations-browser">
      <div className="browser-header">
        <h1>Derivations Browser</h1>
        <p className="subtitle">
          {derivations.length} derivations loaded from filesystem
        </p>
      </div>

      {/* Search Bar */}
      <div className="search-section">
        <input
          type="text"
          className="search-input"
          placeholder="Search derivations..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {/* Category Filters */}
      <div className="category-filters">
        {categories.map(cat => (
          <button
            key={cat.id}
            className={`category-btn ${selectedCategory === cat.id ? 'active' : ''}`}
            onClick={() => setSelectedCategory(cat.id)}
          >
            {cat.name}
            <span className="count">{cat.count}</span>
          </button>
        ))}
      </div>

      <div className="browser-content">
        {/* Derivations List */}
        <div className="derivations-list">
          <div className="list-header">
            <h2>Derivations ({filteredDerivations.length})</h2>
          </div>

          <div className="derivation-cards">
            {filteredDerivations.map(derivation => (
              <div
                key={derivation.id}
                className={`derivation-card ${selectedDerivation?.id === derivation.id ? 'selected' : ''}`}
                onClick={() => handleDerivationClick(derivation)}
              >
                <div className="card-header">
                  <span className="derivation-number">#{derivation.number}</span>
                  <span className={`difficulty-badge ${getDifficultyColor(derivation.pythonCount, derivation.markdownCount)}`}>
                    {getDifficultyFromFiles(derivation.pythonCount, derivation.markdownCount)}
                  </span>
                </div>
                <h3 className="derivation-title">
                  {derivation.title ? derivation.title :
                   derivation.name ? `Law ${derivation.number}: ${derivation.name}` :
                   `Law ${derivation.number}`}
                </h3>
                <p className="description">{derivation.description}</p>
                <div className="card-footer">
                  <span className={`category-badge ${derivation.category}`}>
                    {derivation.category}
                  </span>
                  <span className="steps-count">
                    {derivation.pythonCount} Python, {derivation.markdownCount} Markdown
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Derivation Details */}
        {selectedDerivation && (
          <div className="derivation-details">
            <div className="details-header">
              <h2>{selectedDerivation.title}</h2>
              <button className="close-btn" onClick={handleCloseDerivation}>
                Close
              </button>
            </div>

            <div className="details-meta">
              <div className="meta-item">
                <span className="meta-label">Category:</span>
                <span className={`category-badge ${selectedDerivation.category}`}>
                  {selectedDerivation.category}
                </span>
              </div>
              <div className="meta-item">
                <span className="meta-label">Files:</span>
                <span>
                  {selectedDerivation.pythonCount} Python, {selectedDerivation.markdownCount} Docs
                </span>
              </div>
              <div className="meta-item">
                <span className="meta-label">Folder:</span>
                <span className="folder-name">{selectedDerivation.folderName}</span>
              </div>
            </div>

            <div className="details-content">
              <p className="description">{selectedDerivation.description}</p>

              <DerivationViewerNew
                derivationId={selectedDerivation.id.toString()}
                title={selectedDerivation.title}
                folder={selectedDerivation.folderName}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};