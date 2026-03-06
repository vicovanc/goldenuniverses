/**
 * Content Service API
 *
 * Provides methods to access parsed Golden Universe content:
 * - Theory documents
 * - Derivation folders
 * - Python scripts
 * - Equations
 * - Full-text search
 */

import type {
  TheoryDocument,
  DerivationFolder,
  PythonScript,
  Equation,
  SearchResult,
  SearchQuery,
  ContentCatalog,
  DerivationsMap,
  EquationsCatalog,
  PrecisionResult
} from '../types/content';

// ============================================================================
// DATA LOADING
// ============================================================================

let contentCache: ContentCatalog | null = null;
let derivationsCache: DerivationsMap | null = null;
let equationsCache: EquationsCatalog | null = null;

/**
 * Load content index from JSON file
 */
async function loadContentIndex(): Promise<ContentCatalog> {
  if (contentCache) {
    return contentCache;
  }

  try {
    const response = await fetch('/data/content-index.json');
    if (!response.ok) {
      throw new Error(`Failed to load content index: ${response.statusText}`);
    }
    contentCache = await response.json();
    return contentCache!;
  } catch (error) {
    console.error('Error loading content index:', error);
    throw error;
  }
}

/**
 * Load derivations map from JSON file
 */
async function loadDerivationsMap(): Promise<DerivationsMap> {
  if (derivationsCache) {
    return derivationsCache;
  }

  try {
    const response = await fetch('/data/derivations-map.json');
    if (!response.ok) {
      throw new Error(`Failed to load derivations map: ${response.statusText}`);
    }
    derivationsCache = await response.json();
    return derivationsCache!;
  } catch (error) {
    console.error('Error loading derivations map:', error);
    throw error;
  }
}

/**
 * Load equations catalog from JSON file
 */
async function loadEquationsCatalog(): Promise<EquationsCatalog> {
  if (equationsCache) {
    return equationsCache;
  }

  try {
    const response = await fetch('/data/equations-catalog.json');
    if (!response.ok) {
      throw new Error(`Failed to load equations catalog: ${response.statusText}`);
    }
    equationsCache = await response.json();
    return equationsCache!;
  } catch (error) {
    console.error('Error loading equations catalog:', error);
    throw error;
  }
}

/**
 * Clear all caches (useful for hot reload in development)
 */
export function clearCaches(): void {
  contentCache = null;
  derivationsCache = null;
  equationsCache = null;
}

// ============================================================================
// THEORY DOCUMENTS API
// ============================================================================

/**
 * Get all theory documents
 */
export async function getTheoryDocuments(): Promise<TheoryDocument[]> {
  const catalog = await loadContentIndex();
  return catalog.theories;
}

/**
 * Get a specific theory document by ID
 */
export async function getTheoryDocument(id: string): Promise<TheoryDocument | null> {
  const catalog = await loadContentIndex();
  return catalog.theories.find(t => t.id === id) || null;
}

/**
 * Get theory documents by category or tag
 */
export async function getTheoryDocumentsByTag(tag: string): Promise<TheoryDocument[]> {
  const catalog = await loadContentIndex();
  return catalog.theories.filter(t =>
    t.metadata?.tags?.includes(tag) || t.metadata?.category === tag
  );
}

/**
 * Get recently updated theory documents
 */
export async function getRecentTheoryDocuments(limit: number = 10): Promise<TheoryDocument[]> {
  const catalog = await loadContentIndex();
  return [...catalog.theories]
    .sort((a, b) => new Date(b.modifiedAt).getTime() - new Date(a.modifiedAt).getTime())
    .slice(0, limit);
}

// ============================================================================
// DERIVATIONS API
// ============================================================================

/**
 * Get all derivation folders
 */
export async function getDerivationFolders(): Promise<DerivationFolder[]> {
  const map = await loadDerivationsMap();
  return map.derivations;
}

/**
 * Get a specific derivation folder by ID
 */
export async function getDerivationFolder(id: string): Promise<DerivationFolder | null> {
  const map = await loadDerivationsMap();
  return map.derivations.find(d => d.id === id) || null;
}

/**
 * Get derivation folder by folder name (e.g., "01_FORCE_UNIFICATION")
 */
export async function getDerivationByName(folderName: string): Promise<DerivationFolder | null> {
  const map = await loadDerivationsMap();
  return map.derivations.find(d => d.folderName === folderName) || null;
}

/**
 * Get derivations by status
 */
export async function getDerivationsByStatus(
  status: 'active' | 'archived' | 'deprecated'
): Promise<DerivationFolder[]> {
  const map = await loadDerivationsMap();
  return map.derivations.filter(d => d.status === status);
}

/**
 * Get derivations by category
 */
export async function getDerivationsByCategory(category: string): Promise<DerivationFolder[]> {
  const map = await loadDerivationsMap();
  return map.derivations.filter(d => d.category === category);
}

// ============================================================================
// PYTHON SCRIPTS API
// ============================================================================

/**
 * Get all Python scripts
 */
export async function getPythonScripts(): Promise<PythonScript[]> {
  const catalog = await loadContentIndex();
  return catalog.pythonScripts;
}

/**
 * Get a specific Python script by path
 */
export async function getPythonScript(scriptPath: string): Promise<PythonScript | null> {
  const catalog = await loadContentIndex();
  return catalog.pythonScripts.find(p => p.path === scriptPath) || null;
}

/**
 * Get Python scripts by folder
 */
export async function getPythonScriptsByFolder(folderPath: string): Promise<PythonScript[]> {
  const catalog = await loadContentIndex();
  return catalog.pythonScripts.filter(p => p.folderPath === folderPath);
}

/**
 * Get Python scripts for a derivation
 */
export async function getPythonScriptsForDerivation(
  derivationId: string
): Promise<PythonScript[]> {
  const derivation = await getDerivationFolder(derivationId);
  return derivation?.pythonScripts || [];
}

/**
 * Search Python functions by name
 */
export async function searchPythonFunctions(functionName: string): Promise<Array<{
  script: PythonScript;
  functionIndex: number;
}>> {
  const catalog = await loadContentIndex();
  const results: Array<{ script: PythonScript; functionIndex: number }> = [];

  for (const script of catalog.pythonScripts) {
    script.functions?.forEach((func, index) => {
      if (func.name.toLowerCase().includes(functionName.toLowerCase())) {
        results.push({ script, functionIndex: index });
      }
    });
  }

  return results;
}

// ============================================================================
// EQUATIONS API
// ============================================================================

/**
 * Get all equations
 */
export async function getEquations(): Promise<Equation[]> {
  const catalog = await loadEquationsCatalog();
  return catalog.equations;
}

/**
 * Get equations for a specific document
 */
export async function getEquationsForDocument(documentId: string): Promise<Equation[]> {
  const catalog = await loadEquationsCatalog();
  return catalog.byDocument[documentId] || [];
}

/**
 * Get equations by category
 */
export async function getEquationsByCategory(
  category: 'fundamental' | 'derived' | 'result' | 'identity'
): Promise<Equation[]> {
  const catalog = await loadEquationsCatalog();
  return catalog.byCategory[category] || [];
}

/**
 * Search equations by LaTeX content
 */
export async function searchEquations(searchTerm: string): Promise<Equation[]> {
  const catalog = await loadEquationsCatalog();
  const term = searchTerm.toLowerCase();

  return catalog.equations.filter(eq =>
    eq.latex.toLowerCase().includes(term) ||
    eq.label?.toLowerCase().includes(term) ||
    eq.context?.toLowerCase().includes(term)
  );
}

// ============================================================================
// PRECISION RESULTS API
// ============================================================================

/**
 * Get all precision results
 */
export async function getPrecisionResults(): Promise<PrecisionResult[]> {
  const catalog = await loadContentIndex();
  return catalog.precisionResults || [];
}

/**
 * Get precision results by unit
 */
export async function getPrecisionResultsByUnit(
  unit: 'ppm' | 'percentage' | 'digits'
): Promise<PrecisionResult[]> {
  const results = await getPrecisionResults();
  return results.filter(r => r.unit === unit);
}

/**
 * Get best precision results (lowest ppm, highest accuracy)
 */
export async function getBestPrecisionResults(limit: number = 10): Promise<PrecisionResult[]> {
  const results = await getPrecisionResults();

  // Sort by value (ascending for ppm, descending for digits)
  return [...results]
    .sort((a, b) => {
      if (a.unit === 'ppm') return a.value - b.value;
      if (a.unit === 'digits') return b.value - a.value;
      return a.value - b.value;
    })
    .slice(0, limit);
}

// ============================================================================
// SEARCH API
// ============================================================================

/**
 * Simple client-side full-text search
 */
export async function searchContent(query: SearchQuery): Promise<SearchResult[]> {
  const catalog = await loadContentIndex();
  const searchTerm = query.query.toLowerCase();
  const results: SearchResult[] = [];

  // Search theories
  if (!query.type || query.type === 'theory' || query.type === 'all') {
    for (const theory of catalog.theories) {
      const titleMatch = theory.title.toLowerCase().includes(searchTerm);
      const contentMatch = theory.content.toLowerCase().includes(searchTerm);

      if (titleMatch || contentMatch) {
        // Calculate relevance score (simple heuristic)
        let score = 0;
        if (titleMatch) score += 10;
        if (contentMatch) {
          const occurrences = (theory.content.toLowerCase().match(new RegExp(searchTerm, 'g')) || []).length;
          score += Math.min(occurrences, 10);
        }

        results.push({
          id: theory.id,
          type: 'theory',
          title: theory.title,
          description: theory.content.substring(0, 200) + '...',
          path: theory.path,
          relevanceScore: score,
          url: `/theory/${theory.id}`
        });
      }
    }
  }

  // Search derivations
  if (!query.type || query.type === 'derivation' || query.type === 'all') {
    for (const derivation of catalog.derivations) {
      const titleMatch = derivation.displayName.toLowerCase().includes(searchTerm);
      const readmeMatch = derivation.readme?.content.toLowerCase().includes(searchTerm);

      if (titleMatch || readmeMatch) {
        let score = 0;
        if (titleMatch) score += 10;
        if (readmeMatch) score += 5;

        results.push({
          id: derivation.id,
          type: 'derivation',
          title: derivation.displayName,
          description: derivation.readme?.content.substring(0, 200) + '...' || '',
          path: derivation.path,
          relevanceScore: score,
          url: `/derivations/${derivation.id}`
        });
      }
    }
  }

  // Search Python scripts
  if (!query.type || query.type === 'python' || query.type === 'all') {
    for (const script of catalog.pythonScripts) {
      const filenameMatch = script.filename.toLowerCase().includes(searchTerm);
      const docstringMatch = script.docstring?.toLowerCase().includes(searchTerm);
      const functionMatch = script.functions?.some(f =>
        f.name.toLowerCase().includes(searchTerm) ||
        f.docstring?.toLowerCase().includes(searchTerm)
      );

      if (filenameMatch || docstringMatch || functionMatch) {
        let score = 0;
        if (filenameMatch) score += 8;
        if (docstringMatch) score += 5;
        if (functionMatch) score += 3;

        results.push({
          id: script.id,
          type: 'python',
          title: script.filename,
          description: script.docstring || `Python script with ${script.functions?.length || 0} functions`,
          path: script.path,
          relevanceScore: score,
          url: `/python/${script.id}`
        });
      }
    }
  }

  // Search equations
  if (!query.type || query.type === 'equation' || query.type === 'all') {
    for (const equation of catalog.equations) {
      const latexMatch = equation.latex.toLowerCase().includes(searchTerm);
      const contextMatch = equation.context?.toLowerCase().includes(searchTerm);

      if (latexMatch || contextMatch) {
        let score = 0;
        if (latexMatch) score += 7;
        if (contextMatch) score += 3;

        results.push({
          id: equation.id,
          type: 'equation',
          title: equation.label || equation.latex.substring(0, 50) + '...',
          description: equation.context || equation.latex,
          path: equation.documentId || '',
          relevanceScore: score,
          url: `/equations/${equation.id}`
        });
      }
    }
  }

  // Sort by relevance score
  results.sort((a, b) => b.relevanceScore - a.relevanceScore);

  // Apply limit
  const limit = query.limit || 50;
  return results.slice(0, limit);
}

/**
 * Get search suggestions based on partial query
 */
export async function getSearchSuggestions(partial: string, limit: number = 5): Promise<string[]> {
  const catalog = await loadContentIndex();
  const suggestions = new Set<string>();

  const term = partial.toLowerCase();

  // Collect titles
  catalog.theories.forEach(t => {
    if (t.title.toLowerCase().includes(term)) {
      suggestions.add(t.title);
    }
  });

  catalog.derivations.forEach(d => {
    if (d.displayName.toLowerCase().includes(term)) {
      suggestions.add(d.displayName);
    }
  });

  // Collect function names
  catalog.pythonScripts.forEach(s => {
    s.functions?.forEach(f => {
      if (f.name.toLowerCase().includes(term)) {
        suggestions.add(f.name);
      }
    });
  });

  return Array.from(suggestions).slice(0, limit);
}

// ============================================================================
// STATISTICS API
// ============================================================================

/**
 * Get content statistics
 */
export async function getContentStats() {
  const catalog = await loadContentIndex();

  return {
    totalTheories: catalog.theories.length,
    totalDerivations: catalog.derivations.length,
    totalPythonScripts: catalog.pythonScripts.length,
    totalEquations: catalog.equations.length,
    totalPrecisionResults: catalog.precisionResults?.length || 0,
    totalWords: catalog.theories.reduce((sum, t) => sum + t.wordCount, 0),
    totalFunctions: catalog.pythonScripts.reduce((sum, s) => sum + (s.functions?.length || 0), 0),
    activeDerivations: catalog.derivations.filter(d => d.status === 'active').length,
    archivedDerivations: catalog.derivations.filter(d => d.status === 'archived').length
  };
}

/**
 * Get metadata about the content catalog
 */
export async function getCatalogMetadata() {
  const catalog = await loadContentIndex();
  return catalog.metadata;
}

// ============================================================================
// CROSS-REFERENCES API
// ============================================================================

/**
 * Find related documents based on keywords and content similarity
 */
export async function getRelatedDocuments(
  documentId: string,
  limit: number = 5
): Promise<TheoryDocument[]> {
  const catalog = await loadContentIndex();
  const document = catalog.theories.find(t => t.id === documentId);

  if (!document) {
    return [];
  }

  // Simple keyword-based similarity
  const documentWords = new Set(
    document.content
      .toLowerCase()
      .split(/\W+/)
      .filter(w => w.length > 4)
  );

  const scored = catalog.theories
    .filter(t => t.id !== documentId)
    .map(t => {
      const words = new Set(
        t.content
          .toLowerCase()
          .split(/\W+/)
          .filter(w => w.length > 4)
      );

      // Count common words
      let commonWords = 0;
      documentWords.forEach(w => {
        if (words.has(w)) commonWords++;
      });

      return {
        document: t,
        similarity: commonWords / Math.max(documentWords.size, words.size)
      };
    })
    .sort((a, b) => b.similarity - a.similarity)
    .slice(0, limit);

  return scored.map(s => s.document);
}

/**
 * Get document tree/hierarchy for navigation
 */
export async function getDocumentTree() {
  const catalog = await loadContentIndex();

  // Group by category/folder structure
  const tree: Record<string, TheoryDocument[]> = {};

  catalog.theories.forEach(doc => {
    const category = doc.metadata?.category || 'Uncategorized';
    if (!tree[category]) {
      tree[category] = [];
    }
    tree[category].push(doc);
  });

  return tree;
}

// ============================================================================
// EXPORT ALL
// ============================================================================

export default {
  // Theory
  getTheoryDocuments,
  getTheoryDocument,
  getTheoryDocumentsByTag,
  getRecentTheoryDocuments,

  // Derivations
  getDerivationFolders,
  getDerivationFolder,
  getDerivationByName,
  getDerivationsByStatus,
  getDerivationsByCategory,

  // Python
  getPythonScripts,
  getPythonScript,
  getPythonScriptsByFolder,
  getPythonScriptsForDerivation,
  searchPythonFunctions,

  // Equations
  getEquations,
  getEquationsForDocument,
  getEquationsByCategory,
  searchEquations,

  // Precision
  getPrecisionResults,
  getPrecisionResultsByUnit,
  getBestPrecisionResults,

  // Search
  searchContent,
  getSearchSuggestions,

  // Stats
  getContentStats,
  getCatalogMetadata,

  // Relations
  getRelatedDocuments,
  getDocumentTree,

  // Utils
  clearCaches
};
