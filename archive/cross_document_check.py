#!/usr/bin/env python3
"""
Cross-Document Equation Consistency Check
Finds equations that appear in multiple documents and checks for variations
"""

import re
import json
from collections import defaultdict
from difflib import SequenceMatcher

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

def similarity(a, b):
    """Calculate similarity ratio between two strings"""
    return SequenceMatcher(None, a, b).ratio()

def find_cross_document_equations():
    """Find equations that appear in multiple documents"""
    from pathlib import Path
    
    docs_path = Path("/Users/Cristiana_1/Documents/Golden Universe")
    docs = [
        "GU Couplings and Particles.md",
        "GU next in line.md",
        "Golden Universe Theory for the Calculation of Particles v2.md",
        "More Particles Stuff GU.md",
        "Some GU Particles Stuff.md"
    ]
    
    print("="*80)
    print("CROSS-DOCUMENT EQUATION CONSISTENCY CHECK")
    print("="*80)
    
    # Extract equations from all documents
    all_equations = {}
    for doc_name in docs:
        filepath = docs_path / doc_name
        if filepath.exists():
            equations = extract_equations_from_file(filepath)
            all_equations[doc_name] = equations
            print(f"\n{doc_name}: {len(equations)} equations")
    
    # Find duplicates and near-duplicates
    duplicates = defaultdict(list)
    near_duplicates = defaultdict(list)
    variations = []
    
    doc_names = list(all_equations.keys())
    
    for i, doc1 in enumerate(doc_names):
        for j, doc2 in enumerate(doc_names):
            if j <= i:
                continue
            
            eqs1 = all_equations[doc1]
            eqs2 = all_equations[doc2]
            
            for eq1 in eqs1:
                for eq2 in eqs2:
                    # Exact match
                    if eq1['normalized'] == eq2['normalized']:
                        key = eq1['normalized']
                        if key not in [d['equation'] for d in duplicates.values()]:
                            duplicates[len(duplicates)] = {
                                'equation': key,
                                'occurrences': [
                                    {'doc': doc1, 'line': eq1['line'], 'text': eq1['text']},
                                    {'doc': doc2, 'line': eq2['line'], 'text': eq2['text']}
                                ]
                            }
                        else:
                            # Add to existing
                            for dup in duplicates.values():
                                if dup['equation'] == key:
                                    if {'doc': doc2, 'line': eq2['line'], 'text': eq2['text']} not in dup['occurrences']:
                                        dup['occurrences'].append({'doc': doc2, 'line': eq2['line'], 'text': eq2['text']})
                    
                    # Near match (similarity > 0.8)
                    elif similarity(eq1['normalized'], eq2['normalized']) > 0.8:
                        # Check if it's a significant equation (has = and is longer than 20 chars)
                        if '=' in eq1['text'] and len(eq1['normalized']) > 20:
                            sim = similarity(eq1['normalized'], eq2['normalized'])
                            variations.append({
                                'similarity': sim,
                                'doc1': doc1,
                                'line1': eq1['line'],
                                'text1': eq1['text'][:100],
                                'doc2': doc2,
                                'line2': eq2['line'],
                                'text2': eq2['text'][:100]
                            })
    
    # Report findings
    print(f"\n{'='*80}")
    print(f"FINDINGS:")
    print(f"  Exact duplicates found: {len(duplicates)}")
    print(f"  Near-duplicate variations: {len(variations)}")
    print(f"{'='*80}")
    
    # Show some exact duplicates
    if duplicates:
        print(f"\n📋 EXACT DUPLICATES (first 10):")
        for i, (idx, dup) in enumerate(list(duplicates.items())[:10]):
            print(f"\n{i+1}. Appears in {len(dup['occurrences'])} documents:")
            print(f"   Equation: {dup['equation'][:80]}...")
            for occ in dup['occurrences']:
                print(f"   - {occ['doc']}, line {occ['line']}")
    
    # Show some variations
    if variations:
        print(f"\n⚠️  NEAR-DUPLICATE VARIATIONS (first 5 - may indicate inconsistencies):")
        for i, var in enumerate(sorted(variations, key=lambda x: -x['similarity'])[:5]):
            print(f"\n{i+1}. Similarity: {var['similarity']:.1%}")
            print(f"   {var['doc1']}, line {var['line1']}:")
            print(f"   {var['text1']}")
            print(f"   {var['doc2']}, line {var['line2']}:")
            print(f"   {var['text2']}")
    
    # Save results
    results = {
        'exact_duplicates': [dict(d) for d in duplicates.values()],
        'near_duplicates': variations,
        'summary': {
            'total_exact': len(duplicates),
            'total_near': len(variations),
            'documents_analyzed': len(docs)
        }
    }
    
    with open(docs_path / "CROSS_DOCUMENT_CHECK.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Cross-document check saved to: CROSS_DOCUMENT_CHECK.json")

if __name__ == "__main__":
    find_cross_document_equations()
