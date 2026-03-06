# Golden Universe Content Parsing System

A comprehensive content indexing and search system for the Golden Universe repository. This system parses all theory documents, derivation folders, Python scripts, and equations to make them searchable and accessible through the visualizer app.

## Overview

The parsing system consists of:

1. **TypeScript Types** - Complete type definitions for all content structures
2. **Parsing Scripts** - Node.js scripts that scan and index all content
3. **Content Service API** - TypeScript service layer for accessing parsed content
4. **Database Schema** - SQLite schema for full-text search (optional)
5. **JSON Output** - Static JSON files for direct browser access

## Quick Start

### Generate Content Index

```bash
npm run index
```

This will scan the entire Golden Universe repository and generate three JSON files in `public/data/`:

- `content-index.json` - Complete catalog of all content (1.8MB)
- `derivations-map.json` - Derivation folders with metadata (296KB)
- `equations-catalog.json` - All LaTeX equations extracted (766KB)

### Using the Content Service API

```typescript
import contentService from './services/contentService';

// Get all theory documents
const theories = await contentService.getTheoryDocuments();

// Get a specific derivation folder
const derivation = await contentService.getDerivationFolder('some-id');

// Search content
const results = await contentService.searchContent({
  query: 'electron mass',
  type: 'all',
  limit: 10
});

// Get equations for a document
const equations = await contentService.getEquationsForDocument('doc-id');

// Get precision results (ppm, percentages)
const precisionResults = await contentService.getBestPrecisionResults(10);
```

## Architecture

### Parsing Pipeline

```
Golden Universe Repository
    ↓
┌───────────────────────────────────────┐
│  Parser (scripts/quick-parse.js)     │
│  - Scans theory/ directory            │
│  - Scans derivations/ folders         │
│  - Extracts Python function signatures│
│  - Parses LaTeX equations              │
│  - Extracts precision results         │
└───────────────────────────────────────┘
    ↓
┌───────────────────────────────────────┐
│  JSON Output (public/data/)           │
│  - content-index.json                 │
│  - derivations-map.json               │
│  - equations-catalog.json             │
└───────────────────────────────────────┘
    ↓
┌───────────────────────────────────────┐
│  Content Service (src/services/)      │
│  - Loads and caches JSON              │
│  - Provides query API                 │
│  - Client-side search                 │
└───────────────────────────────────────┘
    ↓
React Components
```

### Type System

All content types are defined in `src/types/content.ts`:

- `TheoryDocument` - Markdown documents from theory/ folder
- `DerivationFolder` - Derivation directories with READMEs and scripts
- `PythonScript` - Python files with extracted functions
- `Equation` - LaTeX equations with context
- `PrecisionResult` - Accuracy measurements (ppm, %)
- `SearchResult` - Search query results
- `ContentCatalog` - Complete catalog structure

## Content Statistics

Current parsed content (as of February 2026):

| Content Type | Count |
|--------------|-------|
| Theory Documents | 13 |
| Explanatory Documents | 5 |
| Derivation Folders | 42 |
| Python Scripts | 218 |
| LaTeX Equations | 1,245 |
| Precision Results | 113 |

## Parsing Scripts

### Quick Parser (Recommended)

**File**: `scripts/quick-parse.js`
**Command**: `npm run parse-content`
**Duration**: ~0.15 seconds

Fast, optimized parser that handles the most common use cases:
- Parses all markdown files
- Extracts equations (both inline and display)
- Parses Python function signatures
- Extracts precision results (ppm, %, digits)
- Generates JSON output files

### Full Parser (Advanced)

**File**: `scripts/parse-content.ts`
**Command**: `npm run parse-content:full`
**Duration**: ~2-5 seconds

More comprehensive parser with additional features:
- Full Python AST parsing
- Cross-reference detection
- Table of contents generation
- Enhanced equation context extraction
- Requires `tsx` for TypeScript execution

### Test Parser

**File**: `scripts/test-parser.js`

Quick test to verify repository paths and file access:

```bash
node scripts/test-parser.js
```

## Content Service API Reference

### Theory Documents

```typescript
// Get all theory documents
getTheoryDocuments(): Promise<TheoryDocument[]>

// Get specific document by ID
getTheoryDocument(id: string): Promise<TheoryDocument | null>

// Get documents by tag/category
getTheoryDocumentsByTag(tag: string): Promise<TheoryDocument[]>

// Get recently updated documents
getRecentTheoryDocuments(limit?: number): Promise<TheoryDocument[]>
```

### Derivation Folders

```typescript
// Get all derivation folders
getDerivationFolders(): Promise<DerivationFolder[]>

// Get specific derivation by ID
getDerivationFolder(id: string): Promise<DerivationFolder | null>

// Get derivation by folder name
getDerivationByName(folderName: string): Promise<DerivationFolder | null>

// Get derivations by status
getDerivationsByStatus(status: 'active' | 'archived' | 'deprecated'): Promise<DerivationFolder[]>
```

### Python Scripts

```typescript
// Get all Python scripts
getPythonScripts(): Promise<PythonScript[]>

// Get specific script by path
getPythonScript(path: string): Promise<PythonScript | null>

// Get scripts in a folder
getPythonScriptsByFolder(folderPath: string): Promise<PythonScript[]>

// Search function names
searchPythonFunctions(name: string): Promise<Array<{script: PythonScript, functionIndex: number}>>
```

### Equations

```typescript
// Get all equations
getEquations(): Promise<Equation[]>

// Get equations for a document
getEquationsForDocument(documentId: string): Promise<Equation[]>

// Get equations by category
getEquationsByCategory(category: 'fundamental' | 'derived' | 'result' | 'identity'): Promise<Equation[]>

// Search equations
searchEquations(searchTerm: string): Promise<Equation[]>
```

### Precision Results

```typescript
// Get all precision results
getPrecisionResults(): Promise<PrecisionResult[]>

// Get by unit type
getPrecisionResultsByUnit(unit: 'ppm' | 'percentage' | 'digits'): Promise<PrecisionResult[]>

// Get best results (lowest error)
getBestPrecisionResults(limit?: number): Promise<PrecisionResult[]>
```

### Search

```typescript
// Full-text search
searchContent(query: SearchQuery): Promise<SearchResult[]>

// Get search suggestions
getSearchSuggestions(partial: string, limit?: number): Promise<string[]>

// Get content statistics
getContentStats(): Promise<ContentStats>
```

## Database Schema (Optional)

A SQLite database schema is provided in `scripts/db-schema.sql` for server-side full-text search:

```bash
sqlite3 public/data/content.db < scripts/db-schema.sql
```

Features:
- Full-text search indexes (FTS5)
- Cross-reference tables
- Precision results tracking
- Automatic triggers for index updates

Note: The current implementation uses JSON files and client-side search. The database is optional for advanced use cases.

## Customization

### Adding New Content Types

1. Add type definition to `src/types/content.ts`
2. Add parsing logic to `scripts/quick-parse.js`
3. Add service methods to `src/services/contentService.ts`
4. Update JSON output format

### Custom Search Filters

Extend the `SearchQuery` interface in `src/types/content.ts`:

```typescript
interface SearchQuery {
  query: string;
  type?: 'theory' | 'derivation' | 'python' | 'equation' | 'all';
  filters?: SearchFilters;
  limit?: number;
  offset?: number;
}

interface SearchFilters {
  category?: string;
  tags?: string[];
  status?: string;
  dateRange?: { start: string; end: string };
  hasEquations?: boolean;
  hasPython?: boolean;
}
```

### Performance Optimization

For large repositories:

1. **Pagination**: Use `limit` and `offset` in search queries
2. **Lazy Loading**: Load content on-demand instead of caching everything
3. **Web Workers**: Move search to a background thread
4. **IndexedDB**: Cache parsed content in browser storage

## Maintenance

### Updating the Index

Run the parser after content changes:

```bash
npm run index
```

### Automatic Updates

Add a git hook to automatically reindex on pull:

```bash
# .git/hooks/post-merge
#!/bin/sh
cd app/golden-universe-visualizer
npm run index
```

### Monitoring

Check parsing statistics:

```bash
npm run parse-content 2>&1 | grep "Statistics:"
```

## Troubleshooting

### Parser Hangs

If the full parser hangs, use the quick parser:
```bash
npm run parse-content  # Uses quick-parse.js
```

### Missing Content

Verify repository paths:
```bash
node scripts/test-parser.js
```

### JSON Too Large

The content index is ~1.8MB. To reduce size:
- Limit content length: `content.substring(0, 50000)`
- Remove inline equations: Keep only display equations
- Exclude archived derivations

### Type Errors

Ensure TypeScript types are up to date:
```bash
npm run type-check
```

## Development

### Project Structure

```
app/golden-universe-visualizer/
├── scripts/
│   ├── parse-content.ts      # Full parser (TypeScript)
│   ├── quick-parse.js         # Fast parser (JavaScript)
│   ├── test-parser.js         # Path verification
│   └── db-schema.sql          # SQLite schema
├── src/
│   ├── types/
│   │   └── content.ts         # Type definitions
│   └── services/
│       └── contentService.ts  # API service
└── public/
    └── data/
        ├── content-index.json     # Full catalog
        ├── derivations-map.json   # Derivations
        └── equations-catalog.json # Equations
```

### Contributing

When adding new features:

1. Update type definitions first
2. Implement parsing logic
3. Add service API methods
4. Update this README
5. Run tests and verify output

### Testing

Test the content service:

```typescript
import contentService from './services/contentService';

// Run in browser console
const stats = await contentService.getContentStats();
console.log(stats);

const results = await contentService.searchContent({
  query: 'golden ratio',
  limit: 5
});
console.log(results);
```

## Performance Benchmarks

| Operation | Time | Notes |
|-----------|------|-------|
| Initial Parse | 0.15s | Quick parser |
| Load JSON (cached) | <1ms | In-memory cache |
| Search Query | 5-20ms | Client-side, 1000+ items |
| Equation Extraction | 0.05s | 1245 equations |
| Python Parsing | 0.08s | 218 scripts |

## Future Enhancements

- [ ] Real-time incremental updates
- [ ] Server-side search with ranking
- [ ] Machine learning-based relevance scoring
- [ ] PDF and Jupyter notebook parsing
- [ ] Image and diagram extraction
- [ ] Citation graph visualization
- [ ] Semantic search using embeddings

## License

Part of the Golden Universe project. See main repository LICENSE.

## Contact

For questions about the parsing system, refer to the main Golden Universe documentation or open an issue.

---

**Last Updated**: February 2026
**Parser Version**: 1.0.0
**Total Content**: 18 theory docs, 42 derivations, 218 Python scripts, 1,245 equations
