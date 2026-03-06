# Contributing to Golden Universe Theory

Thank you for your interest in contributing to the Golden Universe Theory project! This document provides guidelines for contributing to this revolutionary theoretical physics framework.

## 🌟 Project Vision

The Golden Universe Theory aims to:
- Derive particle masses and fundamental constants (including G_N) from first principles
- Achieve sub-percent precision with ZERO fitted parameters
- Provide open access to cutting-edge theoretical physics
- Enable reproducible research in fundamental physics
- Foster collaborative development of theoretical frameworks

## 🎯 How to Contribute

### Areas of Contribution

#### 1. **Theory Development**
- New particle derivations and extensions
- Gravity sector: c_R residual (0.26% gap), tensor-to-scalar ratio suppression, M₀ confirmation
- Seeley-DeWitt heat kernel: threshold corrections, non-minimal coupling effects
- Cosmological constant: understanding why Str(a₀) = 3 (not exactly 0)
- Theoretical refinements and corrections
- Mathematical framework improvements
- Novel applications of GU principles

#### 2. **Numerical Methods**
- NLDE solver improvements
- Optimization of winding number algorithms
- Performance enhancements
- Numerical stability improvements

#### 3. **Validation & Testing**
- Experimental data comparisons
- Precision validation
- Edge case testing
- Regression test development

#### 4. **Documentation**
- Tutorial creation
- Theory explanations
- Code documentation
- Example development

#### 5. **Analysis Tools**
- Visualization improvements
- Data analysis utilities
- Comparison frameworks
- Plotting and graphing tools

## 🚀 Getting Started

### 1. **Set Up Development Environment**

```bash
# Clone the repository
git clone https://github.com/your-username/golden-universe-theory.git
cd golden-universe-theory

# Install Python scientific computing libraries
pip install numpy scipy matplotlib mpmath sympy jupyter pandas

# Optional: Additional libraries for advanced analysis
pip install plotly seaborn tqdm
```

### 2. **Explore the Theory**
```bash
# Start with the core theory document
cat theory/theory-laws.md

# Run the gravity derivation (G_N from m_e, 47 ppm)
cd derivations/39_GRAVITY/
python 20_GRAVITY_FROM_FIRST_PRINCIPLES.py

# Run key derivation scripts
cd ../30_WINDING_NUMBERS/
python 02_corrected_winding_solver.py

cd ../31_QUARK_MASSES/
python 25_corrected_quark_derivations.py
```

### 3. **Validate Results**
```bash
# Check precision achievements
python -c "
import sys, os
sys.path.append('derivations')
# Run validation scripts in derivations folders
"
```

## 📋 Contribution Process

### 1. **Issue Creation**
Before starting work, create or find an existing issue:

- **Bug reports**: Describe the problem, expected behavior, and steps to reproduce
- **Feature requests**: Explain the proposed enhancement and its benefits
- **Theory discussions**: Propose theoretical improvements or corrections

### 2. **Development Workflow**

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "feat: add corrected resonance analysis for new particle"

# Push and create pull request
git push origin feature/your-feature-name
```

### 3. **Pull Request Guidelines**

#### **Title Format**
- `feat: add new particle derivation`
- `fix: correct winding number calculation`
- `docs: improve theory explanation`
- `test: add precision validation tests`

#### **Description Template**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Theory improvement
- [ ] Documentation update
- [ ] Performance improvement

## Theoretical Validation
- [ ] Mathematical derivation verified
- [ ] Precision benchmarks met
- [ ] Consistency with existing theory

## Testing
- [ ] Tests pass
- [ ] New tests added if needed
- [ ] Precision validation included

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Breaking changes documented
```

## 🧪 Testing Standards

### 1. **Theory Validation**
All theoretical contributions must include:
- Mathematical derivation verification
- Precision validation against experimental data
- Consistency checks with existing framework
- Edge case analysis

### 2. **Code Testing**
- **Unit tests**: Individual function validation
- **Integration tests**: Component interaction testing
- **Precision tests**: Numerical accuracy validation
- **Regression tests**: Preserve existing results

### 3. **Performance Testing**
- Benchmark critical algorithms
- Memory usage validation
- Scalability testing
- Optimization verification

## 📐 Theoretical Contribution Guidelines

### 1. **Mathematical Rigor**
- Provide complete derivations
- Include all assumptions and approximations
- Validate against known results
- Document precision achievements

### 2. **Consistency Requirements**
- Must be consistent with core GU principles
- Should not contradict existing validated results
- Must respect the corrected resonance framework
- Must respect the non-circular gravity derivation (G_N from m_e, not fitted)
- GU memory modes are classical backgrounds — do NOT include in Seeley-DeWitt DOF counting
- Should maintain sub-percent precision standards

### 3. **Documentation Standards**
- Include theoretical background
- Provide implementation details
- Add usage examples
- Document precision expectations

## 🎨 Code Style Guidelines

### 1. **Python Standards**
- Follow PEP 8 style guide
- Use type hints for all functions
- Include comprehensive docstrings
- Maintain consistent naming conventions

### 2. **Theoretical Code**
```python
def derive_particle_mass(
    particle_name: str,
    epoch: int,
    winding_numbers: Tuple[int, int],
    precision_corrections: bool = True
) -> Tuple[float, float]:
    """
    Derive particle mass using Golden Universe framework.
    
    Args:
        particle_name: Name of the particle
        epoch: Epoch number N
        winding_numbers: Topological charges (p, q)
        precision_corrections: Apply δC corrections for resonant particles
        
    Returns:
        Tuple of (predicted_mass_MeV, precision_error_percent)
        
    Raises:
        ValueError: If particle is not recognized
        TheoryError: If derivation fails consistency checks
    """
```

### 3. **Mathematical Constants**
```python
# Use canonical GU constants
PHI = (1 + sqrt(5)) / 2          # Golden ratio
PI = 3.141592653589793           # π (not φ-refined)
E = 2.718281828459045            # e (not φ-refined)
M_P = 1.22089e22                 # Planck mass (MeV)

# Forbidden: φ₁₁₁, π₁₁₁, e₁₁₁ (no epoch-refined constants)
```

## 🔬 Theoretical Review Process

### 1. **Peer Review**
All theoretical contributions undergo peer review:
- Mathematical accuracy verification
- Physical consistency validation
- Precision requirement compliance
- Integration with existing framework

### 2. **Review Criteria**
- **Correctness**: Mathematical and physical accuracy
- **Precision**: Sub-percent error achievement
- **Consistency**: Alignment with GU principles
- **Completeness**: Thorough derivation and validation

### 3. **Review Timeline**
- Initial review: 1-2 weeks
- Revision cycles: As needed
- Final approval: Core maintainer sign-off
- Integration: Merge after all checks pass

## 📚 Documentation Standards

### 1. **Theory Documentation**
- **Background**: Theoretical foundation
- **Derivation**: Step-by-step mathematical development
- **Implementation**: Code realization
- **Validation**: Precision and consistency checks
- **Examples**: Usage demonstrations

### 2. **Code Documentation**
- **Docstrings**: Comprehensive function documentation
- **Comments**: Explain complex theoretical concepts
- **Examples**: Demonstrate usage patterns
- **API docs**: Auto-generated reference material

### 3. **Tutorial Creation**
- **Beginner-friendly**: Accessible to newcomers
- **Progressive complexity**: Build understanding gradually
- **Working examples**: Complete, runnable code
- **Theoretical context**: Explain the physics

## 🏆 Recognition

### Contributor Recognition
- Contributors listed in project acknowledgments
- Significant contributions highlighted in releases
- Theoretical breakthroughs credited appropriately
- Academic citation guidelines provided

### Types of Contributions Recognized
- **Theoretical advances**: New derivations or improvements
- **Numerical innovations**: Algorithm improvements
- **Validation work**: Precision testing and verification
- **Documentation**: Educational and explanatory content
- **Community building**: Outreach and collaboration

## 🤝 Community Guidelines

### 1. **Code of Conduct**
- Be respectful and inclusive
- Focus on constructive feedback
- Encourage learning and collaboration
- Maintain professional communication

### 2. **Scientific Integrity**
- Ensure accuracy in theoretical work
- Acknowledge sources and inspirations
- Report errors honestly and promptly
- Maintain reproducibility standards

### 3. **Collaboration Principles**
- Share knowledge openly
- Help newcomers learn the framework
- Provide constructive code reviews
- Foster a supportive community

## 📞 Getting Help

### Resources
- **Documentation**: [docs/](./docs/)
- **Discussions**: [GitHub Discussions](./discussions)
- **Issues**: [GitHub Issues](./issues)
- **Theory Guide**: [Theory Overview](./docs/theory/)

### Contact
- **General questions**: Use GitHub Discussions
- **Bug reports**: Create GitHub Issues
- **Theoretical discussions**: Theory-specific discussion threads
- **Direct contact**: [maintainer-email@domain.com]

## 🎉 Thank You!

Your contributions help advance our understanding of fundamental physics and make cutting-edge theory accessible to the global community. Every contribution, whether theoretical, computational, or educational, helps build a better understanding of the universe's deepest principles.

**Welcome to the Golden Universe Theory community!** 🌟