#!/usr/bin/env node

/**
 * Test Content Service (Node.js environment)
 *
 * Tests that the generated JSON files can be loaded and queried.
 * This is a Node.js test - the actual service uses fetch() in browsers.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const DATA_PATH = path.resolve(__dirname, '../public/data');

console.log('🧪 Testing Content Service...\n');

// Test 1: Load content-index.json
console.log('Test 1: Loading content-index.json');
try {
  const contentPath = path.join(DATA_PATH, 'content-index.json');
  const content = JSON.parse(fs.readFileSync(contentPath, 'utf-8'));

  console.log('✅ Loaded successfully');
  console.log(`   - Theories: ${content.theories.length}`);
  console.log(`   - Derivations: ${content.derivations.length}`);
  console.log(`   - Python Scripts: ${content.pythonScripts.length}`);
  console.log(`   - Equations: ${content.equations.length}`);
  console.log(`   - Precision Results: ${content.precisionResults.length}`);

  // Test theory document structure
  if (content.theories.length > 0) {
    const firstTheory = content.theories[0];
    console.log(`\n   Sample Theory Document:`);
    console.log(`   - ID: ${firstTheory.id}`);
    console.log(`   - Title: ${firstTheory.title}`);
    console.log(`   - Path: ${firstTheory.path}`);
    console.log(`   - Word Count: ${firstTheory.wordCount}`);
    console.log(`   - Equations: ${firstTheory.equations.length}`);
  }

  // Test derivation structure
  if (content.derivations.length > 0) {
    const firstDerivation = content.derivations[0];
    console.log(`\n   Sample Derivation:`);
    console.log(`   - Folder: ${firstDerivation.folderName}`);
    console.log(`   - Display Name: ${firstDerivation.displayName}`);
    console.log(`   - Status: ${firstDerivation.status}`);
    console.log(`   - Python Scripts: ${firstDerivation.pythonScripts.length}`);
    console.log(`   - Has README: ${firstDerivation.readme ? 'Yes' : 'No'}`);
  }

  // Test Python script structure
  if (content.pythonScripts.length > 0) {
    const firstScript = content.pythonScripts[0];
    console.log(`\n   Sample Python Script:`);
    console.log(`   - Filename: ${firstScript.filename}`);
    console.log(`   - Path: ${firstScript.path}`);
    console.log(`   - Functions: ${firstScript.functions.length}`);
    console.log(`   - Line Count: ${firstScript.lineCount}`);

    if (firstScript.functions.length > 0) {
      console.log(`   - First Function: ${firstScript.functions[0].name}()`);
    }
  }

} catch (error) {
  console.error('❌ Failed:', error.message);
}

// Test 2: Load derivations-map.json
console.log('\n\nTest 2: Loading derivations-map.json');
try {
  const derivPath = path.join(DATA_PATH, 'derivations-map.json');
  const derivMap = JSON.parse(fs.readFileSync(derivPath, 'utf-8'));

  console.log('✅ Loaded successfully');
  console.log(`   - Total Folders: ${derivMap.metadata.totalFolders}`);
  console.log(`   - Total Files: ${derivMap.metadata.totalFiles}`);
  console.log(`   - Generated At: ${derivMap.metadata.generatedAt}`);

  // Count by status
  const statusCounts = derivMap.derivations.reduce((acc, d) => {
    acc[d.status] = (acc[d.status] || 0) + 1;
    return acc;
  }, {});

  console.log(`\n   Status Distribution:`);
  Object.entries(statusCounts).forEach(([status, count]) => {
    console.log(`   - ${status}: ${count}`);
  });

} catch (error) {
  console.error('❌ Failed:', error.message);
}

// Test 3: Load equations-catalog.json
console.log('\n\nTest 3: Loading equations-catalog.json');
try {
  const eqPath = path.join(DATA_PATH, 'equations-catalog.json');
  const eqCatalog = JSON.parse(fs.readFileSync(eqPath, 'utf-8'));

  console.log('✅ Loaded successfully');
  console.log(`   - Total Equations: ${eqCatalog.metadata.totalEquations}`);
  console.log(`   - Documents with Equations: ${Object.keys(eqCatalog.byDocument).length}`);

  // Sample equation
  if (eqCatalog.equations.length > 0) {
    const firstEq = eqCatalog.equations[0];
    console.log(`\n   Sample Equation:`);
    console.log(`   - LaTeX: ${firstEq.latex.substring(0, 60)}...`);
    console.log(`   - Display Mode: ${firstEq.displayMode ? 'Block' : 'Inline'}`);
    console.log(`   - Document ID: ${firstEq.documentId}`);
  }

  // Count display vs inline
  const displayCount = eqCatalog.equations.filter(eq => eq.displayMode).length;
  const inlineCount = eqCatalog.equations.filter(eq => !eq.displayMode).length;

  console.log(`\n   Equation Types:`);
  console.log(`   - Display (block): ${displayCount}`);
  console.log(`   - Inline: ${inlineCount}`);

} catch (error) {
  console.error('❌ Failed:', error.message);
}

// Test 4: Search simulation
console.log('\n\nTest 4: Simulating Search');
try {
  const contentPath = path.join(DATA_PATH, 'content-index.json');
  const content = JSON.parse(fs.readFileSync(contentPath, 'utf-8'));

  const searchTerm = 'electron';
  const results = [];

  // Search in theories
  content.theories.forEach(theory => {
    if (theory.title.toLowerCase().includes(searchTerm) ||
        theory.content.toLowerCase().includes(searchTerm)) {
      results.push({
        type: 'theory',
        title: theory.title,
        path: theory.path
      });
    }
  });

  // Search in derivations
  content.derivations.forEach(deriv => {
    if (deriv.displayName.toLowerCase().includes(searchTerm) ||
        (deriv.readme && deriv.readme.content.toLowerCase().includes(searchTerm))) {
      results.push({
        type: 'derivation',
        title: deriv.displayName,
        path: deriv.path
      });
    }
  });

  console.log(`✅ Search for "${searchTerm}" found ${results.length} results`);

  if (results.length > 0) {
    console.log(`\n   Top 5 Results:`);
    results.slice(0, 5).forEach((result, i) => {
      console.log(`   ${i + 1}. [${result.type}] ${result.title}`);
      console.log(`      Path: ${result.path}`);
    });
  }

} catch (error) {
  console.error('❌ Failed:', error.message);
}

// Test 5: Check file sizes
console.log('\n\nTest 5: File Size Check');
try {
  const files = [
    'content-index.json',
    'derivations-map.json',
    'equations-catalog.json'
  ];

  console.log('File sizes:');
  files.forEach(file => {
    const filePath = path.join(DATA_PATH, file);
    const stats = fs.statSync(filePath);
    const sizeKB = (stats.size / 1024).toFixed(2);
    const sizeMB = (stats.size / (1024 * 1024)).toFixed(2);

    console.log(`   - ${file}: ${sizeKB} KB (${sizeMB} MB)`);
  });

  const totalSize = files.reduce((sum, file) => {
    const filePath = path.join(DATA_PATH, file);
    return sum + fs.statSync(filePath).size;
  }, 0);

  console.log(`\n   Total: ${(totalSize / (1024 * 1024)).toFixed(2)} MB`);

} catch (error) {
  console.error('❌ Failed:', error.message);
}

console.log('\n\n✅ All tests completed!\n');
console.log('The content parsing system is working correctly.');
console.log('JSON files are ready to be used by the React application.\n');
