import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { CalculationRunner } from '@/components/Calculations/CalculationRunner';
import { ParticleMassCalculatorUI } from '@/components/Calculations/ParticleMassCalculator';
import './Calculations.scss';

type CalculationMode = 'runner' | 'particles';

const Calculations: React.FC = () => {
  const { '*': submenu } = useParams();
  const navigate = useNavigate();
  const [mode, setMode] = useState<CalculationMode>('particles');

  // Update mode based on URL parameter
  useEffect(() => {
    // Check if submenu is a particle mass calculation route
    const particleRoutes = ['interactive', 'particles', 'particle-masses', 'electron-mass', 'muon-mass', 'tau-mass',
      'up-quark', 'down-quark', 'charm-quark', 'strange-quark', 'top-quark', 'bottom-quark', 'neutrinos'];

    if (!submenu || particleRoutes.some(route => submenu.includes(route))) {
      setMode('particles');
    } else if (submenu === 'series' || submenu === 'runner') {
      setMode('runner');
    }
  }, [submenu]);

  // Update URL when mode changes
  const handleModeChange = (newMode: CalculationMode) => {
    setMode(newMode);
    const path = newMode === 'particles' ? '/calculations/interactive' : '/calculations/series';
    navigate(path);
  };

  return (
    <div className="calculations-page">
      <div className="page-header">
        <h1>Calculations Engine</h1>
        <p className="subtitle">Interactive Python-powered calculations for Golden Universe theory</p>
      </div>

      <div className="mode-selector">
        <button
          className={`mode-btn ${mode === 'particles' ? 'active' : ''}`}
          onClick={() => handleModeChange('particles')}
        >
          Particle Mass Calculator
        </button>
        <button
          className={`mode-btn ${mode === 'runner' ? 'active' : ''}`}
          onClick={() => handleModeChange('runner')}
        >
          Python Engine
        </button>
      </div>

      <div className="calculations-content">
        {mode === 'particles' && <ParticleMassCalculatorUI />}
        {mode === 'runner' && <CalculationRunner />}
      </div>
    </div>
  );
};

export default Calculations;
