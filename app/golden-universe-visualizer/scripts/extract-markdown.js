#!/usr/bin/env node

/**
 * Script to extract markdown content from content-index.json
 * and save as separate markdown files
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Read the content index
const contentIndexPath = path.join(__dirname, '..', 'public', 'data', 'content-index.json');
const outputDir = path.join(__dirname, '..', 'public', 'data', 'theory');

// Ensure output directory exists
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

console.log('Reading content-index.json...');
const contentData = JSON.parse(fs.readFileSync(contentIndexPath, 'utf-8'));

// Process theories
if (contentData.theories && Array.isArray(contentData.theories)) {
  console.log(`Found ${contentData.theories.length} theory documents`);

  contentData.theories.forEach((theory, index) => {
    if (theory.content && theory.filename) {
      const outputPath = path.join(outputDir, theory.filename);
      console.log(`Writing ${theory.filename}...`);
      fs.writeFileSync(outputPath, theory.content, 'utf-8');
      console.log(`  ✓ Saved to ${outputPath}`);
    }
  });
}

// Process explanations
if (contentData.explanations && Array.isArray(contentData.explanations)) {
  console.log(`Found ${contentData.explanations.length} explanation documents`);

  contentData.explanations.forEach((explanation, index) => {
    if (explanation.content && explanation.filename) {
      const outputPath = path.join(outputDir, explanation.filename);
      console.log(`Writing ${explanation.filename}...`);
      fs.writeFileSync(outputPath, explanation.content, 'utf-8');
      console.log(`  ✓ Saved to ${outputPath}`);
    }
  });
}

// Process demonstrations
if (contentData.demonstrations && Array.isArray(contentData.demonstrations)) {
  console.log(`Found ${contentData.demonstrations.length} demonstration documents`);

  contentData.demonstrations.forEach((demo, index) => {
    if (demo.content && demo.filename) {
      const outputPath = path.join(outputDir, demo.filename);
      console.log(`Writing ${demo.filename}...`);
      fs.writeFileSync(outputPath, demo.content, 'utf-8');
      console.log(`  ✓ Saved to ${outputPath}`);
    }
  });
}

console.log('✅ Extraction complete!');