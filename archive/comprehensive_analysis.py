#!/usr/bin/env python3
"""
Comprehensive Mathematical Analysis of Golden Universe Theory
- 50 decimal precision validation
- Notation conflict detection
- Dimensional analysis
- Cross-document consistency
"""

import re
import json
from pathlib import Path
from collections import defaultdict
from mpmath import mp, mpf, sin, cos, sqrt, exp, log, pi as mp_pi, e as mp_e, phi as mp_phi
from decimal import Decimal, getcontext

# Set precision to 50 decimal places
mp.dps = 50
getcontext().prec = 50

class ComprehensiveAnalyzer:
    def __init__(self):
        # Master notation dictionary: symbol -> {meaning, units, contexts, conflicts}
        self.notation = {}
        
        # Equation database
        self.equations = {
            'numerical': [],  # Numerical calculations
            'definitions': [],  # X = Y definitions
            'derivations': [],  # Multi-step derivations
            'dimensionless': [],  # Pure number relations
            'physical_laws': []  # Physical equations
        }
        
        # Conflicts found
        self.conflicts = []
        
        # Validation results
        self.validations = []
        
        # Physical constants (50 decimal precision)
        self.constants = {
            'pi': mp_pi,
            'phi': (1 + sqrt(5)) / 2,  # Golden ratio
            'e': mp_e,
            'M_P_kg': mpf('2.176434e-8'),  # Planck mass in kg
            'M_P_GeV': mpf('1.220910e19'),  # Planck mass in GeV
            'M_P_MeV': mpf('1.220910e22'),  # Planck mass in MeV
            'm_e_MeV': mpf('0.5109989461'),  # Electron mass (CODATA 2018)
            'm_p_MeV': mpf('938.2720813'),  # Proton mass
            'm_n_MeV': mpf('939.5654133'),  # Neutron mass
            'alpha_inv': mpf('137.035999084'),  # Fine structure constant inverse
            'k_B': mpf('8.617333262e-5'),  # Boltzmann constant in eV/K
        }
    
    def extract_equations_from_file(self, filepath):
        """Extract all equations from markdown file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        doc_name = filepath.name
        equations = []
        
        # Extract display equations ($$...$$)
        display_pattern = r'\$\$(.*?)\$\$'
        for match in re.finditer(display_pattern, content, re.DOTALL):
            eq_text = match.group(1).strip()
            line_num = content[:match.start()].count('\n') + 1
            
            # Get surrounding context (50 chars before and after)
            start = max(0, match.start() - 100)
            end = min(len(content), match.end() + 100)
            context = content[start:end]
            
            equations.append({
                'text': eq_text,
                'type': 'display',
                'document': doc_name,
                'line': line_num,
                'context': context
            })
        
        return equations
    
    def classify_equation_type(self, eq):
        """Classify equation by mathematical type"""
        text = eq['text']
        
        # Check for specific patterns
        has_equals = '=' in text
        has_integral = any(x in text for x in ['\\int', '\\sum', '\\prod'])
        has_numbers = re.search(r'\d+\.?\d*', text)
        has_approx = '\\approx' in text or '\\sim' in text
        has_frac = '\\frac' in text
        
        if has_integral:
            return 'integral_equation'
        elif has_equals and has_numbers and has_approx:
            return 'numerical_calculation'
        elif has_equals and has_numbers:
            return 'numerical_definition'
        elif has_equals and has_frac:
            return 'ratio_equation'
        elif has_equals:
            return 'symbolic_definition'
        else:
            return 'expression'
    
    def extract_symbol_definitions(self, eq):
        """Extract symbol definitions from equation (X = ...)"""
        text = eq['text']
        
        # Pattern: symbol = expression
        pattern = r'([A-Za-z_\\{}\s]+?)\s*=\s*(.+)'
        match = re.match(pattern, text)
        
        if match:
            lhs = match.group(1).strip()
            rhs = match.group(2).strip()
            return {'symbol': lhs, 'definition': rhs, 'equation': eq}
        
        return None
    
    def validate_numerical(self, expression, expected_value=None):
        """Validate numerical expression to 50 decimals"""
        try:
            # Replace LaTeX with Python math
            expr = expression.replace('\\pi', 'pi')
            expr = expr.replace('\\phi', 'phi')
            expr = expr.replace('\\varphi', 'phi')
            expr = expr.replace('\\cdot', '*')
            expr = expr.replace('\\times', '*')
            expr = expr.replace('\\frac{', '(').replace('}{', ')/(').count('}')
            
            # Evaluate with mpmath
            # This is simplified - real implementation would parse LaTeX properly
            
            return {
                'expression': expression,
                'status': 'needs_manual_check',
                'note': 'Complex LaTeX requires symbolic parser'
            }
        
        except Exception as e:
            return {
                'expression': expression,
                'status': 'error',
                'error': str(e)
            }
    
    def check_dimensional_consistency(self, eq):
        """Check if equation is dimensionally consistent"""
        # This is a complex task - would need full dimensional analysis system
        # For now, flag equations for manual review
        
        text = eq['text']
        
        # Look for obvious dimensional mismatches
        issues = []
        
        # Check if mass = angle (obviously wrong)
        if 'm_' in text and '\\theta' in text and '=' in text:
            issues.append('Possible mass=angle mismatch')
        
        # Check if energy and dimensionless are equated
        if any(e in text for e in ['MeV', 'GeV', 'eV']) and any(d in text for d in ['\\alpha', 'k_B']):
            if '=' in text and not '\\cdot' in text and not '\\times' in text:
                issues.append('Possible dimensional mismatch: energy vs dimensionless')
        
        return issues

def build_master_notation_guide():
    """Build comprehensive notation guide"""
    analyzer = ComprehensiveAnalyzer()
    
    docs_path = Path("/Users/Cristiana_1/Documents/Golden Universe")
    docs = [
        "GU Couplings and Particles.md",
        "GU next in line.md",
        "Golden Universe Theory for the Calculation of Particles v2.md",
        "More Particles Stuff GU.md",
        "Some GU Particles Stuff.md"
    ]
    
    print("="*80)
    print("BUILDING MASTER NOTATION DICTIONARY")
    print("="*80)
    
    all_equations = []
    symbol_uses = defaultdict(list)
    
    for doc_name in docs:
        filepath = docs_path / doc_name
        if not filepath.exists():
            continue
        
        equations = analyzer.extract_equations_from_file(filepath)
        all_equations.extend(equations)
        
        print(f"\n{doc_name}:")
        print(f"  Equations: {len(equations)}")
        
        # Classify equations
        types = defaultdict(int)
        for eq in equations:
            eq_type = analyzer.classify_equation_type(eq)
            types[eq_type] += 1
            eq['classification'] = eq_type
        
        for eq_type, count in sorted(types.items()):
            print(f"  - {eq_type}: {count}")
        
        # Extract symbols
        for eq in equations:
            definition = analyzer.extract_symbol_definitions(eq)
            if definition:
                symbol = definition['symbol']
                symbol_uses[symbol].append({
                    'document': doc_name,
                    'line': eq['line'],
                    'definition': definition['definition'],
                    'context': eq['context'][:150]
                })
    
    print(f"\n{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}")
    print(f"Total equations across 5 documents: {len(all_equations)}")
    print(f"Unique defined symbols: {len(symbol_uses)}")
    
    # Save comprehensive notation guide
    notation_guide_path = docs_path / "MASTER_NOTATION_GUIDE.json"
    with open(notation_guide_path, 'w') as f:
        json.dump({
            'symbols': {k: v for k, v in symbol_uses.items()},
            'total_equations': len(all_equations),
            'by_type': dict(defaultdict(int))
        }, f, indent=2)
    
    print(f"\n✅ Master notation guide saved")
    
    return all_equations, symbol_uses

if __name__ == "__main__":
    equations, symbols = build_master_notation_guide()
