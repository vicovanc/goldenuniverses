#!/usr/bin/env python3
"""
Comprehensive Equation Analysis for Golden Universe Theory
Extracts, classifies, and validates all equations across documents
"""

import re
import os
from pathlib import Path
from collections import defaultdict
from decimal import Decimal, getcontext
import math

# Set precision to 50 decimal places
getcontext().prec = 50

class EquationAnalyzer:
    def __init__(self):
        self.equations = []
        self.notation = defaultdict(list)  # symbol -> [(context, units, document, line)]
        self.conflicts = []
        self.numerical_checks = []
        
    def extract_equations(self, filepath):
        """Extract all equations from a markdown file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
        
        doc_name = os.path.basename(filepath)
        equations_found = []
        
        # Extract display equations ($$...$$)
        display_pattern = r'\$\$(.*?)\$\$'
        for match in re.finditer(display_pattern, content, re.DOTALL):
            eq_text = match.group(1).strip()
            # Find line number
            line_num = content[:match.start()].count('\n') + 1
            equations_found.append({
                'type': 'display',
                'text': eq_text,
                'document': doc_name,
                'line': line_num,
                'raw': match.group(0)
            })
        
        # Extract inline equations ($...$)
        inline_pattern = r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)'
        for match in re.finditer(inline_pattern, content):
            eq_text = match.group(1).strip()
            line_num = content[:match.start()].count('\n') + 1
            # Skip if too short (likely just a variable)
            if len(eq_text) > 2:
                equations_found.append({
                    'type': 'inline',
                    'text': eq_text,
                    'document': doc_name,
                    'line': line_num,
                    'raw': match.group(0)
                })
        
        return equations_found
    
    def classify_equation(self, eq):
        """Classify equation by type"""
        text = eq['text']
        
        # Check for different types
        if '=' in text:
            if any(op in text for op in ['\\int', '\\sum', '\\prod']):
                return 'integral/sum'
            elif '\\frac' in text or '/' in text:
                return 'ratio/fraction'
            elif any(num in text for num in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
                return 'numerical'
            else:
                return 'definition'
        elif '\\approx' in text or '\\sim' in text:
            return 'approximation'
        elif '>' in text or '<' in text or '\\geq' in text or '\\leq' in text:
            return 'inequality'
        else:
            return 'expression'
    
    def extract_symbols(self, eq_text):
        """Extract mathematical symbols from equation"""
        # Common physics symbols
        symbols = []
        
        # Greek letters
        greek = r'\\(alpha|beta|gamma|delta|epsilon|zeta|eta|theta|iota|kappa|lambda|mu|nu|xi|pi|rho|sigma|tau|upsilon|phi|chi|psi|omega|Omega|Phi|Pi|Sigma)'
        for match in re.finditer(greek, eq_text):
            symbols.append(match.group(0))
        
        # Subscripted variables (e.g., M_P, k_B)
        subscript = r'([A-Za-z])_\{?([A-Za-z0-9]+)\}?'
        for match in re.finditer(subscript, eq_text):
            symbols.append(match.group(0))
        
        # Simple variables
        simple = r'\b([A-Z][a-z]?|[a-z])\b'
        for match in re.finditer(simple, eq_text):
            if match.group(0) not in ['e', 'i', 'ln', 'sin', 'cos', 'tan', 'log']:
                symbols.append(match.group(0))
        
        return list(set(symbols))
    
    def check_numerical_value(self, expression, expected=None):
        """Validate numerical calculation to 50 decimal places"""
        try:
            # This is a placeholder - would need actual symbolic math
            # For now, just flag for manual check
            return {
                'expression': expression,
                'needs_validation': True,
                'expected': expected
            }
        except:
            return {
                'expression': expression,
                'error': 'Cannot evaluate',
                'expected': expected
            }

def analyze_document(filepath):
    """Analyze a single document"""
    analyzer = EquationAnalyzer()
    
    print(f"\n{'='*80}")
    print(f"ANALYZING: {os.path.basename(filepath)}")
    print(f"{'='*80}\n")
    
    equations = analyzer.extract_equations(filepath)
    
    print(f"Total equations found: {len(equations)}")
    print(f"  - Display equations ($$...$$): {sum(1 for e in equations if e['type'] == 'display')}")
    print(f"  - Inline equations ($...$): {sum(1 for e in equations if e['type'] == 'inline')}")
    
    # Classify equations
    classifications = defaultdict(list)
    for eq in equations:
        class_type = analyzer.classify_equation(eq)
        classifications[class_type].append(eq)
    
    print(f"\nEquation Types:")
    for eq_type, eqs in sorted(classifications.items()):
        print(f"  - {eq_type}: {len(eqs)}")
    
    # Extract unique symbols
    all_symbols = set()
    for eq in equations:
        symbols = analyzer.extract_symbols(eq['text'])
        all_symbols.update(symbols)
    
    print(f"\nUnique symbols found: {len(all_symbols)}")
    
    return {
        'document': filepath,
        'equations': equations,
        'classifications': classifications,
        'symbols': all_symbols,
        'analyzer': analyzer
    }

def main():
    """Main analysis function"""
    # Get all markdown documents
    docs_path = Path("/Users/Cristiana_1/Documents/Golden Universe")
    md_files = [
        "GU Couplings and Particles.md",
        "GU next in line.md",
        "Golden Universe Theory for the Calculation of Particles v2.md",
        "More Particles Stuff GU.md",
        "Some GU Particles Stuff.md",
        "The Golden Universe Formation.md",
        "The Golden Universe- A Theory of Emergent Reality from Geometric First Principles - V2.md"
    ]
    
    all_results = []
    
    for md_file in md_files:
        filepath = docs_path / md_file
        if filepath.exists():
            result = analyze_document(filepath)
            all_results.append(result)
    
    # Cross-document analysis
    print(f"\n{'='*80}")
    print("CROSS-DOCUMENT ANALYSIS")
    print(f"{'='*80}\n")
    
    # Build master notation dictionary
    notation_dict = defaultdict(list)
    for result in all_results:
        for symbol in result['symbols']:
            notation_dict[symbol].append(result['document'].name)
    
    print(f"Total unique symbols across all documents: {len(notation_dict)}")
    
    # Find symbols used in multiple documents
    multi_doc_symbols = {k: v for k, v in notation_dict.items() if len(set(v)) > 1}
    print(f"Symbols appearing in multiple documents: {len(multi_doc_symbols)}")
    
    return all_results, notation_dict

if __name__ == "__main__":
    results, notation = main()
    
    print("\n" + "="*80)
    print("Analysis complete! Results stored in memory.")
    print("="*80)
