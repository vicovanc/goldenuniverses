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

      // Priority: output (stdout) > result (return value)
      if (result.output && result.output.trim()) {
        // Use captured stdout
        setOutput(result.output);
      } else if (result.result) {
        // Fallback to result if no stdout but there's a return value
        const output = typeof result.result === 'string'
          ? result.result
          : JSON.stringify(result.result, null, 2);
        setOutput(output);
      } else if (result.success) {
        // Execution succeeded but produced no output
        setOutput('Execution completed (no output captured)');
      } else {
        setOutput('No output available');
      }
    } catch (err: any) {
      console.error('Python execution error:', err);

      // Parse the error to provide a friendly message
      const errorMessage = err instanceof Error ? err.message : (err?.error || String(err));
      const errorString = String(err); // Full error string including stack trace
      const hint = err?.hint; // Worker may provide a hint

      // Check for file import errors (trying to import other .py files)
      if (errorMessage.includes('FileNotFoundError') ||
          errorString.includes('FileNotFoundError') ||
          errorMessage.includes('No such file or directory') && errorMessage.includes('.py')) {
        // Extract file path if available
        const fileMatch = errorMessage.match(/['"]([^'"]*\.py)['"]/);
        const fileName = fileMatch ? fileMatch[1] : 'Python module file';

        setError(`📁 This script imports other Python files from the file system.\n\n` +
          `Missing file: "${fileName}"\n\n` +
          `This script has dependencies on other Python modules in the repository that ` +
          `are not available in the browser environment.\n\n` +
          `To run this script:\n` +
          `• Clone the Golden Universe repository\n` +
          `• Ensure all required files are in place\n` +
          `• Run the script locally in Python\n\n` +
          `You can still view the source code above to understand the derivation.`);
      }
      // Check for subprocess/process errors (check both message and full string)
      else if (errorMessage.includes('subprocess') ||
          errorMessage.includes('emscripten does not support processes') ||
          errorMessage.includes('Subprocess detected') ||
          errorString.includes('subprocess') ||
          errorString.includes('emscripten does not support processes') ||
          errorString.includes('OSError: [Errno 138]') ||
          hint?.includes('subprocess')) {
        setError(`⚙️ This script uses subprocesses which are not supported in the browser.\n\n` +
          `This script is an orchestrator that runs other Python scripts, which requires:\n` +
          `• A full Python environment\n` +
          `• Access to the file system\n` +
          `• Process execution capabilities\n\n` +
          `To run this script:\n` +
          `• Clone the Golden Universe repository\n` +
          `• Install Python dependencies\n` +
          `• Run the script in your terminal\n\n` +
          `You can still view the source code above to understand how the derivation works.`);
      }
      // Check for missing module errors
      else if (errorMessage.includes('ModuleNotFoundError') || errorMessage.includes('No module named')) {
        // Extract module name
        const moduleMatch = errorMessage.match(/No module named ['"]?([^'"]+)['"]?/);
        const moduleName = moduleMatch ? moduleMatch[1] : 'unknown';

        // Check if it's a custom module (not available in browser)
        const customModules = ['nn_redo_common', 'gu_constants', 'gu_common', 'common', 'utils'];
        const isCustomModule = customModules.some(mod => moduleName.includes(mod));

        if (isCustomModule) {
          setError(`📦 This script requires custom modules that are not available in the browser.\n\n` +
            `Missing module: "${moduleName}"\n\n` +
            `This script is designed to run in a full Python environment with access to the Golden Universe codebase. ` +
            `To run this script:\n` +
            `• Clone the repository\n` +
            `• Install Python dependencies\n` +
            `• Run the script locally\n\n` +
            `You can still view the source code above to understand the derivation.`);
        } else {
          setError(`📦 This script requires the "${moduleName}" package which is not currently loaded.\n\n` +
            `This package may be available in Pyodide but is not pre-loaded for performance reasons.\n\n` +
            `You can still view the source code above to understand the derivation.`);
        }
      } else {
        setError(errorMessage);
      }
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
            <div className={error.includes('📦') || error.includes('⚙️') || error.includes('📁') ? 'info-output' : 'error-output'}>
              <strong>{error.includes('📦') || error.includes('⚙️') || error.includes('📁') ? 'Information:' : 'Error:'}</strong>
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
