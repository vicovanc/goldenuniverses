/**
 * Visualization Gallery
 * Demo page showcasing all visualization components
 */

import React, { useState } from 'react';
import {
  WindingNumbersVisualization,
  PhaseSpaceVisualization,
  MemoryEvolutionVisualization,
  EpochLadderVisualization,
  FieldDynamicsVisualization,
  SymmetryBreakingVisualization,
} from './index';
import './VisualizationGallery.scss';

type VisualizationType =
  | 'winding'
  | 'phase'
  | 'memory'
  | 'epoch'
  | 'field'
  | 'symmetry';

interface VisualizationInfo {
  id: VisualizationType;
  name: string;
  description: string;
  component: React.ComponentType;
}

const VISUALIZATIONS: VisualizationInfo[] = [
  {
    id: 'symmetry',
    name: 'Symmetry Breaking',
    description:
      'Shows how perfect φ symmetry breaks to create particles through field perturbations',
    component: SymmetryBreakingVisualization,
  },
  {
    id: 'winding',
    name: 'Winding Numbers Torus',
    description:
      '3D torus with (p,q) winding paths showing particle topologies and resonance states',
    component: WindingNumbersVisualization,
  },
  {
    id: 'phase',
    name: 'Phase Space Trajectories',
    description:
      'Interactive 2D/3D phase space plots with multiple trajectory overlays and energy gradients',
    component: PhaseSpaceVisualization,
  },
  {
    id: 'memory',
    name: 'Memory Evolution',
    description: 'Time evolution of the memory integral M(t) with decay envelope',
    component: MemoryEvolutionVisualization,
  },
  {
    id: 'epoch',
    name: 'Epoch Ladder',
    description:
      'Animated descent through epochs N=0 to N=1000 showing particle formation timeline',
    component: EpochLadderVisualization,
  },
  {
    id: 'field',
    name: 'Field Dynamics',
    description: 'Real-time Omega field evolution with energy particles and field lines',
    component: FieldDynamicsVisualization,
  },
];

export function VisualizationGallery() {
  const [selected, setSelected] = useState<VisualizationType>('symmetry');
  const [isFullscreen, setIsFullscreen] = useState(false);

  const currentViz = VISUALIZATIONS.find((v) => v.id === selected);
  const VisualizationComponent = currentViz?.component;

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen();
      setIsFullscreen(true);
    } else {
      document.exitFullscreen();
      setIsFullscreen(false);
    }
  };

  return (
    <div className="visualization-gallery">
      <header className="gallery-header">
        <h1>Golden Universe Visualizations</h1>
        <p>Interactive 3D visualizations of the Golden Ratio universe theory</p>
      </header>

      <div className="gallery-container">
        <aside className="sidebar">
          <h2>Visualizations</h2>
          <nav className="viz-nav">
            {VISUALIZATIONS.map((viz) => (
              <button
                key={viz.id}
                className={`viz-button ${selected === viz.id ? 'active' : ''}`}
                onClick={() => setSelected(viz.id)}
              >
                <h3>{viz.name}</h3>
                <p>{viz.description}</p>
              </button>
            ))}
          </nav>

          <div className="controls-info">
            <h3>Controls</h3>
            <ul>
              <li>
                <strong>Mouse:</strong> Orbit (left), Pan (right), Zoom (scroll)
              </li>
              <li>
                <strong>Touch:</strong> One finger orbit, two finger pan/zoom
              </li>
              <li>
                <strong>GUI:</strong> Top-right panel for parameters
              </li>
            </ul>
          </div>
        </aside>

        <main className="visualization-main">
          <div className="visualization-header">
            <div className="viz-info">
              <h2>{currentViz?.name}</h2>
              <p>{currentViz?.description}</p>
            </div>
            <div className="viz-controls">
              <button className="control-button" onClick={toggleFullscreen}>
                {isFullscreen ? '📉 Exit Fullscreen' : '📈 Fullscreen'}
              </button>
            </div>
          </div>

          <div className="visualization-viewport">
            {VisualizationComponent && <VisualizationComponent />}
          </div>

          <div className="visualization-footer">
            <div className="physics-info">
              <h4>Physics Context</h4>
              {selected === 'symmetry' && (
                <p>
                  Perfect φ symmetry at N=0 breaks through perturbations creating particles.
                  Breaking strength determines particle masses through m = m₀φⁿ scaling.
                </p>
              )}
              {selected === 'winding' && (
                <p>
                  Winding numbers (p,q) classify particle topologies on the torus. Resonance k_res
                  = round(N/φ²) determines even (resonant) or odd (anti-resonant) states.
                </p>
              )}
              {selected === 'phase' && (
                <p>
                  Phase space coordinates (ρ, θ, π_ρ, π_θ) describe the complete state of the
                  system. Golden ratio frequency creates quasi-periodic orbits.
                </p>
              )}
              {selected === 'memory' && (
                <p>
                  Memory integral M(t) tracks energy flow over time. Exponential decay with
                  oscillations at golden ratio frequency φ.
                </p>
              )}
              {selected === 'epoch' && (
                <p>
                  Particles form at specific epochs as energy ladder descends. Each generation
                  appears at epochs related by φ scaling.
                </p>
              )}
              {selected === 'field' && (
                <p>
                  Omega field Ω(r,t) represents the fundamental quantum field. Wave packets travel
                  with group velocity determined by φ.
                </p>
              )}
            </div>

            <div className="performance-info">
              <h4>Performance</h4>
              <p>Target: 60 FPS | LOD: Automatic | GPU: WebGL 2.0</p>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

export default VisualizationGallery;
