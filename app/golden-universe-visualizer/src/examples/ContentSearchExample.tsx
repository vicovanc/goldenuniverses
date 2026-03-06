/**
 * Example React Component: Content Search
 *
 * Demonstrates how to use the contentService API to search and display
 * Golden Universe content in a React application.
 */

import React, { useState, useEffect } from 'react';
import contentService from '../services/contentService';
import type { SearchResult, ContentCatalog } from '../types/content';

interface ContentStats {
  totalTheories: number;
  totalDerivations: number;
  totalPythonScripts: number;
  totalEquations: number;
  totalPrecisionResults: number;
}

export const ContentSearchExample: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [stats, setStats] = useState<ContentStats | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load statistics on mount
  useEffect(() => {
    const loadStats = async () => {
      try {
        const contentStats = await contentService.getContentStats();
        setStats(contentStats);
      } catch (err) {
        console.error('Failed to load stats:', err);
        setError('Failed to load content statistics');
      }
    };

    loadStats();
  }, []);

  // Handle search
  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!searchQuery.trim()) {
      setSearchResults([]);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const results = await contentService.searchContent({
        query: searchQuery,
        type: 'all',
        limit: 20
      });

      setSearchResults(results);
    } catch (err) {
      console.error('Search failed:', err);
      setError('Search failed. Please try again.');
      setSearchResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1>Golden Universe Content Search</h1>

      {/* Statistics */}
      {stats && (
        <div style={{
          background: '#f5f5f5',
          padding: '20px',
          borderRadius: '8px',
          marginBottom: '20px'
        }}>
          <h2>Content Statistics</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '10px' }}>
            <div>
              <strong>Theory Documents:</strong> {stats.totalTheories}
            </div>
            <div>
              <strong>Derivation Folders:</strong> {stats.totalDerivations}
            </div>
            <div>
              <strong>Python Scripts:</strong> {stats.totalPythonScripts}
            </div>
            <div>
              <strong>Equations:</strong> {stats.totalEquations}
            </div>
            <div>
              <strong>Precision Results:</strong> {stats.totalPrecisionResults}
            </div>
          </div>
        </div>
      )}

      {/* Search Form */}
      <form onSubmit={handleSearch} style={{ marginBottom: '20px' }}>
        <div style={{ display: 'flex', gap: '10px' }}>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search theories, derivations, equations..."
            style={{
              flex: 1,
              padding: '10px',
              fontSize: '16px',
              border: '1px solid #ccc',
              borderRadius: '4px'
            }}
          />
          <button
            type="submit"
            disabled={loading}
            style={{
              padding: '10px 20px',
              fontSize: '16px',
              background: '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: loading ? 'not-allowed' : 'pointer'
            }}
          >
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>
      </form>

      {/* Error Message */}
      {error && (
        <div style={{
          background: '#ffebee',
          color: '#c62828',
          padding: '10px',
          borderRadius: '4px',
          marginBottom: '20px'
        }}>
          {error}
        </div>
      )}

      {/* Search Results */}
      {searchResults.length > 0 && (
        <div>
          <h2>Search Results ({searchResults.length})</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
            {searchResults.map((result) => (
              <SearchResultCard key={result.id} result={result} />
            ))}
          </div>
        </div>
      )}

      {/* No Results */}
      {!loading && searchQuery && searchResults.length === 0 && (
        <div style={{
          textAlign: 'center',
          padding: '40px',
          color: '#666'
        }}>
          No results found for "{searchQuery}"
        </div>
      )}
    </div>
  );
};

/**
 * Individual Search Result Card
 */
const SearchResultCard: React.FC<{ result: SearchResult }> = ({ result }) => {
  const getTypeColor = (type: string) => {
    switch (type) {
      case 'theory': return '#4CAF50';
      case 'derivation': return '#2196F3';
      case 'python': return '#FF9800';
      case 'equation': return '#9C27B0';
      default: return '#757575';
    }
  };

  return (
    <div style={{
      border: '1px solid #ddd',
      borderRadius: '8px',
      padding: '15px',
      background: 'white',
      transition: 'box-shadow 0.2s',
      cursor: 'pointer'
    }}
    onMouseEnter={(e) => {
      e.currentTarget.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
    }}
    onMouseLeave={(e) => {
      e.currentTarget.style.boxShadow = 'none';
    }}
    onClick={() => {
      // Navigate to result URL
      if (result.url) {
        window.location.href = result.url;
      }
    }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
        <span style={{
          background: getTypeColor(result.type),
          color: 'white',
          padding: '4px 8px',
          borderRadius: '4px',
          fontSize: '12px',
          fontWeight: 'bold',
          textTransform: 'uppercase'
        }}>
          {result.type}
        </span>
        <span style={{
          fontSize: '12px',
          color: '#666'
        }}>
          Score: {result.relevanceScore}
        </span>
      </div>

      <h3 style={{ margin: '0 0 10px 0', fontSize: '18px' }}>
        {result.title}
      </h3>

      {result.description && (
        <p style={{ margin: '0 0 10px 0', color: '#666', fontSize: '14px' }}>
          {result.description}
        </p>
      )}

      <div style={{ fontSize: '12px', color: '#999' }}>
        Path: {result.path}
      </div>
    </div>
  );
};

/**
 * Example: Display Theory Documents
 */
export const TheoryDocumentsList: React.FC = () => {
  const [theories, setTheories] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadTheories = async () => {
      try {
        const docs = await contentService.getTheoryDocuments();
        setTheories(docs);
      } catch (err) {
        console.error('Failed to load theories:', err);
      } finally {
        setLoading(false);
      }
    };

    loadTheories();
  }, []);

  if (loading) {
    return <div>Loading theories...</div>;
  }

  return (
    <div style={{ padding: '20px' }}>
      <h2>Theory Documents ({theories.length})</h2>
      <ul>
        {theories.map((theory) => (
          <li key={theory.id} style={{ marginBottom: '10px' }}>
            <strong>{theory.title}</strong>
            <br />
            <small>
              {theory.wordCount} words • {theory.equations?.length || 0} equations
            </small>
          </li>
        ))}
      </ul>
    </div>
  );
};

/**
 * Example: Display Precision Results
 */
export const PrecisionResultsList: React.FC = () => {
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadResults = async () => {
      try {
        const best = await contentService.getBestPrecisionResults(10);
        setResults(best);
      } catch (err) {
        console.error('Failed to load precision results:', err);
      } finally {
        setLoading(false);
      }
    };

    loadResults();
  }, []);

  if (loading) {
    return <div>Loading precision results...</div>;
  }

  return (
    <div style={{ padding: '20px' }}>
      <h2>Best Precision Results (Top 10)</h2>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ background: '#f5f5f5' }}>
            <th style={{ padding: '10px', textAlign: 'left', border: '1px solid #ddd' }}>Description</th>
            <th style={{ padding: '10px', textAlign: 'left', border: '1px solid #ddd' }}>Value</th>
            <th style={{ padding: '10px', textAlign: 'left', border: '1px solid #ddd' }}>Unit</th>
          </tr>
        </thead>
        <tbody>
          {results.map((result, index) => (
            <tr key={index}>
              <td style={{ padding: '10px', border: '1px solid #ddd' }}>
                {result.description}
              </td>
              <td style={{ padding: '10px', border: '1px solid #ddd' }}>
                {result.value.toFixed(3)}
              </td>
              <td style={{ padding: '10px', border: '1px solid #ddd' }}>
                {result.unit}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ContentSearchExample;
