#!/usr/bin/env node

/**
 * Quick Content Parser - Simplified version for fast execution
 */

import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const ROOT_PATH = path.resolve(__dirname, '../../..');
const OUTPUT_PATH = path.resolve(__dirname, '../public/data');

console.log('🔍 Quick parsing Golden Universe content...\n');
const startTime = Date.now();

// Helper to generate ID
const generateId = (str) => crypto.createHash('md5').update(str).digest('hex');

// Helper to get file stats
const getStats = (filePath) => {
  const stats = fs.statSync(filePath);
  return {
    createdAt: stats.birthtime.toISOString(),
    modifiedAt: stats.mtime.toISOString()
  };
};

// Parse theory documents
console.log('📚 Parsing theory documents...');
const theoryPath = path.join(ROOT_PATH, 'theory');
const theoryFiles = fs.readdirSync(theoryPath).filter(f => f.endsWith('.md'));

const theories = theoryFiles.map(filename => {
  const filePath = path.join(theoryPath, filename);
  const content = fs.readFileSync(filePath, 'utf-8');
  const stats = getStats(filePath);

  // Extract title from first # heading or filename
  const titleMatch = content.match(/^#\s+(.+)$/m);
  const title = titleMatch ? titleMatch[1].trim() : filename.replace(/\.md$/, '');

  // Extract equations (simplified - just count them)
  const blockEquations = (content.match(/\$\$([\s\S]+?)\$\$/g) || []).map((eq, i) => ({
    id: generateId(filePath + eq),
    latex: eq.replace(/\$\$/g, '').trim(),
    displayMode: true,
    lineNumber: i + 1
  }));

  const inlineEquations = (content.match(/\$([^\$\n]+?)\$/g) || [])
    .slice(0, 50) // Limit inline equations
    .map((eq, i) => ({
      id: generateId(filePath + eq + i),
      latex: eq.replace(/\$/g, '').trim(),
      displayMode: false,
      lineNumber: i + 1
    }));

  const equations = [...blockEquations, ...inlineEquations];

  return {
    id: generateId(filePath),
    path: path.relative(ROOT_PATH, filePath),
    filename,
    title,
    content: content.substring(0, 50000), // Limit content length for JSON size
    wordCount: content.split(/\s+/).length,
    equations,
    metadata: {
      title,
      category: 'theory'
    },
    ...stats
  };
});

console.log(`   Found ${theories.length} theory documents`);

// Parse explanatory documents
console.log('📖 Parsing explanatory documents...');
const explanatoryPath = path.join(ROOT_PATH, 'explanatory');
let explanatory = [];

if (fs.existsSync(explanatoryPath)) {
  const explFiles = fs.readdirSync(explanatoryPath).filter(f => f.endsWith('.md'));
  explanatory = explFiles.map(filename => {
    const filePath = path.join(explanatoryPath, filename);
    const content = fs.readFileSync(filePath, 'utf-8');
    const stats = getStats(filePath);
    const titleMatch = content.match(/^#\s+(.+)$/m);
    const title = titleMatch ? titleMatch[1].trim() : filename.replace(/\.md$/, '');

    return {
      id: generateId(filePath),
      path: path.relative(ROOT_PATH, filePath),
      filename,
      title,
      content: content.substring(0, 50000),
      wordCount: content.split(/\s+/).length,
      equations: [],
      metadata: {
        title,
        category: 'explanatory'
      },
      ...stats
    };
  });
}

console.log(`   Found ${explanatory.length} explanatory documents`);

// Parse derivation folders
console.log('🔬 Parsing derivation folders...');
const derivationsPath = path.join(ROOT_PATH, 'derivations');
const derivationDirs = fs.readdirSync(derivationsPath)
  .filter(d => {
    const fullPath = path.join(derivationsPath, d);
    return fs.statSync(fullPath).isDirectory() &&
           !d.includes('archive') &&
           !d.includes('utils');
  });

const derivations = derivationDirs.map(folderName => {
  const folderPath = path.join(derivationsPath, folderName);
  const stats = getStats(folderPath);

  // Check for README
  const readmePath = path.join(folderPath, 'README.md');
  let readme = null;

  if (fs.existsSync(readmePath)) {
    const content = fs.readFileSync(readmePath, 'utf-8');
    const readmeStats = getStats(readmePath);
    const titleMatch = content.match(/^#\s+(.+)$/m);

    readme = {
      id: generateId(readmePath),
      path: path.relative(ROOT_PATH, readmePath),
      filename: 'README.md',
      title: titleMatch ? titleMatch[1].trim() : folderName,
      content: content.substring(0, 50000),
      wordCount: content.split(/\s+/).length,
      equations: [],
      ...readmeStats
    };
  }

  // Count files
  const allFiles = fs.readdirSync(folderPath);
  const pythonFiles = allFiles.filter(f => f.endsWith('.py'));
  const markdownFiles = allFiles.filter(f => f.endsWith('.md') && f !== 'README.md');

  // Parse Python files (simplified)
  const pythonScripts = pythonFiles.slice(0, 20).map(filename => { // Limit to 20 per folder
    const filePath = path.join(folderPath, filename);
    const content = fs.readFileSync(filePath, 'utf-8');
    const pyStats = getStats(filePath);

    // Extract docstring
    const docMatch = content.match(/^[\s\n]*[\"']{3}([\s\S]*?)[\"']{3}/);
    const docstring = docMatch ? docMatch[1].trim() : undefined;

    // Extract function definitions (simple regex)
    const funcMatches = [...content.matchAll(/def\s+(\w+)\s*\([^)]*\):/g)];
    const functions = funcMatches.map((m, i) => ({
      name: m[1],
      signature: m[0],
      lineNumber: i + 1
    }));

    return {
      id: generateId(filePath),
      path: path.relative(ROOT_PATH, filePath),
      filename,
      folderPath: path.relative(ROOT_PATH, folderPath),
      content: content, // Include full Python code content
      docstring,
      functions,
      lineCount: content.split('\n').length,
      contentHash: generateId(content),
      ...pyStats
    };
  });

  // Parse Markdown files (excluding README.md)
  const markdownDocs = markdownFiles.slice(0, 20).map(filename => { // Limit to 20 per folder
    const filePath = path.join(folderPath, filename);
    const content = fs.readFileSync(filePath, 'utf-8');
    const mdStats = getStats(filePath);

    // Extract title from first heading
    const titleMatch = content.match(/^#\s+(.+)$/m);
    const title = titleMatch ? titleMatch[1].trim() : filename.replace('.md', '');

    return {
      id: generateId(filePath),
      path: path.relative(ROOT_PATH, filePath),
      filename,
      folderPath: path.relative(ROOT_PATH, folderPath),
      title,
      content: content.substring(0, 50000), // Limit content size
      lineCount: content.split('\n').length,
      wordCount: content.split(/\s+/).length,
      contentHash: generateId(content),
      ...mdStats
    };
  });

  // Determine status
  let status = 'active';
  if (readme && readme.content.toLowerCase().includes('archived')) {
    status = 'archived';
  } else if (readme && readme.content.toLowerCase().includes('deprecated')) {
    status = 'deprecated';
  }

  // Create display name
  const displayName = folderName
    .replace(/^\d+_/, '')
    .replace(/_/g, ' ')
    .toLowerCase()
    .split(' ')
    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');

  return {
    id: generateId(folderPath),
    folderName,
    path: path.relative(ROOT_PATH, folderPath),
    displayName,
    readme,
    pythonScripts,
    markdownFiles: markdownDocs,
    status,
    fileCount: pythonFiles.length + markdownFiles.length,
    ...stats
  };
});

console.log(`   Found ${derivations.length} derivation folders`);

// Collect all Python scripts
const pythonScripts = derivations.flatMap(d => d.pythonScripts);
console.log(`🐍 Total Python scripts: ${pythonScripts.length}`);

// Collect all equations
const allEquations = theories.flatMap(t =>
  t.equations.map(e => ({ ...e, documentId: t.id }))
);
console.log(`📐 Total equations: ${allEquations.length}`);

// Extract precision results
console.log('📊 Extracting precision results...');
const precisionResults = [];

[...theories, ...derivations.map(d => d.readme).filter(Boolean)].forEach(doc => {
  const lines = doc.content.split('\n');
  lines.forEach((line, i) => {
    // Match ppm
    const ppmMatch = line.match(/(\d+(?:\.\d+)?)\s*ppm/i);
    if (ppmMatch) {
      precisionResults.push({
        description: line.trim(),
        value: parseFloat(ppmMatch[1]),
        unit: 'ppm',
        context: lines.slice(Math.max(0, i - 1), i + 2).join('\n'),
        documentId: doc.id
      });
    }

    // Match percentages
    const percentMatch = line.match(/(\d+(?:\.\d+)?)\s*%/);
    if (percentMatch && !line.includes('100%')) {
      precisionResults.push({
        description: line.trim(),
        value: parseFloat(percentMatch[1]),
        unit: 'percentage',
        context: lines.slice(Math.max(0, i - 1), i + 2).join('\n'),
        documentId: doc.id
      });
    }
  });
});

console.log(`   Found ${precisionResults.length} precision results`);

// Build catalog
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
    totalMarkdownFiles: theories.length + explanatory.length,
    repositoryPath: ROOT_PATH
  }
};

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_PATH)) {
  fs.mkdirSync(OUTPUT_PATH, { recursive: true });
}

// Write output files
console.log('\n💾 Writing output files...');

fs.writeFileSync(
  path.join(OUTPUT_PATH, 'content-index.json'),
  JSON.stringify(catalog, null, 2)
);
console.log('   ✓ content-index.json');

fs.writeFileSync(
  path.join(OUTPUT_PATH, 'derivations-map.json'),
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

fs.writeFileSync(
  path.join(OUTPUT_PATH, 'equations-catalog.json'),
  JSON.stringify({
    equations: allEquations,
    byDocument: allEquations.reduce((acc, eq) => {
      if (!acc[eq.documentId]) acc[eq.documentId] = [];
      acc[eq.documentId].push(eq);
      return acc;
    }, {}),
    metadata: {
      totalEquations: allEquations.length,
      generatedAt: new Date().toISOString()
    }
  }, null, 2)
);
console.log('   ✓ equations-catalog.json');

const duration = Date.now() - startTime;
console.log('\n✅ Parsing complete!\n');
console.log('Statistics:');
console.log(`  - Theory documents: ${theories.length}`);
console.log(`  - Explanatory documents: ${explanatory.length}`);
console.log(`  - Derivation folders: ${derivations.length}`);
console.log(`  - Python scripts: ${pythonScripts.length}`);
console.log(`  - Equations: ${allEquations.length}`);
console.log(`  - Precision results: ${precisionResults.length}`);
console.log(`  - Duration: ${(duration / 1000).toFixed(2)}s`);
console.log(`\nOutput directory: ${OUTPUT_PATH}\n`);
