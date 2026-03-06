import { Router, Request, Response } from 'express';
import { getDatabase } from '../database/schema';
import { asyncHandler } from '../middleware/errorHandler';
import * as fs from 'fs';
import config from '../config/config';

const router = Router();

// Health check endpoint
router.get(
  '/',
  asyncHandler(async (req: Request, res: Response) => {
    const health = {
      status: 'ok',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      checks: {
        database: false,
        filesystem: false,
        python: false,
      },
    };

    // Check database
    try {
      const db = getDatabase();
      db.prepare('SELECT 1').get();
      db.close();
      health.checks.database = true;
    } catch (error) {
      health.checks.database = false;
      health.status = 'degraded';
    }

    // Check filesystem access
    try {
      fs.accessSync(config.content.basePath, fs.constants.R_OK);
      health.checks.filesystem = true;
    } catch (error) {
      health.checks.filesystem = false;
      health.status = 'degraded';
    }

    // Check Python availability
    try {
      const { execSync } = require('child_process');
      execSync(`${config.python.executable} --version`, { timeout: 5000 });
      health.checks.python = true;
    } catch (error) {
      health.checks.python = false;
      health.status = 'degraded';
    }

    const statusCode = health.status === 'ok' ? 200 : 503;
    res.status(statusCode).json(health);
  })
);

// Metrics endpoint
router.get(
  '/metrics',
  asyncHandler(async (req: Request, res: Response) => {
    const db = getDatabase();

    try {
      const metrics = {
        timestamp: new Date().toISOString(),
        system: {
          uptime: process.uptime(),
          memory: process.memoryUsage(),
          cpu: process.cpuUsage(),
        },
        database: {
          theories: db.prepare('SELECT COUNT(*) as count FROM theories').get() as { count: number },
          derivations: db.prepare('SELECT COUNT(*) as count FROM derivations').get() as { count: number },
          equations: db.prepare('SELECT COUNT(*) as count FROM equations').get() as { count: number },
          calculations: {
            total: db.prepare('SELECT COUNT(*) as count FROM calculations').get() as { count: number },
            pending: db.prepare("SELECT COUNT(*) as count FROM calculations WHERE status = 'pending'").get() as { count: number },
            running: db.prepare("SELECT COUNT(*) as count FROM calculations WHERE status = 'running'").get() as { count: number },
            completed: db.prepare("SELECT COUNT(*) as count FROM calculations WHERE status = 'completed'").get() as { count: number },
            failed: db.prepare("SELECT COUNT(*) as count FROM calculations WHERE status = 'failed'").get() as { count: number },
          },
        },
      };

      res.json(metrics);
    } finally {
      db.close();
    }
  })
);

export default router;
