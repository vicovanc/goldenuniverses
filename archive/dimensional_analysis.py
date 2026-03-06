#!/usr/bin/env python3
"""
Comprehensive Dimensional Analysis of Golden Universe Theory
Checks every equation for dimensional consistency
"""

import re
import json
from collections import defaultdict

class DimensionalAnalyzer:
    def __init__(self):
        # Define dimensional units for common symbols
        # Format: symbol -> (name, dimensions as [M, L, T, Θ, Q])
        # M=mass, L=length, T=time, Θ=temperature/energy, Q=charge
        
        self.symbol_dimensions = {
            # Fundamental constants
            'M_P': ('Planck mass', [1, 0, 0, 0, 0]),
            'm_e': ('electron mass', [1, 0, 0, 0, 0]),
            'm_p': ('proton mass', [1, 0, 0, 0, 0]),
            'm_n': ('neutron mass', [1, 0, 0, 0, 0]),
            'm_{\\mu}': ('muon mass', [1, 0, 0, 0, 0]),
            'm_{\\tau}': ('tau mass', [1, 0, 0, 0, 0]),
            'm_W': ('W boson mass', [1, 0, 0, 0, 0]),
            'm_Z': ('Z boson mass', [1, 0, 0, 0, 0]),
            'm_H': ('Higgs mass', [1, 0, 0, 0, 0]),
            
            'c': ('speed of light', [0, 1, -1, 0, 0]),
            'G': ('gravitational constant', [-1, 3, -2, 0, 0]),
            '\\hbar': ('reduced Planck constant', [1, 2, -1, 0, 0]),
            'k_B': ('Boltzmann constant', [1, 2, -2, -1, 0]),
            
            # Dimensionless constants
            '\\pi': ('pi', [0, 0, 0, 0, 0]),
            '\\phi': ('golden ratio', [0, 0, 0, 0, 0]),
            '\\varphi': ('golden ratio', [0, 0, 0, 0, 0]),
            '\\alpha': ('fine structure constant', [0, 0, 0, 0, 0]),
            'e': ('Euler number', [0, 0, 0, 0, 0]),
            
            # Angles/phases (dimensionless in natural units)
            '\\theta': ('angle', [0, 0, 0, 0, 0]),
            '\\phi': ('phase angle', [0, 0, 0, 0, 0]),
            
            # Energies (mass in natural units where c=1)
            'E': ('energy', [1, 0, 0, 0, 0]),
            'T': ('temperature/energy', [1, 0, 0, 0, 0]),
            
            # Entropy (dimensionless when divided by k_B)
            'S': ('entropy', [1, 2, -2, -1, 0]),  # Full dimensions
            'S/k_B': ('dimensionless entropy', [0, 0, 0, 0, 0]),
            
            # Epochs/integers
            'n': ('epoch number', [0, 0, 0, 0, 0]),
            'N': ('integer', [0, 0, 0, 0, 0]),
            'N_e': ('electron epoch', [0, 0, 0, 0, 0]),
            'k': ('resonance number', [0, 0, 0, 0, 0]),
            
            # Couplings (Yukawa couplings are dimensionless)
            'y_e': ('electron Yukawa coupling', [0, 0, 0, 0, 0]),
            'y_{\\mu}': ('muon Yukawa coupling', [0, 0, 0, 0, 0]),
            'y_{\\tau}': ('tau Yukawa coupling', [0, 0, 0, 0, 0]),
            
            # Structural factors (dimensionless)
            'S_e': ('electron structural factor', [0, 0, 0, 0, 0]),
            'S_{\\mu}': ('muon structural factor', [0, 0, 0, 0, 0]),
            'S_{\\tau}': ('tau structural factor', [0, 0, 0, 0, 0]),
        }
        
        self.conflicts = []
        self.warnings = []
        self.issues_by_document = defaultdict(list)
    
    def get_dimensions(self, symbol):
        """Get dimensional analysis for a symbol"""
        # Clean symbol
        symbol = symbol.strip()
        
        # Check direct match
        if symbol in self.symbol_dimensions:
            return self.symbol_dimensions[symbol]
        
        # Check for mass pattern
        if symbol.startswith('m_') or symbol.startswith('m_{'):
            return ('mass', [1, 0, 0, 0, 0])
        
        # Check for angle pattern
        if 'theta' in symbol.lower() or 'phi' in symbol.lower():
            return ('angle', [0, 0, 0, 0, 0])
        
        # Check for integer pattern
        if symbol in ['n', 'N', 'k'] or symbol.startswith('N_'):
            return ('integer', [0, 0, 0, 0, 0])
        
        # Check for coupling pattern
        if symbol.startswith('y_') or symbol.startswith('y_{'):
            return ('coupling', [0, 0, 0, 0, 0])
        
        # Unknown
        return ('unknown', None)
    
    def check_equation_dimensions(self, eq):
        """Check if an equation is dimensionally consistent"""
        text = eq['text']
        
        # Only check equations with = sign
        if '=' not in text:
            return None
        
        # Split on =
        parts = text.split('=')
        if len(parts) != 2:
            return None  # Multiple equals or complex equation
        
        lhs, rhs = parts
        
        # Extract main symbols
        lhs_symbol = self.extract_main_symbol(lhs)
        rhs_components = self.extract_expression_components(rhs)
        
        if not lhs_symbol:
            return None
        
        lhs_dims = self.get_dimensions(lhs_symbol)
        
        issues = []
        
        # Check for obvious dimensional mismatches
        # 1. Mass = angle?
        if lhs_dims[0] == 'mass' and any('angle' in str(comp) for comp in rhs_components):
            if not any(dim in rhs for dim in ['\\cdot', '\\times', '*']):
                issues.append({
                    'type': 'dimensional_mismatch',
                    'issue': 'Mass = angle?',
                    'lhs': lhs_symbol,
                    'rhs': rhs,
                    'severity': 'HIGH'
                })
        
        # 2. Energy with no mass on RHS?
        if 'MeV' in lhs or 'GeV' in lhs or 'eV' in lhs:
            has_mass = any(m in rhs for m in ['M_P', 'm_e', 'm_p', 'm_n', 'm_\\mu', 'm_\\tau'])
            has_energy_unit = any(e in rhs for e in ['MeV', 'GeV', 'eV'])
            if not has_mass and not has_energy_unit and 'approx' not in rhs:
                issues.append({
                    'type': 'dimensional_check',
                    'issue': 'Energy value but no mass/energy on RHS',
                    'lhs': lhs,
                    'rhs': rhs,
                    'severity': 'MEDIUM'
                })
        
        # 3. Dimensionless = dimensional?
        if lhs_dims[1] and lhs_dims[1] == [0,0,0,0,0]:  # dimensionless
            if any(m in rhs for m in ['M_P', 'm_e', 'MeV', 'GeV']):
                if '/' not in rhs:  # No ratio
                    issues.append({
                        'type': 'dimensional_mismatch',
                        'issue': 'Dimensionless = dimensional quantity',
                        'lhs': lhs_symbol,
                        'rhs': rhs,
                        'severity': 'HIGH'
                    })
        
        return issues
    
    def extract_main_symbol(self, expression):
        """Extract the main symbol from LHS"""
        expression = expression.strip()
        
        # Remove subscripts, superscripts for now
        # Just get first meaningful symbol
        match = re.search(r'([A-Za-z_\\]+[\{\}A-Za-z0-9]*)', expression)
        if match:
            return match.group(1)
        return None
    
    def extract_expression_components(self, expression):
        """Extract components from RHS expression"""
        # Find all symbols
        components = []
        for match in re.finditer(r'([A-Za-z_\\]+[\{\}A-Za-z0-9]*)', expression):
            symbol = match.group(1)
            dims = self.get_dimensions(symbol)
            components.append((symbol, dims))
        return components
    
    def analyze_documents(self):
        """Analyze all documents for dimensional consistency"""
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
        print("DIMENSIONAL ANALYSIS")
        print("="*80)
        
        total_equations = 0
        total_issues = 0
        
        for doc_name in docs:
            filepath = docs_path / doc_name
            if not filepath.exists():
                continue
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract equations
            display_pattern = r'\$\$(.*?)\$\$'
            equations = []
            for match in re.finditer(display_pattern, content, re.DOTALL):
                eq_text = match.group(1).strip()
                line_num = content[:match.start()].count('\n') + 1
                equations.append({
                    'text': eq_text,
                    'document': doc_name,
                    'line': line_num
                })
            
            total_equations += len(equations)
            
            # Check dimensions
            doc_issues = []
            for eq in equations:
                issues = self.check_equation_dimensions(eq)
                if issues:
                    for issue in issues:
                        issue['document'] = doc_name
                        issue['line'] = eq['line']
                        issue['full_equation'] = eq['text']
                        doc_issues.append(issue)
                        total_issues += 1
            
            if doc_issues:
                self.issues_by_document[doc_name] = doc_issues
                print(f"\n{doc_name}:")
                print(f"  Equations: {len(equations)}")
                print(f"  Dimensional issues found: {len(doc_issues)}")
        
        print(f"\n{'='*80}")
        print(f"Total equations analyzed: {total_equations}")
        print(f"Total potential dimensional issues: {total_issues}")
        print(f"{'='*80}")
        
        return total_issues
    
    def generate_report(self):
        """Generate dimensional analysis report"""
        report_path = "/Users/Cristiana_1/Documents/Golden Universe/DIMENSIONAL_ANALYSIS_REPORT.json"
        
        with open(report_path, 'w') as f:
            json.dump({
                'symbol_dimensions': {k: {'name': v[0], 'dimensions': v[1]} 
                                     for k, v in self.symbol_dimensions.items()},
                'issues_by_document': dict(self.issues_by_document),
                'summary': {
                    'total_documents': len(self.issues_by_document),
                    'total_issues': sum(len(issues) for issues in self.issues_by_document.values())
                }
            }, f, indent=2)
        
        print(f"\n✅ Dimensional analysis report saved to: DIMENSIONAL_ANALYSIS_REPORT.json")

if __name__ == "__main__":
    analyzer = DimensionalAnalyzer()
    issues = analyzer.analyze_documents()
    analyzer.generate_report()
    
    # Print detailed issues
    if analyzer.issues_by_document:
        print("\n" + "="*80)
        print("DETAILED DIMENSIONAL ISSUES")
        print("="*80)
        
        for doc, issues in analyzer.issues_by_document.items():
            print(f"\n📄 {doc}:")
            for i, issue in enumerate(issues[:10], 1):  # First 10 per document
                print(f"\n  {i}. Line {issue['line']} - {issue['severity']} PRIORITY")
                print(f"     Issue: {issue['issue']}")
                print(f"     LHS: {issue['lhs']}")
                print(f"     RHS: {issue['rhs'][:80]}...")
