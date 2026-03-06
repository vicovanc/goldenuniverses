/**
 * SearchHistory Component - GU-027: Search History
 *
 * Features:
 * - Display recent searches
 * - Click to re-run search
 * - Clear history
 * - Show timestamp and result count
 */

import React from 'react';
import { SearchHistoryEntry } from '../../services/searchService';

interface SearchHistoryProps {
  history: SearchHistoryEntry[];
  onSearchSelect: (query: string) => void;
  onClearHistory: () => void;
  show: boolean;
}

const SearchHistory: React.FC<SearchHistoryProps> = ({
  history,
  onSearchSelect,
  onClearHistory,
  show,
}) => {
  const formatTimestamp = (timestamp: Date): string => {
    const now = new Date();
    const diff = now.getTime() - timestamp.getTime();
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (days > 0) {
      return `${days} day${days > 1 ? 's' : ''} ago`;
    } else if (hours > 0) {
      return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    } else if (minutes > 0) {
      return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    } else {
      return 'Just now';
    }
  };

  const handleSearchClick = (query: string) => {
    onSearchSelect(query);
  };

  const handleClearClick = () => {
    if (window.confirm('Clear all search history?')) {
      onClearHistory();
    }
  };

  if (!show || history.length === 0) {
    return null;
  }

  return (
    <div className="search-history">
      <div className="search-history__header">
        <h3 className="search-history__title">Recent Searches</h3>
        <button
          className="search-history__clear"
          onClick={handleClearClick}
          aria-label="Clear search history"
        >
          Clear All
        </button>
      </div>

      <ul className="search-history__list">
        {history.map((entry, index) => (
          <li
            key={`${entry.query}-${entry.timestamp.getTime()}-${index}`}
            className="search-history__item"
            onClick={() => handleSearchClick(entry.query)}
          >
            <div className="search-history__item-content">
              <span className="search-history__item-icon">🕐</span>
              <div className="search-history__item-details">
                <span className="search-history__item-query">
                  {entry.query}
                </span>
                <div className="search-history__item-meta">
                  <span className="search-history__item-time">
                    {formatTimestamp(entry.timestamp)}
                  </span>
                  <span className="search-history__item-separator">•</span>
                  <span className="search-history__item-results">
                    {entry.resultsCount} result
                    {entry.resultsCount !== 1 ? 's' : ''}
                  </span>
                </div>
              </div>
            </div>
            <svg
              className="search-history__item-arrow"
              width="16"
              height="16"
              viewBox="0 0 16 16"
              fill="none"
            >
              <path
                d="M6 4l4 4-4 4"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SearchHistory;
