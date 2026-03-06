/**
 * Results Dashboard - Usage Examples
 * Demonstrates how to integrate and use the Results Dashboard components
 */

import React from 'react';
import {
  ResultsDashboard,
  PrecisionTable,
  AchievementCards,
  ResultsCharts,
  CODATAComparison,
  ExportOptions,
  goldenUniverseResults,
  achievements,
  getStatistics,
  getResultsByCategory,
  getBreakthroughResults,
} from './index';

// ============================================================================
// Example 1: Full Dashboard (Recommended)
// ============================================================================

export function Example1_FullDashboard() {
  return (
    <div className="app-container">
      <ResultsDashboard />
    </div>
  );
}

// ============================================================================
// Example 2: Individual Components
// ============================================================================

export function Example2_IndividualComponents() {
  const handleShare = (achievement: any) => {
    console.log('Sharing achievement:', achievement.title);
  };

  return (
    <div className="custom-layout">
      {/* Precision Table Only */}
      <section>
        <h2>Precision Comparison</h2>
        <PrecisionTable results={goldenUniverseResults} />
      </section>

      {/* Achievement Cards Only */}
      <section>
        <h2>Breakthroughs</h2>
        <AchievementCards achievements={achievements} onShare={handleShare} />
      </section>

      {/* Charts Only */}
      <section>
        <h2>Visualizations</h2>
        <ResultsCharts results={goldenUniverseResults} />
      </section>

      {/* CODATA Comparison Only */}
      <section>
        <h2>CODATA Validation</h2>
        <CODATAComparison results={goldenUniverseResults} />
      </section>
    </div>
  );
}

// ============================================================================
// Example 3: Filtered Results
// ============================================================================

export function Example3_FilteredResults() {
  // Show only leptons
  const leptonResults = getResultsByCategory('leptons');

  // Show only breakthrough results
  const breakthroughs = getBreakthroughResults();

  return (
    <div className="filtered-view">
      <section>
        <h2>Lepton Predictions</h2>
        <PrecisionTable results={leptonResults} />
      </section>

      <section>
        <h2>Breakthrough Results Only</h2>
        <PrecisionTable results={breakthroughs} />
      </section>
    </div>
  );
}

// ============================================================================
// Example 4: Custom Export Handler
// ============================================================================

export function Example4_CustomExport() {
  const handleExport = () => {
    // Custom export logic
    const data = goldenUniverseResults.map(r => ({
      name: r.name,
      precision: r.errorPpm,
      category: r.category,
    }));

    console.log('Exporting data:', data);
    // Could trigger custom analytics, logging, etc.
  };

  return (
    <div className="export-demo">
      <PrecisionTable results={goldenUniverseResults} onExport={handleExport} />
    </div>
  );
}

// ============================================================================
// Example 5: Statistics Display
// ============================================================================

export function Example5_Statistics() {
  const stats = getStatistics();

  return (
    <div className="stats-display">
      <h2>Golden Universe Statistics</h2>
      <div className="stats-grid">
        <div className="stat">
          <span className="value">{stats.total}</span>
          <span className="label">Total Predictions</span>
        </div>
        <div className="stat">
          <span className="value">{stats.breakthroughs}</span>
          <span className="label">Breakthroughs</span>
        </div>
        <div className="stat">
          <span className="value">{stats.subPpm}</span>
          <span className="label">Sub-ppm Precision</span>
        </div>
        <div className="stat">
          <span className="value">{stats.sub10Ppm}</span>
          <span className="label">Sub-10 ppm</span>
        </div>
        <div className="stat">
          <span className="value">{stats.sub100Ppm}</span>
          <span className="label">Sub-100 ppm</span>
        </div>
        <div className="stat">
          <span className="value">{stats.averagePrecision.toFixed(1)}</span>
          <span className="label">Average Error (ppm)</span>
        </div>
      </div>

      <h3>By Category</h3>
      <ul>
        <li>Leptons: {stats.categories.leptons}</li>
        <li>Quarks: {stats.categories.quarks}</li>
        <li>Bosons: {stats.categories.bosons}</li>
        <li>Constants: {stats.categories.constants}</li>
      </ul>
    </div>
  );
}

// ============================================================================
// Example 6: React Router Integration
// ============================================================================

/*
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

export function Example6_RouterIntegration() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/results">Results Dashboard</Link>
        <Link to="/results/table">Precision Table</Link>
        <Link to="/results/charts">Visualizations</Link>
        <Link to="/results/achievements">Achievements</Link>
      </nav>

      <Routes>
        <Route path="/results" element={<ResultsDashboard />} />
        <Route path="/results/table" element={<PrecisionTable results={goldenUniverseResults} />} />
        <Route path="/results/charts" element={<ResultsCharts results={goldenUniverseResults} />} />
        <Route path="/results/achievements" element={<AchievementCards achievements={achievements} />} />
      </Routes>
    </BrowserRouter>
  );
}
*/

// ============================================================================
// Example 7: Programmatic Data Access
// ============================================================================

export function Example7_ProgrammaticAccess() {
  // Access individual results
  const electronResult = goldenUniverseResults.find(r => r.id === 'electron-mass');
  console.log('Electron mass precision:', electronResult?.errorPpm, 'ppm');

  // Filter by precision level
  const excellentResults = goldenUniverseResults.filter(
    r => r.precision === 'excellent'
  );
  console.log('Excellent precision results:', excellentResults.length);

  // Find best precision
  const bestResult = goldenUniverseResults.reduce((best, current) =>
    Math.abs(current.errorPpm) < Math.abs(best.errorPpm) ? current : best
  );
  console.log('Best precision:', bestResult.name, '=', bestResult.errorPpm, 'ppm');

  // Calculate average precision by category
  const categoryAverages = ['leptons', 'quarks', 'bosons', 'constants'].map(cat => {
    const categoryResults = getResultsByCategory(cat);
    const avgPrecision = categoryResults.reduce(
      (sum, r) => sum + Math.abs(r.errorPpm),
      0
    ) / categoryResults.length;
    return { category: cat, average: avgPrecision };
  });
  console.log('Category averages:', categoryAverages);

  return (
    <div className="data-access-demo">
      <h2>Programmatic Data Access</h2>
      <p>Check console for examples</p>
    </div>
  );
}

// ============================================================================
// Example 8: Custom Styling
// ============================================================================

export function Example8_CustomStyling() {
  return (
    <div className="custom-themed-dashboard">
      {/* Override default styles with custom classes */}
      <style>{`
        .custom-themed-dashboard .results-dashboard {
          --primary-color: #00ff88;
          --secondary-color: #0088ff;
          background: linear-gradient(135deg, #0a0a1a 0%, #1a1a3a 100%);
        }

        .custom-themed-dashboard .precision-badge.excellent {
          background: var(--primary-color);
        }
      `}</style>

      <ResultsDashboard />
    </div>
  );
}

// ============================================================================
// Example 9: Mobile-Responsive Layout
// ============================================================================

export function Example9_MobileResponsive() {
  const [isMobile, setIsMobile] = React.useState(window.innerWidth < 768);

  React.useEffect(() => {
    const handleResize = () => setIsMobile(window.innerWidth < 768);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  if (isMobile) {
    return (
      <div className="mobile-layout">
        {/* Mobile-optimized view */}
        <h2>Results Summary</h2>
        <AchievementCards achievements={achievements.slice(0, 3)} />
        <ResultsCharts results={goldenUniverseResults.slice(0, 5)} />
      </div>
    );
  }

  return (
    <div className="desktop-layout">
      <ResultsDashboard />
    </div>
  );
}

// ============================================================================
// Example 10: Export Functionality
// ============================================================================

export function Example10_ExportFunctionality() {
  return (
    <div className="export-demo">
      <h2>Export Options</h2>
      <p>Export results in multiple formats:</p>

      <ExportOptions
        results={goldenUniverseResults}
        filename="my-custom-results"
      />

      {/* Standalone export for specific categories */}
      <section>
        <h3>Export Leptons Only</h3>
        <ExportOptions
          results={getResultsByCategory('leptons')}
          filename="lepton-results"
        />
      </section>

      <section>
        <h3>Export Breakthroughs Only</h3>
        <ExportOptions
          results={getBreakthroughResults()}
          filename="breakthrough-results"
        />
      </section>
    </div>
  );
}
