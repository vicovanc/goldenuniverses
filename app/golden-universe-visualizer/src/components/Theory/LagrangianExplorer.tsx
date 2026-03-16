import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';
import { lagrangianTerms } from '@/data/theoryLaws';
import { LagrangianTerm } from '@/types/theory';

interface LagrangianExplorerProps {
  onNavigateToLaw?: (lawId: number) => void;
}

const LagrangianExplorer: React.FC<LagrangianExplorerProps> = ({ onNavigateToLaw }) => {
  const [expandedTerms, setExpandedTerms] = useState<Set<string>>(new Set());
  const [selectedTerm, setSelectedTerm] = useState<LagrangianTerm | null>(null);

  // Parameter calculation state (for interactive calculations)
  const [parameters, setParameters] = useState<{ [key: string]: number }>({
    X: 1.0,
    M_P: 1.22e19, // Planck mass in GeV
    phi: 1.618033988749895,
    pi: Math.PI,
    e: Math.E,
  });

  const toggleExpanded = (symbol: string) => {
    const newExpanded = new Set(expandedTerms);
    if (newExpanded.has(symbol)) {
      newExpanded.delete(symbol);
    } else {
      newExpanded.add(symbol);
    }
    setExpandedTerms(newExpanded);
  };

  const handleParameterChange = (param: string, value: number) => {
    setParameters({
      ...parameters,
      [param]: value,
    });
  };

  return (
    <div className="lagrangian-explorer">
      <div className="explorer-header">
        <h2>Lagrangian Structure Explorer</h2>
        <p className="explorer-description">
          The total Lagrangian L_M decomposes into six fundamental sectors, each with distinct physical roles in the
          Golden Universe theory.
        </p>
      </div>

      {/* Total Lagrangian */}
      <div className="total-lagrangian">
        <h3>Total Master Lagrangian</h3>
        <div className="equation-display">
          <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}>
            {`$$L_M = \\int d^4x \\, [L_{\\Omega} + L_X + L_{\\text{int}} + L_{\\text{gauge}}]$$`}
          </ReactMarkdown>
        </div>
        <p className="equation-note">
          The complete action integrates over all spacetime, incorporating substrate dynamics, cosmic driver evolution,
          interaction terms, and gauge fields.
        </p>

        <div className="lagrangian-breakdown">
          <h4>Complete Lagrangian Breakdown</h4>

          <div className="breakdown-section">
            <h5>L_Ω (Substrate)</h5>
            <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}>
              {`$$L_{\\Omega} = L_{\\Omega,\\text{kin}} - V_{\\text{full}\\Omega}(\\Omega, X) + L_{\\text{phase-driver}}(\\Omega, X) + L_{\\text{recursive-mimic}}(\\Omega, X)$$`}
            </ReactMarkdown>
            <p className="breakdown-description">
              Full kinetic terms + potential with X-dependent coefficients + phase-locking driver + recursive memory
            </p>
          </div>

          <div className="breakdown-section">
            <h5>L_X (Cosmic Driver)</h5>
            <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}>
              {`$$L_X = \\frac{1}{2}(\\partial_\\mu X)^2 - V_X(X)$$`}
            </ReactMarkdown>
            <p className="breakdown-description">
              Standard scalar field kinetic term minus self-potential
            </p>
          </div>

          <div className="breakdown-section">
            <h5>L_int (Interaction)</h5>
            <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}>
              {`$$L_{\\text{int}} = -g_{\\Omega X}(X) \\cdot S_{\\text{coupling}}(\\Omega) \\cdot X$$`}
            </ReactMarkdown>
            <p className="breakdown-description">
              Direct coupling between substrate and cosmic driver fields
            </p>
          </div>

          <div className="breakdown-section">
            <h5>L_gauge (Gauge Fields)</h5>
            <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}>
              {`$$L_{\\text{gauge}} = -\\frac{1}{4}\\sum_b F^b_{\\mu\\nu} F^{b\\mu\\nu}$$`}
            </ReactMarkdown>
            <p className="breakdown-description">
              Yang-Mills kinetic terms for G_prim gauge bosons
            </p>
          </div>

          <div className="breakdown-section specialized-term">
            <h5>L_lock (Angular Modulation)</h5>
            <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}>
              {`$$L_{\\text{lock}} = -\\kappa_p(X) \\cdot S_{\\text{phase}}(\\Omega) \\cdot (\\partial_t \\arg \\Omega + \\omega_{\\text{target}})^2$$`}
            </ReactMarkdown>
            <p className="breakdown-description">
              Phase-locking mechanism that drives angular oscillations to target frequency
            </p>
          </div>

          <div className="breakdown-section specialized-term">
            <h5>L_mem (Memory Energy)</h5>
            <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}>
              {`$$L_{\\text{mem}} = -\\lambda_{\\text{rec}}(X) \\cdot \\int d\\tau \\, G(t,\\tau) \\cdot H[\\Omega(\\tau)]$$`}
            </ReactMarkdown>
            <p className="breakdown-description">
              Non-local memory integral with exponential kernel G(t,τ) encoding field history
            </p>
          </div>
        </div>
      </div>

      {/* Lagrangian Terms */}
      <div className="lagrangian-terms">
        {lagrangianTerms.map((term) => {
          const isExpanded = expandedTerms.has(term.symbol);
          const isSelected = selectedTerm?.symbol === term.symbol;

          return (
            <div
              key={term.symbol}
              className={`lagrangian-term ${isExpanded ? 'expanded' : ''} ${isSelected ? 'selected' : ''}`}
            >
              <div className="term-header" onClick={() => toggleExpanded(term.symbol)}>
                <div className="term-symbol">
                  <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}>
                    {`$${term.symbol}$`}
                  </ReactMarkdown>
                </div>
                <div className="term-name-section">
                  <h4 className="term-name">{term.name}</h4>
                  <p className="term-description">{term.description}</p>
                </div>
                <button className="expand-button" aria-label={isExpanded ? 'Collapse' : 'Expand'}>
                  {isExpanded ? '−' : '+'}
                </button>
              </div>

              {isExpanded && (
                <div className="term-details">
                  <div className="term-equation">
                    <h5>Mathematical Form</h5>
                    <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}>
                      {`$$${term.equation}$$`}
                    </ReactMarkdown>
                  </div>

                  {term.components && term.components.length > 0 && (
                    <div className="term-components">
                      <h5>Components</h5>
                      {term.components.map((component, index) => (
                        <div key={index} className="component-item">
                          <h6>{component.name}</h6>
                          <p className="component-description">{component.description}</p>
                          <div className="component-equation">
                            <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}>
                              {`$$${component.equation}$$`}
                            </ReactMarkdown>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  {term.relatedLaws && term.relatedLaws.length > 0 && (
                    <div className="term-related-laws">
                      <h5>Related Laws</h5>
                      <div className="related-laws-list">
                        {term.relatedLaws.map((lawId) => (
                          <button
                            key={lawId}
                            className="law-link-button"
                            onClick={() => onNavigateToLaw?.(lawId)}
                            aria-label={`Navigate to Law ${lawId}`}
                          >
                            Law {lawId}
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  <button className="select-term-button" onClick={() => setSelectedTerm(term)}>
                    View Implementation Details
                  </button>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Parameter Calculator */}
      <div className="parameter-calculator">
        <h3>Parameter Calculator</h3>
        <p className="calculator-description">
          Adjust parameters to explore how different values affect the Lagrangian terms.
        </p>

        <div className="parameter-inputs">
          <div className="parameter-group">
            <label htmlFor="param-X">
              Cosmic Driver X:
              <input
                id="param-X"
                type="number"
                value={parameters.X}
                onChange={(e) => handleParameterChange('X', parseFloat(e.target.value))}
                step="0.1"
              />
            </label>
          </div>

          <div className="parameter-group">
            <label htmlFor="param-M_P">
              Planck Mass M_P (GeV):
              <input
                id="param-M_P"
                type="number"
                value={parameters.M_P}
                onChange={(e) => handleParameterChange('M_P', parseFloat(e.target.value))}
                step="1e18"
              />
            </label>
          </div>

          <div className="parameter-group">
            <label htmlFor="param-phi">
              Golden Ratio φ:
              <input
                id="param-phi"
                type="number"
                value={parameters.phi}
                onChange={(e) => handleParameterChange('phi', parseFloat(e.target.value))}
                step="0.000001"
                readOnly
              />
            </label>
          </div>

          <div className="parameter-group">
            <label htmlFor="param-pi">
              π:
              <input
                id="param-pi"
                type="number"
                value={parameters.pi}
                onChange={(e) => handleParameterChange('pi', parseFloat(e.target.value))}
                step="0.000001"
                readOnly
              />
            </label>
          </div>
        </div>

        <div className="calculation-results">
          <h4>Derived Values</h4>
          <div className="result-item">
            <span className="result-label">X-dependent mass scale:</span>
            <span className="result-value">
              {(parameters.M_P * parameters.X).toExponential(3)} GeV<sup>2</sup>
            </span>
          </div>
          <div className="result-item">
            <span className="result-label">φ-scaled coupling:</span>
            <span className="result-value">{(Math.exp(parameters.phi) / (parameters.pi * parameters.pi)).toFixed(6)}</span>
          </div>
          <div className="result-item">
            <span className="result-label">Golden angle (2π/φ²):</span>
            <span className="result-value">
              {((2 * parameters.pi) / (parameters.phi * parameters.phi)).toFixed(6)} rad ≈ 137.5°
            </span>
          </div>
        </div>
      </div>

      {/* Python Implementation Links */}
      <div className="implementation-links">
        <h3>Python Implementation</h3>
        <p>Explore computational implementations of these Lagrangian terms:</p>
        <div className="links-list">
          <a href="#" className="implementation-link">
            lagrangian_omega.py - L_Ω substrate dynamics
          </a>
          <a href="#" className="implementation-link">
            cosmic_driver.py - L_X cosmic driver evolution
          </a>
          <a href="#" className="implementation-link">
            phase_driver.py - Phase-locking mechanism
          </a>
          <a href="#" className="implementation-link">
            memory_integral.py - Recursive memory calculations
          </a>
        </div>
      </div>

      {/* Selected Term Detail Modal */}
      {selectedTerm && (
        <div className="term-detail-modal" onClick={() => setSelectedTerm(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={() => setSelectedTerm(null)} aria-label="Close">
              ×
            </button>
            <h3>
              {selectedTerm.symbol}: {selectedTerm.name}
            </h3>
            <div className="modal-equation">
              <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}>
                {`$$${selectedTerm.equation}$$`}
              </ReactMarkdown>
            </div>
            <p className="modal-description">{selectedTerm.description}</p>

            <div className="modal-implementation">
              <h4>Implementation Notes</h4>
              <p>
                This term can be numerically evaluated using the Python calculation engine. See the related laws for
                theoretical foundations and the implementation files for computational methods.
              </p>
            </div>

            {selectedTerm.relatedLaws && selectedTerm.relatedLaws.length > 0 && (
              <div className="modal-laws">
                <h4>Theoretical Foundation</h4>
                <div className="modal-laws-grid">
                  {selectedTerm.relatedLaws.map((lawId) => (
                    <button
                      key={lawId}
                      className="modal-law-button"
                      onClick={() => {
                        setSelectedTerm(null);
                        onNavigateToLaw?.(lawId);
                      }}
                    >
                      Go to Law {lawId}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default LagrangianExplorer;
