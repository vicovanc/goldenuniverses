import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { TheoryLaw } from '@/types/theory';
import { getLawById, theoryLaws } from '@/data/theoryLaws';
import LawsBrowser from './LawsBrowser';
import LawDetail from './LawDetail';
import DependencyGraph from './DependencyGraph';
import LagrangianExplorer from './LagrangianExplorer';
import TheoryDocViewer from './TheoryDocViewer';
import './TheoryExplorer.scss';

type ViewMode = 'browser' | 'detail' | 'graph' | 'lagrangian' | 'document';

const TheoryExplorer: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [viewMode, setViewMode] = useState<ViewMode>('browser');
  const [selectedLaw, setSelectedLaw] = useState<TheoryLaw | null>(null);

  // Handle URL changes from sidebar navigation
  useEffect(() => {
    const path = location.pathname;

    // Match patterns like /theory/law-1, /theory/law-0, etc.
    const lawMatch = path.match(/\/theory\/law-(\d+)/);
    if (lawMatch) {
      const lawId = parseInt(lawMatch[1], 10);
      const law = getLawById(lawId);
      if (law) {
        setSelectedLaw(law);
        setViewMode('detail');
        return;
      }
    }

    // Match patterns like /theory/laws-1-10, etc.
    const lawsRangeMatch = path.match(/\/theory\/laws-(\d+)-(\d+)/);
    if (lawsRangeMatch) {
      const startId = parseInt(lawsRangeMatch[1], 10);
      const law = getLawById(startId);
      if (law) {
        setSelectedLaw(law);
        setViewMode('detail');
        return;
      }
    }

    // Handle specific views
    if (path.includes('/theory/lagrangian')) {
      setViewMode('lagrangian');
    } else if (path.includes('/theory/field-equations')) {
      setViewMode('document');
    } else if (path.includes('/theory/symmetry-breaking')) {
      setViewMode('document');
    } else if (path === '/theory' || path === '/theory/') {
      setViewMode('browser');
      setSelectedLaw(null);
    }
  }, [location.pathname]);

  const handleSelectLaw = (law: TheoryLaw) => {
    setSelectedLaw(law);
    setViewMode('detail');
    // Update URL to reflect the selection
    navigate(`/theory/law-${law.id}`);
  };

  const handleNavigateToLaw = (lawId: number) => {
    const law = getLawById(lawId);
    if (law) {
      handleSelectLaw(law);
    }
  };

  const renderMainContent = () => {
    switch (viewMode) {
      case 'browser':
        return <LawsBrowser onSelectLaw={handleSelectLaw} selectedLawId={selectedLaw?.id} />;

      case 'detail':
        return selectedLaw ? <LawDetail law={selectedLaw} onNavigate={handleNavigateToLaw} /> : <div>No law selected</div>;

      case 'graph':
        return <DependencyGraph onSelectLaw={handleNavigateToLaw} highlightLawId={selectedLaw?.id} />;

      case 'lagrangian':
        return <LagrangianExplorer onNavigateToLaw={handleNavigateToLaw} />;

      case 'document':
        return (
          <TheoryDocViewer
            initialContent={`
# Golden Universe Theory - Complete Documentation

## Overview

The Golden Universe theory is a comprehensive framework that derives fundamental physics from the golden ratio (φ) and related mathematical constants (π, e). This theory encompasses 38 foundational laws that describe the universe from action principles to particle masses.

## Key Achievements

### Validated Predictions
- **Electron Mass**: Predicted m_e = 0.510121 MeV (0.17% error from experimental 0.511 MeV)
- **Epoch Number**: N_e = 111 derived from geometric resonance
- **Geometric Factor**: C_e = 1.050774 (O(1) as predicted)

### Zero-Parameter Framework
The theory operates as a zero-parameter framework when the electron mass is used as a boundary condition. Both Route-A (elliptic integral) and Route-B (Gel'fand-Yaglom) approaches have been validated.

## Theory Structure

The theory is organized into four major categories:

### Foundation Laws (0-5)
- Action principle and Lagrangian decomposition
- Substrate, cosmic driver, interaction, and gauge sectors
- Establishes the fundamental mathematical framework

### Symmetry Laws (6-15)
- X-dependent potential coefficients
- Symmetry-breaking cascade
- Fermionic sector and NLDE
- Phase driver and angular modulation

### Particle Laws (16-25)
- Electron as soliton
- Mass from energy functional
- Lepton hierarchy
- Golden impulse and canonical conventions

### Advanced Laws (26-38)
- Route-A elliptic closure
- Route-B Gel'fand-Yaglom closure
- Three μ scales reconciliation
- High-precision values
- Zero-parameter classification

## Lagrangian Structure

The total master Lagrangian decomposes into six fundamental terms:

1. **L_Ω**: Substrate dynamics (kinetic, potential, phase driver, memory)
2. **L_X**: Cosmic driver dynamics
3. **L_int**: Ω-X interaction coupling
4. **L_gauge**: Yang-Mills gauge sector
5. **L_lock**: Angular modulation lock potential
6. **L_mem**: Memory energy binding

## Mathematical Constants

All values computed to 50-digit precision:
- φ = 1.6180339887498948482045868343656381177203091798058
- π = 3.1415926535897932384626433832795028841971693993751
- e = 2.7182818284590452353602874713526624977572470937000
- λ_rec/β = e^φ/π² = 0.51097951228960997824303381840723004398203106664718

## Python Implementation

The theory includes comprehensive Python implementations:
- derive_Xe_corrected.py: X_e derivation
- nlde_dimensionless.py: NLDE solver (5/5 Yukawa tests passed)
- Complete calculation pipeline from action to electron mass

## References

See the complete theory-laws.md document for full mathematical derivations, proofs, and detailed explanations of all 38 laws.
          `}
          />
        );

      default:
        return <div>Unknown view mode</div>;
    }
  };

  return (
    <div className="theory-explorer">
      {/* Header */}
      <div className="explorer-header">
        <h1 className="explorer-title">Golden Universe Theory Explorer</h1>
        <p className="explorer-subtitle">Interactive exploration of 38 fundamental theory laws</p>
      </div>

      {/* Navigation Bar */}
      <div className="explorer-nav">
        <button
          className={`nav-button ${viewMode === 'browser' ? 'active' : ''}`}
          onClick={() => setViewMode('browser')}
          aria-label="Laws Browser"
        >
          <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
            <path d="M2 4h16v2H2V4zm0 5h16v2H2V9zm0 5h16v2H2v-2z" />
          </svg>
          <span>Laws Browser</span>
        </button>

        <button
          className={`nav-button ${viewMode === 'detail' ? 'active' : ''}`}
          onClick={() => {
            if (selectedLaw) setViewMode('detail');
          }}
          disabled={!selectedLaw}
          aria-label="Law Detail"
        >
          <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
            <path d="M4 2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2zm1 3v2h10V5H5zm0 4v2h10V9H5zm0 4v2h7v-2H5z" />
          </svg>
          <span>Law Detail</span>
        </button>

        <button
          className={`nav-button ${viewMode === 'graph' ? 'active' : ''}`}
          onClick={() => setViewMode('graph')}
          aria-label="Dependency Graph"
        >
          <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
            <circle cx="5" cy="5" r="3" />
            <circle cx="15" cy="5" r="3" />
            <circle cx="5" cy="15" r="3" />
            <circle cx="15" cy="15" r="3" />
            <line x1="7" y1="6" x2="13" y2="6" stroke="currentColor" strokeWidth="1.5" />
            <line x1="6" y1="7" x2="6" y2="13" stroke="currentColor" strokeWidth="1.5" />
            <line x1="14" y1="7" x2="14" y2="13" stroke="currentColor" strokeWidth="1.5" />
            <line x1="7" y1="14" x2="13" y2="14" stroke="currentColor" strokeWidth="1.5" />
          </svg>
          <span>Dependencies</span>
        </button>

        <button
          className={`nav-button ${viewMode === 'lagrangian' ? 'active' : ''}`}
          onClick={() => setViewMode('lagrangian')}
          aria-label="Lagrangian Explorer"
        >
          <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
            <path d="M10 2l8 6v8l-8 6-8-6V8l8-6zm0 2.5L4 9v6l6 4.5 6-4.5V9l-6-4.5z" />
          </svg>
          <span>Lagrangian</span>
        </button>

        <button
          className={`nav-button ${viewMode === 'document' ? 'active' : ''}`}
          onClick={() => setViewMode('document')}
          aria-label="Documentation"
        >
          <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
            <path d="M4 2h8l4 4v10a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2zm1 3v2h6V5H5zm0 4v2h10V9H5zm0 4v2h10v-2H5z" />
          </svg>
          <span>Documentation</span>
        </button>
      </div>

      {/* Main Content Area - Full Width */}
      <div className="explorer-content">
        {/* Main View */}
        <main className="explorer-main">{renderMainContent()}</main>
      </div>
    </div>
  );
};

export default TheoryExplorer;
