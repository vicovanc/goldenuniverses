import { Request, Response } from 'express';
import { spawn } from 'child_process';
import { AppError, asyncHandler } from '../middleware/errorHandler';
import * as path from 'path';
import * as fs from 'fs';
import * as os from 'os';

export const pythonController = {
  /**
   * Execute Python code directly
   */
  exec: asyncHandler(async (req: Request, res: Response) => {
    const { code, filename = 'script.py' } = req.body;

    if (!code) {
      throw new AppError('No code provided', 400);
    }

    try {
      // Create a temporary file for the Python code
      const tmpDir = os.tmpdir();
      const tmpFile = path.join(tmpDir, `golden-universe-${Date.now()}-${filename}`);

      // Write the code to the temporary file
      fs.writeFileSync(tmpFile, code);

      // Execute the Python code
      const result = await executePython(tmpFile);

      // Clean up the temporary file
      try {
        fs.unlinkSync(tmpFile);
      } catch (err) {
        console.error('Failed to delete temp file:', err);
      }

      res.json({
        success: true,
        data: result
      });
    } catch (error) {
      console.error('Python execution error:', error);
      throw new AppError(
        error instanceof Error ? error.message : 'Python execution failed',
        500
      );
    }
  }),

  /**
   * Execute a Python file from the derivations folder
   */
  execFile: asyncHandler(async (req: Request, res: Response) => {
    const { folderName, filename } = req.body;

    if (!folderName || !filename) {
      throw new AppError('folderName and filename are required', 400);
    }

    try {
      // Construct the file path
      const filePath = path.join(
        __dirname,
        '../../../../derivations',
        folderName,
        filename
      );

      // Security check
      if (!filePath.includes('/derivations/')) {
        throw new AppError('Invalid file path', 403);
      }

      // Check if file exists
      if (!fs.existsSync(filePath)) {
        throw new AppError('File not found', 404);
      }

      // Execute the Python file
      const result = await executePython(filePath);

      res.json({
        success: true,
        data: {
          ...result,
          file: filename,
          folder: folderName
        }
      });
    } catch (error) {
      console.error('Python file execution error:', error);
      if (error instanceof AppError) throw error;
      throw new AppError(
        error instanceof Error ? error.message : 'Python file execution failed',
        500
      );
    }
  }),

  /**
   * Test Python availability
   */
  test: asyncHandler(async (req: Request, res: Response) => {
    try {
      const testCode = `
import sys
import json

result = {
    "python_version": sys.version,
    "executable": sys.executable,
    "platform": sys.platform
}

print(json.dumps(result, indent=2))
`;

      // Create temp file
      const tmpDir = os.tmpdir();
      const tmpFile = path.join(tmpDir, `test-${Date.now()}.py`);
      fs.writeFileSync(tmpFile, testCode);

      // Execute
      const result = await executePython(tmpFile);

      // Clean up
      try {
        fs.unlinkSync(tmpFile);
      } catch (err) {
        console.error('Failed to delete temp file:', err);
      }

      res.json({
        success: true,
        message: 'Python is available',
        data: result
      });
    } catch (error) {
      res.json({
        success: false,
        message: 'Python is not available',
        error: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  })
};

/**
 * Execute a Python file and return the result
 */
function executePython(filePath: string): Promise<{
  output: string;
  error?: string;
  exitCode: number;
  executionTime: number;
}> {
  return new Promise((resolve, reject) => {
    const startTime = Date.now();
    let output = '';
    let errorOutput = '';

    // Try python3 first, then python
    const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';

    const pythonProcess = spawn(pythonCmd, [filePath], {
      env: {
        ...process.env,
        PYTHONUNBUFFERED: '1'
      }
    });

    pythonProcess.stdout.on('data', (data) => {
      output += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      errorOutput += data.toString();
    });

    pythonProcess.on('close', (code) => {
      const executionTime = Date.now() - startTime;

      if (code === 0) {
        resolve({
          output: output.trim(),
          exitCode: code || 0,
          executionTime
        });
      } else {
        // Even with non-zero exit code, we might have useful output
        resolve({
          output: output.trim(),
          error: errorOutput.trim() || `Process exited with code ${code}`,
          exitCode: code || 1,
          executionTime
        });
      }
    });

    pythonProcess.on('error', (err) => {
      const executionTime = Date.now() - startTime;

      if (err.message.includes('ENOENT')) {
        // Python not found, try alternative command
        const altCmd = pythonCmd === 'python3' ? 'python' : 'python3';

        const altProcess = spawn(altCmd, [filePath], {
          env: {
            ...process.env,
            PYTHONUNBUFFERED: '1'
          }
        });

        let altOutput = '';
        let altError = '';

        altProcess.stdout.on('data', (data) => {
          altOutput += data.toString();
        });

        altProcess.stderr.on('data', (data) => {
          altError += data.toString();
        });

        altProcess.on('close', (code) => {
          const altExecutionTime = Date.now() - startTime;

          if (code === 0) {
            resolve({
              output: altOutput.trim(),
              exitCode: code || 0,
              executionTime: altExecutionTime
            });
          } else {
            resolve({
              output: altOutput.trim(),
              error: altError.trim() || `Process exited with code ${code}`,
              exitCode: code || 1,
              executionTime: altExecutionTime
            });
          }
        });

        altProcess.on('error', () => {
          reject(new Error('Python is not installed or not in PATH'));
        });
      } else {
        reject(err);
      }
    });

    // Set a timeout
    setTimeout(() => {
      pythonProcess.kill();
      reject(new Error('Python execution timeout'));
    }, 30000); // 30 second timeout
  });
}

export default pythonController;