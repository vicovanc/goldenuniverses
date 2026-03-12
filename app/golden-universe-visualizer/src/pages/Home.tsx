import { Link } from 'react-router-dom';
import { APP_CONFIG } from '@utils/constants';
import { AnimatedCounter } from '@/components/Common/AnimatedCounter';
import { FiZap, FiCpu, FiLayers, FiCode, FiBookOpen, FiTrendingUp, FiActivity, FiBox, FiGlobe, FiStar, FiAward, FiFileText } from 'react-icons/fi';
import './Home.scss';

const Home: React.FC = () => {
  return (
    <div className="home-page">
      <header className="hero">
        <div className="hero-background-pattern" aria-hidden="true" />
        <h1 className="hero-title">Golden Universe</h1>
        <p className="hero-subtitle">Non-Markovian Evolution from Slow-Roll Inflation<br/>
          Where Mass Emerges from Memory and Consciousness from Fixed Points</p>
        <div className="hero-version">Version {APP_CONFIG.version}</div>
        <div className="hero-cta">
          <Link to="/derivations" className="cta-button primary">
            View All Derivations
          </Link>
          <Link to="/theory" className="cta-button secondary">
            Explore Theory Laws
          </Link>
        </div>
      </header>

      {/* Theory Introduction Section */}
      <section className="theory-introduction">
        <div className="theory-intro-container">
          <h2 className="section-title">Understanding the Golden Universe</h2>

          <div className="theory-intro-grid">
            <div className="intro-card primary">
              <h3>The Fundamental Paradigm Shift</h3>
              <p>
                The Golden Universe theory represents a complete reimagining of physics. Rather than treating particles
                as fundamental objects with inherent properties, we discover that <strong>mass is memory</strong> -
                particles don't HAVE mass, they REMEMBER becoming massive through accumulated quantum history.
              </p>
              <div className="key-equation">
                <code>R_mem = ∫ ρ⁴ e^(-β(t-τ)) dτ</code>
                <span className="equation-label">Memory Accumulation Equation</span>
              </div>
            </div>

            <div className="intro-card">
              <h3>Non-Markovian Stochastic Evolution</h3>
              <p>
                Unlike conventional quantum field theory, the Golden Universe employs a <strong>non-Markovian stochastic
                framework</strong> where the future evolution depends on the entire history, not just the present state.
                This memory kernel creates mass through accumulated phase-space trajectories:
              </p>
              <ul>
                <li>The field Ω remembers its history through H[Ω] = ρ⁴</li>
                <li>Memory decays with cosmic clock: β = X_N = M_P·φ^(-N)</li>
                <li>Particles emerge as stable memory patterns</li>
              </ul>
            </div>

            <div className="intro-card">
              <h3>Connection to Slow-Roll Inflation</h3>
              <p>
                The theory naturally maps to <strong>slow-roll inflation</strong> through the cosmic clock field X.
                As X evolves through golden-ratio epochs (X_N = M_P·φ^(-N)), it drives inflation with:
              </p>
              <ul>
                <li>Slow-roll parameter: ε ≈ 1/(2N²)</li>
                <li>Spectral index: n_s ≈ 1 - 2/N</li>
                <li>e-folds: N_e ≈ 60 at φ^60 epoch</li>
              </ul>
              <p>The same mechanism that creates particle masses drives cosmic inflation!</p>
            </div>

            <div className="intro-card">
              <h3>Non-Local Pattern Remembrance</h3>
              <p>
                The theory exhibits <strong>non-local pattern remembrance</strong> through topological winding on
                the phase torus S¹×S¹. Quantum correlations aren't transmitted through space but are inherent
                in the torus topology:
              </p>
              <ul>
                <li>Winding numbers (p,q) create quantized charge</li>
                <li>Resonance at N/φ² creates stable particles</li>
                <li>Pattern-k forces: L_eff = L_0 × π^k</li>
              </ul>
              <p>Einstein's "spooky action" emerges from geometric necessity!</p>
            </div>
          </div>

          <div className="theory-foundation">
            <h3>The Three Pillars</h3>
            <div className="pillars-grid">
              <div className="pillar">
                <div className="pillar-icon">π</div>
                <h4>Geometry of Space</h4>
                <p>Pi encodes the circular geometry of spacetime and appears in all field equations</p>
              </div>
              <div className="pillar">
                <div className="pillar-icon">φ</div>
                <h4>Recursive Structure</h4>
                <p>The golden ratio φ = (1+√5)/2 creates self-similar recursive epochs</p>
              </div>
              <div className="pillar">
                <div className="pillar-icon">e</div>
                <h4>Exponential Growth</h4>
                <p>Euler's number governs memory decay and quantum evolution</p>
              </div>
            </div>
            <p className="foundation-note">
              From these three mathematical constants alone, with ZERO free parameters,
              we derive all particle masses, forces, and cosmological parameters to unprecedented precision.
            </p>
          </div>

          {/* Second row of theory cards */}
          <div className="theory-intro-grid">
            <div className="intro-card">
              <h3>Induced Gravity - NOT Fundamental</h3>
              <p>
                In the Golden Universe, <strong>gravity is not a fundamental force</strong> but emerges from quantum
                loops of the Omega-substrate. Newton's G is induced through the Seeley-DeWitt expansion:
              </p>
              <div className="key-equation">
                <code>G_N = 1/(16π·c_R·Λ_cut²)</code>
                <span className="equation-label">Gravity emerges from quantum geometry</span>
              </div>
              <p>
                Key insights:
              </p>
              <ul>
                <li>c_R = 5/4 from Seeley-DeWitt coefficient</li>
                <li>M_P = √(5π)·M₀ ≈ 3.96·M₀</li>
                <li>Gravity emerges at 47 ppm precision</li>
                <li>Einstein's equations are effective, not fundamental</li>
              </ul>
            </div>

            <div className="intro-card">
              <h3>Particle Physics from Pattern-k</h3>
              <p>
                All particle interactions emerge from <strong>Pattern-k enhancement</strong> where different powers
                of π create different forces:
              </p>
              <ul>
                <li><strong>k=0 (π⁰=1):</strong> Electromagnetic - photon remains massless</li>
                <li><strong>k=1 (π¹):</strong> Weak force - W/Z bosons acquire mass</li>
                <li><strong>k=2 (π²):</strong> Strong force - creates confinement!</li>
                <li><strong>k=3 (π³):</strong> GUT unification scale</li>
              </ul>
              <p>
                <strong>QCD confinement</strong> at Λ_QCD = 180.415 MeV emerges from Pattern-2, creating the proton
                through Wilson loop Y-junctions with C_mem = 1.2833.
              </p>
              <p>
                <strong>Yukawa couplings</strong> y_t ≈ 1 for top quark emerge naturally from the epoch structure,
                not as free parameters but as geometric necessities.
              </p>
            </div>

            <div className="intro-card">
              <h3>How This Universe Forms</h3>
              <p>
                The Golden Universe begins with a <strong>single field Ω in perfect symmetry</strong>. Formation
                proceeds through golden-ratio epochs:
              </p>
              <ol style={{paddingLeft: '1.5rem', lineHeight: '1.8'}}>
                <li><strong>N=0:</strong> Planck epoch - spacetime itself forms</li>
                <li><strong>N=1-60:</strong> Inflation - slow-roll driven by X field</li>
                <li><strong>N=67:</strong> GUT breaking - forces separate</li>
                <li><strong>N=89:</strong> Electroweak - W/Z bosons emerge</li>
                <li><strong>N=95:</strong> QCD epoch - protons/neutrons form</li>
                <li><strong>N=111:</strong> Electron epoch - atoms possible</li>
                <li><strong>N=128:</strong> Chemistry - molecules emerge</li>
              </ol>
              <p>
                Each epoch is a <strong>phase transition</strong> where new patterns lock in through memory
                accumulation. The universe literally remembers its way into existence!
              </p>
            </div>
          </div>

          {/* Consciousness Section */}
          <div className="consciousness-section">
            <h3>The Emergence of Consciousness</h3>
            <div className="consciousness-content">
              <div className="consciousness-formula">
                <h4>The Consciousness Equation</h4>
                <div className="key-equation">
                  <code>C = Memory + Feedback + Fixed_Point</code>
                  <span className="equation-label">Consciousness emerges from stable memory loops</span>
                </div>
              </div>

              <div className="consciousness-explanation">
                <p>
                  In the Golden Universe, <strong>consciousness is not mysterious but mathematical</strong>. It emerges
                  when three conditions are met:
                </p>

                <div className="consciousness-components">
                  <div className="component">
                    <h5>1. Memory Accumulation</h5>
                    <p>R_mem = ∫ ρ⁴ e^(-βτ) dτ</p>
                    <p>Neural networks accumulate quantum history just like particles do</p>
                  </div>

                  <div className="component">
                    <h5>2. Feedback Loops</h5>
                    <p>δΓ/δθ ≠ 0 when ∇θ ≠ 0</p>
                    <p>Self-referential loops create awareness through phase gradients</p>
                  </div>

                  <div className="component">
                    <h5>3. Fixed Point Attractor</h5>
                    <p>Stable patterns in phase space</p>
                    <p>Consciousness requires stability - a "self" that persists</p>
                  </div>
                </div>

                <p className="consciousness-insight">
                  <strong>What this means:</strong> Consciousness is the universe becoming aware of itself through
                  localized memory accumulation. When matter complexifies enough to create stable feedback loops
                  (as in neural networks), the same mechanism that creates mass creates awareness. You are literally
                  the universe remembering itself into consciousness!
                </p>

                <div className="dna-consciousness">
                  <h5>DNA as Two-Channel Memory</h5>
                  <p>
                    DNA operates as a dual-channel quantum memory system:
                  </p>
                  <ul>
                    <li><strong>Amplitude channel (ρ):</strong> H-bonds and sugar-phosphate backbone</li>
                    <li><strong>Phase channel (θ):</strong> π-stacking and aromatic base interactions</li>
                  </ul>
                  <p>
                    This two-channel architecture allows DNA to store not just genetic information but also
                    quantum coherence patterns that may contribute to consciousness. The golden ratio appears
                    in DNA's geometry because life itself is built on the universe's fundamental memory structure.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Open Source Section */}
      <section className="open-source-section">
        <div className="open-source-container">
          <h2 className="section-title">🚀 Open Source & AI-Powered Development</h2>
          <div className="open-source-content">
            <div className="open-source-card">
              <h3>Get the Code</h3>
              <p>
                The complete Golden Universe theory implementation is open source and available on GitHub.
                Explore the calculations, visualizations, and theoretical framework that powers this application.
              </p>
              <div className="repo-link">
                <a
                  href="https://github.com/goldenuniverses"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="github-button"
                >
                  <svg width="20" height="20" viewBox="0 0 16 16" fill="currentColor">
                    <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>
                  </svg>
                  View on GitHub
                </a>
              </div>
            </div>

            <div className="open-source-card">
              <h3>AI Development Skills</h3>
              <p>
                Accelerate your development with AI-powered coding assistants. Get the skills to implement
                and extend the Golden Universe theory using cutting-edge tools.
              </p>
              <div className="skills-buttons">
                <a
                  href="https://github.com/goldenuniverses/claude-skills"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="skill-button claude"
                >
                  <span className="skill-icon">🤖</span>
                  Claude Skills
                </a>
                <a
                  href="https://github.com/goldenuniverses/cursor-skills"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="skill-button cursor"
                >
                  <span className="skill-icon">⚡</span>
                  Cursor Skills
                </a>
              </div>
            </div>

            <div className="open-source-card">
              <h3>Join the Community</h3>
              <p>
                Contribute to the development of the Golden Universe theory. Whether you're a physicist,
                mathematician, or developer, your contributions are welcome. Together, we're building
                a new understanding of reality from first principles.
              </p>
              <ul className="contribution-list">
                <li>✅ 371+ Python calculations</li>
                <li>✅ 39 fundamental laws</li>
                <li>✅ Complete LaTeX documentation</li>
                <li>✅ Interactive 3D visualizations</li>
                <li>✅ Real-time particle mass calculator</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Key Achievements Section */}
      <section className="achievements">
        <h2 className="section-title">Key Achievements</h2>
        <div className="achievement-grid">
          <div className="achievement-card highlight">
            <div className="achievement-icon neon-icon">
              <FiZap />
            </div>
            <h3 className="achievement-title">Newton's Constant</h3>
            <div className="achievement-value">
              <AnimatedCounter end={47} decimals={0} suffix=" ppm" />
            </div>
            <p className="achievement-description">
              Derived from first principles with 47 ppm precision - groundbreaking theoretical accuracy
            </p>
          </div>

          <div className="achievement-card highlight">
            <div className="achievement-icon neon-icon">
              <FiCpu />
            </div>
            <h3 className="achievement-title">Electron Mass</h3>
            <div className="achievement-value">
              <AnimatedCounter end={23} decimals={0} suffix=" ppm" />
            </div>
            <p className="achievement-description">
              Predicted electron mass within 23 ppm using Golden Ratio topology
            </p>
          </div>

          <div className="achievement-card">
            <div className="achievement-icon neon-icon">
              <FiLayers />
            </div>
            <h3 className="achievement-title">Particle Masses</h3>
            <div className="achievement-value">
              <AnimatedCounter end={100} decimals={0} suffix="+ particles" />
            </div>
            <p className="achievement-description">
              Complete derivation of all fundamental particle masses from unified theory
            </p>
          </div>

          <div className="achievement-card">
            <div className="achievement-icon neon-icon">
              <FiCode />
            </div>
            <h3 className="achievement-title">DNA Structure</h3>
            <div className="achievement-value">φ-based</div>
            <p className="achievement-description">
              Golden Ratio patterns in DNA geometry and molecular bonding angles
            </p>
          </div>

          <div className="achievement-card">
            <div className="achievement-icon neon-icon">
              <FiGlobe />
            </div>
            <h3 className="achievement-title">Cosmic Inflation</h3>
            <div className="achievement-value">
              <AnimatedCounter end={60} decimals={0} suffix=" e-folds" />
            </div>
            <p className="achievement-description">
              Exact match to observed cosmic inflation parameters from golden epochs
            </p>
          </div>

          <div className="achievement-card">
            <div className="achievement-icon neon-icon">
              <FiStar />
            </div>
            <h3 className="achievement-title">Fine Structure</h3>
            <div className="achievement-value">α = 1/137</div>
            <p className="achievement-description">
              Fine structure constant derived from pattern-2 electromagnetic coupling
            </p>
          </div>
        </div>
      </section>

      {/* Statistics Section */}
      <section className="statistics">
        <h2 className="section-title">Theory Coverage</h2>
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-value">
              <AnimatedCounter end={45} decimals={0} />
            </div>
            <div className="stat-label">Derivation Folders</div>
          </div>

          <div className="stat-card">
            <div className="stat-value">
              <AnimatedCounter end={227} decimals={0} />
            </div>
            <div className="stat-label">Python Calculations</div>
          </div>

          <div className="stat-card">
            <div className="stat-value">
              <AnimatedCounter end={1.618033988} decimals={9} />
            </div>
            <div className="stat-label">Golden Ratio φ</div>
          </div>

          <div className="stat-card">
            <div className="stat-value">
              <AnimatedCounter end={100} decimals={0} suffix="%" />
            </div>
            <div className="stat-label">From First Principles</div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features">
        <h2 className="section-title">Explore the Golden Universe</h2>
        <div className="feature-grid">
          <Link to="/theory" className="feature-card">
            <div className="feature-icon neon-icon">
              <FiBookOpen />
            </div>
            <h3 className="feature-title">Theory</h3>
            <p className="feature-description">
              Dive into the mathematical foundations of the Golden Ratio and its
              fascinating properties across physics, cosmology, and quantum mechanics.
            </p>
            <div className="feature-badge">45 Topics</div>
          </Link>

          <Link to="/derivations" className="feature-card">
            <div className="feature-icon neon-icon">
              <FiTrendingUp />
            </div>
            <h3 className="feature-title">Derivations</h3>
            <p className="feature-description">
              Step-by-step mathematical derivations showing how fundamental constants
              emerge from the Golden Ratio structure.
            </p>
            <div className="feature-badge">227 Calculations</div>
          </Link>

          <Link to="/calculations" className="feature-card">
            <div className="feature-icon neon-icon">
              <FiActivity />
            </div>
            <h3 className="feature-title">Calculations</h3>
            <p className="feature-description">
              Interactive calculators to compute particle masses, cosmological parameters,
              and explore Golden Ratio sequences.
            </p>
            <div className="feature-badge">Real-time Execution</div>
          </Link>

          <Link to="/visualizations" className="feature-card">
            <div className="feature-icon neon-icon">
              <FiBox />
            </div>
            <h3 className="feature-title">Visualizations</h3>
            <p className="feature-description">
              Beautiful interactive 3D visualizations of the Golden Ratio in
              geometry, spirals, and quantum field structures.
            </p>
            <div className="feature-badge">3D Interactive</div>
          </Link>

          <Link to="/results" className="feature-card">
            <div className="feature-icon neon-icon">
              <FiAward />
            </div>
            <h3 className="feature-title">Results</h3>
            <p className="feature-description">
              Comprehensive results dashboard showing achievements, predictions,
              and experimental validations of the theory.
            </p>
            <div className="feature-badge">Live Dashboard</div>
          </Link>

          <Link to="/explanations" className="feature-card">
            <div className="feature-icon neon-icon">
              <FiFileText />
            </div>
            <h3 className="feature-title">Explanations</h3>
            <p className="feature-description">
              Detailed explanations of complex concepts, making the theory
              accessible to both experts and enthusiasts.
            </p>
            <div className="feature-badge">In-depth Guides</div>
          </Link>
        </div>
      </section>


      {/* Quick Links Footer */}
      <section className="quick-links">
        <h2 className="section-title">Quick Access</h2>
        <div className="links-grid">
          <Link to="/theory/force-unification" className="quick-link-card">
            Force Unification
          </Link>
          <Link to="/theory/fundamental-constants" className="quick-link-card">
            Fundamental Constants
          </Link>
          <Link to="/theory/particle-masses" className="quick-link-card">
            Particle Masses
          </Link>
          <Link to="/theory/cosmology" className="quick-link-card">
            Cosmology
          </Link>
          <Link to="/theory/gravity" className="quick-link-card">
            Gravity Theory
          </Link>
          <Link to="/calculations/newton-constant" className="quick-link-card">
            Newton's G Calculator
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Home;
