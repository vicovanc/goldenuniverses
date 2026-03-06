import { Link } from 'react-router-dom';
import './NotFound.scss';

const NotFound: React.FC = () => {
  return (
    <div className="not-found-page">
      <div className="not-found-content">
        <div className="not-found-icon">🌌</div>
        <h1 className="not-found-title">404</h1>
        <h2 className="not-found-subtitle">Lost in the Golden Universe</h2>
        <p className="not-found-message">
          The page you're looking for seems to have vanished into the void.
          Perhaps it's hiding behind the Golden Ratio?
        </p>

        <div className="golden-ratio-visual">
          <div className="phi-symbol">φ</div>
          <div className="ratio-text">≈ 1.618033988749895</div>
        </div>

        <div className="not-found-actions">
          <Link to="/" className="button primary">
            Return Home
          </Link>
          <Link to="/theory" className="button secondary">
            Explore Theory
          </Link>
        </div>

        <div className="helpful-links">
          <h3>Popular Destinations</h3>
          <ul>
            <li><Link to="/theory">Theory Overview</Link></li>
            <li><Link to="/derivations">Derivations</Link></li>
            <li><Link to="/calculations">Calculations</Link></li>
            <li><Link to="/visualizations">Visualizations</Link></li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
