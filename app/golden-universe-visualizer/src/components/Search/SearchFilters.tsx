/**
 * SearchFilters Component - GU-027: Advanced Search UI
 *
 * Features:
 * - Category checkboxes (Theory, Derivations, Python, Equations)
 * - Date range selector
 * - File type filter
 * - Precision range slider
 * - Reset filters button
 */

import React, { useState, useEffect } from 'react';
import { SearchFilters as SearchFiltersType } from '../../services/searchService';

interface SearchFiltersProps {
  onFiltersChange: (filters: SearchFiltersType) => void;
  initialFilters?: SearchFiltersType;
  show: boolean;
}

const SearchFilters: React.FC<SearchFiltersProps> = ({
  onFiltersChange,
  initialFilters = {},
  show,
}) => {
  const [selectedCategories, setSelectedCategories] = useState<string[]>(
    initialFilters.categories || []
  );
  const [selectedFileTypes, setSelectedFileTypes] = useState<string[]>(
    initialFilters.fileTypes || []
  );
  const [dateRange, setDateRange] = useState<{
    start?: string;
    end?: string;
  }>({
    start: initialFilters.dateRange?.start?.toISOString().split('T')[0],
    end: initialFilters.dateRange?.end?.toISOString().split('T')[0],
  });
  const [precisionRange, setPrecisionRange] = useState<{
    min: number;
    max: number;
  }>({
    min: initialFilters.precisionRange?.min ?? 0,
    max: initialFilters.precisionRange?.max ?? 100,
  });

  const categories = [
    { id: 'theory', label: 'Theory', icon: '📚' },
    { id: 'derivations', label: 'Derivations', icon: '📐' },
    { id: 'python', label: 'Python', icon: '🐍' },
    { id: 'equations', label: 'Equations', icon: '∑' },
  ];

  const fileTypes = [
    { id: 'theory', label: 'Theory (.md)', extension: '.md' },
    { id: 'derivation', label: 'Derivation (.md)', extension: '.md' },
    { id: 'python', label: 'Python (.py)', extension: '.py' },
    { id: 'equation', label: 'Equation', extension: '' },
  ];

  useEffect(() => {
    const filters: SearchFiltersType = {};

    if (selectedCategories.length > 0) {
      // Map category ids to display names
      filters.categories = selectedCategories.map(id => {
        const category = categories.find(c => c.id === id);
        return category?.label || id;
      });
    }

    if (selectedFileTypes.length > 0) {
      filters.fileTypes = selectedFileTypes;
    }

    if (dateRange.start || dateRange.end) {
      filters.dateRange = {
        start: dateRange.start ? new Date(dateRange.start) : undefined,
        end: dateRange.end ? new Date(dateRange.end) : undefined,
      };
    }

    if (precisionRange.min > 0 || precisionRange.max < 100) {
      filters.precisionRange = precisionRange;
    }

    onFiltersChange(filters);
  }, [selectedCategories, selectedFileTypes, dateRange, precisionRange]);

  const handleCategoryToggle = (categoryId: string) => {
    setSelectedCategories(prev =>
      prev.includes(categoryId)
        ? prev.filter(c => c !== categoryId)
        : [...prev, categoryId]
    );
  };

  const handleFileTypeToggle = (fileTypeId: string) => {
    setSelectedFileTypes(prev =>
      prev.includes(fileTypeId)
        ? prev.filter(t => t !== fileTypeId)
        : [...prev, fileTypeId]
    );
  };

  const handleDateChange = (field: 'start' | 'end', value: string) => {
    setDateRange(prev => ({
      ...prev,
      [field]: value || undefined,
    }));
  };

  const handlePrecisionChange = (field: 'min' | 'max', value: number) => {
    setPrecisionRange(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleResetFilters = () => {
    setSelectedCategories([]);
    setSelectedFileTypes([]);
    setDateRange({ start: undefined, end: undefined });
    setPrecisionRange({ min: 0, max: 100 });
  };

  const hasActiveFilters =
    selectedCategories.length > 0 ||
    selectedFileTypes.length > 0 ||
    dateRange.start ||
    dateRange.end ||
    precisionRange.min > 0 ||
    precisionRange.max < 100;

  if (!show) {
    return null;
  }

  return (
    <div className="search-filters">
      <div className="search-filters__header">
        <h3 className="search-filters__title">Filters</h3>
        {hasActiveFilters && (
          <button
            className="search-filters__reset"
            onClick={handleResetFilters}
            aria-label="Reset filters"
          >
            Reset All
          </button>
        )}
      </div>

      {/* Category Filter */}
      <div className="search-filters__section">
        <h4 className="search-filters__section-title">Categories</h4>
        <div className="search-filters__checkboxes">
          {categories.map(category => (
            <label
              key={category.id}
              className="search-filters__checkbox-label"
            >
              <input
                type="checkbox"
                className="search-filters__checkbox"
                checked={selectedCategories.includes(category.id)}
                onChange={() => handleCategoryToggle(category.id)}
              />
              <span className="search-filters__checkbox-icon">
                {category.icon}
              </span>
              <span className="search-filters__checkbox-text">
                {category.label}
              </span>
            </label>
          ))}
        </div>
      </div>

      {/* File Type Filter */}
      <div className="search-filters__section">
        <h4 className="search-filters__section-title">File Types</h4>
        <div className="search-filters__checkboxes">
          {fileTypes.map(fileType => (
            <label
              key={fileType.id}
              className="search-filters__checkbox-label"
            >
              <input
                type="checkbox"
                className="search-filters__checkbox"
                checked={selectedFileTypes.includes(fileType.id)}
                onChange={() => handleFileTypeToggle(fileType.id)}
              />
              <span className="search-filters__checkbox-text">
                {fileType.label}
              </span>
            </label>
          ))}
        </div>
      </div>

      {/* Date Range Filter */}
      <div className="search-filters__section">
        <h4 className="search-filters__section-title">Date Range</h4>
        <div className="search-filters__date-range">
          <div className="search-filters__date-field">
            <label
              htmlFor="date-start"
              className="search-filters__date-label"
            >
              From
            </label>
            <input
              id="date-start"
              type="date"
              className="search-filters__date-input"
              value={dateRange.start || ''}
              onChange={e => handleDateChange('start', e.target.value)}
            />
          </div>
          <div className="search-filters__date-field">
            <label
              htmlFor="date-end"
              className="search-filters__date-label"
            >
              To
            </label>
            <input
              id="date-end"
              type="date"
              className="search-filters__date-input"
              value={dateRange.end || ''}
              onChange={e => handleDateChange('end', e.target.value)}
            />
          </div>
        </div>
      </div>

      {/* Precision Range Filter */}
      <div className="search-filters__section">
        <h4 className="search-filters__section-title">
          Precision Range (for results)
        </h4>
        <div className="search-filters__range">
          <div className="search-filters__range-inputs">
            <div className="search-filters__range-field">
              <label
                htmlFor="precision-min"
                className="search-filters__range-label"
              >
                Min
              </label>
              <input
                id="precision-min"
                type="number"
                className="search-filters__range-input"
                min="0"
                max="100"
                step="0.1"
                value={precisionRange.min}
                onChange={e =>
                  handlePrecisionChange('min', parseFloat(e.target.value) || 0)
                }
              />
              <span className="search-filters__range-unit">%</span>
            </div>
            <div className="search-filters__range-field">
              <label
                htmlFor="precision-max"
                className="search-filters__range-label"
              >
                Max
              </label>
              <input
                id="precision-max"
                type="number"
                className="search-filters__range-input"
                min="0"
                max="100"
                step="0.1"
                value={precisionRange.max}
                onChange={e =>
                  handlePrecisionChange('max', parseFloat(e.target.value) || 100)
                }
              />
              <span className="search-filters__range-unit">%</span>
            </div>
          </div>
          <div className="search-filters__range-sliders">
            <input
              type="range"
              className="search-filters__range-slider"
              min="0"
              max="100"
              step="0.1"
              value={precisionRange.min}
              onChange={e =>
                handlePrecisionChange('min', parseFloat(e.target.value))
              }
            />
            <input
              type="range"
              className="search-filters__range-slider"
              min="0"
              max="100"
              step="0.1"
              value={precisionRange.max}
              onChange={e =>
                handlePrecisionChange('max', parseFloat(e.target.value))
              }
            />
          </div>
          <div className="search-filters__range-display">
            {precisionRange.min.toFixed(1)}% - {precisionRange.max.toFixed(1)}%
          </div>
        </div>
      </div>

      {/* Active Filters Summary */}
      {hasActiveFilters && (
        <div className="search-filters__summary">
          <h4 className="search-filters__summary-title">Active Filters:</h4>
          <div className="search-filters__summary-tags">
            {selectedCategories.map(id => {
              const category = categories.find(c => c.id === id);
              return category ? (
                <span
                  key={id}
                  className="search-filters__summary-tag"
                >
                  {category.icon} {category.label}
                  <button
                    className="search-filters__summary-tag-remove"
                    onClick={() => handleCategoryToggle(id)}
                    aria-label={`Remove ${category.label} filter`}
                  >
                    ×
                  </button>
                </span>
              ) : null;
            })}
            {selectedFileTypes.map(id => {
              const fileType = fileTypes.find(t => t.id === id);
              return fileType ? (
                <span
                  key={id}
                  className="search-filters__summary-tag"
                >
                  {fileType.label}
                  <button
                    className="search-filters__summary-tag-remove"
                    onClick={() => handleFileTypeToggle(id)}
                    aria-label={`Remove ${fileType.label} filter`}
                  >
                    ×
                  </button>
                </span>
              ) : null;
            })}
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchFilters;
