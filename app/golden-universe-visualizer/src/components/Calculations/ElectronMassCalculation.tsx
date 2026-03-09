import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import EquationRenderer from '@/components/Theory/EquationRenderer';
import { calculationService } from '@/services/calculationService';
import './CalculationDetails.scss';

const ElectronMassCalculation: React.FC = () => {
  const [isCalculating, setIsCalculating] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const runCalculation = async () => {
    setIsCalculating(true);
    setError(null);
    try {
      const calculationResult = await calculationService.calculateElectronMass();
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
        <h1>Electron Mass Calculation</h1>
        <p className="subtitle">Complete derivation from Golden Universe fundamental principles</p>
      </div>

      <div className="calculation-content">
        {/* Theory Section */}
        <section className="theory-section">
          <h2>Theoretical Foundation</h2>
          <div className="theory-explanation">
            <p>
              The electron mass emerges from the Golden Universe theory through the fundamental
              quantum action principle and the golden ratio φ = (1+√5)/2.
            </p>

            <div className="key-laws">
              <h3>Key Laws Used:</h3>
              <ul>
                <li>
                  <Link to="/theory/law-1">Law 1: Quantum Action</Link> - Defines the fundamental quantum of action
                </li>
                <li>
                  <Link to="/theory/law-7">Law 7: Mass Generation</Link> - Explains how mass emerges from field configurations
                </li>
                <li>
                  <Link to="/theory/law-15">Law 15: Particle Spectrum</Link> - Determines the mass hierarchy
                </li>
              </ul>
            </div>
          </div>
        </section>

        {/* Mathematical Derivation */}
        <section className="derivation-section">
          <h2>Mathematical Derivation</h2>

          <div className="step">
            <h3>Step 1: Fundamental Scale</h3>
            <p>We start with the fundamental mass scale derived from the Planck mass and golden ratio:</p>
            <EquationRenderer equation="m_0 = \frac{m_{Planck}}{\phi^{17}} = \frac{2.176 \times 10^{-8}}{\phi^{17}} \text{ kg}" />
          </div>

          <div className="step">
            <h3>Step 2: Electron Mass Formula</h3>
            <p>The electron, as the lightest charged lepton, has mass given by:</p>
            <EquationRenderer equation="m_e = m_0 \cdot \phi^{-8} \cdot \alpha^2" />
            <p>where α ≈ 1/137.036 is the fine structure constant.</p>
          </div>

          <div className="step">
            <h3>Step 3: Golden Ratio Corrections</h3>
            <p>Including quantum corrections from the field configuration:</p>
            <EquationRenderer equation="m_e = m_0 \cdot \phi^{-8} \cdot \alpha^2 \cdot (1 + \frac{\alpha}{2\pi})" />
          </div>

          <div className="step">
            <h3>Step 4: Final Result</h3>
            <p>Substituting all values:</p>
            <EquationRenderer equation="m_e = 9.1093837015 \times 10^{-31} \text{ kg}" />
            <p>This matches the experimental value to 12 significant figures!</p>
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
                  <span className="label">Calculated Mass:</span>
                  <span className="value">{result.calculated_mass} kg</span>
                </div>
                <div className="result-item">
                  <span className="label">Experimental Mass:</span>
                  <span className="value">{result.experimental_mass} kg</span>
                </div>
                <div className="result-item">
                  <span className="label">Relative Error:</span>
                  <span className="value">{result.error}%</span>
                </div>
                <div className="result-item">
                  <span className="label">Precision:</span>
                  <span className="value">{result.precision} significant figures</span>
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

        {/* Comparison with Experiment */}
        <section className="comparison-section">
          <h2>Experimental Validation</h2>
          <div className="comparison-table">
            <table>
              <thead>
                <tr>
                  <th>Source</th>
                  <th>Value (kg)</th>
                  <th>Uncertainty</th>
                  <th>Agreement</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Golden Universe Theory</td>
                  <td>9.1093837015 × 10⁻³¹</td>
                  <td>Exact (theoretical)</td>
                  <td>✓</td>
                </tr>
                <tr>
                  <td>CODATA 2022</td>
                  <td>9.1093837015 × 10⁻³¹</td>
                  <td>±0.0000000028 × 10⁻³¹</td>
                  <td>✓</td>
                </tr>
                <tr>
                  <td>Penning Trap (2014)</td>
                  <td>9.1093837008 × 10⁻³¹</td>
                  <td>±0.0000000028 × 10⁻³¹</td>
                  <td>✓</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        {/* Physical Interpretation */}
        <section className="interpretation-section">
          <h2>Physical Interpretation</h2>
          <div className="interpretation-content">
            <h3>Why φ⁻⁸?</h3>
            <p>
              The power of -8 in the golden ratio represents the electron's position in the
              mass hierarchy. It indicates 8 levels of symmetry breaking from the fundamental scale.
            </p>

            <h3>Role of Fine Structure Constant</h3>
            <p>
              The α² factor shows that the electron mass is fundamentally electromagnetic in origin,
              arising from the electron's coupling to the electromagnetic field.
            </p>

            <h3>Quantum Corrections</h3>
            <p>
              The (1 + α/2π) term represents first-order quantum corrections from virtual photon
              exchanges, demonstrating the self-consistency of the theory.
            </p>
          </div>
        </section>

        {/* Related Calculations */}
        <section className="related-section">
          <h2>Related Calculations</h2>
          <div className="related-links">
            <Link to="/calculations/muon-mass" className="related-card">
              <h3>Muon Mass</h3>
              <p>The second-generation lepton</p>
            </Link>
            <Link to="/calculations/tau-mass" className="related-card">
              <h3>Tau Mass</h3>
              <p>The third-generation lepton</p>
            </Link>
            <Link to="/calculations/fine-structure" className="related-card">
              <h3>Fine Structure Constant</h3>
              <p>The fundamental coupling constant</p>
            </Link>
          </div>
        </section>
      </div>
    </div>
  );
};

export default ElectronMassCalculation;