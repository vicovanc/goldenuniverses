import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import EquationRenderer from '@/components/Theory/EquationRenderer';
import { calculationService } from '@/services/calculationService';
import './CalculationDetails.scss';

interface QuarkMassCalculationProps {
  quarkType: string;
}

const QuarkMassCalculation: React.FC<QuarkMassCalculationProps> = ({ quarkType }) => {
  const [isCalculating, setIsCalculating] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const quarkInfo: { [key: string]: { name: string, generation: number, charge: string, partner: string } } = {
    'up': { name: 'Up Quark', generation: 1, charge: '+2/3', partner: 'down' },
    'down': { name: 'Down Quark', generation: 1, charge: '-1/3', partner: 'up' },
    'charm': { name: 'Charm Quark', generation: 2, charge: '+2/3', partner: 'strange' },
    'strange': { name: 'Strange Quark', generation: 2, charge: '-1/3', partner: 'charm' },
    'top': { name: 'Top Quark', generation: 3, charge: '+2/3', partner: 'bottom' },
    'bottom': { name: 'Bottom Quark', generation: 3, charge: '-1/3', partner: 'top' }
  };

  const info = quarkInfo[quarkType] || quarkInfo['up'];

  const runCalculation = async () => {
    setIsCalculating(true);
    setError(null);
    try {
      const calculationResult = await calculationService.calculateQuarkMass(quarkType);
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
        <h1>{info.name} Mass Calculation</h1>
        <p className="subtitle">Generation {info.generation} quark with charge {info.charge}</p>
      </div>

      <div className="calculation-content">
        {/* Theory Section */}
        <section className="theory-section">
          <h2>Theoretical Foundation</h2>
          <div className="theory-explanation">
            <p>
              Quarks are fundamental constituents of hadrons, confined by the strong force.
              The {info.name.toLowerCase()} is a generation-{info.generation} quark that
              combines with other quarks to form baryons and mesons.
            </p>

            <div className="key-laws">
              <h3>Key Laws Used:</h3>
              <ul>
                <li>
                  <Link to="/theory/law-7">Law 7: Mass Generation</Link> - Quark mass hierarchy
                </li>
                <li>
                  <Link to="/theory/law-8">Law 8: Charge Quantization</Link> - Fractional charges
                </li>
                <li>
                  <Link to="/theory/law-10">Law 10: Coupling Constants</Link> - QCD corrections
                </li>
              </ul>
            </div>
          </div>
        </section>

        {/* Mathematical Derivation */}
        <section className="derivation-section">
          <h2>Mathematical Derivation</h2>

          <div className="step">
            <h3>Step 1: Base Mass Formula</h3>
            <p>Quark masses include QCD running and confinement effects:</p>
            <EquationRenderer equation={`m_{${quarkType}} = m_0 \\cdot \\phi^{n} \\cdot \\alpha_s \\cdot f_{QCD}`} />
            <p>where α_s is the strong coupling and f_QCD represents QCD corrections</p>
          </div>

          <div className="step">
            <h3>Step 2: Generation Structure</h3>
            <p>The generation pattern follows:</p>
            <EquationRenderer equation={`\\text{Gen } ${info.generation}: \\phi^{${info.generation === 1 ? '-7' : info.generation === 2 ? '-5' : '-1'}}`} />
          </div>

          <div className="step">
            <h3>Step 3: QCD Running</h3>
            <p>Mass runs with energy scale μ:</p>
            <EquationRenderer equation="m(\\mu) = m(\\mu_0) \\cdot \\left[\\frac{\\alpha_s(\\mu)}{\\alpha_s(\\mu_0)}\\right]^{\\gamma_m}" />
          </div>

          {quarkType === 'top' && (
            <div className="step">
              <h3>Special: Top Quark</h3>
              <p>The top quark is unique - it decays before hadronization:</p>
              <EquationRenderer equation="\\Gamma_t > \\Lambda_{QCD} \\Rightarrow \\text{No bound states}" />
            </div>
          )}
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
            <h3>Confinement</h3>
            <p>
              Unlike leptons, quarks are confined and cannot exist as free particles.
              They are always found in color-neutral combinations.
            </p>

            <h3>Mass Running</h3>
            <p>
              Quark masses are scale-dependent due to QCD interactions.
              The values depend on the renormalization scheme used.
            </p>

            <h3>Isospin Partnership</h3>
            <p>
              The {info.name.toLowerCase()} forms an isospin doublet with the {info.partner} quark,
              fundamental to the structure of matter.
            </p>
          </div>
        </section>

        {/* Related Calculations */}
        <section className="related-section">
          <h2>Related Calculations</h2>
          <div className="related-links">
            <Link to={`/calculations/${info.partner}-quark`} className="related-card">
              <h3>{info.partner.charAt(0).toUpperCase() + info.partner.slice(1)} Quark</h3>
              <p>Isospin partner</p>
            </Link>
            {info.generation === 1 && (
              <Link to="/calculations/charm-quark" className="related-card">
                <h3>Charm Quark</h3>
                <p>Second generation</p>
              </Link>
            )}
            {info.generation === 2 && (
              <Link to="/calculations/top-quark" className="related-card">
                <h3>Top Quark</h3>
                <p>Third generation</p>
              </Link>
            )}
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

export default QuarkMassCalculation;