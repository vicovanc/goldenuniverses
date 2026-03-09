/**
 * Backend Python Executor Service
 * Executes Python code via the backend API instead of Pyodide in browser
 */

interface ExecutionResult {
  success: boolean;
  output?: string;
  error?: string;
  exitCode?: number;
  executionTime?: number;
}

interface JobStatus {
  id: number;
  status: 'pending' | 'running' | 'completed' | 'failed';
  result?: any;
  error?: string;
  progress?: number;
}

class BackendPythonExecutor {
  private apiBase: string;

  constructor() {
    // Use the backend API on port 3001 for development
    // In production (Vercel), use the /api routes
    if (import.meta.env.DEV) {
      this.apiBase = 'http://localhost:3001/api';
    } else if (import.meta.env.VITE_VERCEL || window.location.hostname.includes('vercel')) {
      // On Vercel, use serverless functions
      this.apiBase = '/api';
    } else {
      // Standard production with backend server
      this.apiBase = '/api';
    }
  }

  /**
   * Execute Python code via the backend
   */
  async execute(code: string, filename?: string): Promise<ExecutionResult> {
    try {
      // For now, directly execute the code using the exec endpoint
      const response = await fetch(`${this.apiBase}/python/exec`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code,
          filename: filename || 'script.py',
        }),
      });

      if (!response.ok) {
        const error = await response.text();
        throw new Error(`HTTP ${response.status}: ${error}`);
      }

      const data = await response.json();

      if (data.success) {
        return {
          success: true,
          output: data.data?.output || '',
          exitCode: data.data?.exitCode || 0,
          executionTime: data.data?.executionTime,
        };
      } else {
        return {
          success: false,
          error: data.error || 'Unknown error',
          exitCode: 1,
        };
      }
    } catch (error) {
      console.error('Backend execution error:', error);

      // Fallback to trying a simple fetch to check if server is running
      try {
        const healthCheck = await fetch(`${this.apiBase}/health`, {
          method: 'GET',
        }).catch(() => null);

        if (!healthCheck || !healthCheck.ok) {
          return {
            success: false,
            error: 'Backend server is not running. Please start the server with: npm run server:dev',
            exitCode: 1,
          };
        }
      } catch {
        // Server not reachable
      }

      return {
        success: false,
        error: error instanceof Error ? error.message : 'Failed to execute Python code',
        exitCode: 1,
      };
    }
  }

  /**
   * Execute a Python script file from the server
   */
  async executeFile(scriptPath: string, parameters?: Record<string, any>): Promise<ExecutionResult> {
    try {
      const response = await fetch(`${this.apiBase}/calculations/execute`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          scriptName: scriptPath,
          parameters: parameters || {},
        }),
      });

      if (!response.ok) {
        const error = await response.text();
        throw new Error(`HTTP ${response.status}: ${error}`);
      }

      const data = await response.json();

      if (data.success && data.data?.jobId) {
        // Poll for job completion
        return await this.pollJobStatus(data.data.jobId);
      } else {
        return {
          success: false,
          error: data.error || 'Failed to start execution',
          exitCode: 1,
        };
      }
    } catch (error) {
      console.error('Backend file execution error:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Failed to execute Python file',
        exitCode: 1,
      };
    }
  }

  /**
   * Poll for job completion
   */
  private async pollJobStatus(jobId: number, maxAttempts = 30): Promise<ExecutionResult> {
    for (let i = 0; i < maxAttempts; i++) {
      try {
        const response = await fetch(`${this.apiBase}/calculations/status/${jobId}`);

        if (!response.ok) {
          throw new Error(`Failed to get job status: ${response.status}`);
        }

        const data = await response.json();
        const job = data.data as JobStatus;

        if (job.status === 'completed') {
          return {
            success: true,
            output: JSON.stringify(job.result, null, 2),
            exitCode: 0,
          };
        } else if (job.status === 'failed') {
          return {
            success: false,
            error: job.error || 'Execution failed',
            exitCode: 1,
          };
        }

        // Wait before next poll
        await new Promise(resolve => setTimeout(resolve, 1000));
      } catch (error) {
        console.error('Polling error:', error);
      }
    }

    return {
      success: false,
      error: 'Execution timeout - job took too long',
      exitCode: 1,
    };
  }

  /**
   * Check if backend server is running
   */
  async isServerRunning(): Promise<boolean> {
    try {
      const response = await fetch(`${this.apiBase}/health`, {
        method: 'GET',
      }).catch(() => null);

      return response !== null && response.ok;
    } catch {
      return false;
    }
  }

  /**
   * Get server status with detailed info
   */
  async getServerStatus(): Promise<{ running: boolean; message: string }> {
    const running = await this.isServerRunning();

    if (running) {
      return {
        running: true,
        message: 'Backend server is running',
      };
    } else {
      return {
        running: false,
        message: 'Backend server is not running. Start it with: npm run server:dev',
      };
    }
  }
}

export const backendPythonExecutor = new BackendPythonExecutor();
export default backendPythonExecutor;