/**
 * ResultsFilters - Category and precision filtering
 * GU-036: Filter by category (leptons, quarks, bosons, constants)
 */

import React from 'react';
import type { ParticleCategory, PrecisionLevel, FilterOptions } from './types';

interface ResultsFiltersProps {
  filters: FilterOptions;
  onFiltersChange: (filters: FilterOptions) => void;
}

export const ResultsFilters: React.FC<ResultsFiltersProps> = ({
  filters,
  onFiltersChange,
}) => {
  const categories: { value: ParticleCategory; label: string }[] = [
    { value: 'leptons', label: 'Leptons' },
    { value: 'quarks', label: 'Quarks' },
    { value: 'bosons', label: 'Bosons' },
    { value: 'constants', label: 'Constants' },
  ];

  const precisionLevels: { value: PrecisionLevel; label: string; ppm: string }[] = [
    { value: 'excellent', label: 'Excellent', ppm: '< 100 ppm' },
    { value: 'very-good', label: 'Very Good', ppm: '< 0.1%' },
    { value: 'good', label: 'Good', ppm: '< 1%' },
    { value: 'fair', label: 'Fair', ppm: '< 10%' },
    { value: 'poor', label: 'Poor', ppm: '> 10%' },
  ];

  const toggleCategory = (category: ParticleCategory) => {
    const newCategories = filters.categories.includes(category)
      ? filters.categories.filter(c => c !== category)
      : [...filters.categories, category];

    onFiltersChange({ ...filters, categories: newCategories });
  };

  const togglePrecision = (level: PrecisionLevel) => {
    const newLevels = filters.precisionLevels.includes(level)
      ? filters.precisionLevels.filter(l => l !== level)
      : [...filters.precisionLevels, level];

    onFiltersChange({ ...filters, precisionLevels: newLevels });
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onFiltersChange({ ...filters, searchTerm: e.target.value });
  };

  const clearFilters = () => {
    onFiltersChange({
      categories: ['leptons', 'quarks', 'bosons', 'constants'],
      precisionLevels: ['excellent', 'very-good', 'good', 'fair', 'poor'],
      searchTerm: '',
    });
  };

  const isAllSelected =
    filters.categories.length === 4 && filters.precisionLevels.length === 5;

  return (
    <div className="results-filters">
      <div className="filters-header">
        <h3>Filters</h3>
        {!isAllSelected && (
          <button className="clear-filters-btn" onClick={clearFilters}>
            Clear All
          </button>
        )}
      </div>

      {/* Search */}
      <div className="filter-section">
        <label className="filter-label">Search</label>
        <input
          type="text"
          className="search-input"
          placeholder="Search by name..."
          value={filters.searchTerm || ''}
          onChange={handleSearchChange}
        />
      </div>

      {/* Category Filter */}
      <div className="filter-section">
        <label className="filter-label">Categories</label>
        <div className="filter-options">
          {categories.map(cat => (
            <button
              key={cat.value}
              className={`filter-chip ${
                filters.categories.includes(cat.value) ? 'active' : ''
              } ${cat.value}`}
              onClick={() => toggleCategory(cat.value)}
            >
              {cat.label}
              {filters.categories.includes(cat.value) && (
                <span className="check-icon">✓</span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Precision Filter */}
      <div className="filter-section">
        <label className="filter-label">Precision Level</label>
        <div className="filter-options precision-options">
          {precisionLevels.map(level => (
            <button
              key={level.value}
              className={`filter-chip precision-chip ${level.value} ${
                filters.precisionLevels.includes(level.value) ? 'active' : ''
              }`}
              onClick={() => togglePrecision(level.value)}
            >
              <span className="precision-label">{level.label}</span>
              <span className="precision-range">{level.ppm}</span>
              {filters.precisionLevels.includes(level.value) && (
                <span className="check-icon">✓</span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Active Filters Summary */}
      <div className="active-filters-summary">
        <div className="summary-text">
          Showing {filters.categories.length} categories,{' '}
          {filters.precisionLevels.length} precision levels
        </div>
      </div>
    </div>
  );
};
