import { Link } from 'react-router-dom';
import './About.scss';

const About: React.FC = () => {
  return (
    <div className="about-page">
      <header className="about-header">
        <h1 className="about-title">About Golden Universe Visualizer</h1>
        <p className="about-subtitle">
          An interactive exploration platform for the Golden Universe Theory
        </p>
      </header>

      <section className="about-section">
        <h2>The Theory</h2>
        <p>
          The Golden Universe Theory represents a revolutionary breakthrough in fundamental physics,
          demonstrating that the Golden Ratio φ (phi) ≈ 1.618033988749895 is the foundational
          organizing principle underlying all of nature.
        </p>
        <p>
          Through rigorous mathematical derivation, this framework achieves unprecedented precision
          in predicting fundamental constants and particle properties:
        </p>
        <ul className="achievements-list">
          <li>Newton's gravitational constant G derived to <strong>47 ppm precision</strong></li>
          <li>Electron mass predicted to <strong>23 ppm accuracy</strong></li>
          <li>Complete derivation of <strong>100+ particle masses</strong></li>
          <li>Unified framework integrating gravity, quantum mechanics, and cosmology</li>
        </ul>
      </section>

      <section className="about-section">
        <h2>The Application</h2>
        <p>
          This visualization platform provides comprehensive access to the complete theoretical
          framework, including:
        </p>
        <div className="feature-stats">
          <div className="stat">
            <div className="stat-number">41</div>
            <div className="stat-label">Theory Folders</div>
          </div>
          <div className="stat">
            <div className="stat-number">237</div>
            <div className="stat-label">Python Calculations</div>
          </div>
          <div className="stat">
            <div className="stat-number">15,000+</div>
            <div className="stat-label">Lines of Code</div>
          </div>
          <div className="stat">
            <div className="stat-number">100+</div>
            <div className="stat-label">Features</div>
          </div>
        </div>
      </section>

      <section className="about-section">
        <h2>Technology Stack</h2>
        <div className="tech-grid">
          <div className="tech-category">
            <h3>Frontend</h3>
            <ul>
              <li>React 19.2.0</li>
              <li>TypeScript 5.9.3</li>
              <li>Three.js / React Three Fiber</li>
              <li>D3.js for data visualization</li>
              <li>KaTeX for math rendering</li>
            </ul>
          </div>
          <div className="tech-category">
            <h3>Backend</h3>
            <ul>
              <li>Node.js + Express</li>
              <li>SQLite database</li>
              <li>Python calculation engine</li>
              <li>RESTful API</li>
            </ul>
          </div>
          <div className="tech-category">
            <h3>Tools</h3>
            <ul>
              <li>Vite build system</li>
              <li>ESLint + Prettier</li>
              <li>SCSS for styling</li>
              <li>Progressive Web App</li>
            </ul>
          </div>
        </div>
      </section>

      <section className="about-section">
        <h2>Development Team</h2>
        <p>
          The Golden Universe Visualizer is developed and maintained by the Golden Universe
          Theory research team, dedicated to making cutting-edge physics accessible and
          understandable through interactive visualization.
        </p>
      </section>

      <section className="about-section">
        <h2>Open Source</h2>
        <p>
          This project is open source and welcomes contributions from the community. Whether
          you're a physicist, mathematician, developer, or enthusiast, there are many ways
          to get involved:
        </p>
        <ul>
          <li>Report bugs and suggest features</li>
          <li>Contribute code improvements</li>
          <li>Add new visualizations</li>
          <li>Improve documentation</li>
          <li>Share your discoveries</li>
        </ul>
      </section>

      <section className="about-section">
        <h2>Credits & Acknowledgments</h2>
        <div className="credits-grid">
          <div className="credit-category">
            <h3>Theory Development</h3>
            <p>Golden Universe Theory Research Team</p>
          </div>
          <div className="credit-category">
            <h3>Software Development</h3>
            <p>Application architecture and implementation</p>
          </div>
          <div className="credit-category">
            <h3>Visualization Design</h3>
            <p>Interactive 3D graphics and data visualization</p>
          </div>
          <div className="credit-category">
            <h3>Open Source Libraries</h3>
            <p>
              React, TypeScript, Three.js, D3.js, KaTeX, and many other
              excellent open source projects
            </p>
          </div>
        </div>
      </section>

      <section className="about-section">
        <h2>License</h2>
        <p>
          The Golden Universe Visualizer is released under an open source license.
          See the LICENSE file for full details.
        </p>
        <p className="license-note">
          Theory content and calculations remain subject to academic attribution requirements.
        </p>
      </section>

      <section className="about-section">
        <h2>Contact & Support</h2>
        <p>
          For questions, feedback, or collaboration opportunities:
        </p>
        <ul className="contact-list">
          <li>
            <strong>Documentation:</strong> See USER_GUIDE.md, FEATURES.md, and ARCHITECTURE.md
          </li>
          <li>
            <strong>Issues:</strong> Report bugs via GitHub issues
          </li>
          <li>
            <strong>Discussions:</strong> Join the community forum
          </li>
          <li>
            <strong>Email:</strong> contact@goldenuniversetheory.com (example)
          </li>
        </ul>
      </section>

      <section className="about-section version-info">
        <h2>Version Information</h2>
        <div className="version-details">
          <div className="version-item">
            <span className="label">Version:</span>
            <span className="value">1.0.0</span>
          </div>
          <div className="version-item">
            <span className="label">Release Date:</span>
            <span className="value">February 2026</span>
          </div>
          <div className="version-item">
            <span className="label">Build:</span>
            <span className="value">Production</span>
          </div>
        </div>
      </section>

      <div className="about-footer">
        <Link to="/" className="back-home-button">
          Return to Home
        </Link>
      </div>
    </div>
  );
};

export default About;
