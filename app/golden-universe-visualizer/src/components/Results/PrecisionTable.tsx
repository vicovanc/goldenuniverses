/**
 * PrecisionTable - Two-column comparison table
 * GU-036: Precision Comparison Table
 * - Color coding by precision
 * - Sort by error percentage
 * - Expandable details
 */

import React, { useState } from 'react';
import type { ResultData } from './types';

interface PrecisionTableProps {
  results: ResultData[];
  onExport?: () => void;
}

type SortField = 'name' | 'error' | 'category' | 'precision';
type SortDirection = 'asc' | 'desc';

export const PrecisionTable: React.FC<PrecisionTableProps> = ({
  results,
  onExport,
}) => {
  const [sortField, setSortField] = useState<SortField>('error');
  const [sortDirection, setSortDirection] = useState<SortDirection>('asc');
  const [expandedRows, setExpandedRows] = useState<Set<string>>(new Set());

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };

  const sortedResults = [...results].sort((a, b) => {
    let comparison = 0;

    switch (sortField) {
      case 'name':
        comparison = a.name.localeCompare(b.name);
        break;
      case 'error':
        comparison = Math.abs(a.errorPpm) - Math.abs(b.errorPpm);
        break;
      case 'category':
        comparison = a.category.localeCompare(b.category);
        break;
      case 'precision':
        comparison = a.precision.localeCompare(b.precision);
        break;
    }

    return sortDirection === 'asc' ? comparison : -comparison;
  });

  const toggleExpanded = (id: string) => {
    const newExpanded = new Set(expandedRows);
    if (newExpanded.has(id)) {
      newExpanded.delete(id);
    } else {
      newExpanded.add(id);
    }
    setExpandedRows(newExpanded);
  };

  const getPrecisionColor = (precision: string): string => {
    const colorMap: Record<string, string> = {
      'excellent': '#00C853',     // Green
      'very-good': '#64DD17',     // Light green
      'good': '#FFD600',          // Yellow
      'fair': '#FF9100',          // Orange
      'poor': '#FF3D00',          // Red
    };
    return colorMap[precision] || '#888';
  };

  const formatValue = (value: number, unit: string): string => {
    if (unit === 'm³/(kg·s²)' || unit === 'dimensionless' || Math.abs(value) < 0.01 || Math.abs(value) > 1e6) {
      return value.toExponential(10);
    }
    return value.toFixed(8);
  };

  const formatError = (ppm: number): string => {
    const abs = Math.abs(ppm);
    if (abs < 0.01) return '< 0.01 ppm';
    if (abs < 1) return `${abs.toFixed(3)} ppm`;
    if (abs < 1000) return `${abs.toFixed(2)} ppm`;
    return `${(abs / 10000).toFixed(3)}%`;
  };

  return (
    <div className="precision-table-container">
      <div className="table-header">
        <h3>Precision Comparison</h3>
        {onExport && (
          <button className="export-btn" onClick={onExport}>
            Export Data
          </button>
        )}
      </div>

      <div className="table-scroll">
        <table className="precision-table">
          <thead>
            <tr>
              <th className="expand-col"></th>
              <th
                className={`sortable ${sortField === 'name' ? 'active' : ''}`}
                onClick={() => handleSort('name')}
              >
                Quantity
                <span className="sort-icon">
                  {sortField === 'name' && (sortDirection === 'asc' ? '↑' : '↓')}
                </span>
              </th>
              <th
                className={`sortable ${sortField === 'category' ? 'active' : ''}`}
                onClick={() => handleSort('category')}
              >
                Category
                <span className="sort-icon">
                  {sortField === 'category' && (sortDirection === 'asc' ? '↑' : '↓')}
                </span>
              </th>
              <th>Theoretical</th>
              <th>Experimental</th>
              <th
                className={`sortable ${sortField === 'error' ? 'active' : ''}`}
                onClick={() => handleSort('error')}
              >
                Error
                <span className="sort-icon">
                  {sortField === 'error' && (sortDirection === 'asc' ? '↑' : '↓')}
                </span>
              </th>
              <th
                className={`sortable ${sortField === 'precision' ? 'active' : ''}`}
                onClick={() => handleSort('precision')}
              >
                Precision
                <span className="sort-icon">
                  {sortField === 'precision' && (sortDirection === 'asc' ? '↑' : '↓')}
                </span>
              </th>
              <th>Unit</th>
            </tr>
          </thead>
          <tbody>
            {sortedResults.map(result => {
              const isExpanded = expandedRows.has(result.id);
              const precisionColor = getPrecisionColor(result.precision);

              return (
                <React.Fragment key={result.id}>
                  <tr className={`result-row ${result.category}`}>
                    <td className="expand-col">
                      <button
                        className={`expand-btn ${isExpanded ? 'expanded' : ''}`}
                        onClick={() => toggleExpanded(result.id)}
                        aria-label={isExpanded ? 'Collapse' : 'Expand'}
                      >
                        {isExpanded ? '−' : '+'}
                      </button>
                    </td>
                    <td className="name-col">
                      <div className="name-content">
                        <span className="name">{result.name}</span>
                        {result.breakthrough && (
                          <span className="breakthrough-badge" title="Breakthrough result">
                            ★
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="category-col">
                      <span className={`category-badge ${result.category}`}>
                        {result.category}
                      </span>
                    </td>
                    <td className="value-col theoretical">
                      {formatValue(result.theoretical, result.unit)}
                    </td>
                    <td className="value-col experimental">
                      {formatValue(result.experimental, result.unit)}
                    </td>
                    <td className="error-col">
                      <span className="error-value">{formatError(result.errorPpm)}</span>
                    </td>
                    <td className="precision-col">
                      <span
                        className={`precision-badge ${result.precision}`}
                        style={{ backgroundColor: precisionColor }}
                      >
                        {result.precision.replace('-', ' ')}
                      </span>
                    </td>
                    <td className="unit-col">{result.unit}</td>
                  </tr>
                  {isExpanded && (
                    <tr className="details-row">
                      <td colSpan={8}>
                        <div className="details-content">
                          <div className="details-grid">
                            {result.formula && (
                              <div className="detail-section">
                                <h4>Formula</h4>
                                <div className="formula-text">{result.formula}</div>
                              </div>
                            )}
                            {result.derivation && (
                              <div className="detail-section">
                                <h4>Derivation</h4>
                                <p>{result.derivation}</p>
                              </div>
                            )}
                            <div className="detail-section">
                              <h4>Precision Details</h4>
                              <table className="detail-table">
                                <tbody>
                                  <tr>
                                    <td>Error (ppm):</td>
                                    <td>{Math.abs(result.errorPpm).toFixed(6)}</td>
                                  </tr>
                                  <tr>
                                    <td>Error (%):</td>
                                    <td>{(Math.abs(result.errorPercent) * 100).toFixed(6)}%</td>
                                  </tr>
                                  <tr>
                                    <td>Relative error:</td>
                                    <td>
                                      {((result.theoretical - result.experimental) / result.experimental).toExponential(4)}
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
                            </div>
                            {result.references && result.references.length > 0 && (
                              <div className="detail-section">
                                <h4>References</h4>
                                <ul className="references-list">
                                  {result.references.map((ref, idx) => (
                                    <li key={idx}>{ref}</li>
                                  ))}
                                </ul>
                              </div>
                            )}
                            {result.discoveryDate && (
                              <div className="detail-section">
                                <h4>Discovery Date</h4>
                                <p>{result.discoveryDate}</p>
                              </div>
                            )}
                          </div>
                        </div>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Summary */}
      <div className="table-summary">
        <div className="summary-stats">
          <span>Total results: {results.length}</span>
          <span>•</span>
          <span>
            Sub-100 ppm:{' '}
            {results.filter(r => Math.abs(r.errorPpm) < 100).length}
          </span>
          <span>•</span>
          <span>
            Breakthroughs: {results.filter(r => r.breakthrough).length}
          </span>
        </div>
      </div>
    </div>
  );
};
