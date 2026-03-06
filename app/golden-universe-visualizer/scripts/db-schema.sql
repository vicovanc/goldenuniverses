-- ============================================================================
-- Golden Universe Content Database Schema
-- SQLite Database for indexing theories, derivations, Python scripts, and equations
-- ============================================================================

-- Drop existing tables if they exist (for clean rebuild)
DROP TABLE IF EXISTS search_index;
DROP TABLE IF EXISTS equations;
DROP TABLE IF EXISTS python_scripts;
DROP TABLE IF EXISTS derivation_folders;
DROP TABLE IF EXISTS theory_documents;
DROP TABLE IF EXISTS cross_references;
DROP TABLE IF EXISTS precision_results;

-- ============================================================================
-- THEORY DOCUMENTS TABLE
-- ============================================================================
CREATE TABLE theory_documents (
    id TEXT PRIMARY KEY,
    path TEXT NOT NULL UNIQUE,
    filename TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    html_content TEXT NOT NULL,
    metadata_json TEXT, -- JSON string of DocumentMetadata
    word_count INTEGER DEFAULT 0,
    created_at TEXT NOT NULL,
    modified_at TEXT NOT NULL,
    indexed_at TEXT NOT NULL,
    CONSTRAINT valid_dates CHECK (
        datetime(created_at) IS NOT NULL AND
        datetime(modified_at) IS NOT NULL AND
        datetime(indexed_at) IS NOT NULL
    )
);

-- Indexes for theory_documents
CREATE INDEX idx_theory_title ON theory_documents(title);
CREATE INDEX idx_theory_modified ON theory_documents(modified_at DESC);
CREATE INDEX idx_theory_path ON theory_documents(path);

-- Full-text search for theory documents
CREATE VIRTUAL TABLE theory_documents_fts USING fts5(
    title,
    content,
    metadata_json,
    content=theory_documents,
    content_rowid=rowid
);

-- Triggers to keep FTS index in sync
CREATE TRIGGER theory_documents_ai AFTER INSERT ON theory_documents BEGIN
    INSERT INTO theory_documents_fts(rowid, title, content, metadata_json)
    VALUES (new.rowid, new.title, new.content, new.metadata_json);
END;

CREATE TRIGGER theory_documents_ad AFTER DELETE ON theory_documents BEGIN
    DELETE FROM theory_documents_fts WHERE rowid = old.rowid;
END;

CREATE TRIGGER theory_documents_au AFTER UPDATE ON theory_documents BEGIN
    UPDATE theory_documents_fts
    SET title = new.title, content = new.content, metadata_json = new.metadata_json
    WHERE rowid = new.rowid;
END;

-- ============================================================================
-- DERIVATION FOLDERS TABLE
-- ============================================================================
CREATE TABLE derivation_folders (
    id TEXT PRIMARY KEY,
    folder_name TEXT NOT NULL UNIQUE,
    path TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'archived', 'deprecated')),
    category TEXT,
    file_count INTEGER DEFAULT 0,
    readme_content TEXT,
    created_at TEXT NOT NULL,
    modified_at TEXT NOT NULL,
    metadata_json TEXT, -- JSON string with key results, equations, etc.
    CONSTRAINT valid_dates CHECK (
        datetime(created_at) IS NOT NULL AND
        datetime(modified_at) IS NOT NULL
    )
);

-- Indexes for derivation_folders
CREATE INDEX idx_derivation_status ON derivation_folders(status);
CREATE INDEX idx_derivation_category ON derivation_folders(category);
CREATE INDEX idx_derivation_modified ON derivation_folders(modified_at DESC);

-- ============================================================================
-- PYTHON SCRIPTS TABLE
-- ============================================================================
CREATE TABLE python_scripts (
    id TEXT PRIMARY KEY,
    path TEXT NOT NULL UNIQUE,
    filename TEXT NOT NULL,
    folder_path TEXT NOT NULL,
    derivation_id TEXT,
    docstring TEXT,
    metadata_json TEXT, -- JSON string of PythonMetadata
    functions_json TEXT, -- JSON array of PythonFunction[]
    classes_json TEXT, -- JSON array of PythonClass[]
    imports_json TEXT, -- JSON array of imports
    content_hash TEXT NOT NULL,
    line_count INTEGER DEFAULT 0,
    created_at TEXT NOT NULL,
    modified_at TEXT NOT NULL,
    indexed_at TEXT NOT NULL,
    FOREIGN KEY (derivation_id) REFERENCES derivation_folders(id) ON DELETE CASCADE,
    CONSTRAINT valid_dates CHECK (
        datetime(created_at) IS NOT NULL AND
        datetime(modified_at) IS NOT NULL AND
        datetime(indexed_at) IS NOT NULL
    )
);

-- Indexes for python_scripts
CREATE INDEX idx_python_folder ON python_scripts(folder_path);
CREATE INDEX idx_python_derivation ON python_scripts(derivation_id);
CREATE INDEX idx_python_filename ON python_scripts(filename);
CREATE INDEX idx_python_hash ON python_scripts(content_hash);

-- Full-text search for Python scripts
CREATE VIRTUAL TABLE python_scripts_fts USING fts5(
    filename,
    docstring,
    functions_json,
    content=python_scripts,
    content_rowid=rowid
);

-- Triggers to keep FTS index in sync
CREATE TRIGGER python_scripts_ai AFTER INSERT ON python_scripts BEGIN
    INSERT INTO python_scripts_fts(rowid, filename, docstring, functions_json)
    VALUES (new.rowid, new.filename, new.docstring, new.functions_json);
END;

CREATE TRIGGER python_scripts_ad AFTER DELETE ON python_scripts BEGIN
    DELETE FROM python_scripts_fts WHERE rowid = old.rowid;
END;

CREATE TRIGGER python_scripts_au AFTER UPDATE ON python_scripts BEGIN
    UPDATE python_scripts_fts
    SET filename = new.filename, docstring = new.docstring, functions_json = new.functions_json
    WHERE rowid = new.rowid;
END;

-- ============================================================================
-- EQUATIONS TABLE
-- ============================================================================
CREATE TABLE equations (
    id TEXT PRIMARY KEY,
    document_id TEXT NOT NULL,
    latex TEXT NOT NULL,
    display_mode INTEGER DEFAULT 0, -- 0 = inline, 1 = block
    context TEXT, -- surrounding text
    label TEXT,
    variables_json TEXT, -- JSON array of variable names
    category TEXT CHECK (category IN ('fundamental', 'derived', 'result', 'identity', NULL)),
    line_number INTEGER,
    created_at TEXT NOT NULL,
    FOREIGN KEY (document_id) REFERENCES theory_documents(id) ON DELETE CASCADE,
    CONSTRAINT valid_date CHECK (datetime(created_at) IS NOT NULL)
);

-- Indexes for equations
CREATE INDEX idx_equation_document ON equations(document_id);
CREATE INDEX idx_equation_category ON equations(category);
CREATE INDEX idx_equation_label ON equations(label);

-- Full-text search for equations
CREATE VIRTUAL TABLE equations_fts USING fts5(
    latex,
    context,
    label,
    content=equations,
    content_rowid=rowid
);

-- Triggers to keep FTS index in sync
CREATE TRIGGER equations_ai AFTER INSERT ON equations BEGIN
    INSERT INTO equations_fts(rowid, latex, context, label)
    VALUES (new.rowid, new.latex, new.context, new.label);
END;

CREATE TRIGGER equations_ad AFTER DELETE ON equations BEGIN
    DELETE FROM equations_fts WHERE rowid = old.rowid;
END;

CREATE TRIGGER equations_au AFTER UPDATE ON equations BEGIN
    UPDATE equations_fts
    SET latex = new.latex, context = new.context, label = new.label
    WHERE rowid = new.rowid;
END;

-- ============================================================================
-- CROSS REFERENCES TABLE
-- ============================================================================
CREATE TABLE cross_references (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id TEXT NOT NULL,
    target_id TEXT NOT NULL,
    ref_type TEXT NOT NULL CHECK (ref_type IN ('reference', 'dependency', 'related', 'supersedes', 'superseded_by')),
    context TEXT,
    created_at TEXT NOT NULL,
    CONSTRAINT valid_date CHECK (datetime(created_at) IS NOT NULL),
    CONSTRAINT unique_reference UNIQUE (source_id, target_id, ref_type)
);

-- Indexes for cross_references
CREATE INDEX idx_crossref_source ON cross_references(source_id);
CREATE INDEX idx_crossref_target ON cross_references(target_id);
CREATE INDEX idx_crossref_type ON cross_references(ref_type);

-- ============================================================================
-- PRECISION RESULTS TABLE
-- ============================================================================
CREATE TABLE precision_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id TEXT,
    derivation_id TEXT,
    description TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT NOT NULL CHECK (unit IN ('ppm', 'percentage', 'digits')),
    context TEXT,
    equation TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (document_id) REFERENCES theory_documents(id) ON DELETE CASCADE,
    FOREIGN KEY (derivation_id) REFERENCES derivation_folders(id) ON DELETE CASCADE,
    CONSTRAINT valid_date CHECK (datetime(created_at) IS NOT NULL)
);

-- Indexes for precision_results
CREATE INDEX idx_precision_document ON precision_results(document_id);
CREATE INDEX idx_precision_derivation ON precision_results(derivation_id);
CREATE INDEX idx_precision_value ON precision_results(value);
CREATE INDEX idx_precision_unit ON precision_results(unit);

-- ============================================================================
-- UNIFIED SEARCH INDEX TABLE
-- ============================================================================
CREATE TABLE search_index (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL CHECK (type IN ('theory', 'derivation', 'python', 'equation', 'law')),
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    path TEXT NOT NULL,
    metadata_json TEXT,
    created_at TEXT NOT NULL,
    CONSTRAINT valid_date CHECK (datetime(created_at) IS NOT NULL)
);

-- Indexes for search_index
CREATE INDEX idx_search_type ON search_index(type);
CREATE INDEX idx_search_path ON search_index(path);

-- Full-text search for unified search
CREATE VIRTUAL TABLE search_index_fts USING fts5(
    title,
    content,
    metadata_json,
    content=search_index,
    content_rowid=rowid,
    tokenize = 'porter unicode61'
);

-- Triggers to keep FTS index in sync
CREATE TRIGGER search_index_ai AFTER INSERT ON search_index BEGIN
    INSERT INTO search_index_fts(rowid, title, content, metadata_json)
    VALUES (new.rowid, new.title, new.content, new.metadata_json);
END;

CREATE TRIGGER search_index_ad AFTER DELETE ON search_index BEGIN
    DELETE FROM search_index_fts WHERE rowid = old.rowid;
END;

CREATE TRIGGER search_index_au AFTER UPDATE ON search_index BEGIN
    UPDATE search_index_fts
    SET title = new.title, content = new.content, metadata_json = new.metadata_json
    WHERE rowid = new.rowid;
END;

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- View for derivations with their file counts
CREATE VIEW derivations_summary AS
SELECT
    d.id,
    d.folder_name,
    d.display_name,
    d.status,
    d.category,
    d.file_count,
    COUNT(DISTINCT p.id) as python_count,
    d.modified_at
FROM derivation_folders d
LEFT JOIN python_scripts p ON d.id = p.derivation_id
GROUP BY d.id;

-- View for documents with equation counts
CREATE VIEW documents_with_equations AS
SELECT
    t.id,
    t.title,
    t.path,
    t.word_count,
    COUNT(e.id) as equation_count,
    t.modified_at
FROM theory_documents t
LEFT JOIN equations e ON t.id = e.document_id
GROUP BY t.id;

-- View for search statistics
CREATE VIEW search_stats AS
SELECT
    (SELECT COUNT(*) FROM theory_documents) as total_theories,
    (SELECT COUNT(*) FROM derivation_folders) as total_derivations,
    (SELECT COUNT(*) FROM python_scripts) as total_python_scripts,
    (SELECT COUNT(*) FROM equations) as total_equations,
    (SELECT COUNT(*) FROM search_index) as total_searchable_items;

-- ============================================================================
-- INITIAL DATA / METADATA
-- ============================================================================

-- Create a metadata table for schema version and statistics
CREATE TABLE schema_metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

INSERT INTO schema_metadata (key, value, updated_at) VALUES
    ('schema_version', '1.0.0', datetime('now')),
    ('created_at', datetime('now'), datetime('now')),
    ('last_indexed', '', datetime('now'));

-- ============================================================================
-- STORED QUERIES / FUNCTIONS
-- ============================================================================

-- Note: SQLite doesn't support stored procedures, but we can create views
-- for common query patterns. These will be used by the TypeScript service layer.

-- View for recent updates
CREATE VIEW recent_updates AS
SELECT
    id,
    'theory' as type,
    title,
    path,
    modified_at
FROM theory_documents
UNION ALL
SELECT
    id,
    'derivation' as type,
    display_name as title,
    path,
    modified_at
FROM derivation_folders
UNION ALL
SELECT
    id,
    'python' as type,
    filename as title,
    path,
    modified_at
FROM python_scripts
ORDER BY modified_at DESC
LIMIT 50;

-- ============================================================================
-- PERFORMANCE OPTIMIZATIONS
-- ============================================================================

-- Enable WAL mode for better concurrent access
PRAGMA journal_mode = WAL;

-- Set cache size (negative value = KB)
PRAGMA cache_size = -64000; -- 64MB cache

-- Enable foreign keys
PRAGMA foreign_keys = ON;

-- Auto-vacuum to keep database size optimized
PRAGMA auto_vacuum = INCREMENTAL;

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================
