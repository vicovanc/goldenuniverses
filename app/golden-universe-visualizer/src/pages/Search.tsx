/**
 * Search Page
 *
 * Dedicated search page for Golden Universe content
 * EPIC-006: Search & Discovery System
 */

import React from 'react';
import { useSearchParams } from 'react-router-dom';
import { SearchContainer } from '../components/Search';

const SearchPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const initialQuery = searchParams.get('q') || '';

  return (
    <div className="search-page">
      <SearchContainer initialQuery={initialQuery} autoFocus={true} />
    </div>
  );
};

export default SearchPage;
