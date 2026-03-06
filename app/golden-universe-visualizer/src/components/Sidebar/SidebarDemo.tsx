/**
 * SidebarDemo Component
 *
 * A standalone demo component for testing and showcasing the sidebar functionality.
 * This can be used in Storybook or as a standalone demo page.
 */

import React, { useState } from 'react';
import { BrowserRouter } from 'react-router-dom';
import { SidebarNew } from './index';
import { useSidebarStore } from './store';
import { useAppStore } from '@utils/store';

const SidebarControls: React.FC = () => {
  const {
    expandedSections,
    expandedItems,
    searchQuery,
    pinnedItems,
    recentItems,
    activeItemId,
    expandAll,
    collapseAll,
    reset,
  } = useSidebarStore();

  const { sidebarCollapsed, theme, toggleSidebar, setTheme } = useAppStore();

  return (
    <div className="sidebar-demo-controls">
      <h2>Sidebar Controls</h2>

      <div className="control-section">
        <h3>Global Controls</h3>
        <button onClick={toggleSidebar}>
          Toggle Sidebar {sidebarCollapsed ? '(Collapsed)' : '(Expanded)'}
        </button>
        <button onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}>
          Switch Theme (Current: {theme})
        </button>
      </div>

      <div className="control-section">
        <h3>Section Controls</h3>
        <button onClick={expandAll}>Expand All Sections</button>
        <button onClick={collapseAll}>Collapse All Sections</button>
        <button onClick={reset}>Reset All State</button>
      </div>

      <div className="control-section">
        <h3>Current State</h3>
        <div className="state-display">
          <div>
            <strong>Expanded Sections:</strong>
            <ul>
              {Array.from(expandedSections).map((id) => (
                <li key={id}>{id}</li>
              ))}
            </ul>
          </div>

          <div>
            <strong>Expanded Items:</strong>
            <ul>
              {Array.from(expandedItems).map((id) => (
                <li key={id}>{id}</li>
              ))}
            </ul>
          </div>

          <div>
            <strong>Search Query:</strong>
            <p>{searchQuery || '(none)'}</p>
          </div>

          <div>
            <strong>Pinned Items ({pinnedItems.length}):</strong>
            <ul>
              {pinnedItems.map((id) => (
                <li key={id}>{id}</li>
              ))}
            </ul>
          </div>

          <div>
            <strong>Recent Items ({recentItems.length}):</strong>
            <ul>
              {recentItems.slice(0, 5).map((id) => (
                <li key={id}>{id}</li>
              ))}
            </ul>
          </div>

          <div>
            <strong>Active Item:</strong>
            <p>{activeItemId || '(none)'}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

const SidebarDemo: React.FC = () => {
  const [showControls, setShowControls] = useState(true);

  return (
    <BrowserRouter>
      <div className="sidebar-demo">
        <SidebarNew />

        <main className="sidebar-demo-main">
          <div className="demo-header">
            <h1>ContextLoom-Style Sidebar Demo</h1>
            <button
              className="toggle-controls-btn"
              onClick={() => setShowControls(!showControls)}
            >
              {showControls ? 'Hide' : 'Show'} Controls
            </button>
          </div>

          <div className="demo-content">
            <section className="demo-section">
              <h2>Features</h2>
              <ul>
                <li>✅ Hierarchical tree structure with 6 main sections</li>
                <li>✅ 39 Laws organized in collapsible groups</li>
                <li>✅ 41 Derivation folders with PDF badges</li>
                <li>✅ Particle mass calculations with checkmarks</li>
                <li>✅ Interactive visualizations</li>
                <li>✅ Comprehensive explanations</li>
                <li>✅ Results and achievements tracking</li>
              </ul>
            </section>

            <section className="demo-section">
              <h2>Keyboard Shortcuts</h2>
              <table>
                <thead>
                  <tr>
                    <th>Shortcut</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><kbd>⌘</kbd> + <kbd>K</kbd></td>
                    <td>Focus search</td>
                  </tr>
                  <tr>
                    <td><kbd>⌘</kbd> + <kbd>⇧</kbd> + <kbd>E</kbd></td>
                    <td>Expand all sections</td>
                  </tr>
                  <tr>
                    <td><kbd>⌘</kbd> + <kbd>⇧</kbd> + <kbd>C</kbd></td>
                    <td>Collapse all sections</td>
                  </tr>
                  <tr>
                    <td><kbd>↑</kbd> / <kbd>↓</kbd></td>
                    <td>Navigate items</td>
                  </tr>
                  <tr>
                    <td><kbd>Enter</kbd></td>
                    <td>Select item</td>
                  </tr>
                  <tr>
                    <td><kbd>Esc</kbd></td>
                    <td>Clear search</td>
                  </tr>
                </tbody>
              </table>
            </section>

            <section className="demo-section">
              <h2>Try These Actions</h2>
              <ol>
                <li>Click on "THEORY" to expand the section</li>
                <li>Expand "Laws 1-10: Core Principles" to see nested items</li>
                <li>Search for "electron" to see auto-expansion</li>
                <li>Hover over items to see tooltips</li>
                <li>Click the pin button (📍) to pin an item</li>
                <li>Use keyboard shortcuts to navigate</li>
                <li>Toggle the sidebar collapse/expand</li>
                <li>Check the state display to see real-time updates</li>
              </ol>
            </section>

            <section className="demo-section">
              <h2>Navigation Hierarchy</h2>
              <pre>{`
📚 THEORY (39 Laws total)
├── Law 0: Foundational Symmetry
├── Laws 1-10: Core Principles
│   ├── Law 1: Quantum Action
│   ├── Law 2: Phase Structure
│   └── ... (8 more)
├── Laws 11-20: Field Dynamics
├── Laws 21-30: Gravitational Theory
├── Laws 31-38: Advanced Topics
├── Lagrangian Structure
├── Field Equations
└── Symmetry Breaking

🧪 DERIVATIONS (41 folders)
├── 01: Force Unification [PDF]
├── 02: Mass Spectrum [PDF]
└── ... (39 more)

💫 CALCULATIONS
├── Quick Calculate ⚡
├── Particle Masses
│   ├── Electron Mass ✓
│   ├── Muon Mass ✓
│   └── ... (8 more)
├── Newton's G ✓
├── Fine Structure α ✓
└── Coupling Constants

📊 VISUALIZATIONS
├── Winding Numbers 🌀
├── Phase Space 🎯
├── Memory Evolution 🧠
└── ... (3 more)

📝 EXPLANATIONS
├── What is the Electron? ⚛️
├── What is Gravity? 🌍
└── ... (4 more)

📈 RESULTS
├── Precision Table [NEW]
├── Comparison Charts
├── Key Achievements [15]
└── Predictions [TESTABLE]
              `}</pre>
            </section>
          </div>

          {showControls && <SidebarControls />}
        </main>
      </div>

      <style>{`
        .sidebar-demo {
          display: flex;
          height: 100vh;
          background: #0a0a0a;
          color: #e0e0e0;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        .sidebar-demo-main {
          flex: 1;
          margin-left: 320px;
          overflow-y: auto;
          padding: 2rem;
          transition: margin-left 0.3s ease;
        }

        .sidebar-collapsed .sidebar-demo-main {
          margin-left: 70px;
        }

        .demo-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 2rem;
          padding-bottom: 1rem;
          border-bottom: 1px solid rgba(201, 168, 78, 0.2);
        }

        .demo-header h1 {
          background: linear-gradient(135deg, #c9a84e 0%, #ffd700 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
          margin: 0;
        }

        .toggle-controls-btn {
          padding: 0.5rem 1rem;
          background: rgba(201, 168, 78, 0.1);
          border: 1px solid rgba(201, 168, 78, 0.3);
          border-radius: 4px;
          color: #c9a84e;
          cursor: pointer;
          transition: all 0.15s ease;
        }

        .toggle-controls-btn:hover {
          background: rgba(201, 168, 78, 0.2);
        }

        .demo-content {
          max-width: 900px;
        }

        .demo-section {
          background: rgba(26, 26, 26, 0.5);
          border: 1px solid rgba(201, 168, 78, 0.15);
          border-radius: 8px;
          padding: 1.5rem;
          margin-bottom: 1.5rem;
        }

        .demo-section h2 {
          color: #c9a84e;
          margin-top: 0;
          margin-bottom: 1rem;
        }

        .demo-section ul,
        .demo-section ol {
          line-height: 1.8;
        }

        .demo-section pre {
          background: #0a0a0a;
          border: 1px solid rgba(201, 168, 78, 0.2);
          border-radius: 4px;
          padding: 1rem;
          overflow-x: auto;
          font-size: 0.9rem;
          line-height: 1.6;
        }

        .demo-section table {
          width: 100%;
          border-collapse: collapse;
        }

        .demo-section th,
        .demo-section td {
          padding: 0.75rem;
          text-align: left;
          border-bottom: 1px solid rgba(201, 168, 78, 0.1);
        }

        .demo-section th {
          color: #c9a84e;
          font-weight: 600;
        }

        .demo-section kbd {
          display: inline-block;
          padding: 0.2rem 0.5rem;
          background: rgba(0, 0, 0, 0.3);
          border: 1px solid rgba(201, 168, 78, 0.3);
          border-radius: 3px;
          font-family: monospace;
          font-size: 0.85rem;
        }

        .sidebar-demo-controls {
          background: rgba(26, 26, 26, 0.5);
          border: 1px solid rgba(201, 168, 78, 0.15);
          border-radius: 8px;
          padding: 1.5rem;
          margin-top: 2rem;
        }

        .sidebar-demo-controls h2 {
          color: #c9a84e;
          margin-top: 0;
          margin-bottom: 1.5rem;
        }

        .control-section {
          margin-bottom: 1.5rem;
        }

        .control-section h3 {
          color: #ffd700;
          font-size: 1rem;
          margin-bottom: 0.75rem;
        }

        .control-section button {
          padding: 0.5rem 1rem;
          margin: 0.25rem;
          background: rgba(201, 168, 78, 0.1);
          border: 1px solid rgba(201, 168, 78, 0.3);
          border-radius: 4px;
          color: #c9a84e;
          cursor: pointer;
          transition: all 0.15s ease;
          font-size: 0.9rem;
        }

        .control-section button:hover {
          background: rgba(201, 168, 78, 0.2);
        }

        .state-display {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 1rem;
          margin-top: 1rem;
        }

        .state-display > div {
          background: rgba(0, 0, 0, 0.3);
          border: 1px solid rgba(201, 168, 78, 0.2);
          border-radius: 4px;
          padding: 1rem;
        }

        .state-display strong {
          color: #ffd700;
          display: block;
          margin-bottom: 0.5rem;
        }

        .state-display ul {
          list-style: none;
          padding: 0;
          margin: 0;
          max-height: 150px;
          overflow-y: auto;
        }

        .state-display li {
          padding: 0.25rem 0;
          font-size: 0.85rem;
          color: rgba(224, 224, 224, 0.8);
          font-family: monospace;
        }

        .state-display p {
          margin: 0;
          font-family: monospace;
          color: rgba(224, 224, 224, 0.8);
        }

        @media (max-width: 768px) {
          .sidebar-demo-main {
            margin-left: 0;
            padding: 1rem;
          }

          .demo-header {
            flex-direction: column;
            align-items: flex-start;
            gap: 1rem;
          }
        }
      `}</style>
    </BrowserRouter>
  );
};

export default SidebarDemo;
