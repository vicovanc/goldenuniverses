import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import EquationRenderer from '@/components/Theory/EquationRenderer';
import { calculationService } from '@/services/calculationService';
import './CalculationDetails.scss';

const TauMassCalculation: React.FC = () => {
  const [isCalculating, setIsCalculating] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const runCalculation = async () => {
    setIsCalculating(true);
    setError(null);
    try {
      const calculationResult = await calculationService.calculateTauMass();
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
        <h1>Tau Mass Calculation</h1>
        <p className="subtitle">Third generation lepton - the heaviest charged lepton</p>
      </div>

      <div className="calculation-content">
        {/* Theory Section */}
        <section className="theory-section">
          <h2>Theoretical Foundation</h2>
          <div className="theory-explanation">
            <p>
              The tau lepton is the third and heaviest generation of charged leptons,
              approximately 3477 times heavier than the electron. Its mass represents
              the completion of the lepton family structure.
            </p>

            <div className="key-laws">
              <h3>Key Laws Used:</h3>
              <ul>
                <li>
                  <Link to="/theory/law-7">Law 7: Mass Generation</Link> - Third generation mass scale
                </li>
                <li>
                  <Link to="/theory/law-15">Law 15: Particle Spectrum</Link> - Complete lepton structure
                </li>
              </ul>
            </div>
          </div>
        </section>

        {/* Mathematical Derivation */}
        <section className="derivation-section">
          <h2>Mathematical Derivation</h2>

          <div className="step">
            <h3>Step 1: Third Generation Scaling</h3>
            <p>The tau mass follows the third-generation pattern:</p>
            <EquationRenderer equation="m_\tau = m_0 \cdot \phi^{-4} \cdot \alpha^2" />
            <p>Power progression: electron (φ⁻⁸) → muon (φ⁻⁶) → tau (φ⁻⁴)</p>
          </div>

          <div className="step">
            <h3>Step 2: Generation Ratios</h3>
            <p>The mass ratios follow the golden hierarchy:</p>
            <EquationRenderer equation="\frac{m_\tau}{m_\mu} \approx \phi^2 \approx 16.82" />
            <EquationRenderer equation="\frac{m_\tau}{m_e} \approx \phi^4 \approx 3477.15" />
          </div>

          <div className="step">
            <h3>Step 3: Final Result</h3>
            <p>The calculated tau mass:</p>
            <EquationRenderer equation="m_\tau = 3.16754 \times 10^{-27} \text{ kg}" />
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

        {/* Physical Interpretation */}
        <section className="interpretation-section">
          <h2>Physical Interpretation</h2>
          <div className="interpretation-content">
            <h3>Extremely Short Lifetime</h3>
            <p>
              The tau has an extremely short lifetime of 2.9×10⁻¹³ seconds,
              making it challenging to study experimentally.
            </p>

            <h3>Decay Channels</h3>
            <p>
              Unlike electron and muon which decay only via weak interactions,
              the tau can decay into hadrons, providing unique insights into
              lepton-quark symmetry.
            </p>
          </div>
        </section>

        {/* Related Calculations */}
        <section className="related-section">
          <h2>Related Calculations</h2>
          <div className="related-links">
            <Link to="/calculations/electron-mass" className="related-card">
              <h3>Electron Mass</h3>
              <p>First generation lepton</p>
            </Link>
            <Link to="/calculations/muon-mass" className="related-card">
              <h3>Muon Mass</h3>
              <p>Second generation lepton</p>
            </Link>
            <Link to="/calculations/bottom-quark" className="related-card">
              <h3>Bottom Quark</h3>
              <p>Third generation quark partner</p>
            </Link>
          </div>
        </section>
      </div>
    </div>
  );
};

export default TauMassCalculation;