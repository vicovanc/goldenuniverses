#!/usr/bin/env node

/**
 * Golden Universe Content Parser
 *
 * Scans and indexes all content from the Golden Universe repository:
 * - Theory documents (markdown files)
 * - Derivation folders with READMEs
 * - Python scripts with function extraction
 * - LaTeX equations
 * - Precision results
 *
 * Outputs:
 * - SQLite database with full-text search
 * - JSON files for static access
 * - Search index for client-side searching
 */

import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { fileURLToPath } from 'url';

// ES Module compatibility
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Types
interface ParsedMarkdown {
  frontmatter: Record<string, any>;
  content: string;
  html: string;
}

interface PythonFunction {
  name: string;
  signature: string;
  docstring?: string;
  parameters: Array<{
    name: string;
    type?: string;
    defaultValue?: string;
  }>;
  lineNumber: number;
}

interface Equation {
  id: string;
  latex: string;
  displayMode: boolean;
  context?: string;
  lineNumber?: number;
}

interface TheoryDocument {
  id: string;
  path: string;
  filename: string;
  title: string;
  content: string;
  equations: Equation[];
  wordCount: number;
  createdAt: string;
  modifiedAt: string;
}

interface DerivationFolder {
  id: string;
  folderName: string;
  path: string;
  displayName: string;
  readme?: TheoryDocument;
  pythonScripts: any[];
  markdownFiles: any[];
  status: string;
  fileCount: number;
  createdAt: string;
  modifiedAt: string;
}

interface PrecisionResult {
  description: string;
  value: number;
  unit: string;
  context: string;
}

// Configuration
const CONFIG = {
  rootPath: path.resolve(__dirname, '../../..'), // Points to Golden Universe root
  outputPath: path.resolve(__dirname, '../public/data'),
  dbPath: path.resolve(__dirname, '../public/data/content.db'),
  includePatterns: {
    theory: ['theory/**/*.md'],
    derivations: ['derivations/**/README.md', 'derivations/**/*.md'],
    python: ['**/*.py'],
    explanatory: ['explanatory/**/*.md']
  },
  excludePatterns: [
    '**/node_modules/**',
    '**/archive/**',
    '**/.git/**',
    '**/dist/**',
    '**/build/**'
  ]
};

// ============================================================================
// MARKDOWN PARSING
// ============================================================================

/**
 * Parse markdown frontmatter (YAML between --- delimiters)
 */
function parseFrontmatter(content: string): { frontmatter: Record<string, any>; content: string } {
  const frontmatterRegex = /^---\s*\n([\s\S]*?)\n---\s*\n([\s\S]*)$/;
  const match = content.match(frontmatterRegex);

  if (!match) {
    return { frontmatter: {}, content };
  }

  const frontmatterText = match[1];
  const mainContent = match[2];
  const frontmatter: Record<string, any> = {};

  // Simple YAML parser for common cases
  const lines = frontmatterText.split('\n');
  for (const line of lines) {
    const colonIndex = line.indexOf(':');
    if (colonIndex > 0) {
      const key = line.substring(0, colonIndex).trim();
      const value = line.substring(colonIndex + 1).trim();

      // Remove quotes if present
      const cleanValue = value.replace(/^["']|["']$/g, '');

      // Try to parse as array
      if (cleanValue.startsWith('[') && cleanValue.endsWith(']')) {
        frontmatter[key] = cleanValue
          .slice(1, -1)
          .split(',')
          .map(v => v.trim().replace(/^["']|["']$/g, ''));
      } else {
        frontmatter[key] = cleanValue;
      }
    }
  }

  return { frontmatter, content: mainContent };
}

/**
 * Convert markdown to basic HTML
 */
function markdownToHtml(markdown: string): string {
  let html = markdown;

  // Headers
  html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
  html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
  html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');

  // Bold and italic
  html = html.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

  // Links
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');

  // Code blocks
  html = html.replace(/```(\w+)?\n([\s\S]+?)```/g, '<pre><code class="language-$1">$2</code></pre>');
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

  // Lists
  html = html.replace(/^\* (.+)$/gim, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');

  // Paragraphs
  html = html.replace(/\n\n/g, '</p><p>');
  html = '<p>' + html + '</p>';

  return html;
}

/**
 * Extract LaTeX equations from markdown
 */
function extractEquations(content: string, documentId: string): Equation[] {
  const equations: Equation[] = [];
  const lines = content.split('\n');

  // Block equations ($$...$$)
  const blockRegex = /\$\$([\s\S]+?)\$\$/g;
  let match;
  while ((match = blockRegex.exec(content)) !== null) {
    const latex = match[1].trim();
    const lineNumber = content.substring(0, match.index).split('\n').length;

    equations.push({
      id: crypto.createHash('md5').update(`${documentId}-${latex}`).digest('hex'),
      latex,
      displayMode: true,
      lineNumber
    });
  }

  // Inline equations ($...$)
  const inlineRegex = /\$([^\$\n]+?)\$/g;
  while ((match = inlineRegex.exec(content)) !== null) {
    const latex = match[1].trim();
    const lineNumber = content.substring(0, match.index).split('\n').length;

    equations.push({
      id: crypto.createHash('md5').update(`${documentId}-${latex}`).digest('hex'),
      latex,
      displayMode: false,
      lineNumber
    });
  }

  return equations;
}

/**
 * Extract title from markdown content
 */
function extractTitle(content: string, filename: string): string {
  // Try to find first # heading
  const match = content.match(/^#\s+(.+)$/m);
  if (match) {
    return match[1].trim();
  }

  // Fall back to filename
  return filename.replace(/\.md$/, '').replace(/_/g, ' ');
}

/**
 * Extract precision results (ppm, percentages, etc.)
 */
function extractPrecisionResults(content: string): PrecisionResult[] {
  const results: PrecisionResult[] = [];
  const lines = content.split('\n');

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Match patterns like "23 ppm", "0.00%", "50 digits"
    const ppmMatch = line.match(/(\d+(?:\.\d+)?)\s*ppm/i);
    if (ppmMatch) {
      results.push({
        description: line.trim(),
        value: parseFloat(ppmMatch[1]),
        unit: 'ppm',
        context: lines.slice(Math.max(0, i - 2), i + 3).join('\n')
      });
    }

    const percentMatch = line.match(/(\d+(?:\.\d+)?)\s*%/);
    if (percentMatch) {
      results.push({
        description: line.trim(),
        value: parseFloat(percentMatch[1]),
        unit: 'percentage',
        context: lines.slice(Math.max(0, i - 2), i + 3).join('\n')
      });
    }

    const digitsMatch = line.match(/(\d+)[\s-]*digits?/i);
    if (digitsMatch) {
      results.push({
        description: line.trim(),
        value: parseInt(digitsMatch[1]),
        unit: 'digits',
        context: lines.slice(Math.max(0, i - 2), i + 3).join('\n')
      });
    }
  }

  return results;
}

// ============================================================================
// PYTHON PARSING
// ============================================================================

/**
 * Extract Python docstring from content
 */
function extractPythonDocstring(content: string): string | undefined {
  // Match triple-quoted strings at the beginning of the file
  const match = content.match(/^[\s\n]*"""([\s\S]*?)"""|^[\s\n]*'''([\s\S]*?)'''/);
  if (match) {
    return (match[1] || match[2]).trim();
  }
  return undefined;
}

/**
 * Extract Python function signatures
 */
function extractPythonFunctions(content: string): PythonFunction[] {
  const functions: PythonFunction[] = [];
  const lines = content.split('\n');

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Match function definitions
    const match = line.match(/^(\s*)def\s+(\w+)\s*\((.*?)\)(?:\s*->\s*([^:]+))?:/);
    if (match) {
      const [, indent, name, params, returnType] = match;

      // Extract docstring for this function
      let docstring: string | undefined;
      if (i + 1 < lines.length) {
        const nextLine = lines[i + 1].trim();
        if (nextLine.startsWith('"""') || nextLine.startsWith("'''")) {
          const docMatch = content.substring(content.indexOf(line) + line.length).match(/"""([\s\S]*?)"""|'''([\s\S]*?)'''/);
          if (docMatch) {
            docstring = (docMatch[1] || docMatch[2]).trim();
          }
        }
      }

      // Parse parameters
      const parameters = params.split(',').map(p => {
        const param = p.trim();
        if (!param) return null;

        const parts = param.split('=');
        const nameType = parts[0].trim();
        const defaultValue = parts[1]?.trim();

        const typeMatch = nameType.match(/(\w+)\s*:\s*(.+)/);
        if (typeMatch) {
          return {
            name: typeMatch[1],
            type: typeMatch[2].trim(),
            defaultValue
          };
        }

        return {
          name: nameType,
          type: undefined,
          defaultValue
        };
      }).filter(Boolean) as any[];

      functions.push({
        name,
        signature: line.trim(),
        docstring,
        parameters,
        lineNumber: i + 1
      });
    }
  }

  return functions;
}

/**
 * Extract Python imports
 */
function extractPythonImports(content: string): string[] {
  const imports: string[] = [];
  const lines = content.split('\n');

  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.startsWith('import ') || trimmed.startsWith('from ')) {
      imports.push(trimmed);
    }
  }

  return imports;
}

// ============================================================================
// FILE SYSTEM OPERATIONS
// ============================================================================

/**
 * Recursively find files matching patterns
 */
function findFiles(dir: string, patterns: string[], excludePatterns: string[] = []): string[] {
  const files: string[] = [];

  function walk(currentPath: string) {
    const entries = fs.readdirSync(currentPath, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(currentPath, entry.name);
      const relativePath = path.relative(CONFIG.rootPath, fullPath);

      // Check exclude patterns
      if (excludePatterns.some(pattern => {
        const regex = new RegExp(pattern.replace(/\*\*/g, '.*').replace(/\*/g, '[^/]*'));
        return regex.test(relativePath);
      })) {
        continue;
      }

      if (entry.isDirectory()) {
        walk(fullPath);
      } else if (entry.isFile()) {
        // Check include patterns
        if (patterns.some(pattern => {
          const regex = new RegExp(pattern.replace(/\*\*/g, '.*').replace(/\*/g, '[^/]*'));
          return regex.test(relativePath);
        })) {
          files.push(fullPath);
        }
      }
    }
  }

  walk(dir);
  return files;
}

/**
 * Get file stats
 */
function getFileStats(filePath: string) {
  const stats = fs.statSync(filePath);
  return {
    size: stats.size,
    createdAt: stats.birthtime.toISOString(),
    modifiedAt: stats.mtime.toISOString()
  };
}

// ============================================================================
// CONTENT PROCESSING
// ============================================================================

/**
 * Process a theory markdown file
 */
function processTheoryDocument(filePath: string): TheoryDocument | null {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    const { frontmatter, content: mainContent } = parseFrontmatter(content);
    const filename = path.basename(filePath);
    const stats = getFileStats(filePath);

    const id = crypto.createHash('md5').update(filePath).digest('hex');
    const title = frontmatter.title || extractTitle(mainContent, filename);
    const equations = extractEquations(mainContent, id);
    const wordCount = mainContent.split(/\s+/).length;

    return {
      id,
      path: path.relative(CONFIG.rootPath, filePath),
      filename,
      title,
      content: mainContent,
      equations,
      wordCount,
      createdAt: stats.createdAt,
      modifiedAt: stats.modifiedAt
    };
  } catch (error) {
    console.error(`Error processing ${filePath}:`, error);
    return null;
  }
}

/**
 * Process a Python script
 */
function processPythonScript(filePath: string) {
  try {
    const content = fs.readFileSync(filePath, 'utf-8');
    const filename = path.basename(filePath);
    const stats = getFileStats(filePath);

    const id = crypto.createHash('md5').update(filePath).digest('hex');
    const docstring = extractPythonDocstring(content);
    const functions = extractPythonFunctions(content);
    const imports = extractPythonImports(content);
    const contentHash = crypto.createHash('md5').update(content).digest('hex');

    return {
      id,
      path: path.relative(CONFIG.rootPath, filePath),
      filename,
      folderPath: path.relative(CONFIG.rootPath, path.dirname(filePath)),
      docstring,
      functions,
      imports,
      contentHash,
      lineCount: content.split('\n').length,
      createdAt: stats.createdAt,
      modifiedAt: stats.modifiedAt
    };
  } catch (error) {
    console.error(`Error processing ${filePath}:`, error);
    return null;
  }
}

/**
 * Process a derivation folder
 */
function processDerivationFolder(folderPath: string): DerivationFolder | null {
  try {
    const folderName = path.basename(folderPath);
    const stats = getFileStats(folderPath);

    // Find README
    const readmePath = path.join(folderPath, 'README.md');
    let readme: TheoryDocument | undefined;
    if (fs.existsSync(readmePath)) {
      readme = processTheoryDocument(readmePath) || undefined;
    }

    // Find Python scripts
    const pythonFiles = fs.readdirSync(folderPath)
      .filter(f => f.endsWith('.py'))
      .map(f => path.join(folderPath, f));

    const pythonScripts = pythonFiles
      .map(f => processPythonScript(f))
      .filter(Boolean);

    // Find markdown files
    const markdownFiles = fs.readdirSync(folderPath)
      .filter(f => f.endsWith('.md') && f !== 'README.md')
      .map(f => path.join(folderPath, f));

    const markdownDocs = markdownFiles
      .map(f => processTheoryDocument(f))
      .filter(Boolean);

    // Determine status from README or folder name
    let status = 'active';
    if (readme?.content.toLowerCase().includes('archived')) {
      status = 'archived';
    } else if (readme?.content.toLowerCase().includes('deprecated')) {
      status = 'deprecated';
    }

    // Create display name
    const displayName = folderName
      .replace(/^\d+_/, '') // Remove number prefix
      .replace(/_/g, ' ')
      .toLowerCase()
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');

    return {
      id: crypto.createHash('md5').update(folderPath).digest('hex'),
      folderName,
      path: path.relative(CONFIG.rootPath, folderPath),
      displayName,
      readme,
      pythonScripts: pythonScripts as any[],
      markdownFiles: markdownDocs as any[],
      status,
      fileCount: pythonFiles.length + markdownFiles.length,
      createdAt: stats.createdAt,
      modifiedAt: stats.modifiedAt
    };
  } catch (error) {
    console.error(`Error processing derivation folder ${folderPath}:`, error);
    return null;
  }
}

// ============================================================================
// MAIN PARSING LOGIC
// ============================================================================

async function parseAllContent() {
  console.log('🔍 Starting Golden Universe content parsing...\n');
  console.log(`Root path: ${CONFIG.rootPath}\n`);

  const startTime = Date.now();

  // Ensure output directory exists
  if (!fs.existsSync(CONFIG.outputPath)) {
    fs.mkdirSync(CONFIG.outputPath, { recursive: true });
  }

  // Parse theory documents
  console.log('📚 Parsing theory documents...');
  const theoryFiles = findFiles(
    path.join(CONFIG.rootPath, 'theory'),
    ['**/*.md'],
    CONFIG.excludePatterns
  );
  const theories = theoryFiles.map(f => processTheoryDocument(f)).filter(Boolean) as TheoryDocument[];
  console.log(`   Found ${theories.length} theory documents\n`);

  // Parse explanatory documents
  console.log('📖 Parsing explanatory documents...');
  const explanatoryPath = path.join(CONFIG.rootPath, 'explanatory');
  const explanatoryFiles = fs.existsSync(explanatoryPath)
    ? findFiles(explanatoryPath, ['**/*.md'], CONFIG.excludePatterns)
    : [];
  const explanatory = explanatoryFiles.map(f => processTheoryDocument(f)).filter(Boolean) as TheoryDocument[];
  console.log(`   Found ${explanatory.length} explanatory documents\n`);

  // Parse derivation folders
  console.log('🔬 Parsing derivation folders...');
  const derivationsPath = path.join(CONFIG.rootPath, 'derivations');
  const derivationDirs = fs.existsSync(derivationsPath)
    ? fs.readdirSync(derivationsPath)
        .map(d => path.join(derivationsPath, d))
        .filter(d => fs.statSync(d).isDirectory())
        .filter(d => !d.includes('archive') && !d.includes('utils'))
    : [];

  const derivations = derivationDirs
    .map(d => processDerivationFolder(d))
    .filter(Boolean) as DerivationFolder[];
  console.log(`   Found ${derivations.length} derivation folders\n`);

  // Parse all Python scripts
  console.log('🐍 Parsing Python scripts...');
  const pythonFiles = findFiles(CONFIG.rootPath, ['**/*.py'], CONFIG.excludePatterns);
  const pythonScripts = pythonFiles.map(f => processPythonScript(f)).filter(Boolean);
  console.log(`   Found ${pythonScripts.length} Python scripts\n`);

  // Collect all equations
  console.log('📐 Collecting equations...');
  const allEquations = [
    ...theories.flatMap(t => t.equations.map(e => ({ ...e, documentId: t.id }))),
    ...explanatory.flatMap(t => t.equations.map(e => ({ ...e, documentId: t.id }))),
    ...derivations.flatMap(d =>
      d.readme?.equations?.map(e => ({ ...e, documentId: d.readme!.id })) || []
    )
  ];
  console.log(`   Found ${allEquations.length} equations\n`);

  // Extract precision results
  console.log('📊 Extracting precision results...');
  const precisionResults = [
    ...theories.flatMap(t => extractPrecisionResults(t.content)),
    ...derivations.flatMap(d => d.readme ? extractPrecisionResults(d.readme.content) : [])
  ];
  console.log(`   Found ${precisionResults.length} precision results\n`);

  // Build content catalog
  const catalog = {
    theories: [...theories, ...explanatory],
    derivations,
    pythonScripts,
    equations: allEquations,
    precisionResults,
    metadata: {
      generatedAt: new Date().toISOString(),
      version: '1.0.0',
      totalTheories: theories.length + explanatory.length,
      totalDerivations: derivations.length,
      totalPythonScripts: pythonScripts.length,
      totalEquations: allEquations.length,
      totalMarkdownFiles: theoryFiles.length + explanatoryFiles.length,
      repositoryPath: CONFIG.rootPath
    }
  };

  // Write output files
  console.log('💾 Writing output files...');

  // Content index
  fs.writeFileSync(
    path.join(CONFIG.outputPath, 'content-index.json'),
    JSON.stringify(catalog, null, 2)
  );
  console.log('   ✓ content-index.json');

  // Derivations map
  fs.writeFileSync(
    path.join(CONFIG.outputPath, 'derivations-map.json'),
    JSON.stringify({
      derivations,
      metadata: {
        totalFolders: derivations.length,
        totalFiles: derivations.reduce((sum, d) => sum + d.fileCount, 0),
        generatedAt: new Date().toISOString()
      }
    }, null, 2)
  );
  console.log('   ✓ derivations-map.json');

  // Equations catalog
  fs.writeFileSync(
    path.join(CONFIG.outputPath, 'equations-catalog.json'),
    JSON.stringify({
      equations: allEquations,
      metadata: {
        totalEquations: allEquations.length,
        generatedAt: new Date().toISOString()
      }
    }, null, 2)
  );
  console.log('   ✓ equations-catalog.json');

  // Summary statistics
  const duration = Date.now() - startTime;
  console.log('\n✅ Parsing complete!\n');
  console.log('Statistics:');
  console.log(`  - Theory documents: ${theories.length}`);
  console.log(`  - Explanatory documents: ${explanatory.length}`);
  console.log(`  - Derivation folders: ${derivations.length}`);
  console.log(`  - Python scripts: ${pythonScripts.length}`);
  console.log(`  - Equations: ${allEquations.length}`);
  console.log(`  - Precision results: ${precisionResults.length}`);
  console.log(`  - Duration: ${(duration / 1000).toFixed(2)}s\n`);

  return catalog;
}

// ============================================================================
// ENTRY POINT
// ============================================================================

if (import.meta.url === `file://${process.argv[1]}`) {
  parseAllContent().catch(error => {
    console.error('❌ Parsing failed:', error);
    process.exit(1);
  });
}

export { parseAllContent, CONFIG };
