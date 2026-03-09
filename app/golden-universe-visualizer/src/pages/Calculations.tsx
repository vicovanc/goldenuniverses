import React, { useState, useEffect, lazy, Suspense } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { CalculationRunner } from '@/components/Calculations/CalculationRunner';
import { ParticleMassCalculatorUI } from '@/components/Calculations/ParticleMassCalculator';
import LoadingFallback from '@/components/Common/LoadingFallback';
import './Calculations.scss';

// Temporarily disable lazy loading until components are created
// const ElectronMassCalculation = lazy(() => import('@/components/Calculations/ElectronMassCalculation'));
// const MuonMassCalculation = lazy(() => import('@/components/Calculations/MuonMassCalculation'));
// const TauMassCalculation = lazy(() => import('@/components/Calculations/TauMassCalculation'));
// const QuarkMassCalculation = lazy(() => import('@/components/Calculations/QuarkMassCalculation'));
// const NeutrinoMassCalculation = lazy(() => import('@/components/Calculations/NeutrinoMassCalculation'));
// const NewtonGCalculation = lazy(() => import('@/components/Calculations/NewtonGCalculation'));
// const FineStructureCalculation = lazy(() => import('@/components/Calculations/FineStructureCalculation'));
// const CouplingConstantsCalculation = lazy(() => import('@/components/Calculations/CouplingConstantsCalculation'));

type CalculationMode = 'runner' | 'particles' | 'specific';

const Calculations: React.FC = () => {
  const { '*': submenu } = useParams();
  const navigate = useNavigate();
  const [mode, setMode] = useState<CalculationMode>('particles');
  const [specificCalculation, setSpecificCalculation] = useState<string | null>(null);

  // Update mode based on URL parameter
  useEffect(() => {
    if (!submenu) {
      setMode('particles');
      setSpecificCalculation(null);
      return;
    }

    // Check for specific calculation routes
    const specificRoutes = {
      'electron-mass': 'electron',
      'muon-mass': 'muon',
      'tau-mass': 'tau',
      'up-quark': 'up',
      'down-quark': 'down',
      'charm-quark': 'charm',
      'strange-quark': 'strange',
      'top-quark': 'top',
      'bottom-quark': 'bottom',
      'neutrinos': 'neutrinos',
      'newton-g': 'newton-g',
      'fine-structure': 'fine-structure',
      'coupling-constants': 'coupling-constants',
      'alpha-em': 'alpha-em',
      'alpha-s': 'alpha-s',
      'alpha-w': 'alpha-w'
    };

    const foundRoute = Object.keys(specificRoutes).find(route => submenu.includes(route));

    if (foundRoute) {
      setMode('specific');
      setSpecificCalculation(specificRoutes[foundRoute as keyof typeof specificRoutes]);
    } else if (submenu === 'series' || submenu === 'runner') {
      setMode('runner');
      setSpecificCalculation(null);
    } else if (submenu === 'interactive' || submenu === 'particles' || submenu === 'particle-masses' || submenu === 'quick') {
      setMode('particles');
      setSpecificCalculation(null);
    }
  }, [submenu]);

  // Update URL when mode changes
  const handleModeChange = (newMode: 'runner' | 'particles') => {
    setMode(newMode);
    setSpecificCalculation(null);
    const path = newMode === 'particles' ? '/calculations/interactive' : '/calculations/series';
    navigate(path);
  };

  // Render specific calculation component
  const renderSpecificCalculation = () => {
    if (!specificCalculation) return null;

    // For now, just show the particle mass calculator for all specific calculations
    // until individual components are ready
    return <ParticleMassCalculatorUI />;

    // switch (specificCalculation) {
    //   case 'electron':
    //     return <ElectronMassCalculation />;
    //   case 'muon':
    //     return <MuonMassCalculation />;
    //   case 'tau':
    //     return <TauMassCalculation />;
    //   case 'up':
    //   case 'down':
    //   case 'charm':
    //   case 'strange':
    //   case 'top':
    //   case 'bottom':
    //     return <QuarkMassCalculation quarkType={specificCalculation} />;
    //   case 'neutrinos':
    //     return <NeutrinoMassCalculation />;
    //   case 'newton-g':
    //     return <NewtonGCalculation />;
    //   case 'fine-structure':
    //   case 'alpha-em':
    //     return <FineStructureCalculation />;
    //   case 'alpha-s':
    //   case 'alpha-w':
    //   case 'coupling-constants':
    //     return <CouplingConstantsCalculation type={specificCalculation} />;
    //   default:
    //     return <ParticleMassCalculatorUI />;
    // }
  };

  // Show specific calculation if mode is 'specific'
  if (mode === 'specific') {
    return (
      <div className="calculations-page">
        <Suspense fallback={<LoadingFallback />}>
          {renderSpecificCalculation()}
        </Suspense>
      </div>
    );
  }

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
