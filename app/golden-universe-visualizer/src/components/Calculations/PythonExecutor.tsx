/**
 * PythonExecutor - Execute Python code and display results
 * Used for derivations and calculations
 */

import React, { useState, useEffect } from 'react';
import { getPythonEngine } from '@/services/pythonEngine';
import './PythonExecutor.scss';

interface PythonExecutorProps {
  code: string;
  autoRun?: boolean;
  title?: string;
  showCode?: boolean;
}

export const PythonExecutor: React.FC<PythonExecutorProps> = ({
  code,
  autoRun = false,
  title = 'Python Calculation',
  showCode = true,
}) => {
  const [output, setOutput] = useState<string>('');
  const [error, setError] = useState<string | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [engineReady, setEngineReady] = useState(false);

  // Format output to add line breaks between terms
  const formatOutput = (text: string): string => {
    // First, add line breaks before capital letters that come after numbers/scientific notation
    // This handles cases like "3.5710002800e+03Coupling:" -> "3.5710002800e+03\nCoupling:"
    let formatted = text.replace(/([0-9]|[0-9]e[+-][0-9]+)([A-Z])/g, '$1\n$2');

    // Also add line breaks before common term patterns
    // Handle patterns like "term: value" when they're concatenated
    formatted = formatted.replace(/([\d.e+-]+)([A-Z][a-z]+\s*term:)/g, '$1\n$2');

    // Handle "Total" or "Final" patterns that might be concatenated
    formatted = formatted.replace(/([\d.e+-]+)(Total|Final)/g, '$1\n$2');

    // Clean up any double line breaks that might have been introduced
    formatted = formatted.replace(/\n\n+/g, '\n');

    return formatted;
  };

  useEffect(() => {
    // Check if Python engine is ready
    const engine = getPythonEngine();
    const unsubscribe = engine.onStatusChange((status) => {
      setEngineReady(status.ready);
    });

    // Check initial status
    setEngineReady(engine.getStatus().ready);

    return unsubscribe;
  }, []);

  useEffect(() => {
    if (autoRun && engineReady && code) {
      executeCode();
    }
  }, [autoRun, engineReady, code]);

  const executeCode = async () => {
    if (!code.trim()) {
      setError('No code to execute');
      return;
    }

    setIsRunning(true);
    setError(null);
    setOutput('');

    try {
      const engine = getPythonEngine();
      const result = await engine.execute(code);

      if (result.result) {
        setOutput(JSON.stringify(result.result, null, 2));
      } else if (result.success) {
        setOutput('Calculation completed successfully');
      } else {
        setOutput('No output available');
      }
    } catch (err) {
      console.error('Python execution error:', err);
      setError(err instanceof Error ? err.message : 'Unknown error occurred');
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="python-executor">
      <div className="executor-header">
        <h4>{title}</h4>
        {!autoRun && (
          <button
            className="run-button"
            onClick={executeCode}
            disabled={isRunning || !engineReady}
          >
            {isRunning ? 'Running...' : engineReady ? 'Run Code' : 'Loading Python...'}
          </button>
        )}
      </div>

      {showCode && (
        <div className="code-section">
          <h5>Python Code</h5>
          <pre className="code-block">
            <code>{code}</code>
          </pre>
        </div>
      )}

      {(output || error || isRunning) && (
        <div className="output-section">
          <h5>Output</h5>
          {isRunning && (
            <div className="loading-spinner">
              <div className="spinner"></div>
              <span>Executing Python code...</span>
            </div>
          )}
          {error && (
            <div className="error-output">
              <strong>Error:</strong>
              <pre>{error}</pre>
            </div>
          )}
          {output && !isRunning && (
            <pre className="output-block">
              <code>{formatOutput(output)}</code>
            </pre>
          )}
        </div>
      )}

      {!engineReady && !isRunning && (
        <div className="status-message">
          <div className="status-icon">⏳</div>
          <p>Python engine is initializing... This may take a moment.</p>
        </div>
      )}
    </div>
  );
};
