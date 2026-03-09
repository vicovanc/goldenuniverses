import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import EquationRenderer from '@/components/Theory/EquationRenderer';
import { calculationService } from '@/services/calculationService';
import './CalculationDetails.scss';

const NeutrinoMassCalculation: React.FC = () => {
  const [isCalculating, setIsCalculating] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const runCalculation = async () => {
    setIsCalculating(true);
    setError(null);
    try {
      const calculationResult = await calculationService.calculateNeutrinoMasses();
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
        <h1>Neutrino Mass Calculation</h1>
        <p className="subtitle">The lightest massive particles in the universe</p>
      </div>

      <div className="calculation-content">
        {/* Theory Section */}
        <section className="theory-section">
          <h2>Theoretical Foundation</h2>
          <div className="theory-explanation">
            <p>
              Neutrinos are the lightest massive particles, with masses millions of times
              smaller than electrons. Golden Universe theory predicts their masses through
              a seesaw mechanism involving the golden ratio hierarchy.
            </p>

            <div className="key-laws">
              <h3>Key Laws Used:</h3>
              <ul>
                <li>
                  <Link to="/theory/law-16">Law 16: Neutrino Oscillations</Link> - Mass mixing
                </li>
                <li>
                  <Link to="/theory/law-7">Law 7: Mass Generation</Link> - Seesaw mechanism
                </li>
              </ul>
            </div>
          </div>
        </section>

        {/* Mathematical Derivation */}
        <section className="derivation-section">
          <h2>Mathematical Derivation</h2>

          <div className="step">
            <h3>Step 1: Seesaw Mechanism</h3>
            <p>Neutrino masses are suppressed by high-scale physics:</p>
            <EquationRenderer equation="m_\nu \sim \frac{m_D^2}{M_R}" />
            <p>where m_D is the Dirac mass and M_R is the right-handed scale</p>
          </div>

          <div className="step">
            <h3>Step 2: Mass Hierarchy</h3>
            <p>The three neutrino masses follow:</p>
            <EquationRenderer equation="m_{\nu_e} : m_{\nu_\mu} : m_{\nu_\tau} = \phi^{-25} : \phi^{-24} : \phi^{-23}" />
          </div>

          <div className="step">
            <h3>Step 3: Oscillation Parameters</h3>
            <p>Mass squared differences:</p>
            <EquationRenderer equation="\Delta m_{21}^2 = 7.5 \times 10^{-5} \text{ eV}^2" />
            <EquationRenderer equation="\Delta m_{31}^2 = 2.5 \times 10^{-3} \text{ eV}^2" />
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
                  <span className="label">ν_e Mass:</span>
                  <span className="value">{result.electron_neutrino}</span>
                </div>
                <div className="result-item">
                  <span className="label">ν_μ Mass:</span>
                  <span className="value">{result.muon_neutrino}</span>
                </div>
                <div className="result-item">
                  <span className="label">ν_τ Mass:</span>
                  <span className="value">{result.tau_neutrino}</span>
                </div>
                <div className="result-item">
                  <span className="label">Sum Σm_ν:</span>
                  <span className="value">{result.sum}</span>
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

        {/* Related Calculations */}
        <section className="related-section">
          <h2>Related Calculations</h2>
          <div className="related-links">
            <Link to="/calculations/electron-mass" className="related-card">
              <h3>Electron Mass</h3>
              <p>Charged lepton partner</p>
            </Link>
            <Link to="/calculations/muon-mass" className="related-card">
              <h3>Muon Mass</h3>
              <p>Second generation</p>
            </Link>
            <Link to="/calculations/tau-mass" className="related-card">
              <h3>Tau Mass</h3>
              <p>Third generation</p>
            </Link>
          </div>
        </section>
      </div>
    </div>
  );
};

export default NeutrinoMassCalculation;