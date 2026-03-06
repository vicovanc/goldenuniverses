import { Link } from 'react-router-dom';
import { APP_CONFIG } from '@utils/constants';
import { AnimatedCounter } from '@/components/Common/AnimatedCounter';
import { FiZap, FiCpu, FiLayers, FiCode, FiBookOpen, FiTrendingUp, FiActivity, FiBox } from 'react-icons/fi';
import './Home.scss';

const Home: React.FC = () => {
  return (
    <div className="home-page">
      <header className="hero">
        <div className="hero-background-pattern" aria-hidden="true" />
        <h1 className="hero-title">Golden Universe</h1>
        <p className="hero-subtitle">Revolutionary Theoretical Physics Framework<br/>
          Newton's G derived to 47 ppm with ZERO fitted parameters</p>
        <div className="hero-version">Version {APP_CONFIG.version}</div>
        <div className="hero-cta">
          <Link to="/theory" className="cta-button primary">
            Start Exploring
          </Link>
          <Link to="/visualizations" className="cta-button secondary">
            View Visualizations
          </Link>
        </div>
      </header>

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
        </div>
      </section>

      {/* Statistics Section */}
      <section className="statistics">
        <h2 className="section-title">Theory Coverage</h2>
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-value">
              <AnimatedCounter end={41} decimals={0} />
            </div>
            <div className="stat-label">Derivation Folders</div>
          </div>

          <div className="stat-card">
            <div className="stat-value">
              <AnimatedCounter end={237} decimals={0} />
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
            <div className="feature-badge">41 Topics</div>
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
            <div className="feature-badge">237 Calculations</div>
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
        </div>
      </section>

      {/* About Section */}
      <section className="about">
        <h2 className="section-title">About the Golden Universe Theory</h2>
        <div className="about-content">
          <p>
            The Golden Universe Theory represents a revolutionary approach to fundamental physics,
            demonstrating that the Golden Ratio φ (phi) ≈ 1.618033988749895 is not merely a
            mathematical curiosity, but the foundational organizing principle of nature itself.
          </p>
          <div className="golden-ratio-formula">
            <code>φ = (1 + √5) / 2 ≈ 1.618033988749895</code>
          </div>
          <p>
            This comprehensive framework derives Newton's gravitational constant to 47 ppm precision,
            predicts particle masses from first principles, explains cosmological parameters, and
            reveals the deep connection between consciousness, geometry, and physical law.
          </p>
          <div className="about-highlights">
            <div className="highlight-item">
              <strong>First Principles:</strong> All results derived from φ and fundamental geometry
            </div>
            <div className="highlight-item">
              <strong>Experimental Validation:</strong> Predictions match measurements to unprecedented precision
            </div>
            <div className="highlight-item">
              <strong>Unified Framework:</strong> Integrates gravity, quantum mechanics, and cosmology
            </div>
          </div>
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
