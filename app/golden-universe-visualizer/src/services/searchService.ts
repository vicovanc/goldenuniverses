/**
 * Search Service - GU-026: Search Index Builder
 *
 * Implements FlexSearch-based indexing and searching for:
 * - 258 markdown files (theories, derivations, docs)
 * - 371 Python files (calculations)
 * - Metadata extraction and relevance scoring
 * - Optimized for <100ms query performance
 */

import FlexSearch from 'flexsearch';

// Search result interface
export interface SearchResult {
  id: string;
  type: 'theory' | 'derivation' | 'python' | 'equation';
  title: string;
  path: string;
  filename: string;
  content: string;
  snippet: string;
  relevance: number;
  category: string;
  highlights: string[];
  metadata?: {
    description?: string;
    equations?: number;
    wordCount?: number;
    tags?: string[];
    createdAt?: string;
    modifiedAt?: string;
  };
}

// Search filters interface
export interface SearchFilters {
  categories?: string[];
  fileTypes?: string[];
  dateRange?: {
    start?: Date;
    end?: Date;
  };
  precisionRange?: {
    min?: number;
    max?: number;
  };
}

// Search suggestion interface
export interface SearchSuggestion {
  text: string;
  type: 'recent' | 'popular' | 'typo' | 'category';
  count?: number;
  category?: string;
}

// Search history entry
export interface SearchHistoryEntry {
  query: string;
  timestamp: Date;
  resultsCount: number;
  filters?: SearchFilters;
}

class SearchService {
  private index: FlexSearch.Document<SearchResult, false> | null = null;
  private indexedContent: Map<string, SearchResult> = new Map();
  private searchHistory: SearchHistoryEntry[] = [];
  private popularSearches: Map<string, number> = new Map();
  private isIndexing: boolean = false;
  private indexReady: boolean = false;

  constructor() {
    this.loadSearchHistory();
    this.loadPopularSearches();
  }

  /**
   * Initialize and build the search index
   * GU-026: Index builder with metadata extraction
   */
  async buildIndex(): Promise<void> {
    if (this.isIndexing) {
      console.warn('Search index is already being built');
      return;
    }

    this.isIndexing = true;
    console.time('Search index build');

    try {
      // Create FlexSearch document index with optimized settings
      this.index = new FlexSearch.Document({
        document: {
          id: 'id',
          index: ['title', 'content', 'filename', 'category'],
          store: ['title', 'path', 'filename', 'type', 'category', 'snippet', 'metadata'],
        },
        tokenize: 'forward',
        cache: true,
        optimize: true,
        resolution: 9,
        depth: 3,
        bidirectional: true,
        context: true,
      });

      // Load and index content from JSON files
      await Promise.all([
        this.indexTheories(),
        this.indexDerivations(),
        this.indexEquations(),
        this.indexPythonFiles(),
      ]);

      this.indexReady = true;
      console.timeEnd('Search index build');
      console.log(`Indexed ${this.indexedContent.size} documents`);
    } catch (error) {
      console.error('Failed to build search index:', error);
      throw error;
    } finally {
      this.isIndexing = false;
    }
  }

  /**
   * Index theory documents from content-index.json
   */
  private async indexTheories(): Promise<void> {
    try {
      const response = await fetch('/data/content-index.json');
      const data = await response.json();

      if (data.theories && Array.isArray(data.theories)) {
        for (const theory of data.theories) {
          const searchResult: SearchResult = {
            id: theory.id,
            type: 'theory',
            title: theory.title || theory.filename,
            path: theory.path,
            filename: theory.filename,
            content: theory.content || '',
            snippet: this.createSnippet(theory.content || '', 200),
            relevance: 0,
            category: 'Theory',
            highlights: [],
            metadata: {
              description: theory.metadata?.description,
              equations: theory.equations?.length || 0,
              wordCount: theory.wordCount,
              createdAt: theory.createdAt,
              modifiedAt: theory.modifiedAt,
            },
          };

          this.indexedContent.set(theory.id, searchResult);
          await this.index?.addAsync(theory.id, searchResult);
        }
      }
    } catch (error) {
      console.error('Failed to index theories:', error);
    }
  }

  /**
   * Index derivation documents
   */
  private async indexDerivations(): Promise<void> {
    try {
      const response = await fetch('/data/derivations-map.json');
      const data = await response.json();

      if (data.derivations && Array.isArray(data.derivations)) {
        for (const derivation of data.derivations) {
          const searchResult: SearchResult = {
            id: derivation.id,
            type: 'derivation',
            title: derivation.title || derivation.filename,
            path: derivation.path,
            filename: derivation.filename,
            content: derivation.content || '',
            snippet: this.createSnippet(derivation.content || '', 200),
            relevance: 0,
            category: 'Derivations',
            highlights: [],
            metadata: {
              description: derivation.metadata?.description,
              equations: derivation.equations?.length || 0,
              wordCount: derivation.wordCount,
              createdAt: derivation.createdAt,
              modifiedAt: derivation.modifiedAt,
            },
          };

          this.indexedContent.set(derivation.id, searchResult);
          await this.index?.addAsync(derivation.id, searchResult);
        }
      }
    } catch (error) {
      console.error('Failed to index derivations:', error);
    }
  }

  /**
   * Index equation catalog
   */
  private async indexEquations(): Promise<void> {
    try {
      const response = await fetch('/data/equations-catalog.json');
      const data = await response.json();

      if (data.equations && Array.isArray(data.equations)) {
        for (const equation of data.equations) {
          const searchResult: SearchResult = {
            id: equation.id,
            type: 'equation',
            title: equation.name || `Equation ${equation.id}`,
            path: equation.sourcePath || '',
            filename: equation.sourceFile || '',
            content: `${equation.latex || ''} ${equation.description || ''}`,
            snippet: equation.description || equation.latex || '',
            relevance: 0,
            category: 'Equations',
            highlights: [],
            metadata: {
              description: equation.description,
              tags: equation.tags,
            },
          };

          this.indexedContent.set(equation.id, searchResult);
          await this.index?.addAsync(equation.id, searchResult);
        }
      }
    } catch (error) {
      console.error('Failed to index equations:', error);
    }
  }

  /**
   * Index Python calculation files
   */
  private async indexPythonFiles(): Promise<void> {
    try {
      const response = await fetch('/data/content-index.json');
      const data = await response.json();

      if (data.pythonFiles && Array.isArray(data.pythonFiles)) {
        for (const pythonFile of data.pythonFiles) {
          const searchResult: SearchResult = {
            id: pythonFile.id,
            type: 'python',
            title: pythonFile.title || pythonFile.filename,
            path: pythonFile.path,
            filename: pythonFile.filename,
            content: pythonFile.content || '',
            snippet: this.createSnippet(pythonFile.content || '', 200),
            relevance: 0,
            category: 'Python',
            highlights: [],
            metadata: {
              description: pythonFile.metadata?.description,
              createdAt: pythonFile.createdAt,
              modifiedAt: pythonFile.modifiedAt,
            },
          };

          this.indexedContent.set(pythonFile.id, searchResult);
          await this.index?.addAsync(pythonFile.id, searchResult);
        }
      }
    } catch (error) {
      console.error('Failed to index Python files:', error);
    }
  }

  /**
   * Search with filters and relevance scoring
   * GU-027 & GU-028: Advanced search with filters
   */
  async search(
    query: string,
    filters?: SearchFilters,
    limit: number = 50
  ): Promise<SearchResult[]> {
    if (!this.indexReady || !this.index) {
      console.warn('Search index not ready');
      return [];
    }

    if (!query.trim()) {
      return [];
    }

    console.time('Search query');

    try {
      // Perform search across all indexed fields
      const searchResults = await this.index.searchAsync(query, {
        limit: limit * 2, // Get more results for filtering
        enrich: true,
      });

      // Aggregate results from all fields
      const resultMap = new Map<string, SearchResult>();
      let maxScore = 0;

      for (const fieldResults of searchResults) {
        if (fieldResults.result && Array.isArray(fieldResults.result)) {
          for (const item of fieldResults.result) {
            const doc = item.doc as unknown as SearchResult;
            const existing = resultMap.get(doc.id);

            if (existing) {
              existing.relevance += 1;
            } else {
              const fullDoc = this.indexedContent.get(doc.id);
              if (fullDoc) {
                const result: SearchResult = {
                  ...fullDoc,
                  relevance: 1,
                  highlights: this.extractHighlights(fullDoc.content, query),
                  snippet: this.createContextSnippet(fullDoc.content, query, 200),
                };
                resultMap.set(doc.id, result);
                maxScore = Math.max(maxScore, result.relevance);
              }
            }
          }
        }
      }

      // Convert to array and normalize relevance scores
      let results = Array.from(resultMap.values());

      if (maxScore > 0) {
        results = results.map(r => ({
          ...r,
          relevance: r.relevance / maxScore,
        }));
      }

      // Apply filters
      results = this.applyFilters(results, filters);

      // Sort by relevance
      results.sort((a, b) => b.relevance - a.relevance);

      // Limit results
      results = results.slice(0, limit);

      // Record search
      this.addToSearchHistory(query, results.length, filters);

      console.timeEnd('Search query');
      return results;
    } catch (error) {
      console.error('Search failed:', error);
      return [];
    }
  }

  /**
   * Apply filters to search results
   */
  private applyFilters(results: SearchResult[], filters?: SearchFilters): SearchResult[] {
    if (!filters) return results;

    let filtered = results;

    // Category filter
    if (filters.categories && filters.categories.length > 0) {
      filtered = filtered.filter(r => filters.categories!.includes(r.category));
    }

    // File type filter
    if (filters.fileTypes && filters.fileTypes.length > 0) {
      filtered = filtered.filter(r => filters.fileTypes!.includes(r.type));
    }

    // Date range filter
    if (filters.dateRange) {
      filtered = filtered.filter(r => {
        if (!r.metadata?.modifiedAt) return true;
        const date = new Date(r.metadata.modifiedAt);
        const start = filters.dateRange!.start;
        const end = filters.dateRange!.end;
        return (!start || date >= start) && (!end || date <= end);
      });
    }

    // Precision range filter (for equations/derivations)
    if (filters.precisionRange) {
      filtered = filtered.filter(r => {
        // Extract precision values from content if available
        const precisionMatch = r.content.match(/precision[:\s]+([0-9.]+)%?/i);
        if (!precisionMatch) return true;
        const precision = parseFloat(precisionMatch[1]);
        const min = filters.precisionRange!.min ?? 0;
        const max = filters.precisionRange!.max ?? 100;
        return precision >= min && precision <= max;
      });
    }

    return filtered;
  }

  /**
   * Get search suggestions based on input
   * GU-029: Auto-complete and suggestions
   */
  async getSuggestions(input: string): Promise<SearchSuggestion[]> {
    if (!input.trim()) {
      return this.getRecentSearches();
    }

    const suggestions: SearchSuggestion[] = [];
    const lowerInput = input.toLowerCase();

    // Recent searches matching input
    const recentMatches = this.searchHistory
      .filter(h => h.query.toLowerCase().includes(lowerInput))
      .slice(0, 3)
      .map(h => ({
        text: h.query,
        type: 'recent' as const,
      }));
    suggestions.push(...recentMatches);

    // Popular searches matching input
    const popularMatches = Array.from(this.popularSearches.entries())
      .filter(([query]) => query.toLowerCase().includes(lowerInput))
      .sort((a, b) => b[1] - a[1])
      .slice(0, 3)
      .map(([query, count]) => ({
        text: query,
        type: 'popular' as const,
        count,
      }));
    suggestions.push(...popularMatches);

    // Category suggestions
    const categories = ['Theory', 'Derivations', 'Python', 'Equations'];
    const categoryMatches = categories
      .filter(c => c.toLowerCase().includes(lowerInput))
      .map(c => ({
        text: c,
        type: 'category' as const,
        category: c,
      }));
    suggestions.push(...categoryMatches);

    // Typo correction (basic Levenshtein distance)
    if (suggestions.length === 0) {
      const corrected = this.tryTypoCorrection(input);
      if (corrected && corrected !== input) {
        suggestions.push({
          text: corrected,
          type: 'typo',
        });
      }
    }

    return suggestions;
  }

  /**
   * Get recent search suggestions
   */
  private getRecentSearches(): SearchSuggestion[] {
    return this.searchHistory
      .slice(0, 5)
      .map(h => ({
        text: h.query,
        type: 'recent' as const,
      }));
  }

  /**
   * Simple typo correction using Levenshtein distance
   */
  private tryTypoCorrection(input: string): string | null {
    const commonTerms = [
      'golden ratio', 'electron', 'proton', 'quark', 'mass', 'binding',
      'energy', 'equation', 'theory', 'derivation', 'physics', 'quantum',
      'nucleus', 'particle', 'phi', 'pi', 'constant', 'calculation',
    ];

    let bestMatch = input;
    let minDistance = 2;

    for (const term of commonTerms) {
      const distance = this.levenshteinDistance(input.toLowerCase(), term.toLowerCase());
      if (distance < minDistance && distance > 0) {
        minDistance = distance;
        bestMatch = term;
      }
    }

    return bestMatch !== input ? bestMatch : null;
  }

  /**
   * Calculate Levenshtein distance between two strings
   */
  private levenshteinDistance(str1: string, str2: string): number {
    const m = str1.length;
    const n = str2.length;
    const dp: number[][] = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));

    for (let i = 0; i <= m; i++) dp[i][0] = i;
    for (let j = 0; j <= n; j++) dp[0][j] = j;

    for (let i = 1; i <= m; i++) {
      for (let j = 1; j <= n; j++) {
        if (str1[i - 1] === str2[j - 1]) {
          dp[i][j] = dp[i - 1][j - 1];
        } else {
          dp[i][j] = Math.min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1;
        }
      }
    }

    return dp[m][n];
  }

  /**
   * Extract highlighted terms from content
   */
  private extractHighlights(content: string, query: string): string[] {
    const highlights: string[] = [];
    const terms = query.toLowerCase().split(/\s+/);
    const sentences = content.split(/[.!?]+/);

    for (const sentence of sentences) {
      const lowerSentence = sentence.toLowerCase();
      for (const term of terms) {
        if (lowerSentence.includes(term)) {
          highlights.push(sentence.trim());
          break;
        }
      }
      if (highlights.length >= 3) break;
    }

    return highlights;
  }

  /**
   * Create snippet with context around search terms
   */
  private createContextSnippet(content: string, query: string, maxLength: number): string {
    const terms = query.toLowerCase().split(/\s+/);
    const lowerContent = content.toLowerCase();

    // Find first occurrence of any term
    let firstIndex = -1;
    for (const term of terms) {
      const index = lowerContent.indexOf(term);
      if (index !== -1 && (firstIndex === -1 || index < firstIndex)) {
        firstIndex = index;
      }
    }

    if (firstIndex === -1) {
      return this.createSnippet(content, maxLength);
    }

    // Extract context around the term
    const start = Math.max(0, firstIndex - maxLength / 2);
    const end = Math.min(content.length, firstIndex + maxLength / 2);
    let snippet = content.substring(start, end);

    if (start > 0) snippet = '...' + snippet;
    if (end < content.length) snippet = snippet + '...';

    return snippet;
  }

  /**
   * Create simple snippet from content
   */
  private createSnippet(content: string, maxLength: number): string {
    if (content.length <= maxLength) {
      return content;
    }
    return content.substring(0, maxLength) + '...';
  }

  /**
   * Add search to history
   */
  private addToSearchHistory(query: string, resultsCount: number, filters?: SearchFilters): void {
    const entry: SearchHistoryEntry = {
      query,
      timestamp: new Date(),
      resultsCount,
      filters,
    };

    this.searchHistory.unshift(entry);
    this.searchHistory = this.searchHistory.slice(0, 50); // Keep last 50 searches

    // Update popular searches
    const count = this.popularSearches.get(query) || 0;
    this.popularSearches.set(query, count + 1);

    this.saveSearchHistory();
    this.savePopularSearches();
  }

  /**
   * Get search history
   */
  getSearchHistory(): SearchHistoryEntry[] {
    return this.searchHistory;
  }

  /**
   * Clear search history
   */
  clearSearchHistory(): void {
    this.searchHistory = [];
    this.saveSearchHistory();
  }

  /**
   * Save search history to localStorage
   */
  private saveSearchHistory(): void {
    try {
      localStorage.setItem('gu-search-history', JSON.stringify(this.searchHistory));
    } catch (error) {
      console.error('Failed to save search history:', error);
    }
  }

  /**
   * Load search history from localStorage
   */
  private loadSearchHistory(): void {
    try {
      const stored = localStorage.getItem('gu-search-history');
      if (stored) {
        this.searchHistory = JSON.parse(stored).map((entry: any) => ({
          ...entry,
          timestamp: new Date(entry.timestamp),
        }));
      }
    } catch (error) {
      console.error('Failed to load search history:', error);
    }
  }

  /**
   * Save popular searches to localStorage
   */
  private savePopularSearches(): void {
    try {
      const data = Array.from(this.popularSearches.entries());
      localStorage.setItem('gu-popular-searches', JSON.stringify(data));
    } catch (error) {
      console.error('Failed to save popular searches:', error);
    }
  }

  /**
   * Load popular searches from localStorage
   */
  private loadPopularSearches(): void {
    try {
      const stored = localStorage.getItem('gu-popular-searches');
      if (stored) {
        const data = JSON.parse(stored);
        this.popularSearches = new Map(data);
      }
    } catch (error) {
      console.error('Failed to load popular searches:', error);
    }
  }

  /**
   * Check if index is ready
   */
  isIndexReady(): boolean {
    return this.indexReady;
  }

  /**
   * Get index statistics
   */
  getIndexStats(): {
    total: number;
    theories: number;
    derivations: number;
    equations: number;
    python: number;
  } {
    const stats = {
      total: this.indexedContent.size,
      theories: 0,
      derivations: 0,
      equations: 0,
      python: 0,
    };

    for (const doc of this.indexedContent.values()) {
      switch (doc.type) {
        case 'theory':
          stats.theories++;
          break;
        case 'derivation':
          stats.derivations++;
          break;
        case 'equation':
          stats.equations++;
          break;
        case 'python':
          stats.python++;
          break;
      }
    }

    return stats;
  }
}

// Export singleton instance
export const searchService = new SearchService();
export default searchService;
