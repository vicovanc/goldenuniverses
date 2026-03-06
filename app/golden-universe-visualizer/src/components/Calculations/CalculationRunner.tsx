/**
 * CalculationRunner - Main interface for running Python calculations
 * Features code editor, preset selection, and real-time execution
 */

import React, { useState, useEffect } from 'react';
import { getPythonEngine } from '../../services/pythonEngine/pythonEngine';
import type {
  CalculationResult,
  PythonEngineStatus,
} from '../../services/pythonEngine/pythonTypes';
import {
  PRESET_CALCULATIONS,
  getPresetById,
  getPresetsByCategory,
  getFeaturedPresets,
} from '../../data/calculations/presetCalculations';
import './CalculationRunner.scss';

export const CalculationRunner: React.FC = () => {
  const [code, setCode] = useState<string>('# Enter Python code or select a preset\n');
  const [result, setResult] = useState<CalculationResult | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [engineStatus, setEngineStatus] = useState<PythonEngineStatus>({
    ready: false,
    loading: false,
    loadedPackages: [],
  });
  const [selectedPreset, setSelectedPreset] = useState<string>('');

  const engine = getPythonEngine();

  useEffect(() => {
    // Subscribe to engine status
    const unsubscribe = engine.onStatusChange(status => {
      setEngineStatus(status);
    });

    // Initialize engine
    engine.initialize().catch(err => {
      console.error('Failed to initialize Python engine:', err);
    });

    return unsubscribe;
  }, []);

  const handleRun = async () => {
    if (!engineStatus.ready || isRunning) return;

    setIsRunning(true);
    setResult(null);

    try {
      const calcResult = await engine.execute(code);
      setResult(calcResult);
    } catch (error) {
      setResult({
        success: false,
        error: error instanceof Error ? error.message : String(error),
        executionTime: 0,
        timestamp: Date.now(),
      });
    } finally {
      setIsRunning(false);
    }
  };

  const handlePresetSelect = (presetId: string) => {
    const preset = getPresetById(presetId);
    if (!preset) return;

    setSelectedPreset(presetId);

    if (preset.input.code) {
      setCode(preset.input.code);
    } else {
      // Generate code from preset params
      const generatedCode = generateCodeFromPreset(preset);
      setCode(generatedCode);
    }
  };

  const generateCodeFromPreset = (preset: typeof PRESET_CALCULATIONS[0]): string => {
    const { type, params } = preset.input;

    switch (type) {
      case 'particle_mass':
        return `# Calculate ${params.particle} mass
result = calculate_electron_mass(NU_E)
to_json(result)`;

      case 'constant':
        if (params.constant === 'G') {
          return `# Calculate Newton's G
result = calculate_newtons_g()
to_json(result)`;
        } else if (params.constant === 'alpha') {
          return `# Calculate fine structure constant
result = calculate_fine_structure()
to_json(result)`;
        }
        break;

      case 'resonance':
        return `# Find resonances
N_min = ${params.N_min}
N_max = ${params.N_max}

resonances = []
phi_sq = PHI ** 2

for N in range(N_min, N_max + 1):
    k_res, delta = calculate_resonance(N, phi_sq)
    if abs(delta) < 0.5:
        resonances.append({
            'N': N,
            'k_res': int(k_res),
            'delta': str(delta)
        })

to_json({'resonances': resonances})`;

      case 'winding':
        return `# Calculate winding numbers
N = ${params.N}

# Find optimal (p,q)
min_action = float('inf')
optimal = None

for p in range(-N, N+1):
    q = N - abs(p)
    if q >= 0:
        l_omega = calculate_winding_length(p, q)
        if l_omega < min_action:
            min_action = l_omega
            optimal = {'p': p, 'q': q, 'l_Omega': str(l_omega)}

to_json(optimal)`;
    }

    return '# Custom calculation\n';
  };

  const formatExecutionTime = (ms: number): string => {
    if (ms < 1000) return `${ms.toFixed(0)}ms`;
    return `${(ms / 1000).toFixed(2)}s`;
  };

  const featuredPresets = getFeaturedPresets();
  const allPresets = PRESET_CALCULATIONS;

  return (
    <div className="calculation-runner">
      <div className="runner-header">
        <h2>Python Calculation Engine</h2>
        <div className="status-indicator">
          {engineStatus.loading && <span className="status loading">Loading...</span>}
          {engineStatus.ready && <span className="status ready">Ready</span>}
          {engineStatus.error && (
            <span className="status error">Error: {engineStatus.error}</span>
          )}
        </div>
      </div>

      <div className="runner-content">
        {/* Preset Selection */}
        <div className="preset-section">
          <h3>Preset Calculations</h3>
          <div className="preset-tabs">
            <button className="tab active">Featured</button>
            <button className="tab">All</button>
            <button className="tab">Particles</button>
            <button className="tab">Constants</button>
            <button className="tab">Advanced</button>
          </div>
          <div className="preset-list">
            {featuredPresets.map(preset => (
              <button
                key={preset.id}
                className={`preset-item ${selectedPreset === preset.id ? 'selected' : ''}`}
                onClick={() => handlePresetSelect(preset.id)}
              >
                <div className="preset-name">{preset.name}</div>
                <div className="preset-description">{preset.description}</div>
                <div className="preset-tags">
                  {preset.tags.slice(0, 3).map(tag => (
                    <span key={tag} className="tag">
                      {tag}
                    </span>
                  ))}
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Code Editor */}
        <div className="editor-section">
          <div className="editor-header">
            <h3>Python Code</h3>
            <div className="editor-actions">
              <button
                className="btn-secondary"
                onClick={() => setCode('')}
                disabled={isRunning}
              >
                Clear
              </button>
              <button
                className="btn-primary"
                onClick={handleRun}
                disabled={!engineStatus.ready || isRunning}
              >
                {isRunning ? 'Running...' : 'Run'}
              </button>
            </div>
          </div>
          <textarea
            className="code-editor"
            value={code}
            onChange={e => setCode(e.target.value)}
            placeholder="Enter Python code here..."
            spellCheck={false}
            disabled={isRunning}
          />
        </div>

        {/* Results Display */}
        {result && (
          <div className="results-section">
            <div className="results-header">
              <h3>Results</h3>
              <span className="execution-time">
                {formatExecutionTime(result.executionTime)}
              </span>
            </div>

            {result.success ? (
              <div className="results-content">
                <pre className="result-json">
                  {JSON.stringify(result.result, null, 2)}
                </pre>
              </div>
            ) : (
              <div className="results-error">
                <div className="error-message">{result.error}</div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Help Section */}
      <div className="help-section">
        <h4>Available Constants & Functions</h4>
        <div className="help-grid">
          <div className="help-item">
            <strong>Constants:</strong>
            <code>PHI, PI, E, PHI_SQ, M_P_MeV, N_E, DELTA_E</code>
          </div>
          <div className="help-item">
            <strong>Functions:</strong>
            <code>
              calculate_electron_mass(), calculate_newtons_g(),
              calculate_fine_structure()
            </code>
          </div>
          <div className="help-item">
            <strong>Precision:</strong>
            <code>mp.dps = 50</code> (50 decimal places)
          </div>
        </div>
      </div>
    </div>
  );
};
