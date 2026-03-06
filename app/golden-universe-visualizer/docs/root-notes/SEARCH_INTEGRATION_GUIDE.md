# Search System Integration Guide

Quick guide to integrate the Search & Discovery system into the Golden Universe Visualizer.

---

## Quick Start (5 Minutes)

### 1. Add Search Route

Edit your router configuration (usually in `App.tsx` or `main.tsx`):

```tsx
import SearchPage from './pages/Search';

// Add to your routes
<Route path="/search" element={<SearchPage />} />
```

### 2. Add Navigation Link

Add a search link to your navigation menu:

```tsx
import { Link } from 'react-router-dom';

<Link to="/search">
  <svg width="20" height="20" viewBox="0 0 20 20">
    <path d="M9 17A8 8 0 1 0 9 1a8 8 0 0 0 0 16zM19 19l-4.35-4.35" />
  </svg>
  Search
</Link>
```

### 3. Initialize Index on App Load (Optional)

To pre-build the search index, add to your App.tsx or main component:

```tsx
import { searchService } from './services/searchService';
import { useEffect } from 'react';

function App() {
  useEffect(() => {
    // Pre-build search index for faster first search
    searchService.buildIndex().catch(console.error);
  }, []);

  // ... rest of your app
}
```

### 4. Test It

1. Run your app: `npm run dev`
2. Navigate to `/search`
3. Try searching for "electron mass" or "golden ratio"
4. Test voice search (Chrome/Firefox only)
5. Try filters and suggestions

---

## Advanced Integration

### Embed Search in Sidebar

```tsx
import { SearchBar } from './components/Search';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Sidebar() {
  const navigate = useNavigate();
  const [showFilters, setShowFilters] = useState(false);

  const handleSearch = (query: string) => {
    navigate(`/search?q=${encodeURIComponent(query)}`);
  };

  return (
    <div className="sidebar">
      <SearchBar
        onSearch={handleSearch}
        onFilterToggle={() => setShowFilters(!showFilters)}
        showFilters={showFilters}
        placeholder="Quick search..."
      />
      {/* ... rest of sidebar ... */}
    </div>
  );
}
```

### Add Search Button to Navbar

```tsx
import { useNavigate } from 'react-router-dom';

function Navbar() {
  const navigate = useNavigate();

  // Keyboard shortcut
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        navigate('/search');
      }
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [navigate]);

  return (
    <nav>
      <button onClick={() => navigate('/search')}>
        🔍 Search <kbd>⌘K</kbd>
      </button>
    </nav>
  );
}
```

### Deep Link to Search Results

```tsx
// Navigate with query
navigate('/search?q=nuclear+binding');

// Navigate with filters
const params = new URLSearchParams({
  q: 'electron',
  categories: 'Theory,Derivations',
});
navigate(`/search?${params}`);
```

### Programmatic Search

```tsx
import { searchService } from './services/searchService';

async function performSearch() {
  // Ensure index is built
  if (!searchService.isIndexReady()) {
    await searchService.buildIndex();
  }

  // Search with filters
  const results = await searchService.search('golden ratio', {
    categories: ['Theory'],
    precisionRange: { min: 95, max: 100 }
  });

  console.log(`Found ${results.length} results`);
  return results;
}
```

---

## Styling Customization

### Override Colors

Add to your main stylesheet:

```scss
// Override search colors
.search-container {
  --primary-color: #your-color;
  --surface-color: #your-surface;
  --text-color: #your-text;
}
```

### Custom Theme

The search system uses SCSS variables. Edit `Search.scss`:

```scss
// At the top of Search.scss
$primary-color: #your-primary-color;
$secondary-color: #your-secondary-color;
$background-color: #your-background;
// ... etc
```

### Hide Components

```scss
// Hide voice search
.voice-search {
  display: none;
}

// Hide filters
.search-filters {
  display: none;
}

// Hide history
.search-history {
  display: none;
}
```

---

## Configuration Options

### SearchContainer Props

```tsx
<SearchContainer
  initialQuery="electron mass"      // Pre-fill search query
  initialFilters={{                 // Pre-apply filters
    categories: ['Theory'],
    precisionRange: { min: 90 }
  }}
  autoFocus={true}                  // Auto-focus search input
/>
```

### SearchBar Props

```tsx
<SearchBar
  onSearch={(query, filters) => {}}
  onFilterToggle={() => {}}
  showFilters={false}
  placeholder="Custom placeholder..."
  initialQuery=""
  autoFocus={false}
/>
```

### Search Service Options

```typescript
// Search with options
await searchService.search(
  'query',
  { categories: ['Theory'] },  // filters
  50                            // limit
);
```

---

## Data Requirements

### Ensure Data Files Exist

The search system requires these files in `/public/data/`:

```
public/data/
├── content-index.json       # Theories and Python files
├── derivations-map.json     # Derivation documents
└── equations-catalog.json   # Equation catalog
```

### Data Format

#### content-index.json
```json
{
  "theories": [
    {
      "id": "unique-id",
      "path": "theory/file.md",
      "filename": "file.md",
      "title": "Theory Title",
      "content": "Full content...",
      "wordCount": 1000,
      "equations": [],
      "metadata": {},
      "createdAt": "2026-01-01",
      "modifiedAt": "2026-02-01"
    }
  ],
  "pythonFiles": [
    {
      "id": "unique-id",
      "path": "python/file.py",
      "filename": "file.py",
      "title": "Calculation Title",
      "content": "Full content...",
      "metadata": {},
      "createdAt": "2026-01-01"
    }
  ]
}
```

#### derivations-map.json
```json
{
  "derivations": [
    {
      "id": "unique-id",
      "path": "derivations/file.md",
      "filename": "file.md",
      "title": "Derivation Title",
      "content": "Full content...",
      "equations": [],
      "metadata": {}
    }
  ]
}
```

#### equations-catalog.json
```json
{
  "equations": [
    {
      "id": "unique-id",
      "name": "Equation Name",
      "latex": "E = mc^2",
      "description": "Description...",
      "sourcePath": "theory/file.md",
      "tags": ["physics", "relativity"]
    }
  ]
}
```

---

## Troubleshooting

### Search Not Working

1. **Check console for errors**
   ```bash
   Open DevTools → Console
   Look for search-related errors
   ```

2. **Verify data files**
   ```bash
   Open Network tab
   Check if data files are loading
   Verify file paths: /data/content-index.json
   ```

3. **Check index status**
   ```typescript
   console.log('Index ready:', searchService.isIndexReady());
   console.log('Stats:', searchService.getIndexStats());
   ```

### Voice Search Not Working

1. **Check browser compatibility**
   - Only works in Chrome/Firefox
   - Not supported in Safari

2. **Check permissions**
   - Allow microphone access
   - Use HTTPS (required)

3. **Check console**
   ```javascript
   console.log('Speech API:', 'webkitSpeechRecognition' in window);
   ```

### Slow Performance

1. **Rebuild index**
   ```typescript
   await searchService.buildIndex();
   ```

2. **Check data file size**
   ```bash
   # Large files (>1MB) can slow down indexing
   du -h public/data/*.json
   ```

3. **Limit results**
   ```typescript
   await searchService.search(query, filters, 20); // Limit to 20
   ```

### Styling Issues

1. **Import Search.scss**
   ```tsx
   import './components/Search/Search.scss';
   ```

2. **Check CSS specificity**
   ```scss
   // Your styles may need !important
   .search-container {
     color: red !important;
   }
   ```

3. **Verify SCSS compilation**
   ```bash
   npm run build
   # Check for SCSS errors
   ```

---

## Performance Tips

### 1. Pre-build Index

Build the index when the app loads, not when the user first searches:

```tsx
// App.tsx
useEffect(() => {
  searchService.buildIndex();
}, []);
```

### 2. Use Web Worker (Future)

For very large indexes, consider moving index building to a Web Worker:

```typescript
// Future enhancement
const worker = new Worker('./searchWorker.js');
worker.postMessage({ action: 'buildIndex' });
```

### 3. Lazy Load Search Page

Use React.lazy to load the search page on-demand:

```tsx
const SearchPage = React.lazy(() => import('./pages/Search'));

<Route path="/search" element={
  <Suspense fallback={<div>Loading...</div>}>
    <SearchPage />
  </Suspense>
} />
```

### 4. Debounce Suggestions

Suggestions are already debounced, but you can adjust:

```typescript
// In SearchSuggestions component
const debouncedFetch = useMemo(
  () => debounce(fetchSuggestions, 300), // 300ms delay
  []
);
```

---

## Analytics Integration

### Track Search Events

```tsx
import { searchService } from './services/searchService';

// After search
analytics.track('Search Performed', {
  query: query,
  resultsCount: results.length,
  hasFilters: Object.keys(filters).length > 0,
  timestamp: new Date(),
});

// Track popular searches
const history = searchService.getSearchHistory();
const popularQueries = history
  .reduce((acc, entry) => {
    acc[entry.query] = (acc[entry.query] || 0) + 1;
    return acc;
  }, {});
```

### Monitor Performance

```typescript
const startTime = performance.now();
const results = await searchService.search(query);
const duration = performance.now() - startTime;

analytics.track('Search Performance', {
  duration: duration,
  resultsCount: results.length,
  query: query,
});
```

---

## Testing

### Manual Testing Checklist

- [ ] Search returns results
- [ ] Filters work correctly
- [ ] Suggestions appear
- [ ] Voice search works (Chrome/Firefox)
- [ ] History persists
- [ ] Keyboard shortcuts work
- [ ] Mobile responsive
- [ ] Error states display
- [ ] Empty states display

### Unit Test Example

```typescript
import { searchService } from './services/searchService';

describe('SearchService', () => {
  beforeAll(async () => {
    await searchService.buildIndex();
  });

  it('should return results for valid query', async () => {
    const results = await searchService.search('electron');
    expect(results.length).toBeGreaterThan(0);
  });

  it('should filter by category', async () => {
    const results = await searchService.search('mass', {
      categories: ['Theory']
    });
    expect(results.every(r => r.category === 'Theory')).toBe(true);
  });
});
```

---

## Support

For issues or questions:

1. Check the README: `src/components/Search/README.md`
2. Review implementation doc: `SEARCH_SYSTEM_IMPLEMENTATION.md`
3. Check type definitions: `src/types/search.ts`
4. Review JIRA tickets: GU-026 through GU-030

---

## Next Steps

After integration:

1. Test thoroughly in all browsers
2. Monitor performance metrics
3. Gather user feedback
4. Plan feature enhancements
5. Update documentation as needed

---

**Happy Searching! 🔍**
