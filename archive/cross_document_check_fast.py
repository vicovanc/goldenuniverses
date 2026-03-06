#!/usr/bin/env python3
"""
Fast Cross-Document Equation Consistency Check
Uses hashing to efficiently find equations that appear in multiple documents
"""

import re
import json
from collections import defaultdict
from pathlib import Path

def normalize_equation(eq_text):
    """Normalize equation for comparison"""
    # Remove extra whitespace
    normalized = re.sub(r'\s+', ' ', eq_text.strip())
    # Remove \text formatting
    normalized = re.sub(r'\\text\{[^}]*\}', '', normalized)
    # Remove extra spaces around operators
    normalized = re.sub(r'\s*([=+\-*/])\s*', r'\1', normalized)
    return normalized

def extract_equations_from_file(filepath):
    """Extract all display equations from a file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    equations = []
    display_pattern = r'\$\$(.*?)\$\$'
    for match in re.finditer(display_pattern, content, re.DOTALL):
        eq_text = match.group(1).strip()
        line_num = content[:match.start()].count('\n') + 1
        equations.append({
            'text': eq_text,
            'normalized': normalize_equation(eq_text),
            'line': line_num
        })
    
    return equations

def find_cross_document_equations():
    """Find equations that appear in multiple documents using hash-based approach"""
    
    docs_path = Path("/Users/Cristiana_1/Documents/Golden Universe")
    docs = [
        "GU Couplings and Particles.md",
        "GU next in line.md",
        "Golden Universe Theory for the Calculation of Particles v2.md",
        "More Particles Stuff GU.md",
        "Some GU Particles Stuff.md"
    ]
    
    print("="*80)
    print("FAST CROSS-DOCUMENT EQUATION CONSISTENCY CHECK")
    print("="*80)
    
    # Extract equations from all documents
    all_equations = {}
    equation_hash = defaultdict(list)  # normalized_eq -> list of (doc, line, text)
    
    for doc_name in docs:
        filepath = docs_path / doc_name
        if filepath.exists():
            equations = extract_equations_from_file(filepath)
            all_equations[doc_name] = equations
            print(f"\n{doc_name}: {len(equations)} equations")
            
            # Build hash table
            for eq in equations:
                # Only track significant equations (with = and > 20 chars)
                if '=' in eq['normalized'] and len(eq['normalized']) > 20:
                    equation_hash[eq['normalized']].append({
                        'doc': doc_name,
                        'line': eq['line'],
                        'text': eq['text']
                    })
    
    # Find duplicates (equations in multiple documents)
    duplicates = []
    for norm_eq, occurrences in equation_hash.items():
        if len(occurrences) > 1:
            # Check that they're actually from different documents
            docs_with_eq = set(occ['doc'] for occ in occurrences)
            if len(docs_with_eq) > 1:
                duplicates.append({
                    'equation': norm_eq,
                    'occurrences': occurrences,
                    'num_documents': len(docs_with_eq)
                })
    
    # Sort by number of documents
    duplicates.sort(key=lambda x: -x['num_documents'])
    
    # Report findings
    print(f"\n{'='*80}")
    print(f"FINDINGS:")
    print(f"  Total equations analyzed: {sum(len(eqs) for eqs in all_equations.values())}")
    print(f"  Unique significant equations: {len(equation_hash)}")
    print(f"  Equations appearing in multiple documents: {len(duplicates)}")
    print(f"{'='*80}")
    
    # Show top duplicates
    if duplicates:
        print(f"\n📋 TOP DUPLICATES (equations in most documents):")
        for i, dup in enumerate(duplicates[:15]):
            print(f"\n{i+1}. Appears in {dup['num_documents']} documents, {len(dup['occurrences'])} times total:")
            print(f"   Equation: {dup['equation'][:100]}...")
            docs_shown = set()
            for occ in dup['occurrences'][:5]:  # Show first 5
                if occ['doc'] not in docs_shown:
                    print(f"   - {occ['doc']}, line {occ['line']}")
                    docs_shown.add(occ['doc'])
    
    # Analyze specific key equations
    print(f"\n{'='*80}")
    print(f"KEY EQUATIONS CROSS-DOCUMENT:")
    print(f"{'='*80}")
    
    key_patterns = [
        ('electron mass', r'm_?\{?e\}?.*=.*M_?[Pp]'),
        ('muon mass', r'm_?\{?\\mu\}?.*=.*M_?[Pp]'),
        ('tau mass', r'm_?\{?\\tau\}?.*=.*M_?[Pp]'),
        ('golden ratio', r'\\phi.*=.*1\.618'),
        ('golden angle', r'\\theta.*=.*2\\pi/\\phi'),
    ]
    
    for pattern_name, pattern in key_patterns:
        matching = []
        for norm_eq, occurrences in equation_hash.items():
            if re.search(pattern, norm_eq, re.IGNORECASE):
                if len(occurrences) >= 1:
                    matching.append((norm_eq, occurrences))
        
        if matching:
            print(f"\n{pattern_name.upper()}:")
            for eq, occs in matching[:3]:  # Top 3
                print(f"  {eq[:80]}...")
                print(f"  Found in: {', '.join(set(o['doc'] for o in occs))}")
    
    # Save results
    results = {
        'duplicates': duplicates[:100],  # Top 100
        'summary': {
            'total_documents': len(docs),
            'total_equations': sum(len(eqs) for eqs in all_equations.values()),
            'unique_equations': len(equation_hash),
            'cross_document_equations': len(duplicates)
        }
    }
    
    with open(docs_path / "CROSS_DOCUMENT_CHECK.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Cross-document check saved to: CROSS_DOCUMENT_CHECK.json")

if __name__ == "__main__":
    find_cross_document_equations()
