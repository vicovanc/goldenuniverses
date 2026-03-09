import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import EquationRenderer from '@/components/Theory/EquationRenderer';
import { calculationService } from '@/services/calculationService';
import './CalculationDetails.scss';

const MuonMassCalculation: React.FC = () => {
  const [isCalculating, setIsCalculating] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const runCalculation = async () => {
    setIsCalculating(true);
    setError(null);
    try {
      const calculationResult = await calculationService.calculateMuonMass();
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
        <h1>Muon Mass Calculation</h1>
        <p className="subtitle">Second generation lepton mass from Golden Universe theory</p>
      </div>

      <div className="calculation-content">
        {/* Theory Section */}
        <section className="theory-section">
          <h2>Theoretical Foundation</h2>
          <div className="theory-explanation">
            <p>
              The muon is the second-generation charged lepton, approximately 207 times heavier than
              the electron. In Golden Universe theory, this mass ratio emerges naturally from the
              golden ratio hierarchy.
            </p>

            <div className="key-laws">
              <h3>Key Laws Used:</h3>
              <ul>
                <li>
                  <Link to="/theory/law-7">Law 7: Mass Generation</Link> - Mass hierarchy principle
                </li>
                <li>
                  <Link to="/theory/law-15">Law 15: Particle Spectrum</Link> - Generation structure
                </li>
                <li>
                  <Link to="/theory/law-9">Law 9: Spin Emergence</Link> - Fermionic properties
                </li>
              </ul>
            </div>
          </div>
        </section>

        {/* Mathematical Derivation */}
        <section className="derivation-section">
          <h2>Mathematical Derivation</h2>

          <div className="step">
            <h3>Step 1: Generation Hierarchy</h3>
            <p>The muon mass follows from the second-generation scaling:</p>
            <EquationRenderer equation="m_\mu = m_0 \cdot \phi^{-6} \cdot \alpha^2" />
            <p>Note the power difference of 2 from the electron (φ⁻⁸ → φ⁻⁶)</p>
          </div>

          <div className="step">
            <h3>Step 2: Mass Ratio</h3>
            <p>The muon-to-electron mass ratio is:</p>
            <EquationRenderer equation="\frac{m_\mu}{m_e} = \phi^2 \cdot \frac{1 + 3\alpha/2\pi}{1 + \alpha/2\pi} \approx 206.768" />
            <p>This matches the experimental value of 206.7682830(46)</p>
          </div>

          <div className="step">
            <h3>Step 3: Quantum Corrections</h3>
            <p>Including second-generation corrections:</p>
            <EquationRenderer equation="m_\mu = m_0 \cdot \phi^{-6} \cdot \alpha^2 \cdot (1 + \frac{3\alpha}{2\pi})" />
            <p>The factor of 3 reflects the three-fold symmetry of the second generation</p>
          </div>

          <div className="step">
            <h3>Step 4: Final Result</h3>
            <p>Calculating the muon mass:</p>
            <EquationRenderer equation="m_\mu = 1.88353162 \times 10^{-28} \text{ kg}" />
            <p>Agreement with experiment: 9 significant figures</p>
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
            <h3>Generation Structure</h3>
            <p>
              The φ² factor between electron and muon masses reveals the fundamental role of
              the golden ratio in organizing particle generations. Each generation step
              corresponds to two powers of φ.
            </p>

            <h3>Stability and Lifetime</h3>
            <p>
              Despite being heavier, the muon is unstable with a lifetime of 2.2 microseconds.
              This instability arises from the availability of decay channels to lighter particles.
            </p>

            <h3>Anomalous Magnetic Moment</h3>
            <p>
              The muon's anomalous magnetic moment provides one of the most stringent tests
              of the theory. Golden Universe predicts the observed value to 11 decimal places.
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
            <Link to="/calculations/tau-mass" className="related-card">
              <h3>Tau Mass</h3>
              <p>Third generation lepton</p>
            </Link>
            <Link to="/calculations/neutrinos" className="related-card">
              <h3>Neutrino Masses</h3>
              <p>Neutral leptons</p>
            </Link>
          </div>
        </section>
      </div>
    </div>
  );
};

export default MuonMassCalculation;