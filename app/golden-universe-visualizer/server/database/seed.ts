import { getDatabase } from './schema';
import * as fs from 'fs';
import * as path from 'path';
import config from '../config/config';

/**
 * Seed the database with content from the project
 */
export function seedDatabase(): void {
  console.log('Starting database seeding...');

  const db = getDatabase();

  try {
    // Start transaction
    db.exec('BEGIN TRANSACTION');

    // Seed theories
    seedTheories(db);

    // Seed derivations
    seedDerivations(db);

    // Seed sample equations
    seedEquations(db);

    // Commit transaction
    db.exec('COMMIT');

    console.log('Database seeding completed successfully');
  } catch (error) {
    db.exec('ROLLBACK');
    console.error('Database seeding failed:', error);
    throw error;
  } finally {
    db.close();
  }
}

function seedTheories(db: any): void {
  console.log('Seeding theories...');

  const theoriesPath = config.content.theoriesPath;

  if (!fs.existsSync(theoriesPath)) {
    console.warn(`Theories path not found: ${theoriesPath}`);
    return;
  }

  const stmt = db.prepare(`
    INSERT OR IGNORE INTO theories (title, filename, content, summary, keywords)
    VALUES (?, ?, ?, ?, ?)
  `);

  let count = 0;
  const files = fs.readdirSync(theoriesPath);

  for (const file of files) {
    if (file.endsWith('.md') || file.endsWith('.txt')) {
      const filePath = path.join(theoriesPath, file);
      const content = fs.readFileSync(filePath, 'utf-8');

      // Extract title from first line or filename
      const lines = content.split('\n');
      const title = lines[0].replace(/^#\s*/, '') || file.replace(/\.(md|txt)$/, '');

      // Extract summary (first paragraph after title)
      const summary = lines.slice(1, 5).join(' ').substring(0, 200);

      stmt.run(title, file, content, summary, '');
      count++;
    }
  }

  console.log(`Seeded ${count} theories`);
}

function seedDerivations(db: any): void {
  console.log('Seeding derivations...');

  const derivationsPath = config.content.derivationsPath;

  if (!fs.existsSync(derivationsPath)) {
    console.warn(`Derivations path not found: ${derivationsPath}`);
    return;
  }

  const stmt = db.prepare(`
    INSERT OR IGNORE INTO derivations (number, title, description, folder_path, files)
    VALUES (?, ?, ?, ?, ?)
  `);

  let count = 0;
  const folders = fs.readdirSync(derivationsPath);

  for (const folder of folders) {
    const folderPath = path.join(derivationsPath, folder);
    const stat = fs.statSync(folderPath);

    if (stat.isDirectory()) {
      // Extract number from folder name
      const match = folder.match(/^(\d+)/);
      if (match) {
        const number = parseInt(match[1], 10);
        const title = folder.replace(/^\d+[-_\s]*/, '');

        // Get list of files
        const files = fs.readdirSync(folderPath);
        const filesJson = JSON.stringify(files);

        stmt.run(number, title, '', folderPath, filesJson);
        count++;
      }
    }
  }

  console.log(`Seeded ${count} derivations`);
}

function seedEquations(db: any): void {
  console.log('Seeding sample equations...');

  const equations = [
    {
      name: 'Golden Ratio',
      latex: '\\phi = \\frac{1 + \\sqrt{5}}{2}',
      category: 'Fundamental Constants',
      description: 'The golden ratio, approximately 1.618033988749',
      variables: JSON.stringify([{ symbol: 'phi', name: 'Golden Ratio' }]),
    },
    {
      name: 'Fine Structure Constant',
      latex: '\\alpha = \\frac{e^2}{4\\pi\\epsilon_0\\hbar c}',
      category: 'Physical Constants',
      description: 'The fine structure constant, fundamental to quantum electrodynamics',
      variables: JSON.stringify([
        { symbol: 'alpha', name: 'Fine Structure Constant' },
        { symbol: 'e', name: 'Elementary Charge' },
        { symbol: 'epsilon_0', name: 'Vacuum Permittivity' },
        { symbol: 'hbar', name: 'Reduced Planck Constant' },
        { symbol: 'c', name: 'Speed of Light' },
      ]),
    },
    {
      name: 'Planck Length',
      latex: 'l_P = \\sqrt{\\frac{\\hbar G}{c^3}}',
      category: 'Planck Units',
      description: 'The Planck length, the smallest meaningful length in physics',
      variables: JSON.stringify([
        { symbol: 'l_P', name: 'Planck Length' },
        { symbol: 'hbar', name: 'Reduced Planck Constant' },
        { symbol: 'G', name: 'Gravitational Constant' },
        { symbol: 'c', name: 'Speed of Light' },
      ]),
    },
    {
      name: 'Electron Mass',
      latex: 'm_e = 9.1093837015 \\times 10^{-31} \\text{ kg}',
      category: 'Particle Masses',
      description: 'The rest mass of an electron',
      variables: JSON.stringify([{ symbol: 'm_e', name: 'Electron Mass' }]),
    },
    {
      name: 'Proton Mass',
      latex: 'm_p = 1.67262192369 \\times 10^{-27} \\text{ kg}',
      category: 'Particle Masses',
      description: 'The rest mass of a proton',
      variables: JSON.stringify([{ symbol: 'm_p', name: 'Proton Mass' }]),
    },
  ];

  const stmt = db.prepare(`
    INSERT OR IGNORE INTO equations (name, latex, category, description, variables)
    VALUES (?, ?, ?, ?, ?)
  `);

  for (const eq of equations) {
    stmt.run(eq.name, eq.latex, eq.category, eq.description, eq.variables);
  }

  console.log(`Seeded ${equations.length} sample equations`);
}

// Run seeding if called directly
if (require.main === module) {
  seedDatabase();
}

export default seedDatabase;
