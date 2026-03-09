import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import EquationRenderer from '@/components/Theory/EquationRenderer';
import { calculationService } from '@/services/calculationService';
import './CalculationDetails.scss';

interface CouplingConstantsCalculationProps {
  type: string;
}

const CouplingConstantsCalculation: React.FC<CouplingConstantsCalculationProps> = ({ type }) => {
  const [isCalculating, setIsCalculating] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const runCalculation = async () => {
    setIsCalculating(true);
    setError(null);
    try {
      const calculationResult = await calculationService.calculateCouplingConstants(type);
      setResult(calculationResult);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Calculation failed');
    } finally {
      setIsCalculating(false);
    }
  };

  const getTitle = () => {
    switch (type) {
      case 'alpha-s': return 'Strong Coupling Constant α_s';
      case 'alpha-w': return 'Weak Coupling Constant α_w';
      case 'coupling-constants': return 'All Coupling Constants';
      default: return 'Coupling Constants';
    }
  };

  return (
    <div className="calculation-details">
      <div className="calculation-header">
        <Link to="/calculations" className="back-button">
          ← Back to Calculations
        </Link>
        <h1>{getTitle()}</h1>
        <p className="subtitle">Fundamental force coupling strengths from Golden Universe theory</p>
      </div>

      <div className="calculation-content">
        {/* Theory Section */}
        <section className="theory-section">
          <h2>Theoretical Foundation</h2>
          <div className="theory-explanation">
            <p>
              The coupling constants determine the strength of fundamental interactions.
              In Golden Universe theory, they all emerge from a single underlying structure
              and unify at high energy.
            </p>

            <div className="key-laws">
              <h3>Key Laws Used:</h3>
              <ul>
                <li>
                  <Link to="/theory/law-10">Law 10: Coupling Constants</Link> - Unified origin
                </li>
                <li>
                  <Link to="/theory/law-6">Law 6: Force Unification</Link> - Grand unification
                </li>
              </ul>
            </div>
          </div>
        </section>

        {/* Mathematical Derivation */}
        <section className="derivation-section">
          <h2>Mathematical Derivation</h2>

          {(type === 'alpha-s' || type === 'coupling-constants') && (
            <div className="step">
              <h3>Strong Coupling α_s</h3>
              <p>At the Z boson mass scale:</p>
              <EquationRenderer equation="\alpha_s(M_Z) = 0.1179 \pm 0.0009" />
              <p>Running with energy scale Q:</p>
              <EquationRenderer equation="\alpha_s(Q) = \frac{12\pi}{(33-2n_f)\ln(Q^2/\Lambda_{QCD}^2)}" />
            </div>
          )}

          {(type === 'alpha-w' || type === 'coupling-constants') && (
            <div className="step">
              <h3>Weak Coupling α_w</h3>
              <p>Electroweak scale coupling:</p>
              <EquationRenderer equation="\alpha_w = \frac{g_w^2}{4\pi} \approx \frac{1}{30}" />
              <p>Related to Weinberg angle:</p>
              <EquationRenderer equation="\sin^2\theta_W = 0.23122" />
            </div>
          )}

          <div className="step">
            <h3>Unification Scale</h3>
            <p>All couplings converge at the GUT scale:</p>
            <EquationRenderer equation="\alpha_1 = \alpha_2 = \alpha_3 \text{ at } E \sim 10^{16} \text{ GeV}" />
          </div>
        </section>

        {/* Interactive Calculation */}
        <section className="calculation-section">
          <h2>Interactive Calculation</h2>
          <div className="calculation-controls">
            <button
              className="calculate-btn"
              onClick={runCalculation}
              disabled={isCalculating}
            >
              {isCalculating ? 'Calculating...' : 'Run Full Calculation'}
            </button>
          </div>

          {result && (
            <div className="calculation-result">
              <h3>Calculation Results:</h3>
              <div className="result-grid">
                <div className="result-item">
                  <span className="label">Value:</span>
                  <span className="value">{result.value}</span>
                </div>
                <div className="result-item">
                  <span className="label">Energy Scale:</span>
                  <span className="value">{result.scale}</span>
                </div>
                <div className="result-item">
                  <span className="label">Theory:</span>
                  <span className="value">{result.theory_value}</span>
                </div>
                <div className="result-item">
                  <span className="label">Experiment:</span>
                  <span className="value">{result.experimental_value}</span>
                </div>
              </div>
            </div>
          )}

          {error && (
            <div className="calculation-error">
              <p>Error: {error}</p>
            </div>
          )}
        </section>

        {/* Comparison Table */}
        {type === 'coupling-constants' && (
          <section className="comparison-section">
            <h2>All Coupling Constants</h2>
            <div className="comparison-table">
              <table>
                <thead>
                  <tr>
                    <th>Force</th>
                    <th>Coupling</th>
                    <th>Value</th>
                    <th>Energy Scale</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Electromagnetic</td>
                    <td>α</td>
                    <td>1/137.036</td>
                    <td>Low energy</td>
                  </tr>
                  <tr>
                    <td>Weak</td>
                    <td>α_w</td>
                    <td>1/30</td>
                    <td>M_W = 80.4 GeV</td>
                  </tr>
                  <tr>
                    <td>Strong</td>
                    <td>α_s</td>
                    <td>0.1179</td>
                    <td>M_Z = 91.2 GeV</td>
                  </tr>
                  <tr>
                    <td>Gravitational</td>
                    <td>α_G</td>
                    <td>~10⁻³⁸</td>
                    <td>Planck scale</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>
        )}

        {/* Related Calculations */}
        <section className="related-section">
          <h2>Related Calculations</h2>
          <div className="related-links">
            <Link to="/calculations/fine-structure" className="related-card">
              <h3>Fine Structure α</h3>
              <p>Electromagnetic coupling</p>
            </Link>
            {type !== 'alpha-s' && (
              <Link to="/calculations/alpha-s" className="related-card">
                <h3>Strong Coupling</h3>
                <p>QCD interaction strength</p>
              </Link>
            )}
            {type !== 'alpha-w' && (
              <Link to="/calculations/alpha-w" className="related-card">
                <h3>Weak Coupling</h3>
                <p>Weak force strength</p>
              </Link>
            )}
          </div>
        </section>
      </div>
    </div>
  );
};

export default CouplingConstantsCalculation;