/**
 * ResultsDashboard - Main dashboard container
 * EPIC-008: Results Dashboard (GU-036 through GU-040)
 * Integrates all results components
 */

import React, { useState } from 'react';
import { PrecisionTable } from './PrecisionTable';
import { AchievementCards } from './AchievementCards';
import { ResultsCharts } from './ResultsCharts';
import { CODATAComparison } from './CODATAComparison';
import { ExportOptions } from './ExportOptions';
import { goldenUniverseResults, achievements, getStatistics } from './resultsData';
import type { AchievementData } from './types';
import './Results.scss';

type DashboardView = 'overview' | 'table' | 'charts' | 'codata' | 'achievements';

export const ResultsDashboard: React.FC = () => {
  const [activeView, setActiveView] = useState<DashboardView>('overview');

  // Use all results without filtering
  const results = goldenUniverseResults;

  const stats = getStatistics();

  const handleShare = (achievement: AchievementData) => {
    const text = `${achievement.title}: ${achievement.description} (${achievement.precision} ppm precision)`;

    if (navigator.share) {
      navigator.share({
        title: 'Golden Universe Achievement',
        text: text,
        url: window.location.href,
      }).catch(err => console.log('Error sharing:', err));
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(text).then(() => {
        alert('Achievement copied to clipboard!');
      });
    }
  };

  return (
    <div className="results-dashboard">
      {/* Header */}
      <div className="dashboard-header">
        <div className="header-content">
          <h1>Results Dashboard</h1>
          <p className="subtitle">
            Golden Universe theoretical predictions compared with experimental measurements
          </p>
        </div>
        <div className="header-actions">
          <ExportOptions results={results} />
        </div>
      </div>

      {/* Statistics Overview */}
      <div className="stats-banner">
        <div className="stat-item">
          <span className="stat-value">{stats.total}</span>
          <span className="stat-label">Total Predictions</span>
        </div>
        <div className="stat-item highlight">
          <span className="stat-value">{stats.breakthroughs}</span>
          <span className="stat-label">Breakthroughs</span>
        </div>
        <div className="stat-item">
          <span className="stat-value">{stats.subPpm}</span>
          <span className="stat-label">Sub-ppm Precision</span>
        </div>
        <div className="stat-item">
          <span className="stat-value">{stats.sub100Ppm}</span>
          <span className="stat-label">Sub-100 ppm</span>
        </div>
        <div className="stat-item">
          <span className="stat-value">{stats.averagePrecision.toFixed(1)}</span>
          <span className="stat-label">Avg Error (ppm)</span>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="dashboard-nav">
        <button
          className={`nav-tab ${activeView === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveView('overview')}
        >
          Overview
        </button>
        <button
          className={`nav-tab ${activeView === 'table' ? 'active' : ''}`}
          onClick={() => setActiveView('table')}
        >
          Precision Table
        </button>
        <button
          className={`nav-tab ${activeView === 'charts' ? 'active' : ''}`}
          onClick={() => setActiveView('charts')}
        >
          Visualizations
        </button>
        <button
          className={`nav-tab ${activeView === 'codata' ? 'active' : ''}`}
          onClick={() => setActiveView('codata')}
        >
          CODATA Comparison
        </button>
        <button
          className={`nav-tab ${activeView === 'achievements' ? 'active' : ''}`}
          onClick={() => setActiveView('achievements')}
        >
          Achievements
        </button>
      </div>

      {/* Main Content Area */}
      <div className="dashboard-content dashboard-content-fullwidth">
        {/* Main View Area - No sidebar, full width */}
        <main className="dashboard-main dashboard-main-fullwidth">
          {activeView === 'overview' && (
            <div className="overview-view">
              <section className="overview-section">
                <AchievementCards achievements={achievements} onShare={handleShare} />
              </section>

              <section className="overview-section">
                <h2>Quick Comparison</h2>
                <PrecisionTable results={results.slice(0, 5)} />
              </section>

              <section className="overview-section">
                <ResultsCharts results={results} />
              </section>
            </div>
          )}

          {activeView === 'table' && (
            <div className="table-view">
              <PrecisionTable results={results} />
            </div>
          )}

          {activeView === 'charts' && (
            <div className="charts-view">
              <ResultsCharts results={results} />
            </div>
          )}

          {activeView === 'codata' && (
            <div className="codata-view">
              <CODATAComparison results={results} />
            </div>
          )}

          {activeView === 'achievements' && (
            <div className="achievements-view">
              <AchievementCards achievements={achievements} onShare={handleShare} />
            </div>
          )}
        </main>
      </div>

      {/* Footer Info */}
      <footer className="dashboard-footer">
        <div className="footer-content">
          <div className="footer-section">
            <h4>About This Dashboard</h4>
            <p>
              This dashboard presents the theoretical predictions of the Golden Universe theory
              compared with experimental measurements from CODATA and particle physics experiments.
            </p>
          </div>
          <div className="footer-section">
            <h4>Data Sources</h4>
            <ul>
              <li>CODATA 2018 Fundamental Constants</li>
              <li>Particle Data Group (PDG) 2022</li>
              <li>LHC/ATLAS/CMS Measurements</li>
              <li>Golden Universe Theoretical Framework</li>
            </ul>
          </div>
          <div className="footer-section">
            <h4>Precision Levels</h4>
            <ul>
              <li><span className="precision-badge excellent">Excellent</span> &lt; 100 ppm</li>
              <li><span className="precision-badge very-good">Very Good</span> &lt; 0.1%</li>
              <li><span className="precision-badge good">Good</span> &lt; 1%</li>
              <li><span className="precision-badge fair">Fair</span> &lt; 10%</li>
            </ul>
          </div>
        </div>
      </footer>
    </div>
  );
};
