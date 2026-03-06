/**
 * CalculationHistory - Track and display previous calculations
 * Export, import, and search functionality
 */

import React, { useState, useEffect } from 'react';
import type { CalculationHistoryEntry } from '../../services/pythonEngine/pythonTypes';
import './CalculationHistory.scss';

export const CalculationHistory: React.FC = () => {
  const [history, setHistory] = useState<CalculationHistoryEntry[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterType, setFilterType] = useState<string>('all');

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = () => {
    // Load from localStorage
    const stored = localStorage.getItem('gu_calculation_history');
    if (stored) {
      try {
        const parsed = JSON.parse(stored);
        setHistory(parsed);
      } catch (error) {
        console.error('Failed to load history:', error);
      }
    }
  };

  const saveHistory = (newHistory: CalculationHistoryEntry[]) => {
    localStorage.setItem('gu_calculation_history', JSON.stringify(newHistory));
    setHistory(newHistory);
  };

  const addEntry = (entry: CalculationHistoryEntry) => {
    const newHistory = [entry, ...history].slice(0, 100); // Keep last 100
    saveHistory(newHistory);
  };

  const clearHistory = () => {
    if (confirm('Are you sure you want to clear all calculation history?')) {
      saveHistory([]);
    }
  };

  const deleteEntry = (id: string) => {
    const newHistory = history.filter(entry => entry.id !== id);
    saveHistory(newHistory);
  };

  const exportHistory = () => {
    const dataStr = JSON.stringify(history, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `gu_calculations_${Date.now()}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const exportCSV = () => {
    const headers = ['Timestamp', 'Type', 'Success', 'Execution Time (ms)', 'Result'];
    const rows = history.map(entry => [
      new Date(entry.timestamp).toISOString(),
      entry.input.type,
      entry.result.success ? 'Yes' : 'No',
      entry.result.executionTime,
      JSON.stringify(entry.result.result),
    ]);

    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.map(cell => `"${cell}"`).join(',')),
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `gu_calculations_${Date.now()}.csv`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const filteredHistory = history.filter(entry => {
    // Filter by type
    if (filterType !== 'all' && entry.input.type !== filterType) {
      return false;
    }

    // Filter by search query
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      const matchesType = entry.input.type.toLowerCase().includes(query);
      const matchesResult = JSON.stringify(entry.result.result)
        .toLowerCase()
        .includes(query);
      return matchesType || matchesResult;
    }

    return true;
  });

  const formatDate = (timestamp: number): string => {
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  const formatDuration = (ms: number): string => {
    if (ms < 1000) return `${ms.toFixed(0)}ms`;
    return `${(ms / 1000).toFixed(2)}s`;
  };

  return (
    <div className="calculation-history">
      <div className="history-header">
        <h2>Calculation History</h2>
        <div className="header-actions">
          <button className="export-btn" onClick={exportHistory}>
            Export JSON
          </button>
          <button className="export-btn" onClick={exportCSV}>
            Export CSV
          </button>
          <button className="clear-btn" onClick={clearHistory}>
            Clear All
          </button>
        </div>
      </div>

      {/* Controls */}
      <div className="history-controls">
        <input
          type="text"
          className="search-input"
          placeholder="Search calculations..."
          value={searchQuery}
          onChange={e => setSearchQuery(e.target.value)}
        />

        <select
          className="filter-select"
          value={filterType}
          onChange={e => setFilterType(e.target.value)}
        >
          <option value="all">All Types</option>
          <option value="particle_mass">Particle Mass</option>
          <option value="constant">Constants</option>
          <option value="winding">Winding Numbers</option>
          <option value="resonance">Resonances</option>
          <option value="custom">Custom</option>
        </select>
      </div>

      {/* Stats */}
      <div className="history-stats">
        <div className="stat">
          <span className="stat-label">Total:</span>
          <span className="stat-value">{history.length}</span>
        </div>
        <div className="stat">
          <span className="stat-label">Successful:</span>
          <span className="stat-value">
            {history.filter(e => e.result.success).length}
          </span>
        </div>
        <div className="stat">
          <span className="stat-label">Failed:</span>
          <span className="stat-value">
            {history.filter(e => !e.result.success).length}
          </span>
        </div>
        <div className="stat">
          <span className="stat-label">Filtered:</span>
          <span className="stat-value">{filteredHistory.length}</span>
        </div>
      </div>

      {/* History List */}
      <div className="history-list">
        {filteredHistory.length === 0 ? (
          <div className="empty-state">
            <p>No calculations in history</p>
            <p className="hint">Run some calculations to see them here</p>
          </div>
        ) : (
          filteredHistory.map(entry => (
            <div
              key={entry.id}
              className={`history-entry ${entry.result.success ? 'success' : 'failed'}`}
            >
              <div className="entry-header">
                <div className="entry-info">
                  <span className="entry-type">{entry.input.type}</span>
                  <span className="entry-time">{formatDate(entry.timestamp)}</span>
                </div>
                <div className="entry-actions">
                  <span className="entry-duration">
                    {formatDuration(entry.result.executionTime)}
                  </span>
                  <button
                    className="delete-btn"
                    onClick={() => deleteEntry(entry.id)}
                    title="Delete entry"
                  >
                    ×
                  </button>
                </div>
              </div>

              <div className="entry-content">
                {entry.result.success ? (
                  <div className="entry-result">
                    <pre>{JSON.stringify(entry.result.result, null, 2)}</pre>
                  </div>
                ) : (
                  <div className="entry-error">
                    <span className="error-label">Error:</span>
                    <span className="error-message">{entry.result.error}</span>
                  </div>
                )}
              </div>

              {entry.notes && (
                <div className="entry-notes">
                  <strong>Notes:</strong> {entry.notes}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

// Helper function to be called from other components
export function addToHistory(entry: CalculationHistoryEntry): void {
  const stored = localStorage.getItem('gu_calculation_history');
  const history = stored ? JSON.parse(stored) : [];
  const newHistory = [entry, ...history].slice(0, 100);
  localStorage.setItem('gu_calculation_history', JSON.stringify(newHistory));
}
