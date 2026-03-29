#!/usr/bin/env node
/**
 * Copy all derivation files to public directory for static serving
 * This ensures Python files can be served directly as static assets on Vercel
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_PATH = path.resolve(__dirname, '..');
const PUBLIC_DERIVATIONS_PATH = path.resolve(ROOT_PATH, 'public/derivations');

// Try multiple possible locations for derivations folder
const possibleDerivationsPaths = [
  path.resolve(ROOT_PATH, '../../derivations'),  // Standard: repo/derivations
  path.resolve(ROOT_PATH, '../../../derivations'), // One level up
  path.resolve(ROOT_PATH, 'derivations'),         // Same level as app
];

// Find the first existing derivations path
let DERIVATIONS_PATH = null;
for (const possiblePath of possibleDerivationsPaths) {
  if (fs.existsSync(possiblePath)) {
    DERIVATIONS_PATH = possiblePath;
    break;
  }
}

if (!DERIVATIONS_PATH) {
  console.error('Error: Could not find derivations folder in any of these locations:');
  possibleDerivationsPaths.forEach(p => console.error(`  - ${p}`));
  process.exit(1);
}

/**
 * Recursively copy directory
 */
function copyDirRecursive(src, dest) {
  // Create destination directory if it doesn't exist
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }

  // Read all files and directories
  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      // Skip certain directories and hidden folders (starting with .)
      if (entry.name === '__pycache__' || entry.name === '.pytest_cache' ||
          entry.name === 'node_modules' || entry.name === '.git' ||
          entry.name.startsWith('.')) {
        continue;
      }
      copyDirRecursive(srcPath, destPath);
    } else {
      // Copy only Python and Markdown files
      if (entry.name.endsWith('.py') || entry.name.endsWith('.md')) {
        fs.copyFileSync(srcPath, destPath);
        console.log(`Copied: ${path.relative(ROOT_PATH, destPath)}`);
      }
    }
  }
}

/**
 * Main execution
 */
function main() {
  console.log('Copying derivation files to public directory...\n');
  console.log(`Source: ${DERIVATIONS_PATH}`);
  console.log(`Destination: ${PUBLIC_DERIVATIONS_PATH}\n`);

  // Remove existing public/derivations directory
  if (fs.existsSync(PUBLIC_DERIVATIONS_PATH)) {
    fs.rmSync(PUBLIC_DERIVATIONS_PATH, { recursive: true, force: true });
    console.log('Removed existing public/derivations directory\n');
  }

  // Copy all derivation files
  copyDirRecursive(DERIVATIONS_PATH, PUBLIC_DERIVATIONS_PATH);

  console.log('\n✅ Successfully copied all derivation files to public directory');

  // Count files
  const countFiles = (dir) => {
    let count = { py: 0, md: 0 };
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        const subCount = countFiles(fullPath);
        count.py += subCount.py;
        count.md += subCount.md;
      } else if (entry.name.endsWith('.py')) {
        count.py++;
      } else if (entry.name.endsWith('.md')) {
        count.md++;
      }
    }
    return count;
  };

  const totals = countFiles(PUBLIC_DERIVATIONS_PATH);
  console.log(`\nTotal files copied:`);
  console.log(`  - Python files: ${totals.py}`);
  console.log(`  - Markdown files: ${totals.md}`);
}

main();
