import Database from 'better-sqlite3';
import * as path from 'path';
import * as fs from 'fs';
import config from '../config/config';

export function initDatabase(): Database.Database {
  // Ensure data directory exists
  const dbDir = path.dirname(config.database.filename);
  if (!fs.existsSync(dbDir)) {
    fs.mkdirSync(dbDir, { recursive: true });
  }

  const db = new Database(config.database.filename);

  // Enable WAL mode for better concurrency
  db.pragma('journal_mode = WAL');

  // Create tables
  createTables(db);

  return db;
}

function createTables(db: Database.Database): void {
  // Theories table
  db.exec(`
    CREATE TABLE IF NOT EXISTS theories (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      filename TEXT UNIQUE NOT NULL,
      content TEXT NOT NULL,
      summary TEXT,
      keywords TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
  `);

  // Derivations table
  db.exec(`
    CREATE TABLE IF NOT EXISTS derivations (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      number INTEGER UNIQUE NOT NULL,
      title TEXT NOT NULL,
      description TEXT,
      folder_path TEXT NOT NULL,
      files TEXT, -- JSON array of files
      equations TEXT, -- JSON array of equations
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
  `);

  // Calculations table
  db.exec(`
    CREATE TABLE IF NOT EXISTS calculations (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      script_name TEXT NOT NULL,
      parameters TEXT, -- JSON object
      result TEXT, -- JSON object
      status TEXT CHECK(status IN ('pending', 'running', 'completed', 'failed')) DEFAULT 'pending',
      error TEXT,
      execution_time INTEGER, -- milliseconds
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      completed_at DATETIME
    );
  `);

  // Results cache table
  db.exec(`
    CREATE TABLE IF NOT EXISTS results_cache (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      key TEXT UNIQUE NOT NULL,
      value TEXT NOT NULL, -- JSON
      expires_at DATETIME NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
  `);

  // Equations catalog table
  db.exec(`
    CREATE TABLE IF NOT EXISTS equations (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      latex TEXT NOT NULL,
      category TEXT,
      description TEXT,
      derivation_id INTEGER,
      theory_id INTEGER,
      variables TEXT, -- JSON array
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (derivation_id) REFERENCES derivations(id),
      FOREIGN KEY (theory_id) REFERENCES theories(id)
    );
  `);

  // Full-text search virtual table for theories
  db.exec(`
    CREATE VIRTUAL TABLE IF NOT EXISTS theories_fts USING fts5(
      title,
      content,
      keywords,
      content='theories',
      content_rowid='id'
    );
  `);

  // Full-text search triggers
  db.exec(`
    CREATE TRIGGER IF NOT EXISTS theories_ai AFTER INSERT ON theories BEGIN
      INSERT INTO theories_fts(rowid, title, content, keywords)
      VALUES (new.id, new.title, new.content, new.keywords);
    END;

    CREATE TRIGGER IF NOT EXISTS theories_ad AFTER DELETE ON theories BEGIN
      DELETE FROM theories_fts WHERE rowid = old.id;
    END;

    CREATE TRIGGER IF NOT EXISTS theories_au AFTER UPDATE ON theories BEGIN
      UPDATE theories_fts SET title = new.title, content = new.content, keywords = new.keywords
      WHERE rowid = new.id;
    END;
  `);

  // Create indexes
  db.exec(`
    CREATE INDEX IF NOT EXISTS idx_calculations_status ON calculations(status);
    CREATE INDEX IF NOT EXISTS idx_calculations_created ON calculations(created_at);
    CREATE INDEX IF NOT EXISTS idx_results_cache_expires ON results_cache(expires_at);
    CREATE INDEX IF NOT EXISTS idx_equations_category ON equations(category);
    CREATE INDEX IF NOT EXISTS idx_derivations_number ON derivations(number);
  `);
}

export function getDatabase(): Database.Database {
  return new Database(config.database.filename);
}

export default { initDatabase, getDatabase };
