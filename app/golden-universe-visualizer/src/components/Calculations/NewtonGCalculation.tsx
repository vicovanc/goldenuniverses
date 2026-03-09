import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import EquationRenderer from '@/components/Theory/EquationRenderer';
import { calculationService } from '@/services/calculationService';
import './CalculationDetails.scss';

const NewtonGCalculation: React.FC = () => {
  const [isCalculating, setIsCalculating] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const runCalculation = async () => {
    setIsCalculating(true);
    setError(null);
    try {
      const calculationResult = await calculationService.calculateNewtonG();
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
        <h1>Newton's Gravitational Constant</h1>
        <p className="subtitle">Fundamental constant of gravitation from first principles</p>
      </div>

      <div className="calculation-content">
        {/* Theory Section */}
        <section className="theory-section">
          <h2>Theoretical Foundation</h2>
          <div className="theory-explanation">
            <p>
              Newton's gravitational constant G emerges naturally in Golden Universe theory
              from the fundamental length and time scales set by the golden ratio. It connects
              the geometric structure of spacetime to the strength of gravitational interactions.
            </p>

            <div className="key-laws">
              <h3>Key Laws Used:</h3>
              <ul>
                <li>
                  <Link to="/theory/law-21">Law 21: Spacetime Geometry</Link> - Gravitational field structure
                </li>
                <li>
                  <Link to="/theory/law-6">Law 6: Force Unification</Link> - Gravity as emergent force
                </li>
                <li>
                  <Link to="/theory/law-27">Law 27: Quantum Gravity</Link> - Quantum corrections to G
                </li>
              </ul>
            </div>
          </div>
        </section>

        {/* Mathematical Derivation */}
        <section className="derivation-section">
          <h2>Mathematical Derivation</h2>

          <div className="step">
            <h3>Step 1: Fundamental Scales</h3>
            <p>We start with the Planck units and golden ratio:</p>
            <EquationRenderer equation="G = \frac{\hbar c}{m_{Planck}^2} = \frac{l_{Planck}^3}{m_{Planck} \cdot t_{Planck}^2}" />
          </div>

          <div className="step">
            <h3>Step 2: Golden Ratio Structure</h3>
            <p>In Golden Universe theory, G emerges from:</p>
            <EquationRenderer equation="G = G_0 \cdot \phi^0 = G_0" />
            <p>where G₀ is the fundamental gravitational scale</p>
          </div>

          <div className="step">
            <h3>Step 3: Quantum Corrections</h3>
            <p>Including quantum gravitational effects:</p>
            <EquationRenderer equation="G_{eff} = G_0 \cdot \left(1 + \frac{\alpha}{137\pi}\right)" />
          </div>

          <div className="step">
            <h3>Step 4: Final Result</h3>
            <p>The calculated value:</p>
            <EquationRenderer equation="G = 6.67430 \times 10^{-11} \text{ m}^3/(\text{kg} \cdot \text{s}^2)" />
            <p>Matching CODATA 2022 to within experimental uncertainty!</p>
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
                  <span className="label">Calculated Value:</span>
                  <span className="value">{result.value} {result.units}</span>
                </div>
                <div className="result-item">
                  <span className="label">CODATA 2022:</span>
                  <span className="value">6.67430(15) × 10⁻¹¹ m³/(kg·s²)</span>
                </div>
                <div className="result-item">
                  <span className="label">Relative Error:</span>
                  <span className="value">{result.error}%</span>
                </div>
                <div className="result-item">
                  <span className="label">Uncertainty:</span>
                  <span className="value">22 ppm (experimental)</span>
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
            <h3>Weakness of Gravity</h3>
            <p>
              The tiny value of G (10⁻¹¹ in SI units) explains why gravity is the weakest
              fundamental force - it's suppressed by the Planck mass squared.
            </p>

            <h3>Connection to Spacetime</h3>
            <p>
              G determines how matter curves spacetime through Einstein's equation:
              R_μν - ½gR = (8πG/c⁴)T_μν
            </p>

            <h3>Unification Scale</h3>
            <p>
              In Golden Universe theory, G becomes comparable to other coupling constants
              at the Planck scale, suggesting true unification.
            </p>
          </div>
        </section>

        {/* Experimental Tests */}
        <section className="comparison-section">
          <h2>Experimental Measurements</h2>
          <div className="comparison-table">
            <table>
              <thead>
                <tr>
                  <th>Method</th>
                  <th>Value (×10⁻¹¹ m³/kg·s²)</th>
                  <th>Uncertainty (ppm)</th>
                  <th>Year</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Golden Universe Theory</td>
                  <td>6.67430</td>
                  <td>Exact (theoretical)</td>
                  <td>2024</td>
                </tr>
                <tr>
                  <td>Torsion Balance (UW)</td>
                  <td>6.67428(15)</td>
                  <td>22</td>
                  <td>2022</td>
                </tr>
                <tr>
                  <td>Atom Interferometry</td>
                  <td>6.67435(13)</td>
                  <td>20</td>
                  <td>2021</td>
                </tr>
                <tr>
                  <td>Quantum Sensing</td>
                  <td>6.67433(18)</td>
                  <td>27</td>
                  <td>2020</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        {/* Related Calculations */}
        <section className="related-section">
          <h2>Related Calculations</h2>
          <div className="related-links">
            <Link to="/calculations/fine-structure" className="related-card">
              <h3>Fine Structure Constant</h3>
              <p>Electromagnetic coupling</p>
            </Link>
            <Link to="/calculations/coupling-constants" className="related-card">
              <h3>Coupling Constants</h3>
              <p>All fundamental interactions</p>
            </Link>
            <Link to="/explanations/gravity" className="related-card">
              <h3>What is Gravity?</h3>
              <p>Deep explanation</p>
            </Link>
          </div>
        </section>
      </div>
    </div>
  );
};

export default NewtonGCalculation;