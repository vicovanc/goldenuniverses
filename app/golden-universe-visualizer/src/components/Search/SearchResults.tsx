/**
 * SearchResults Component - GU-028: Search Results Page
 *
 * Features:
 * - Display search results effectively
 * - Grouped by category
 * - Highlighted search terms
 * - Relevance scoring
 * - Pagination
 * - Preview snippets
 * - Quick actions (Open, Run, Copy)
 */

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { SearchResult } from '../../services/searchService';

interface SearchResultsProps {
  results: SearchResult[];
  query: string;
  loading: boolean;
  totalResults: number;
  onLoadMore?: () => void;
  hasMore?: boolean;
}

const RESULTS_PER_PAGE = 10;

const SearchResults: React.FC<SearchResultsProps> = ({
  results,
  query,
  loading,
  totalResults,
  onLoadMore,
  hasMore = false,
}) => {
  const navigate = useNavigate();
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [expandedResults, setExpandedResults] = useState<Set<string>>(new Set());

  // Group results by category
  const groupedResults = results.reduce((acc, result) => {
    const category = result.category || 'Other';
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(result);
    return acc;
  }, {} as Record<string, SearchResult[]>);

  const categories = Object.keys(groupedResults).sort();

  const handleResultClick = (result: SearchResult) => {
    // Navigate to the appropriate page based on result type
    switch (result.type) {
      case 'theory':
        navigate(`/theory/${result.id}`);
        break;
      case 'derivation':
        navigate(`/derivations/${result.id}`);
        break;
      case 'equation':
        navigate(`/equations/${result.id}`);
        break;
      case 'python':
        navigate(`/calculations/${result.id}`);
        break;
      default:
        console.warn('Unknown result type:', result.type);
    }
  };

  const handleCopyPath = async (path: string) => {
    try {
      await navigator.clipboard.writeText(path);
      // Show toast notification (implement toast system if needed)
      console.log('Path copied to clipboard');
    } catch (error) {
      console.error('Failed to copy path:', error);
    }
  };

  const handleRunPython = (result: SearchResult) => {
    if (result.type === 'python') {
      navigate(`/calculations/${result.id}?autorun=true`);
    }
  };

  const toggleExpanded = (id: string) => {
    setExpandedResults(prev => {
      const newSet = new Set(prev);
      if (newSet.has(id)) {
        newSet.delete(id);
      } else {
        newSet.add(id);
      }
      return newSet;
    });
  };

  const highlightText = (text: string, query: string): React.ReactNode => {
    if (!query.trim()) {
      return text;
    }

    const terms = query.toLowerCase().split(/\s+/);
    const parts: React.ReactNode[] = [];
    let lastIndex = 0;

    const matches: Array<{ start: number; end: number }> = [];

    // Find all matches
    terms.forEach(term => {
      const lowerText = text.toLowerCase();
      let index = lowerText.indexOf(term, 0);
      while (index !== -1) {
        matches.push({ start: index, end: index + term.length });
        index = lowerText.indexOf(term, index + 1);
      }
    });

    // Sort and merge overlapping matches
    matches.sort((a, b) => a.start - b.start);
    const mergedMatches: Array<{ start: number; end: number }> = [];
    matches.forEach(match => {
      if (mergedMatches.length === 0) {
        mergedMatches.push(match);
      } else {
        const last = mergedMatches[mergedMatches.length - 1];
        if (match.start <= last.end) {
          last.end = Math.max(last.end, match.end);
        } else {
          mergedMatches.push(match);
        }
      }
    });

    // Create highlighted text
    mergedMatches.forEach((match, i) => {
      parts.push(text.slice(lastIndex, match.start));
      parts.push(
        <mark key={i} className="search-results__highlight">
          {text.slice(match.start, match.end)}
        </mark>
      );
      lastIndex = match.end;
    });
    parts.push(text.slice(lastIndex));

    return parts;
  };

  const getTypeIcon = (type: string): string => {
    switch (type) {
      case 'theory':
        return '📚';
      case 'derivation':
        return '📐';
      case 'python':
        return '🐍';
      case 'equation':
        return '∑';
      default:
        return '📄';
    }
  };

  const getRelevanceColor = (relevance: number): string => {
    if (relevance >= 0.8) return 'high';
    if (relevance >= 0.5) return 'medium';
    return 'low';
  };

  if (loading) {
    return (
      <div className="search-results search-results--loading">
        <div className="search-results__spinner" />
        <p>Searching...</p>
      </div>
    );
  }

  if (results.length === 0 && query) {
    return (
      <div className="search-results search-results--empty">
        <div className="search-results__empty-icon">🔍</div>
        <h3>No results found</h3>
        <p>
          No results found for "<strong>{query}</strong>"
        </p>
        <div className="search-results__suggestions">
          <p>Try:</p>
          <ul>
            <li>Using different keywords</li>
            <li>Checking your spelling</li>
            <li>Using more general terms</li>
            <li>Removing filters</li>
          </ul>
        </div>
      </div>
    );
  }

  return (
    <div className="search-results">
      {/* Results Header */}
      <div className="search-results__header">
        <h2 className="search-results__title">
          {totalResults} {totalResults === 1 ? 'result' : 'results'} for "
          {query}"
        </h2>
      </div>

      {/* Grouped Results */}
      {categories.map(category => (
        <div key={category} className="search-results__category">
          <h3 className="search-results__category-title">
            {category}
            <span className="search-results__category-count">
              {groupedResults[category].length}
            </span>
          </h3>

          <div className="search-results__list">
            {groupedResults[category].map(result => {
              const isExpanded = expandedResults.has(result.id);

              return (
                <article
                  key={result.id}
                  className="search-results__item"
                >
                  {/* Result Header */}
                  <div className="search-results__item-header">
                    <span className="search-results__item-icon">
                      {getTypeIcon(result.type)}
                    </span>
                    <h4
                      className="search-results__item-title"
                      onClick={() => handleResultClick(result)}
                    >
                      {highlightText(result.title, query)}
                    </h4>
                    <div
                      className={`search-results__relevance search-results__relevance--${getRelevanceColor(
                        result.relevance
                      )}`}
                      title={`Relevance: ${(result.relevance * 100).toFixed(0)}%`}
                    >
                      {(result.relevance * 100).toFixed(0)}%
                    </div>
                  </div>

                  {/* Result Path */}
                  <div className="search-results__item-path">
                    {result.path}
                  </div>

                  {/* Result Snippet */}
                  <div className="search-results__item-snippet">
                    {highlightText(result.snippet, query)}
                  </div>

                  {/* Highlights */}
                  {result.highlights && result.highlights.length > 0 && (
                    <div className="search-results__item-highlights">
                      {result.highlights.slice(0, 2).map((highlight, i) => (
                        <div
                          key={i}
                          className="search-results__item-highlight"
                        >
                          {highlightText(highlight, query)}
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Metadata */}
                  {result.metadata && (
                    <div className="search-results__item-metadata">
                      {result.metadata.wordCount && (
                        <span className="search-results__item-meta">
                          {result.metadata.wordCount.toLocaleString()} words
                        </span>
                      )}
                      {result.metadata.equations !== undefined && (
                        <span className="search-results__item-meta">
                          {result.metadata.equations} equations
                        </span>
                      )}
                      {result.metadata.modifiedAt && (
                        <span className="search-results__item-meta">
                          Updated:{' '}
                          {new Date(result.metadata.modifiedAt).toLocaleDateString()}
                        </span>
                      )}
                    </div>
                  )}

                  {/* Actions */}
                  <div className="search-results__item-actions">
                    <button
                      className="search-results__item-action"
                      onClick={() => handleResultClick(result)}
                      title="Open"
                    >
                      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                        <path
                          d="M8 2v12M2 8h12"
                          stroke="currentColor"
                          strokeWidth="2"
                          strokeLinecap="round"
                        />
                      </svg>
                      Open
                    </button>

                    {result.type === 'python' && (
                      <button
                        className="search-results__item-action"
                        onClick={() => handleRunPython(result)}
                        title="Run"
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                          <path
                            d="M4 2l8 6-8 6V2z"
                            fill="currentColor"
                          />
                        </svg>
                        Run
                      </button>
                    )}

                    <button
                      className="search-results__item-action"
                      onClick={() => handleCopyPath(result.path)}
                      title="Copy path"
                    >
                      <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                        <rect
                          x="4"
                          y="4"
                          width="8"
                          height="10"
                          stroke="currentColor"
                          strokeWidth="2"
                          fill="none"
                        />
                        <path
                          d="M6 4V2h8v10h-2"
                          stroke="currentColor"
                          strokeWidth="2"
                          fill="none"
                        />
                      </svg>
                      Copy
                    </button>

                    <button
                      className="search-results__item-action"
                      onClick={() => toggleExpanded(result.id)}
                      title={isExpanded ? 'Show less' : 'Show more'}
                    >
                      {isExpanded ? 'Less' : 'More'}
                    </button>
                  </div>

                  {/* Expanded Content */}
                  {isExpanded && (
                    <div className="search-results__item-expanded">
                      <pre className="search-results__item-content">
                        {result.content.slice(0, 500)}
                        {result.content.length > 500 && '...'}
                      </pre>
                    </div>
                  )}
                </article>
              );
            })}
          </div>
        </div>
      ))}

      {/* Pagination / Load More */}
      {hasMore && onLoadMore && (
        <div className="search-results__footer">
          <button
            className="search-results__load-more"
            onClick={onLoadMore}
            disabled={loading}
          >
            {loading ? 'Loading...' : 'Load More Results'}
          </button>
        </div>
      )}
    </div>
  );
};

export default SearchResults;
