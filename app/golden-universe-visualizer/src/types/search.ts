/**
 * Search System Type Definitions
 *
 * Centralized type definitions for the Search & Discovery system
 * EPIC-006: GU-026 through GU-030
 */

// Content types that can be searched
export type ContentType = 'theory' | 'derivation' | 'python' | 'equation';

// Category display names
export type CategoryName = 'Theory' | 'Derivations' | 'Python' | 'Equations';

// Search result interface
export interface SearchResult {
  id: string;
  type: ContentType;
  title: string;
  path: string;
  filename: string;
  content: string;
  snippet: string;
  relevance: number;
  category: CategoryName;
  highlights: string[];
  metadata?: SearchResultMetadata;
}

// Search result metadata
export interface SearchResultMetadata {
  description?: string;
  equations?: number;
  wordCount?: number;
  tags?: string[];
  createdAt?: string;
  modifiedAt?: string;
  author?: string;
  precision?: number;
}

// Search filters
export interface SearchFilters {
  categories?: CategoryName[];
  fileTypes?: ContentType[];
  dateRange?: DateRange;
  precisionRange?: PrecisionRange;
}

// Date range filter
export interface DateRange {
  start?: Date;
  end?: Date;
}

// Precision range filter (for results)
export interface PrecisionRange {
  min?: number;
  max?: number;
}

// Search suggestion types
export type SuggestionType = 'recent' | 'popular' | 'typo' | 'category';

// Search suggestion interface
export interface SearchSuggestion {
  text: string;
  type: SuggestionType;
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

// Index statistics
export interface IndexStats {
  total: number;
  theories: number;
  derivations: number;
  equations: number;
  python: number;
}

// Content index structure (from JSON files)
export interface ContentIndex {
  theories?: TheoryDocument[];
  derivations?: DerivationDocument[];
  equations?: EquationDocument[];
  pythonFiles?: PythonDocument[];
}

// Theory document
export interface TheoryDocument {
  id: string;
  path: string;
  filename: string;
  title: string;
  content: string;
  wordCount?: number;
  equations?: EquationReference[];
  metadata?: DocumentMetadata;
  createdAt?: string;
  modifiedAt?: string;
}

// Derivation document
export interface DerivationDocument {
  id: string;
  path: string;
  filename: string;
  title: string;
  content: string;
  wordCount?: number;
  equations?: EquationReference[];
  metadata?: DocumentMetadata;
  createdAt?: string;
  modifiedAt?: string;
}

// Python document
export interface PythonDocument {
  id: string;
  path: string;
  filename: string;
  title: string;
  content: string;
  metadata?: DocumentMetadata;
  createdAt?: string;
  modifiedAt?: string;
}

// Equation document
export interface EquationDocument {
  id: string;
  name?: string;
  latex?: string;
  description?: string;
  sourcePath?: string;
  sourceFile?: string;
  tags?: string[];
}

// Equation reference in documents
export interface EquationReference {
  id: string;
  latex: string;
  displayMode?: boolean;
  lineNumber?: number;
}

// Document metadata
export interface DocumentMetadata {
  title?: string;
  description?: string;
  category?: string;
  tags?: string[];
  author?: string;
  precision?: number;
}

// Voice search state
export interface VoiceSearchState {
  isListening: boolean;
  isSupported: boolean;
  transcript: string;
  error: string | null;
}

// Voice search error types
export type VoiceSearchError =
  | 'no-speech'
  | 'audio-capture'
  | 'not-allowed'
  | 'network'
  | 'aborted'
  | 'service-not-allowed'
  | 'bad-grammar'
  | 'language-not-supported';

// Search service state
export interface SearchServiceState {
  indexReady: boolean;
  isIndexing: boolean;
  error: string | null;
  stats: IndexStats | null;
}

// Search query options
export interface SearchOptions {
  limit?: number;
  offset?: number;
  fuzzy?: boolean;
  sortBy?: 'relevance' | 'date' | 'title';
  sortOrder?: 'asc' | 'desc';
}

// Relevance scoring thresholds
export enum RelevanceScore {
  HIGH = 0.8,
  MEDIUM = 0.5,
  LOW = 0.0,
}

// Search result group
export interface SearchResultGroup {
  category: CategoryName;
  results: SearchResult[];
  count: number;
}

// Keyboard shortcut
export interface KeyboardShortcut {
  keys: string[];
  description: string;
  action: () => void;
}

// Search analytics
export interface SearchAnalytics {
  totalSearches: number;
  averageResultsPerSearch: number;
  mostSearchedTerms: Array<{ term: string; count: number }>;
  averageQueryTime: number;
  popularCategories: Array<{ category: CategoryName; count: number }>;
}
