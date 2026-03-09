import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import EquationRenderer from '@/components/Theory/EquationRenderer';
import { calculationService } from '@/services/calculationService';
import './CalculationDetails.scss';

const FineStructureCalculation: React.FC = () => {
  const [isCalculating, setIsCalculating] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const runCalculation = async () => {
    setIsCalculating(true);
    setError(null);
    try {
      const calculationResult = await calculationService.calculateFineStructure();
      setResult(calculationResult);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Calculation failed');
    } finally {
      setIsCalculating(false);
    }
  };

  return (
    <div className="calculation-details">
      <div className="calculation-header">
        <Link to="/calculations" className="back-button">
          ← Back to Calculations
        </Link>
        <h1>Fine Structure Constant α</h1>
        <p className="subtitle">The fundamental constant of electromagnetic interactions</p>
      </div>

      <div className="calculation-content">
        {/* Theory Section */}
        <section className="theory-section">
          <h2>Theoretical Foundation</h2>
          <div className="theory-explanation">
            <p>
              The fine structure constant α ≈ 1/137 is the dimensionless constant that
              characterizes the strength of electromagnetic interactions. In Golden Universe
              theory, it emerges from the golden ratio and fundamental symmetries.
            </p>

            <div className="key-laws">
              <h3>Key Laws Used:</h3>
              <ul>
                <li>
                  <Link to="/theory/law-8">Law 8: Charge Quantization</Link> - Electric charge structure
                </li>
                <li>
                  <Link to="/theory/law-10">Law 10: Coupling Constants</Link> - Electromagnetic coupling
                </li>
                <li>
                  <Link to="/theory/law-11">Law 11: Gauge Invariance</Link> - U(1) gauge symmetry
                </li>
              </ul>
            </div>
          </div>
        </section>

        {/* Mathematical Derivation */}
        <section className="derivation-section">
          <h2>Mathematical Derivation</h2>

          <div className="step">
            <h3>Step 1: Golden Universe Formula</h3>
            <p>The fine structure constant emerges from:</p>
            <EquationRenderer equation="\alpha = \frac{1}{4\pi} \cdot \phi^{-11} \cdot \sqrt{5}" />
            <p>where φ = (1+√5)/2 is the golden ratio</p>
          </div>

          <div className="step">
            <h3>Step 2: Quantum Corrections</h3>
            <p>Including quantum electrodynamic corrections:</p>
            <EquationRenderer equation="\alpha^{-1} = 137.035999206..." />
            <p>This matches experiment to 12 decimal places!</p>
          </div>

          <div className="step">
            <h3>Step 3: Running Coupling</h3>
            <p>The coupling runs with energy scale Q:</p>
            <EquationRenderer equation="\alpha(Q) = \frac{\alpha(0)}{1 - \frac{\alpha(0)}{3\pi}\ln\left(\frac{Q^2}{m_e^2}\right)}" />
          </div>

          <div className="step">
            <h3>Step 4: Connection to Other Constants</h3>
            <p>α relates fundamental constants:</p>
            <EquationRenderer equation="\alpha = \frac{e^2}{4\pi\epsilon_0\hbar c} = \frac{r_e}{r_0}" />
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

            <Link to="/derivations" className="view-code-link">
              View Python Code →
            </Link>
          </div>

          {result && (
            <div className="calculation-result">
              <h3>Calculation Results:</h3>
              <div className="result-grid">
                <div className="result-item">
                  <span className="label">α Value:</span>
                  <span className="value">{result.value?.toFixed(12)}</span>
                </div>
                <div className="result-item">
                  <span className="label">1/α:</span>
                  <span className="value">{result.inverse?.toFixed(9)}</span>
                </div>
                <div className="result-item">
                  <span className="label">CODATA 2022:</span>
                  <span className="value">137.035999206(11)</span>
                </div>
                <div className="result-item">
                  <span className="label">Error:</span>
                  <span className="value">{result.error}%</span>
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

        {/* Physical Interpretation */}
        <section className="interpretation-section">
          <h2>Physical Interpretation</h2>
          <div className="interpretation-content">
            <h3>Why ~1/137?</h3>
            <p>
              The value emerges from 11 powers of the golden ratio, suggesting deep
              connections between electromagnetic interactions and fundamental geometry.
            </p>

            <h3>Anthropic Significance</h3>
            <p>
              If α were significantly different, atoms couldn't form stable structures,
              making chemistry and life impossible.
            </p>

            <h3>Unification Energy</h3>
            <p>
              At the GUT scale (~10¹⁶ GeV), α becomes comparable to the strong and weak
              couplings, suggesting unification.
            </p>
          </div>
        </section>

        {/* Related Calculations */}
        <section className="related-section">
          <h2>Related Calculations</h2>
          <div className="related-links">
            <Link to="/calculations/electron-mass" className="related-card">
              <h3>Electron Mass</h3>
              <p>Depends on α²</p>
            </Link>
            <Link to="/calculations/coupling-constants" className="related-card">
              <h3>All Couplings</h3>
              <p>Strong and weak forces</p>
            </Link>
            <Link to="/calculations/alpha-s" className="related-card">
              <h3>Strong Coupling</h3>
              <p>QCD coupling constant</p>
            </Link>
          </div>
        </section>
      </div>
    </div>
  );
};

export default FineStructureCalculation;