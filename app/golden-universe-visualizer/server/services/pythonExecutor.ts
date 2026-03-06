import { spawn, ChildProcess } from 'child_process';
import * as path from 'path';
import * as fs from 'fs';
import config from '../config/config';
import { getDatabase } from '../database/schema';
import { EventEmitter } from 'events';

export interface CalculationJob {
  id: number;
  scriptName: string;
  parameters?: Record<string, any>;
  status: 'pending' | 'running' | 'completed' | 'failed';
  result?: any;
  error?: string;
  progress?: number;
}

export class PythonExecutor extends EventEmitter {
  private queue: CalculationJob[] = [];
  private isProcessing = false;
  private currentProcess: ChildProcess | null = null;

  /**
   * Execute a Python script
   */
  async execute(scriptName: string, parameters: Record<string, any> = {}): Promise<CalculationJob> {
    const scriptPath = this.resolveScriptPath(scriptName);

    if (!fs.existsSync(scriptPath)) {
      throw new Error(`Script not found: ${scriptName}`);
    }

    // Create calculation record
    const jobId = this.createCalculationRecord(scriptName, parameters);

    const job: CalculationJob = {
      id: jobId,
      scriptName,
      parameters,
      status: 'pending',
    };

    // Add to queue
    this.queue.push(job);
    this.emit('job-queued', job);

    // Start processing if not already running
    if (!this.isProcessing) {
      this.processQueue();
    }

    return job;
  }

  /**
   * Process the job queue
   */
  private async processQueue(): Promise<void> {
    if (this.isProcessing || this.queue.length === 0) {
      return;
    }

    this.isProcessing = true;

    while (this.queue.length > 0) {
      const job = this.queue.shift()!;
      await this.runJob(job);
    }

    this.isProcessing = false;
  }

  /**
   * Run a single job
   */
  private async runJob(job: CalculationJob): Promise<void> {
    const startTime = Date.now();
    job.status = 'running';
    this.emit('job-started', job);

    try {
      const scriptPath = this.resolveScriptPath(job.scriptName);
      const result = await this.executePythonScript(scriptPath, job.parameters || {});

      job.status = 'completed';
      job.result = result;

      const executionTime = Date.now() - startTime;

      // Update database
      this.updateCalculationRecord(job.id, {
        status: 'completed',
        result: JSON.stringify(result),
        executionTime,
      });

      this.emit('job-completed', job);
    } catch (error) {
      job.status = 'failed';
      job.error = error instanceof Error ? error.message : String(error);

      const executionTime = Date.now() - startTime;

      // Update database
      this.updateCalculationRecord(job.id, {
        status: 'failed',
        error: job.error,
        executionTime,
      });

      this.emit('job-failed', job);
    }
  }

  /**
   * Execute Python script and return result
   */
  private executePythonScript(scriptPath: string, parameters: Record<string, any>): Promise<any> {
    return new Promise((resolve, reject) => {
      const args = [scriptPath];

      // Add parameters as JSON argument
      if (Object.keys(parameters).length > 0) {
        args.push('--params', JSON.stringify(parameters));
      }

      const pythonProcess = spawn(config.python.executable, args, {
        cwd: config.python.scriptsPath,
        env: { ...process.env, PYTHONUNBUFFERED: '1' },
      });

      this.currentProcess = pythonProcess;

      let stdout = '';
      let stderr = '';

      pythonProcess.stdout.on('data', (data) => {
        const output = data.toString();
        stdout += output;

        // Try to parse progress updates
        const lines = output.split('\n');
        for (const line of lines) {
          if (line.startsWith('PROGRESS:')) {
            const progress = parseFloat(line.split(':')[1]);
            this.emit('progress', { progress });
          }
        }
      });

      pythonProcess.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      pythonProcess.on('error', (error) => {
        this.currentProcess = null;
        reject(new Error(`Failed to start Python process: ${error.message}`));
      });

      pythonProcess.on('close', (code) => {
        this.currentProcess = null;

        if (code === 0) {
          try {
            // Try to parse JSON output
            const result = JSON.parse(stdout);
            resolve(result);
          } catch (error) {
            // If not JSON, return raw output
            resolve({ output: stdout.trim() });
          }
        } else {
          reject(new Error(`Python script failed with code ${code}: ${stderr || stdout}`));
        }
      });

      // Timeout
      setTimeout(() => {
        if (pythonProcess && !pythonProcess.killed) {
          pythonProcess.kill();
          reject(new Error('Python script execution timeout'));
        }
      }, config.python.timeout);
    });
  }

  /**
   * Cancel current job
   */
  cancelCurrent(): void {
    if (this.currentProcess && !this.currentProcess.killed) {
      this.currentProcess.kill();
      this.currentProcess = null;
      this.emit('job-cancelled');
    }
  }

  /**
   * Get job status
   */
  getJobStatus(jobId: number): CalculationJob | null {
    const db = getDatabase();

    try {
      const stmt = db.prepare('SELECT * FROM calculations WHERE id = ?');
      const row = stmt.get(jobId) as any;

      if (!row) return null;

      return {
        id: row.id,
        scriptName: row.script_name,
        parameters: row.parameters ? JSON.parse(row.parameters) : undefined,
        status: row.status,
        result: row.result ? JSON.parse(row.result) : undefined,
        error: row.error,
      };
    } catch (error) {
      console.error('Get job status error:', error);
      return null;
    } finally {
      db.close();
    }
  }

  /**
   * Resolve script path
   */
  private resolveScriptPath(scriptName: string): string {
    // If absolute path, use it
    if (path.isAbsolute(scriptName)) {
      return scriptName;
    }

    // If relative, resolve from scripts path
    return path.join(config.python.scriptsPath, scriptName);
  }

  /**
   * Create calculation record in database
   */
  private createCalculationRecord(scriptName: string, parameters: Record<string, any>): number {
    const db = getDatabase();

    try {
      const stmt = db.prepare(`
        INSERT INTO calculations (script_name, parameters, status)
        VALUES (?, ?, 'pending')
      `);

      const result = stmt.run(scriptName, JSON.stringify(parameters));
      return result.lastInsertRowid as number;
    } catch (error) {
      console.error('Create calculation record error:', error);
      throw error;
    } finally {
      db.close();
    }
  }

  /**
   * Update calculation record
   */
  private updateCalculationRecord(
    id: number,
    data: { status?: string; result?: string; error?: string; executionTime?: number }
  ): void {
    const db = getDatabase();

    try {
      const updates: string[] = [];
      const values: any[] = [];

      if (data.status) {
        updates.push('status = ?');
        values.push(data.status);
      }
      if (data.result !== undefined) {
        updates.push('result = ?');
        values.push(data.result);
      }
      if (data.error !== undefined) {
        updates.push('error = ?');
        values.push(data.error);
      }
      if (data.executionTime !== undefined) {
        updates.push('execution_time = ?');
        values.push(data.executionTime);
      }

      updates.push('completed_at = datetime("now")');
      values.push(id);

      const stmt = db.prepare(`
        UPDATE calculations
        SET ${updates.join(', ')}
        WHERE id = ?
      `);

      stmt.run(...values);
    } catch (error) {
      console.error('Update calculation record error:', error);
    } finally {
      db.close();
    }
  }
}

export default new PythonExecutor();
