/**
 * Results Page
 * Main page for viewing Golden Universe theoretical predictions
 * and comparing with experimental measurements
 */

import React from 'react';
import { Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';
import { ResultsDashboard } from '@/components/Results/ResultsDashboard';
import { CODATAComparison } from '@/components/Results/CODATAComparison';
import { AchievementCards } from '@/components/Results/AchievementCards';
import { PrecisionTable } from '@/components/Results/PrecisionTable';
import { achievements, goldenUniverseResults } from '@/components/Results/resultsData';
import './Results.scss';

const Results: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  // Get current page from route
  const currentPath = location.pathname.split('/').pop() || 'overview';

  const handleNavigation = (path: string) => {
    navigate(`/results/${path}`);
  };

  return (
    <div className="results-page">
      <div className="results-header">
        <h1 className="page-title">Golden Universe Results</h1>
        <p className="page-subtitle">
          Theoretical predictions compared with experimental measurements
        </p>
        <nav className="results-nav">
          <button
            className={`nav-btn ${currentPath === 'overview' ? 'active' : ''}`}
            onClick={() => handleNavigation('overview')}
          >
            Overview
          </button>
          <button
            className={`nav-btn ${currentPath === 'comparison' ? 'active' : ''}`}
            onClick={() => handleNavigation('comparison')}
          >
            CODATA Comparison
          </button>
          <button
            className={`nav-btn ${currentPath === 'achievements' ? 'active' : ''}`}
            onClick={() => handleNavigation('achievements')}
          >
            Achievements
          </button>
          <button
            className={`nav-btn ${currentPath === 'predictions' ? 'active' : ''}`}
            onClick={() => handleNavigation('predictions')}
          >
            Predictions Table
          </button>
        </nav>
      </div>

      <div className="results-content">
        <Routes>
          <Route index element={<Navigate to="overview" replace />} />
          <Route path="overview" element={<ResultsDashboard />} />
          <Route path="comparison" element={
            <div className="comparison-page">
              <CODATAComparison results={goldenUniverseResults} />
            </div>
          } />
          <Route path="achievements" element={
            <div className="achievements-page">
              <AchievementCards
                achievements={achievements}
                onShare={(achievement) => {
                  const text = `${achievement.title}: ${achievement.description} (${achievement.precision} ppm precision)`;
                  if (navigator.share) {
                    navigator.share({
                      title: 'Golden Universe Achievement',
                      text: text,
                      url: window.location.href,
                    }).catch(err => console.log('Error sharing:', err));
                  } else {
                    navigator.clipboard.writeText(text).then(() => {
                      alert('Achievement copied to clipboard!');
                    });
                  }
                }}
              />
            </div>
          } />
          <Route path="predictions" element={
            <div className="predictions-page">
              <PrecisionTable
                results={goldenUniverseResults}
              />
            </div>
          } />
          <Route path="*" element={<Navigate to="overview" replace />} />
        </Routes>
      </div>
    </div>
  );
};

export default Results;