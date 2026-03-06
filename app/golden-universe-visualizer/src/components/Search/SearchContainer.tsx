/**
 * SearchContainer Component - Main Search Interface
 *
 * Integrates all search components:
 * - GU-026: Search Index Builder
 * - GU-027: Advanced Search UI
 * - GU-028: Search Results Page
 * - GU-029: Search Suggestions
 * - GU-030: Voice Search
 */

import React, { useState, useEffect } from 'react';
import SearchBar from './SearchBar';
import SearchFilters from './SearchFilters';
import SearchResults from './SearchResults';
import SearchHistory from './SearchHistory';
import {
  searchService,
  SearchResult,
  SearchFilters as SearchFiltersType,
} from '../../services/searchService';

interface SearchContainerProps {
  initialQuery?: string;
  initialFilters?: SearchFiltersType;
  autoFocus?: boolean;
}

const SearchContainer: React.FC<SearchContainerProps> = ({
  initialQuery = '',
  initialFilters = {},
  autoFocus = false,
}) => {
  const [query, setQuery] = useState<string>(initialQuery);
  const [filters, setFilters] = useState<SearchFiltersType>(initialFilters);
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [showFilters, setShowFilters] = useState<boolean>(false);
  const [showHistory, setShowHistory] = useState<boolean>(false);
  const [indexReady, setIndexReady] = useState<boolean>(false);
  const [indexStats, setIndexStats] = useState<any>(null);

  // Initialize search index on mount
  useEffect(() => {
    const initializeIndex = async () => {
      try {
        if (!searchService.isIndexReady()) {
          console.log('Building search index...');
          await searchService.buildIndex();
          console.log('Search index ready');
        }
        setIndexReady(true);
        setIndexStats(searchService.getIndexStats());
      } catch (error) {
        console.error('Failed to initialize search index:', error);
      }
    };

    initializeIndex();
  }, []);

  // Perform initial search if query provided
  useEffect(() => {
    if (initialQuery && indexReady) {
      handleSearch(initialQuery, initialFilters);
    }
  }, [initialQuery, indexReady]);

  const handleSearch = async (
    searchQuery: string,
    searchFilters: SearchFiltersType
  ) => {
    if (!searchQuery.trim()) {
      setResults([]);
      return;
    }

    setQuery(searchQuery);
    setFilters(searchFilters);
    setLoading(true);

    try {
      const searchResults = await searchService.search(
        searchQuery,
        searchFilters,
        50
      );
      setResults(searchResults);
    } catch (error) {
      console.error('Search failed:', error);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterToggle = () => {
    setShowFilters(prev => !prev);
  };

  const handleFiltersChange = (newFilters: SearchFiltersType) => {
    setFilters(newFilters);
    if (query) {
      handleSearch(query, newFilters);
    }
  };

  const handleHistorySelect = (historyQuery: string) => {
    setShowHistory(false);
    handleSearch(historyQuery, {});
  };

  const handleClearHistory = () => {
    searchService.clearSearchHistory();
    setShowHistory(false);
  };

  const toggleHistory = () => {
    setShowHistory(prev => !prev);
  };

  return (
    <div className="search-container">
      {/* Search Header */}
      <div className="search-container__header">
        <div className="search-container__logo">
          <svg
            width="32"
            height="32"
            viewBox="0 0 32 32"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M16 2L4 9v14l12 7 12-7V9L16 2z"
              stroke="currentColor"
              strokeWidth="2"
              fill="none"
            />
            <circle
              cx="16"
              cy="16"
              r="6"
              stroke="currentColor"
              strokeWidth="2"
              fill="none"
            />
          </svg>
          <h1 className="search-container__title">Golden Universe Search</h1>
        </div>

        {/* History Toggle */}
        <button
          className={`search-container__history-toggle ${showHistory ? 'active' : ''}`}
          onClick={toggleHistory}
          aria-label="Toggle search history"
        >
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path
              d="M10 18a8 8 0 1 0 0-16 8 8 0 0 0 0 16zM10 6v4l3 3"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          History
        </button>
      </div>

      {/* Index Status */}
      {!indexReady && (
        <div className="search-container__index-status">
          <div className="search-container__spinner" />
          <span>Building search index...</span>
        </div>
      )}

      {indexReady && indexStats && (
        <div className="search-container__stats">
          <span className="search-container__stat">
            {indexStats.total.toLocaleString()} documents indexed
          </span>
          <span className="search-container__stat-separator">•</span>
          <span className="search-container__stat">
            {indexStats.theories} theories
          </span>
          <span className="search-container__stat-separator">•</span>
          <span className="search-container__stat">
            {indexStats.derivations} derivations
          </span>
          <span className="search-container__stat-separator">•</span>
          <span className="search-container__stat">
            {indexStats.python} Python files
          </span>
          <span className="search-container__stat-separator">•</span>
          <span className="search-container__stat">
            {indexStats.equations} equations
          </span>
        </div>
      )}

      {/* Search Bar */}
      <SearchBar
        onSearch={handleSearch}
        onFilterToggle={handleFilterToggle}
        showFilters={showFilters}
        initialQuery={initialQuery}
        autoFocus={autoFocus}
      />

      {/* Search Filters */}
      <SearchFilters
        onFiltersChange={handleFiltersChange}
        initialFilters={initialFilters}
        show={showFilters}
      />

      {/* Search History */}
      <SearchHistory
        history={searchService.getSearchHistory()}
        onSearchSelect={handleHistorySelect}
        onClearHistory={handleClearHistory}
        show={showHistory}
      />

      {/* Search Results */}
      <SearchResults
        results={results}
        query={query}
        loading={loading}
        totalResults={results.length}
      />

      {/* No results placeholder when not searching */}
      {!loading && !query && !showHistory && indexReady && (
        <div className="search-container__placeholder">
          <div className="search-container__placeholder-icon">
            <svg
              width="64"
              height="64"
              viewBox="0 0 64 64"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M28 48a20 20 0 1 0 0-40 20 20 0 0 0 0 40zM56 56l-13.5-13.5"
                stroke="currentColor"
                strokeWidth="4"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </div>
          <h2 className="search-container__placeholder-title">
            Search the Golden Universe
          </h2>
          <p className="search-container__placeholder-text">
            Find theories, derivations, equations, and Python calculations.
            Use advanced filters to refine your search.
          </p>
          <div className="search-container__placeholder-examples">
            <h3>Try searching for:</h3>
            <ul>
              <li>
                <button onClick={() => handleSearch('electron mass', {})}>
                  electron mass
                </button>
              </li>
              <li>
                <button onClick={() => handleSearch('golden ratio', {})}>
                  golden ratio
                </button>
              </li>
              <li>
                <button onClick={() => handleSearch('nuclear binding', {})}>
                  nuclear binding
                </button>
              </li>
              <li>
                <button onClick={() => handleSearch('quantum field', {})}>
                  quantum field
                </button>
              </li>
            </ul>
          </div>

          {/* Keyboard shortcuts */}
          <div className="search-container__shortcuts">
            <h3>Keyboard Shortcuts</h3>
            <div className="search-container__shortcuts-list">
              <div className="search-container__shortcut">
                <kbd>⌘</kbd> <kbd>K</kbd>
                <span>Focus search</span>
              </div>
              <div className="search-container__shortcut">
                <kbd>↑</kbd> <kbd>↓</kbd>
                <span>Navigate suggestions</span>
              </div>
              <div className="search-container__shortcut">
                <kbd>Enter</kbd>
                <span>Search / Select</span>
              </div>
              <div className="search-container__shortcut">
                <kbd>Esc</kbd>
                <span>Close suggestions</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchContainer;
