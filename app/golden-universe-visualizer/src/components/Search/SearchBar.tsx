/**
 * SearchBar Component - GU-027: Advanced Search UI
 *
 * Features:
 * - Search input with icon
 * - Filter toggle button
 * - Voice search integration
 * - Search suggestions dropdown
 * - Keyboard shortcuts (Ctrl+K / Cmd+K)
 */

import React, { useState, useEffect, useRef, KeyboardEvent } from 'react';
import VoiceSearch from './VoiceSearch';
import SearchSuggestions from './SearchSuggestions';
import { SearchFilters, SearchSuggestion } from '../../services/searchService';

interface SearchBarProps {
  onSearch: (query: string, filters: SearchFilters) => void;
  onFilterToggle: () => void;
  showFilters: boolean;
  placeholder?: string;
  initialQuery?: string;
  autoFocus?: boolean;
}

const SearchBar: React.FC<SearchBarProps> = ({
  onSearch,
  onFilterToggle,
  showFilters,
  placeholder = 'Search theories, derivations, equations, and Python files...',
  initialQuery = '',
  autoFocus = false,
}) => {
  const [query, setQuery] = useState<string>(initialQuery);
  const [showSuggestions, setShowSuggestions] = useState<boolean>(false);
  const [suggestions, setSuggestions] = useState<SearchSuggestion[]>([]);
  const [selectedSuggestionIndex, setSelectedSuggestionIndex] = useState<number>(-1);
  const inputRef = useRef<HTMLInputElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (autoFocus && inputRef.current) {
      inputRef.current.focus();
    }
  }, [autoFocus]);

  // Keyboard shortcut: Ctrl+K or Cmd+K to focus search
  useEffect(() => {
    const handleKeyDown = (e: globalThis.KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        inputRef.current?.focus();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Click outside to close suggestions
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    setShowSuggestions(true);
    setSelectedSuggestionIndex(-1);
  };

  const handleInputFocus = () => {
    setShowSuggestions(true);
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      if (selectedSuggestionIndex >= 0 && suggestions[selectedSuggestionIndex]) {
        handleSuggestionSelect(suggestions[selectedSuggestionIndex]);
      } else {
        handleSearch();
      }
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedSuggestionIndex(prev =>
        prev < suggestions.length - 1 ? prev + 1 : prev
      );
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedSuggestionIndex(prev => (prev > 0 ? prev - 1 : -1));
    } else if (e.key === 'Escape') {
      setShowSuggestions(false);
      inputRef.current?.blur();
    }
  };

  const handleSearch = () => {
    if (query.trim()) {
      onSearch(query, {});
      setShowSuggestions(false);
    }
  };

  const handleSuggestionSelect = (suggestion: SearchSuggestion) => {
    setQuery(suggestion.text);
    setShowSuggestions(false);
    onSearch(suggestion.text, {});
  };

  const handleVoiceResult = (transcript: string) => {
    setQuery(transcript);
    if (transcript.trim()) {
      onSearch(transcript, {});
    }
  };

  const handleClearSearch = () => {
    setQuery('');
    inputRef.current?.focus();
  };

  return (
    <div className="search-bar" ref={containerRef}>
      <div className="search-bar__container">
        <div className="search-bar__input-wrapper">
          {/* Search Icon */}
          <svg
            className="search-bar__icon search-bar__icon--search"
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M9 17A8 8 0 1 0 9 1a8 8 0 0 0 0 16zM19 19l-4.35-4.35"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>

          {/* Search Input */}
          <input
            ref={inputRef}
            type="text"
            className="search-bar__input"
            placeholder={placeholder}
            value={query}
            onChange={handleInputChange}
            onFocus={handleInputFocus}
            onKeyDown={handleKeyDown}
            aria-label="Search"
            autoComplete="off"
          />

          {/* Keyboard Shortcut Hint */}
          {!query && (
            <div className="search-bar__shortcut">
              <kbd>⌘</kbd>
              <kbd>K</kbd>
            </div>
          )}

          {/* Clear Button */}
          {query && (
            <button
              className="search-bar__clear"
              onClick={handleClearSearch}
              aria-label="Clear search"
            >
              <svg
                width="16"
                height="16"
                viewBox="0 0 16 16"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M12 4L4 12M4 4l8 8"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
            </button>
          )}

          {/* Voice Search */}
          <VoiceSearch onResult={handleVoiceResult} />
        </div>

        {/* Filter Toggle Button */}
        <button
          className={`search-bar__filter-toggle ${showFilters ? 'active' : ''}`}
          onClick={onFilterToggle}
          aria-label="Toggle filters"
          title="Toggle filters"
        >
          <svg
            width="20"
            height="20"
            viewBox="0 0 20 20"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M2 4h16M5 10h10M8 16h4"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <span>Filters</span>
        </button>

        {/* Search Button */}
        <button
          className="search-bar__button"
          onClick={handleSearch}
          disabled={!query.trim()}
          aria-label="Search"
        >
          Search
        </button>
      </div>

      {/* Search Suggestions Dropdown */}
      {showSuggestions && (
        <SearchSuggestions
          query={query}
          onSelect={handleSuggestionSelect}
          selectedIndex={selectedSuggestionIndex}
        />
      )}
    </div>
  );
};

export default SearchBar;
