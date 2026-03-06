import { Request, Response } from 'express';
import { getDatabase } from '../database/schema';
import { AppError, asyncHandler } from '../middleware/errorHandler';
import pythonExecutor from '../services/pythonExecutor';
import Cache from '../utils/cache';

export const calculationsController = {
  /**
   * Execute a calculation
   */
  execute: asyncHandler(async (req: Request, res: Response) => {
    const { scriptName, parameters } = req.body;

    if (!scriptName) {
      throw new AppError('scriptName is required', 400);
    }

    // Start the calculation
    const job = await pythonExecutor.execute(scriptName, parameters || {});

    res.json({
      success: true,
      data: {
        jobId: job.id,
        status: job.status,
        message: 'Calculation started',
      },
    });
  }),

  /**
   * Get calculation status
   */
  getStatus: asyncHandler(async (req: Request, res: Response) => {
    const jobId = parseInt(req.params.jobId, 10);

    if (isNaN(jobId)) {
      throw new AppError('Invalid job ID', 400);
    }

    const job = pythonExecutor.getJobStatus(jobId);

    if (!job) {
      throw new AppError('Job not found', 404);
    }

    res.json({
      success: true,
      data: job,
    });
  }),

  /**
   * Get calculation history
   */
  getHistory: asyncHandler(async (req: Request, res: Response) => {
    const limit = parseInt(req.query.limit as string, 10) || 50;
    const offset = parseInt(req.query.offset as string, 10) || 0;

    const db = getDatabase();

    try {
      const stmt = db.prepare(`
        SELECT id, script_name, status, execution_time, created_at, completed_at
        FROM calculations
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
      `);

      const calculations = stmt.all(limit, offset) as any[];

      const countStmt = db.prepare('SELECT COUNT(*) as count FROM calculations');
      const { count } = countStmt.get() as { count: number };

      res.json({
        success: true,
        data: calculations,
        pagination: {
          total: count,
          limit,
          offset,
          hasMore: offset + limit < count,
        },
      });
    } finally {
      db.close();
    }
  }),

  /**
   * Get calculation result
   */
  getResult: asyncHandler(async (req: Request, res: Response) => {
    const jobId = parseInt(req.params.jobId, 10);

    if (isNaN(jobId)) {
      throw new AppError('Invalid job ID', 400);
    }

    const db = getDatabase();

    try {
      const stmt = db.prepare(`
        SELECT id, script_name, parameters, result, status, error, execution_time, created_at, completed_at
        FROM calculations
        WHERE id = ?
      `);

      const calculation = stmt.get(jobId) as any;

      if (!calculation) {
        throw new AppError('Calculation not found', 404);
      }

      // Parse JSON fields
      if (calculation.parameters) {
        calculation.parameters = JSON.parse(calculation.parameters);
      }
      if (calculation.result) {
        calculation.result = JSON.parse(calculation.result);
      }

      res.json({
        success: true,
        data: calculation,
      });
    } finally {
      db.close();
    }
  }),

  /**
   * Cancel a running calculation
   */
  cancel: asyncHandler(async (req: Request, res: Response) => {
    pythonExecutor.cancelCurrent();

    res.json({
      success: true,
      message: 'Current calculation cancelled',
    });
  }),

  /**
   * Get precision results table
   */
  getResults: asyncHandler(async (req: Request, res: Response) => {
    const cacheKey = 'calculations:results';
    let results = Cache.get<any>(cacheKey);

    if (!results) {
      const db = getDatabase();

      try {
        const stmt = db.prepare(`
          SELECT script_name, result, execution_time, completed_at
          FROM calculations
          WHERE status = 'completed' AND result IS NOT NULL
          ORDER BY completed_at DESC
          LIMIT 100
        `);

        const rows = stmt.all() as any[];

        results = rows.map((row) => ({
          scriptName: row.script_name,
          result: row.result ? JSON.parse(row.result) : null,
          executionTime: row.execution_time,
          completedAt: row.completed_at,
        }));
      } finally {
        db.close();
      }

      Cache.set(cacheKey, results, 600);
    }

    res.json({
      success: true,
      data: results,
    });
  }),
};
