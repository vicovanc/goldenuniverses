# GU Documentation Management — Organization & Knowledge Management

**Use this skill when:** Organizing documentation, managing phase-based progress tracking, converting between formats (DOCX↔MD), maintaining notation databases, generating summaries, or navigating the extensive GU document collection (93+ markdown files).

## Documentation Architecture

### Current State (As of Phase 23+)

**Total files:** 201
**Markdown documents:** 93
**Python scripts:** 58
**JSON data:** 34
**Word documents:** 10
**PDFs:** 4

### Directory Organization

```
Golden Universe/
├── Core Theory Documents (Top Priority)
│   ├── theory/theory-laws.md ★★★ (Authoritative source, 4200+ lines)
│   ├── ⭐_MASTER_EQUATIONS_REFERENCE.md ★★★ (Equation compendium)
│   ├── theory/derived-laws.md ★★ (Step-by-step derivations)
│   ├── Golden Universe Laws.docx ★ (Word export of theory/theory-laws.md)
│   └── .cursor/skills/golden-universe-theory/SKILL.md (Cursor integration)
│
├── Source Manuscripts
│   ├── Golden Universe V2.docx (Main theory manuscript)
│   ├── Formation document.docx (Genesis vector Z₁)
│   ├── Particles v2.docx (Electron calculations)
│   ├── Couplings.docx (Force strengths)
│   └── PDFs/ (4 large PDFs, 3-188 MB)
│
├── Computational Pipeline
│   ├── pipeline/GU_formation_pipeline.py (889 lines, main pipeline)
│   ├── pipeline/GU_particle_masses.py (580 lines)
│   ├── pipeline/PHASE23_*.py (Current phase scripts)
│   └── 55+ other Python scripts
│
├── Progress & Status Documents (50+ files)
│   ├── Work sessions (WORK_SESSION_*.md)
│   ├── Phase summaries (📊_PHASE*.md)
│   ├── Breakthrough announcements (🔥_BREAKTHROUGH_*.md)
│   ├── Investigations (🔍_INVESTIGATION_*.md)
│   ├── Final analyses (✅_FINAL_*.md)
│   └── Assessments (⚠️_ASSESSMENT_*.md)
│
├── Analysis & Audits
│   ├── AUDIT_theory-laws_vs_pipeline.md (Theory-code mapping)
│   ├── GU_formation_pipeline_INVENTORY.md (Function inventory)
│   ├── ALL_FIRST_PRINCIPLES_LIST.md (57+ derivations catalog)
│   └── Dimensional analysis reports
│
├── Reference Data
│   ├── MASTER_NOTATION_GUIDE.json (188 KB, 650+ symbols)
│   ├── NOTATION_ANALYSIS.json (320 KB, cross-references)
│   ├── CODATA constants JSON files
│   └── Results JSON files (34 total)
│
└── Images & Visualizations
    ├── _images/ (5 subdirectories)
    ├── Resonance landscape plots
    └── Theory diagrams
```

## File Naming Conventions

### Emoji Prefixes (Semantic Organization)

```python
EMOJI_CATEGORIES = {
    '✅': 'Completion/Verification',  # Final, verified results
    '🔥': 'Breakthrough/Key Result',  # Major discoveries
    '🔍': 'Investigation',            # Active research
    '🎯': 'Goal/Solution',            # Targeted solutions
    '📊': 'Analysis/Status',          # Summaries and reports
    '🎉': 'Achievement',              # Milestones reached
    '⚠️': 'Warning/Assessment',       # Deprecation, issues
    '📣': 'Announcement',             # Important communications
    '⭐': 'Essential Reference',      # Critical documents
    '🔬': 'Detailed Calculation',     # Technical deep-dives
    '🎊': 'Reconciliation',           # Unifying different approaches
}
```

### Phase Naming

```python
PHASE_STRUCTURE = {
    'Phases 1-3': 'Foundation (Genesis, electron mass, resonance)',
    'Phases 4-10': 'Parameter extraction (Couplings, precision electron)',
    'Phases 11-21': 'Lepton sector & QED/EW corrections',
    'Phase 22': 'Complete organization and documentation',
    'Phase 23': 'All-electron methods and validation',
    'Phase 23+': 'Two-route reconciliation (current)',
}
```

## Document Priority System

### ★★★ Critical References (Always Check First)

1. **theory/theory-laws.md** — The authoritative source
   - 4200+ lines
   - Laws 0-38 with complete formalism
   - Five derivation routes
   - 50-digit precision values
   - **Location:** `/Users/Cristiana_1/Documents/Golden Universe/theory/theory-laws.md`

2. **⭐_MASTER_EQUATIONS_REFERENCE.md** — Equation lookup
   - Comprehensive equation compendium
   - Dimensional analysis
   - Cross-references to theory/theory-laws.md
   - **Location:** `/Users/Cristiana_1/Documents/Golden Universe/⭐_MASTER_EQUATIONS_REFERENCE.md`

3. **.claude/skills/** — Claude Code skills (this directory)
   - golden-universe-theory.md
   - gu-computational-physics.md
   - gu-mathematical-derivation.md
   - gu-code-audit.md
   - gu-documentation.md

### ★★ Essential Supporting Documents

4. **theory/derived-laws.md** — Derivation walkthrough
5. **GU_formation_pipeline_INVENTORY.md** — Code inventory
6. **AUDIT_theory-laws_vs_pipeline.md** — Theory-code mapping
7. **ALL_FIRST_PRINCIPLES_LIST.md** — Derivation catalog

### ★ Current Work & Progress

8. **Most recent PHASE23_*.md files** — Latest results
9. **WORK_SESSION_COMPLETE_SUMMARY.md** — Phase consolidation
10. **🔍_TWO_ROUTES_COMPLETE_ANALYSIS.md** — Route reconciliation

## Documentation Workflows

### 1. Finding Information

```python
def find_information(query: str, category: str = 'all') -> List[str]:
    """
    Find documents related to a query.

    Args:
        query: Search term (e.g., "electron mass", "NLDE", "resonance")
        category: 'theory', 'code', 'progress', 'analysis', or 'all'

    Returns:
        List of relevant file paths
    """
    import glob

    # Define search spaces
    search_patterns = {
        'theory': ['theory-*.md', 'derived-*.md', '*EQUATIONS*.md'],
        'code': ['*.py', '*_INVENTORY.md', 'AUDIT_*.md'],
        'progress': ['WORK_SESSION*.md', 'PHASE*.md', '*SUMMARY*.md'],
        'analysis': ['🔍*.md', '🔥*.md', '✅*.md'],
        'all': ['*.md', '*.py']
    }

    patterns = search_patterns.get(category, search_patterns['all'])
    results = []

    for pattern in patterns:
        files = glob.glob(pattern)
        for file in files:
            # Search file contents
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    if query.lower() in content:
                        results.append(file)
            except:
                pass

    return sorted(set(results))


# Example usage:
# find_information("electron mass", "theory")
# find_information("NLDE solver", "code")
# find_information("Phase 23", "progress")
```

### 2. Navigation Guide

```python
def navigate_to_topic(topic: str) -> dict:
    """
    Navigate to documents related to a specific topic.

    Topics:
    - 'electron_mass': Electron mass derivations
    - 'NLDE': Nonlinear Dirac equation
    - 'FRG': Functional renormalization group
    - 'resonance': N_e = 111 resonance
    - 'lepton_hierarchy': Muon and tau
    - 'gauge_bosons': W, Z, Higgs
    - 'notation': Symbol definitions
    - 'audit': Code verification
    """
    navigation = {
        'electron_mass': {
            'theory': ['theory/theory-laws.md (Laws 33-34)', 'theory/derived-laws.md'],
            'code': ['pipeline/PHASE23_EXACT_ELECTRON_DERIVATION.py', 'pipeline/GU_particle_masses.py'],
            'results': ['✅_FINAL_CORRECT_ANALYSIS.md'],
            'key_equations': ['m_e = M_0 · (2π/φ^111) · C_e']
        },

        'NLDE': {
            'theory': ['theory/theory-laws.md (Section: Route-A)', 'theory/derived-laws.md'],
            'code': ['Missing: NLDE_BVP_solver.py needs implementation'],
            'equations': ['dF/dr = (m + Σ - ω̃)G', 'dG/dr = -(2/r)G - (m + Σ + ω̃)F']
        },

        'FRG': {
            'theory': ['theory/theory-laws.md (Section: Route-C)', 'Formation document'],
            'code': ['pipeline/GU_formation_pipeline.py (FRG functions)'],
            'gaps': ['Lock-sector projection (ℓ_ab coefficients)', 'Beta functions incomplete']
        },

        'resonance': {
            'theory': ['theory/theory-laws.md (Law 21)', 'Formation document'],
            'code': ['pipeline/GU_formation_pipeline.py (resonance scan)'],
            'key_result': ['N_e = 111 → 111/φ² ≈ 42']
        },

        'lepton_hierarchy': {
            'theory': ['theory/theory-laws.md (Laws 35-37)', 'Particles v2 document'],
            'code': ['pipeline/PHASE23_ALL_LEPTONS_EXACT.py', 'pipeline/GU_particle_masses.py'],
            'results': ['📊_PHASE23_FINAL_SUMMARY.md']
        },

        'notation': {
            'reference': ['MASTER_NOTATION_GUIDE.json', 'NOTATION_ANALYSIS.json'],
            'conflicts': ['See gu-code-audit.md for common conflicts'],
            'canonical': ['theory/theory-laws.md (Law 14)', '.claude/skills/golden-universe-theory.md']
        },

        'audit': {
            'reports': ['AUDIT_theory-laws_vs_pipeline.md', 'GU_formation_pipeline_INVENTORY.md'],
            'gaps': ['See KNOWN_GAPS in gu-code-audit.md'],
            'validation': ['✅_FINAL_CORRECT_ANALYSIS.md']
        }
    }

    return navigation.get(topic, {'error': f'Topic "{topic}" not found'})
```

### 3. Document Generation

```python
def generate_progress_summary(phase: int, output_file: str):
    """
    Generate a phase summary document.

    Template includes:
    - Phase objectives
    - Work completed
    - Key results
    - Validation status
    - Next steps
    """
    summary = f"""# 📊 Phase {phase} Summary

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Objectives

[List phase objectives]

## Work Completed

### Theory Development
- [ ] Task 1
- [ ] Task 2

### Implementation
- [ ] Task 1
- [ ] Task 2

### Validation
- [ ] Task 1
- [ ] Task 2

## Key Results

| Quantity | Value | Error | Status |
|----------|-------|-------|--------|
| m_e | 0.51099895 MeV | 23 ppm (ν_topo) / 0% bootstrap | ✓ |
| ... | ... | ... | ... |

## Files Created/Modified

- `file1.py` — Description
- `file2.md` — Description

## Validation Status

- ✓ Theory-code consistency
- ✓ Dimensional analysis
- ✓ CODATA comparison
- ✓ Cross-route validation

## Known Issues

1. Issue 1
2. Issue 2

## Next Steps

1. Step 1
2. Step 2

## References

- theory/theory-laws.md (Laws X-Y)
- Previous phase summary: Phase {phase-1}

---
*Phase {phase} Complete* ✅
"""

    with open(output_file, 'w') as f:
        f.write(summary)

    print(f"Summary generated: {output_file}")
```

### 4. Format Conversion

```python
def convert_docx_to_markdown(docx_file: str, output_md: str):
    """
    Convert Word document to Markdown.

    Preserves:
    - Heading hierarchy
    - Equations (as LaTeX)
    - Lists
    - Tables
    - Basic formatting

    Requires: pandoc or python-docx
    """
    import subprocess

    # Using pandoc (recommended)
    cmd = [
        'pandoc',
        '-f', 'docx',
        '-t', 'markdown',
        '-o', output_md,
        docx_file,
        '--wrap=none',
        '--extract-media=_images'
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"✓ Converted {docx_file} → {output_md}")
    except subprocess.CalledProcessError:
        print(f"✗ Conversion failed. Ensure pandoc is installed.")
    except FileNotFoundError:
        print("✗ pandoc not found. Install with: brew install pandoc")


def markdown_to_html(md_file: str, output_html: str, style: str = 'github'):
    """
    Convert Markdown to HTML with styling.

    Styles:
    - 'github': GitHub-style markdown
    - 'arxiv': Academic paper style
    - 'minimal': Clean minimal style
    """
    import markdown

    with open(md_file, 'r') as f:
        md_content = f.read()

    # Convert with extensions
    html = markdown.markdown(
        md_content,
        extensions=['extra', 'codehilite', 'toc', 'tables', 'fenced_code']
    )

    # Add CSS styling
    css = get_css_style(style)

    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{md_file}</title>
    <style>{css}</style>
</head>
<body>
{html}
</body>
</html>
"""

    with open(output_html, 'w') as f:
        f.write(full_html)

    print(f"✓ Converted {md_file} → {output_html}")


def get_css_style(style: str) -> str:
    """Return CSS for specified style."""
    styles = {
        'github': """
            body { max-width: 900px; margin: 0 auto; padding: 20px;
                   font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; }
            code { background: #f6f8fa; padding: 2px 6px; border-radius: 3px; }
            pre { background: #f6f8fa; padding: 16px; overflow: auto; border-radius: 6px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f6f8fa; }
        """,
        'arxiv': """
            body { max-width: 700px; margin: 0 auto; padding: 40px;
                   font-family: "Computer Modern", serif; line-height: 1.6; }
            h1, h2, h3 { font-weight: bold; }
            code { font-family: "Courier New", monospace; }
        """,
        'minimal': """
            body { max-width: 800px; margin: 0 auto; padding: 20px;
                   font-family: Georgia, serif; line-height: 1.8; }
        """
    }
    return styles.get(style, styles['github'])
```

### 5. Cross-Reference Management

```python
def build_cross_reference_index():
    """
    Build an index of cross-references between documents.

    Returns:
        Dictionary mapping concepts to (file, line_number) references
    """
    import re

    index = {}

    # Key concepts to track
    concepts = [
        'Law [0-9]+',
        'Route [A-E]',
        'STEP [0-9]+',
        'FRG-STEP [0-9]+',
        'N_e = 111',
        'φ²',
        'm_e',
        'C_e',
        'ν = 0.82054',
        'μ = 0.4192',
    ]

    # Scan all markdown files
    import glob
    md_files = glob.glob('*.md')

    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line_num, line in enumerate(lines, 1):
            for concept in concepts:
                if re.search(concept, line):
                    if concept not in index:
                        index[concept] = []
                    index[concept].append((md_file, line_num, line.strip()[:80]))

    return index


def generate_index_file(index: dict, output_file: str = 'CROSS_REFERENCE_INDEX.md'):
    """Generate markdown index file from cross-reference data."""

    content = ["# Cross-Reference Index", "", "Auto-generated index of key concepts across GU documentation.", ""]

    for concept, refs in sorted(index.items()):
        content.append(f"\n## {concept}\n")
        content.append(f"Found in {len(refs)} location(s):\n")

        for file, line_num, text in refs[:10]:  # Show first 10
            content.append(f"- `{file}:{line_num}` — {text}")

        if len(refs) > 10:
            content.append(f"- *...and {len(refs) - 10} more*")

    with open(output_file, 'w') as f:
        f.write('\n'.join(content))

    print(f"✓ Cross-reference index generated: {output_file}")
```

### 6. Notation Database Management

```python
def query_notation(symbol: str, context: str = None) -> dict:
    """
    Query the notation database for symbol definitions.

    Args:
        symbol: The symbol to look up (e.g., 'μ', 'ω', 'φ')
        context: Optional context ('route_A', 'FRG', 'NLDE', etc.)

    Returns:
        Dictionary with all definitions and contexts
    """
    import json

    with open('MASTER_NOTATION_GUIDE.json', 'r') as f:
        notation_db = json.load(f)

    if symbol not in notation_db:
        return {'error': f'Symbol "{symbol}" not found in database'}

    definitions = notation_db[symbol]

    if context:
        # Filter by context
        filtered = [d for d in definitions if context.lower() in d.get('context', '').lower()]
        return {'symbol': symbol, 'context': context, 'definitions': filtered}

    return {'symbol': symbol, 'all_definitions': definitions}


def add_notation_entry(symbol: str, definition: str, context: str, dimension: int):
    """
    Add new notation entry to database.

    Args:
        symbol: The symbol (LaTeX or Unicode)
        definition: Description of what it represents
        context: Where it's used (route, equation, file)
        dimension: Mass dimension in natural units
    """
    import json

    # Load existing database
    with open('MASTER_NOTATION_GUIDE.json', 'r') as f:
        notation_db = json.load(f)

    # Create entry
    entry = {
        'definition': definition,
        'context': context,
        'dimension': dimension,
        'added': datetime.now().isoformat()
    }

    # Add or append
    if symbol in notation_db:
        if isinstance(notation_db[symbol], list):
            notation_db[symbol].append(entry)
        else:
            notation_db[symbol] = [notation_db[symbol], entry]
    else:
        notation_db[symbol] = [entry]

    # Save
    with open('MASTER_NOTATION_GUIDE.json', 'w') as f:
        json.dump(notation_db, f, indent=2)

    print(f"✓ Added notation: {symbol} in context '{context}'")
```

## Document Maintenance

### Deprecation Workflow

```python
def deprecate_document(file_path: str, reason: str, replacement: str = None):
    """
    Mark a document as deprecated.

    Adds deprecation notice at top of file.
    """
    with open(file_path, 'r') as f:
        content = f.read()

    # Create deprecation notice
    notice = f"""---
**⚠️ DEPRECATED**

This document is deprecated and should not be used for new work.

**Reason:** {reason}

{"**Replacement:** " + replacement if replacement else "**Replacement:** None"}

**Deprecated on:** {datetime.now().strftime('%Y-%m-%d')}
---

"""

    # Prepend notice
    new_content = notice + content

    with open(file_path, 'w') as f:
        f.write(new_content)

    print(f"✓ Deprecated: {file_path}")
```

### Consistency Checks

```python
def check_document_consistency():
    """
    Check for common documentation issues:

    1. Orphaned references (links to non-existent files)
    2. Duplicate content
    3. Outdated version numbers
    4. Missing critical sections
    5. Inconsistent notation usage
    """
    issues = []

    # Check 1: Orphaned references
    import glob
    import re

    all_files = set(glob.glob('*.md') + glob.glob('*.py'))

    for md_file in glob.glob('*.md'):
        with open(md_file, 'r') as f:
            content = f.read()

        # Find references like [file.md](file.md) or see file.py
        refs = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
        refs += re.findall(r'see ([a-zA-Z0-9_.-]+\.(?:md|py))', content)

        for ref in refs:
            target = ref[1] if isinstance(ref, tuple) else ref
            if target not in all_files:
                issues.append(f"Orphaned reference in {md_file}: {target}")

    # Check 2: Duplicate content
    # ... (analyze similarity between files)

    return issues
```

## Quick Reference Commands

```python
# Find where electron mass is calculated
files = find_information("electron mass", "code")

# Navigate to NLDE topic
info = navigate_to_topic("NLDE")

# Look up notation
mu_def = query_notation("μ", context="route_B")

# Generate phase summary
generate_progress_summary(phase=23, output_file="📊_PHASE23_SUMMARY.md")

# Convert Word to Markdown
convert_docx_to_markdown("Golden Universe Laws.docx", "theory/theory-laws.md")

# Build cross-reference index
index = build_cross_reference_index()
generate_index_file(index)

# Check for issues
issues = check_document_consistency()
```

## Documentation Style Guide

### Markdown Conventions

```markdown
# Title (H1) — Only one per document

## Main Section (H2)

### Subsection (H3)

#### Detail (H4)

**Bold** for emphasis, *italic* for terms

`inline code` for symbols, variables, file names

```python
# Code blocks with language specification
```

LaTeX math: $m_e = M_0 \cdot \frac{2\pi}{\phi^{111}} \cdot C_e$

Tables:
| Quantity | Value | Unit |
|----------|-------|------|
| m_e      | 0.511 | MeV  |

Lists:
- Item 1
- Item 2

1. Step 1
2. Step 2
```

### File Naming

```
# Good:
theory/theory-laws.md
AUDIT_theory-laws_vs_pipeline.md
pipeline/PHASE23_EXACT_ELECTRON_DERIVATION.py
✅_FINAL_CORRECT_ANALYSIS.md

# Bad:
temp.md
file1.txt
new_document.md  (too vague)
```

## When to Use This Skill

**Invoke when:**
- Organizing or reorganizing documents
- Finding specific information across many files
- Converting between formats (DOCX, MD, HTML)
- Managing notation database
- Generating progress summaries
- Creating cross-reference indices
- Deprecating outdated documents
- Checking documentation consistency

**Related skills:**
- `golden-universe-theory` → Content understanding
- `gu-computational-physics` → Code documentation
- `gu-code-audit` → Audit reports
