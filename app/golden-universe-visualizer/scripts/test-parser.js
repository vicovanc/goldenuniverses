// Quick test to verify paths and file access
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const rootPath = path.resolve(__dirname, '../../..');
console.log('Root path:', rootPath);
console.log('Exists:', fs.existsSync(rootPath));

// Check theory directory
const theoryPath = path.join(rootPath, 'theory');
console.log('\nTheory path:', theoryPath);
console.log('Exists:', fs.existsSync(theoryPath));

if (fs.existsSync(theoryPath)) {
  const files = fs.readdirSync(theoryPath);
  console.log('Files in theory:', files.length);
  console.log('First 5 files:', files.slice(0, 5));
}

// Check derivations directory
const derivPath = path.join(rootPath, 'derivations');
console.log('\nDerivations path:', derivPath);
console.log('Exists:', fs.existsSync(derivPath));

if (fs.existsSync(derivPath)) {
  const dirs = fs.readdirSync(derivPath).filter(d => {
    const fullPath = path.join(derivPath, d);
    return fs.statSync(fullPath).isDirectory();
  });
  console.log('Directories in derivations:', dirs.length);
  console.log('First 5 dirs:', dirs.slice(0, 5));
}

console.log('\nTest complete!');
