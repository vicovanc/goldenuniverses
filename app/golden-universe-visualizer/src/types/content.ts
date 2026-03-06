/**
 * Content Types for Golden Universe Parsing System
 * Defines all data structures for theory documents, derivations, Python scripts, and equations
 */

// ============================================================================
// CORE CONTENT TYPES
// ============================================================================

/**
 * Metadata extracted from markdown frontmatter or document headers
 */
export interface DocumentMetadata {
  title: string;
  description?: string;
  keywords?: string[];
  author?: string;
  date?: string;
  updated?: string;
  version?: string;
  status?: 'draft' | 'complete' | 'archived' | 'deprecated';
  tags?: string[];
  category?: string;
  relatedDocuments?: string[];
}

/**
 * Theory document from theory/ folder
 */
export interface TheoryDocument {
  id: string;
  path: string;
  filename: string;
  metadata: DocumentMetadata;
  content: string;
  htmlContent: string;
  laws?: TheoryLaw[];
  equations?: Equation[];
  crossReferences?: CrossReference[];
  tableOfContents?: TableOfContentsItem[];
  wordCount: number;
  createdAt: string;
  modifiedAt: string;
}

/**
 * Individual law from theory documents (e.g., LAW 0, LAW 1, etc.)
 */
export interface TheoryLaw {
  lawNumber: number;
  title: string;
  statement: string;
  content: string;
  equations?: Equation[];
  status?: string;
  section?: string;
}

/**
 * Derivation folder from derivations/ directory
 */
export interface DerivationFolder {
  id: string;
  folderName: string;
  path: string;
  displayName: string;
  readme?: TheoryDocument;
  pythonScripts: PythonScript[];
  markdownFiles: TheoryDocument[];
  status?: 'active' | 'archived' | 'deprecated';
  category?: string;
  precisionResults?: PrecisionResult[];
  keyResults?: string[];
  equations?: Equation[];
  fileCount: number;
  createdAt: string;
  modifiedAt: string;
}

/**
 * Python script with parsed metadata and function signatures
 */
export interface PythonScript {
  id: string;
  path: string;
  filename: string;
  folderPath: string;
  metadata: PythonMetadata;
  functions: PythonFunction[];
  classes: PythonClass[];
  imports: string[];
  docstring?: string;
  contentHash: string;
  lineCount: number;
  createdAt: string;
  modifiedAt: string;
}

/**
 * Metadata extracted from Python scripts
 */
export interface PythonMetadata {
  title?: string;
  description?: string;
  author?: string;
  date?: string;
  version?: string;
  purpose?: string;
  dependencies?: string[];
}

/**
 * Python function signature and metadata
 */
export interface PythonFunction {
  name: string;
  signature: string;
  docstring?: string;
  parameters: PythonParameter[];
  returnType?: string;
  decorators?: string[];
  lineNumber: number;
  isAsync: boolean;
}

/**
 * Python function parameter
 */
export interface PythonParameter {
  name: string;
  type?: string;
  defaultValue?: string;
  isOptional: boolean;
}

/**
 * Python class definition
 */
export interface PythonClass {
  name: string;
  docstring?: string;
  methods: PythonFunction[];
  baseClasses?: string[];
  lineNumber: number;
}

/**
 * LaTeX equation extracted from markdown
 */
export interface Equation {
  id: string;
  documentId: string;
  latex: string;
  displayMode: boolean; // true for block equations, false for inline
  context?: string; // surrounding text
  label?: string;
  variables?: string[];
  category?: 'fundamental' | 'derived' | 'result' | 'identity';
  lineNumber?: number;
}

/**
 * Precision result (ppm, percentage accuracy, etc.)
 */
export interface PrecisionResult {
  description: string;
  value: number;
  unit: 'ppm' | 'percentage' | 'digits';
  context: string;
  documentId?: string;
  equation?: string;
}

/**
 * Cross-reference between documents
 */
export interface CrossReference {
  sourceId: string;
  targetId: string;
  type: 'reference' | 'dependency' | 'related' | 'supersedes' | 'superseded_by';
  context?: string;
}

/**
 * Table of contents item
 */
export interface TableOfContentsItem {
  level: number; // 1-6 for h1-h6
  title: string;
  slug: string;
  lineNumber?: number;
  children?: TableOfContentsItem[];
}

// ============================================================================
// SEARCH AND INDEX TYPES
// ============================================================================

/**
 * Search result from content index
 */
export interface SearchResult {
  id: string;
  type: 'theory' | 'derivation' | 'python' | 'equation' | 'law';
  title: string;
  description?: string;
  path: string;
  relevanceScore: number;
  highlights?: SearchHighlight[];
  metadata?: Record<string, unknown>;
  url?: string;
}

/**
 * Highlighted text in search results
 */
export interface SearchHighlight {
  field: string;
  text: string;
  startIndex: number;
  endIndex: number;
}

/**
 * Search query parameters
 */
export interface SearchQuery {
  query: string;
  type?: 'theory' | 'derivation' | 'python' | 'equation' | 'all';
  filters?: SearchFilters;
  limit?: number;
  offset?: number;
}

/**
 * Search filters
 */
export interface SearchFilters {
  category?: string;
  tags?: string[];
  status?: string;
  dateRange?: {
    start: string;
    end: string;
  };
  hasEquations?: boolean;
  hasPython?: boolean;
}

/**
 * Full-text search index document
 */
export interface SearchIndexDocument {
  id: string;
  type: string;
  title: string;
  content: string;
  path: string;
  metadata: Record<string, unknown>;
  timestamp: string;
}

// ============================================================================
// CATALOG TYPES
// ============================================================================

/**
 * Complete content catalog
 */
export interface ContentCatalog {
  theories: TheoryDocument[];
  derivations: DerivationFolder[];
  pythonScripts: PythonScript[];
  equations: Equation[];
  metadata: CatalogMetadata;
}

/**
 * Metadata about the catalog
 */
export interface CatalogMetadata {
  generatedAt: string;
  version: string;
  totalTheories: number;
  totalDerivations: number;
  totalPythonScripts: number;
  totalEquations: number;
  totalMarkdownFiles: number;
  repositoryPath: string;
}

/**
 * Derivations map (folder structure)
 */
export interface DerivationsMap {
  derivations: DerivationFolder[];
  categories: CategoryMap;
  metadata: {
    totalFolders: number;
    totalFiles: number;
    generatedAt: string;
  };
}

/**
 * Category mapping for derivations
 */
export interface CategoryMap {
  [category: string]: {
    name: string;
    description?: string;
    derivations: string[]; // derivation IDs
  };
}

/**
 * Equations catalog
 */
export interface EquationsCatalog {
  equations: Equation[];
  byDocument: { [documentId: string]: Equation[] };
  byCategory: { [category: string]: Equation[] };
  metadata: {
    totalEquations: number;
    generatedAt: string;
  };
}

// ============================================================================
// PARSING TYPES
// ============================================================================

/**
 * Parsing options for content parser
 */
export interface ParsingOptions {
  rootPath: string;
  outputPath?: string;
  includePython?: boolean;
  includeTheory?: boolean;
  includeDerivations?: boolean;
  includeExplanatory?: boolean;
  maxFileSize?: number; // in bytes
  ignorePatterns?: string[];
  extractEquations?: boolean;
  extractPrecision?: boolean;
  generateIndex?: boolean;
}

/**
 * Parsing result
 */
export interface ParsingResult {
  success: boolean;
  catalog?: ContentCatalog;
  errors?: ParsingError[];
  warnings?: string[];
  stats: ParsingStats;
}

/**
 * Parsing error
 */
export interface ParsingError {
  file: string;
  message: string;
  line?: number;
  type: 'error' | 'warning';
}

/**
 * Parsing statistics
 */
export interface ParsingStats {
  filesProcessed: number;
  filesSkipped: number;
  markdownFiles: number;
  pythonFiles: number;
  equationsExtracted: number;
  functionsExtracted: number;
  duration: number; // milliseconds
}

// ============================================================================
// DATABASE TYPES
// ============================================================================

/**
 * Database row for theory_documents table
 */
export interface TheoryDocumentRow {
  id: string;
  path: string;
  filename: string;
  title: string;
  content: string;
  html_content: string;
  metadata_json: string;
  word_count: number;
  created_at: string;
  modified_at: string;
  indexed_at: string;
}

/**
 * Database row for derivation_folders table
 */
export interface DerivationFolderRow {
  id: string;
  folder_name: string;
  path: string;
  display_name: string;
  status: string;
  category: string;
  file_count: number;
  created_at: string;
  modified_at: string;
  metadata_json: string;
}

/**
 * Database row for python_scripts table
 */
export interface PythonScriptRow {
  id: string;
  path: string;
  filename: string;
  folder_path: string;
  docstring: string;
  metadata_json: string;
  functions_json: string;
  classes_json: string;
  imports_json: string;
  content_hash: string;
  line_count: number;
  created_at: string;
  modified_at: string;
  indexed_at: string;
}

/**
 * Database row for equations table
 */
export interface EquationRow {
  id: string;
  document_id: string;
  latex: string;
  display_mode: number; // 0 or 1
  context: string;
  label: string;
  variables_json: string;
  category: string;
  line_number: number;
  created_at: string;
}

/**
 * Database row for search_index table
 */
export interface SearchIndexRow {
  id: string;
  type: string;
  title: string;
  content: string;
  path: string;
  metadata_json: string;
  created_at: string;
}

// ============================================================================
// UTILITY TYPES
// ============================================================================

/**
 * File info from filesystem
 */
export interface FileInfo {
  path: string;
  filename: string;
  extension: string;
  size: number;
  createdAt: Date;
  modifiedAt: Date;
}

/**
 * Markdown parsing result
 */
export interface MarkdownParseResult {
  frontmatter: Record<string, unknown>;
  content: string;
  html: string;
  equations: Equation[];
  toc: TableOfContentsItem[];
}

/**
 * Python parsing result
 */
export interface PythonParseResult {
  functions: PythonFunction[];
  classes: PythonClass[];
  imports: string[];
  docstring?: string;
}

export default {
  // Export all types as namespace
};
