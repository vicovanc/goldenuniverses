#!/usr/bin/env python3
"""
Extract and catalog all mathematical notation across GU theory documents
Check for conflicts where same symbol has different meanings/units
"""

import re
import json
from pathlib import Path
from collections import defaultdict

class NotationExtractor:
    def __init__(self):
        self.notation_db = defaultdict(lambda: {
            'contexts': [],
            'documents': set(),
            'likely_units': set(),
            'likely_meaning': set()
        })
        
        # Physics constants and their expected meanings
        self.known_symbols = {
            'M_P': ('Planck mass', 'mass'),
            'M_Z': ('Z boson mass', 'mass'),
            'm_e': ('electron mass', 'mass'),
            'm_p': ('proton mass', 'mass'),
            'm_n': ('neutron mass', 'mass'),
            'k_B': ('Boltzmann constant', 'energy/temperature'),
            'c': ('speed of light', 'velocity'),
            'G': ('gravitational constant', 'length^3/(mass*time^2)'),
            '\\hbar': ('reduced Planck constant', 'action'),
            '\\pi': ('pi', 'dimensionless'),
            '\\phi': ('golden ratio (usually)', 'dimensionless'),
            '\\varphi': ('golden ratio alternate', 'dimensionless'),
            '\\alpha': ('coupling constant (usually fine structure)', 'dimensionless'),
            '\\Lambda': ('energy scale (usually QCD)', 'energy'),
        }
    
    def extract_from_equation(self, eq_text, doc_name, line_num):
        """Extract symbols and their context from an equation"""
        
        # Extract variable definitions (X = ..., m_e = ...)
        definition_pattern = r'([A-Za-z_\\{}]+)\s*=\s*(.+?)(?:\s|$|\)|\]|,)'
        for match in re.finditer(definition_pattern, eq_text):
            symbol = match.group(1).strip()
            rhs = match.group(2).strip()
            
            # Infer units from RHS
            units = self.infer_units(rhs)
            meaning = self.infer_meaning(symbol, rhs)
            
            self.notation_db[symbol]['contexts'].append({
                'equation': eq_text[:80],
                'document': doc_name,
                'line': line_num,
                'rhs': rhs
            })
            self.notation_db[symbol]['documents'].add(doc_name)
            if units:
                self.notation_db[symbol]['likely_units'].add(units)
            if meaning:
                self.notation_db[symbol]['likely_meaning'].add(meaning)
        
        # Extract all symbols that appear
        symbol_pattern = r'\\?[A-Za-z]+_\{?[A-Za-z0-9]+\}?|\\[a-z]+'
        for match in re.finditer(symbol_pattern, eq_text):
            symbol = match.group(0)
            if symbol not in self.notation_db[symbol]['documents']:
                self.notation_db[symbol]['documents'].add(doc_name)
    
    def infer_units(self, expression):
        """Infer dimensional units from expression"""
        if 'MeV' in expression or 'GeV' in expression or 'eV' in expression:
            return 'energy/mass'
        elif any(mass in expression for mass in ['M_P', 'm_e', 'm_p', 'm_n']):
            return 'mass'
        elif 'rad' in expression or '\\pi' in expression or 'angle' in expression.lower():
            return 'angle'
        elif any(dim in expression for dim in ['k_B', 'entropy', 'S_']):
            return 'entropy/dimensionless'
        return None
    
    def infer_meaning(self, symbol, rhs):
        """Infer likely physical meaning"""
        symbol_lower = symbol.lower()
        
        if 'mass' in symbol_lower or symbol.startswith('m_'):
            return 'mass'
        elif 'alpha' in symbol_lower or symbol.startswith('\\alpha'):
            return 'coupling constant'
        elif 'theta' in symbol_lower or '\\theta' in symbol:
            return 'angle/phase'
        elif symbol in ['n', 'N', 'N_e', 'N_q']:
            return 'integer/epoch number'
        elif 'Lambda' in symbol or '\\Lambda' in symbol:
            return 'energy scale'
        
        return None
    
    def find_conflicts(self):
        """Find symbols used with different meanings/units"""
        conflicts = []
        
        for symbol, data in self.notation_db.items():
            # Check if same symbol has multiple unit types
            if len(data['likely_units']) > 1:
                conflicts.append({
                    'symbol': symbol,
                    'issue': 'multiple_units',
                    'units': list(data['likely_units']),
                    'documents': list(data['documents']),
                    'contexts': data['contexts'][:3]  # First 3 uses
                })
            
            # Check if same symbol has multiple meanings
            if len(data['likely_meaning']) > 1:
                conflicts.append({
                    'symbol': symbol,
                    'issue': 'multiple_meanings',
                    'meanings': list(data['likely_meaning']),
                    'documents': list(data['documents']),
                    'contexts': data['contexts'][:3]
                })
        
        return conflicts

def analyze_all_documents():
    """Main analysis function"""
    docs_path = Path("/Users/Cristiana_1/Documents/Golden Universe")
    
    # Documents with proper LaTeX equations
    docs_to_analyze = [
        "GU Couplings and Particles.md",
        "GU next in line.md",
        "Golden Universe Theory for the Calculation of Particles v2.md",
        "More Particles Stuff GU.md",
        "Some GU Particles Stuff.md"
    ]
    
    extractor = NotationExtractor()
    
    print("="*80)
    print("EXTRACTING NOTATION FROM ALL DOCUMENTS")
    print("="*80)
    
    total_equations = 0
    
    for doc_name in docs_to_analyze:
        filepath = docs_path / doc_name
        if not filepath.exists():
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract display equations
        display_pattern = r'\$\$(.*?)\$\$'
        equations = list(re.finditer(display_pattern, content, re.DOTALL))
        
        print(f"\n{doc_name}: {len(equations)} display equations")
        
        for match in equations:
            eq_text = match.group(1).strip()
            line_num = content[:match.start()].count('\n') + 1
            extractor.extract_from_equation(eq_text, doc_name, line_num)
            total_equations += 1
    
    print(f"\n{'='*80}")
    print(f"Total equations analyzed: {total_equations}")
    print(f"Unique symbols cataloged: {len(extractor.notation_db)}")
    print(f"{'='*80}")
    
    # Find conflicts
    conflicts = extractor.find_conflicts()
    
    print(f"\n🚨 NOTATION CONFLICTS FOUND: {len(conflicts)}")
    
    if conflicts:
        print("\nTop conflicts:")
        for i, conflict in enumerate(conflicts[:10], 1):
            print(f"\n{i}. Symbol: {conflict['symbol']}")
            print(f"   Issue: {conflict['issue']}")
            if 'units' in conflict:
                print(f"   Different units: {conflict['units']}")
            if 'meanings' in conflict:
                print(f"   Different meanings: {conflict['meanings']}")
            print(f"   Used in: {conflict['documents']}")
    
    # Save full report
    report_path = docs_path / "NOTATION_ANALYSIS.json"
    with open(report_path, 'w') as f:
        # Convert sets to lists for JSON
        db_serializable = {}
        for symbol, data in extractor.notation_db.items():
            db_serializable[symbol] = {
                'documents': list(data['documents']),
                'units': list(data['likely_units']),
                'meanings': list(data['likely_meaning']),
                'usage_count': len(data['contexts']),
                'sample_contexts': data['contexts'][:5]
            }
        
        json.dump({
            'notation_database': db_serializable,
            'conflicts': conflicts,
            'summary': {
                'total_symbols': len(extractor.notation_db),
                'conflicts_found': len(conflicts),
                'documents_analyzed': len(docs_to_analyze)
            }
        }, f, indent=2)
    
    print(f"\n✅ Full report saved to: NOTATION_ANALYSIS.json")
    
    return extractor, conflicts

if __name__ == "__main__":
    extractor, conflicts = analyze_all_documents()
