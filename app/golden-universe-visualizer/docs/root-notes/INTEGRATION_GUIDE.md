# Content System Integration Guide

Quick guide for integrating the content parsing system into your React application.

## Step 1: Ensure JSON Files Exist

Generate the content index:

```bash
npm run index
```

This creates three files in `public/data/`:
- `content-index.json` (1.8 MB)
- `derivations-map.json` (296 KB)
- `equations-catalog.json` (766 KB)

## Step 2: Import the Content Service

In any React component:

```typescript
import contentService from '../services/contentService';
```

## Step 3: Use in Components

### Example 1: Simple Search

```typescript
import React, { useState } from 'react';
import contentService from '../services/contentService';

export const SimpleSearch: React.FC = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    const searchResults = await contentService.searchContent({
      query,
      type: 'all',
      limit: 10
    });
    setResults(searchResults);
  };

  return (
    <div>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search..."
      />
      <button onClick={handleSearch}>Search</button>

      <ul>
        {results.map(r => (
          <li key={r.id}>{r.title}</li>
        ))}
      </ul>
    </div>
  );
};
```

### Example 2: Theory Documents List

```typescript
import React, { useEffect, useState } from 'react';
import contentService from '../services/contentService';

export const TheoriesList: React.FC = () => {
  const [theories, setTheories] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    contentService.getTheoryDocuments()
      .then(setTheories)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h2>Theory Documents ({theories.length})</h2>
      {theories.map(theory => (
        <div key={theory.id}>
          <h3>{theory.title}</h3>
          <p>{theory.wordCount} words • {theory.equations.length} equations</p>
        </div>
      ))}
    </div>
  );
};
```

### Example 3: Derivation Browser

```typescript
import React, { useEffect, useState } from 'react';
import contentService from '../services/contentService';

export const DerivationBrowser: React.FC = () => {
  const [derivations, setDerivations] = useState([]);
  const [filter, setFilter] = useState<'all' | 'active' | 'archived'>('all');

  useEffect(() => {
    if (filter === 'all') {
      contentService.getDerivationFolders().then(setDerivations);
    } else {
      contentService.getDerivationsByStatus(filter).then(setDerivations);
    }
  }, [filter]);

  return (
    <div>
      <select value={filter} onChange={(e) => setFilter(e.target.value as any)}>
        <option value="all">All</option>
        <option value="active">Active</option>
        <option value="archived">Archived</option>
      </select>

      {derivations.map(d => (
        <div key={d.id}>
          <h3>{d.displayName}</h3>
          <p>
            Status: {d.status} •
            Python Scripts: {d.pythonScripts.length} •
            Files: {d.fileCount}
          </p>
        </div>
      ))}
    </div>
  );
};
```

### Example 4: Equation Display

```typescript
import React, { useEffect, useState } from 'react';
import contentService from '../services/contentService';

export const EquationGallery: React.FC = () => {
  const [equations, setEquations] = useState([]);

  useEffect(() => {
    // Get display equations only
    contentService.getEquations()
      .then(eqs => eqs.filter(eq => eq.displayMode))
      .then(setEquations);
  }, []);

  return (
    <div>
      <h2>Equations ({equations.length})</h2>
      {equations.slice(0, 20).map(eq => (
        <div key={eq.id}>
          <pre>$$  {eq.latex}  $$</pre>
          {eq.context && <p>{eq.context}</p>}
        </div>
      ))}
    </div>
  );
};
```

### Example 5: Statistics Dashboard

```typescript
import React, { useEffect, useState } from 'react';
import contentService from '../services/contentService';

export const StatsDashboard: React.FC = () => {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    contentService.getContentStats().then(setStats);
  }, []);

  if (!stats) return <div>Loading...</div>;

  return (
    <div>
      <h2>Golden Universe Statistics</h2>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '20px' }}>
        <StatCard title="Theory Documents" value={stats.totalTheories} />
        <StatCard title="Derivations" value={stats.totalDerivations} />
        <StatCard title="Python Scripts" value={stats.totalPythonScripts} />
        <StatCard title="Equations" value={stats.totalEquations} />
        <StatCard title="Precision Results" value={stats.totalPrecisionResults} />
        <StatCard title="Total Words" value={stats.totalWords.toLocaleString()} />
      </div>
    </div>
  );
};

const StatCard: React.FC<{ title: string; value: number | string }> = ({ title, value }) => (
  <div style={{ padding: '20px', background: '#f5f5f5', borderRadius: '8px' }}>
    <h3 style={{ margin: '0 0 10px 0', fontSize: '14px', color: '#666' }}>{title}</h3>
    <p style={{ margin: 0, fontSize: '32px', fontWeight: 'bold' }}>{value}</p>
  </div>
);
```

## Step 4: Add Routes (Optional)

If using React Router:

```typescript
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { SimpleSearch } from './components/SimpleSearch';
import { TheoriesList } from './components/TheoriesList';
import { DerivationBrowser } from './components/DerivationBrowser';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/search" element={<SimpleSearch />} />
        <Route path="/theories" element={<TheoriesList />} />
        <Route path="/derivations" element={<DerivationBrowser />} />
      </Routes>
    </BrowserRouter>
  );
}
```

## Step 5: Add to Navigation

```typescript
<nav>
  <Link to="/search">Search</Link>
  <Link to="/theories">Theories</Link>
  <Link to="/derivations">Derivations</Link>
  <Link to="/equations">Equations</Link>
</nav>
```

## Advanced Usage

### Custom Search Filters

```typescript
const results = await contentService.searchContent({
  query: 'electron mass',
  type: 'theory', // Only search theory documents
  filters: {
    hasEquations: true,
    tags: ['particle-physics']
  },
  limit: 20
});
```

### Get Related Documents

```typescript
const related = await contentService.getRelatedDocuments(documentId, 5);
```

### Search Python Functions

```typescript
const functions = await contentService.searchPythonFunctions('calculate');
functions.forEach(({ script, functionIndex }) => {
  const func = script.functions[functionIndex];
  console.log(`${script.filename}: ${func.name}()`);
});
```

### Get Best Precision Results

```typescript
const best = await contentService.getBestPrecisionResults(10);
best.forEach(result => {
  console.log(`${result.description}: ${result.value} ${result.unit}`);
});
```

## Performance Tips

### 1. Use Caching

The content service automatically caches loaded JSON files. To clear cache:

```typescript
import { clearCaches } from '../services/contentService';

// Clear and reload
clearCaches();
const theories = await contentService.getTheoryDocuments();
```

### 2. Pagination

For large result sets:

```typescript
const page1 = await contentService.searchContent({
  query: 'golden ratio',
  limit: 10,
  offset: 0
});

const page2 = await contentService.searchContent({
  query: 'golden ratio',
  limit: 10,
  offset: 10
});
```

### 3. Lazy Loading

Load content on demand:

```typescript
const [content, setContent] = useState(null);

const loadContent = async () => {
  const theories = await contentService.getTheoryDocuments();
  setContent(theories);
};

// Only load when user clicks
<button onClick={loadContent}>Load Theories</button>
```

## TypeScript IntelliSense

The content service is fully typed. Use IntelliSense to discover available methods:

```typescript
import contentService from '../services/contentService';

// Type: Press Ctrl+Space to see all methods
contentService.
// - getTheoryDocuments()
// - getDerivationFolders()
// - searchContent()
// - getEquations()
// ... and more
```

## Error Handling

```typescript
try {
  const results = await contentService.searchContent({ query: 'test' });
  setResults(results);
} catch (error) {
  console.error('Search failed:', error);
  setError('Failed to search content');
}
```

## Updating Content

After making changes to the Golden Universe repository:

```bash
cd app/golden-universe-visualizer
npm run index
```

This regenerates the JSON files with the latest content.

## Troubleshooting

### JSON Files Not Found

Make sure you've run the parser:
```bash
npm run index
```

### Search Returns No Results

Check that the JSON files are accessible:
```typescript
// In browser console
fetch('/data/content-index.json')
  .then(r => r.json())
  .then(console.log)
```

### Type Errors

Ensure types are imported:
```typescript
import type { SearchResult, TheoryDocument } from '../types/content';
```

## Complete Example Component

See `src/examples/ContentSearchExample.tsx` for a complete, production-ready implementation with:
- Search functionality
- Result display
- Statistics dashboard
- Error handling
- Loading states
- Styled components

## Questions?

Refer to:
- `CONTENT_PARSING.md` - Full API reference
- `CONTENT_SYSTEM_SUMMARY.md` - System overview
- `src/types/content.ts` - Type definitions
- `src/services/contentService.ts` - Service implementation

---

**Ready to integrate!** Start with the simple examples above and expand as needed.
