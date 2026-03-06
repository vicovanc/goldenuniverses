/**
 * SearchSuggestions Component - GU-029: Search Suggestions
 *
 * Features:
 * - Auto-complete as typing
 * - Recent searches
 * - Popular searches
 * - Typo correction
 * - Category suggestions
 */

import React, { useState, useEffect } from 'react';
import { searchService, SearchSuggestion } from '../../services/searchService';

interface SearchSuggestionsProps {
  query: string;
  onSelect: (suggestion: SearchSuggestion) => void;
  selectedIndex: number;
}

const SearchSuggestions: React.FC<SearchSuggestionsProps> = ({
  query,
  onSelect,
  selectedIndex,
}) => {
  const [suggestions, setSuggestions] = useState<SearchSuggestion[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    const fetchSuggestions = async () => {
      setLoading(true);
      try {
        const results = await searchService.getSuggestions(query);
        setSuggestions(results);
      } catch (error) {
        console.error('Failed to fetch suggestions:', error);
        setSuggestions([]);
      } finally {
        setLoading(false);
      }
    };

    fetchSuggestions();
  }, [query]);

  const getSuggestionIcon = (type: string): string => {
    switch (type) {
      case 'recent':
        return '🕐';
      case 'popular':
        return '🔥';
      case 'typo':
        return '✨';
      case 'category':
        return '📁';
      default:
        return '🔍';
    }
  };

  const getSuggestionLabel = (type: string): string => {
    switch (type) {
      case 'recent':
        return 'Recent';
      case 'popular':
        return 'Popular';
      case 'typo':
        return 'Did you mean';
      case 'category':
        return 'Category';
      default:
        return '';
    }
  };

  const handleSuggestionClick = (suggestion: SearchSuggestion) => {
    onSelect(suggestion);
  };

  if (suggestions.length === 0 && !loading) {
    return null;
  }

  return (
    <div className="search-suggestions">
      {loading && (
        <div className="search-suggestions__loading">
          <div className="search-suggestions__spinner" />
          <span>Loading suggestions...</span>
        </div>
      )}

      {!loading && suggestions.length > 0 && (
        <ul className="search-suggestions__list">
          {suggestions.map((suggestion, index) => (
            <li
              key={`${suggestion.type}-${suggestion.text}-${index}`}
              className={`search-suggestions__item ${
                index === selectedIndex ? 'selected' : ''
              }`}
              onClick={() => handleSuggestionClick(suggestion)}
              role="option"
              aria-selected={index === selectedIndex}
            >
              <span className="search-suggestions__icon">
                {getSuggestionIcon(suggestion.type)}
              </span>

              <div className="search-suggestions__content">
                <span className="search-suggestions__text">
                  {highlightMatch(suggestion.text, query)}
                </span>

                {suggestion.type !== 'recent' && (
                  <span className="search-suggestions__label">
                    {getSuggestionLabel(suggestion.type)}
                    {suggestion.count !== undefined && (
                      <span className="search-suggestions__count">
                        {suggestion.count}
                      </span>
                    )}
                  </span>
                )}
              </div>

              {suggestion.category && (
                <span className="search-suggestions__category">
                  {suggestion.category}
                </span>
              )}
            </li>
          ))}
        </ul>
      )}

      {!loading && suggestions.length === 0 && query && (
        <div className="search-suggestions__empty">
          <span>No suggestions found</span>
        </div>
      )}
    </div>
  );
};

/**
 * Highlight matching parts of the suggestion text
 */
const highlightMatch = (text: string, query: string): React.ReactNode => {
  if (!query.trim()) {
    return text;
  }

  const lowerText = text.toLowerCase();
  const lowerQuery = query.toLowerCase();
  const index = lowerText.indexOf(lowerQuery);

  if (index === -1) {
    return text;
  }

  const before = text.slice(0, index);
  const match = text.slice(index, index + query.length);
  const after = text.slice(index + query.length);

  return (
    <>
      {before}
      <strong className="search-suggestions__highlight">{match}</strong>
      {after}
    </>
  );
};

export default SearchSuggestions;
