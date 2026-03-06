import { Request, Response } from 'express';
import { getDatabase } from '../database/schema';
import { AppError, asyncHandler } from '../middleware/errorHandler';
import ContentRenderer from '../utils/contentRenderer';
import Cache from '../utils/cache';
import * as fs from 'fs';
import * as path from 'path';
import config from '../config/config';

export const theoriesController = {
  /**
   * Get all theories
   */
  getAll: asyncHandler(async (req: Request, res: Response) => {
    const cacheKey = 'theories:all';
    let theories = Cache.get<any[]>(cacheKey);

    if (!theories) {
      const db = getDatabase();

      try {
        const stmt = db.prepare(`
          SELECT id, title, filename, summary, keywords, created_at, updated_at
          FROM theories
          ORDER BY created_at DESC
        `);

        theories = stmt.all() as any[];
      } finally {
        db.close();
      }

      Cache.set(cacheKey, theories, 3600); // Cache for 1 hour
    }

    res.json({
      success: true,
      data: theories,
      count: theories.length,
    });
  }),

  /**
   * Get theory by ID or filename
   */
  getById: asyncHandler(async (req: Request, res: Response) => {
    const { id } = req.params;
    const renderLatex = req.query.render === 'true';

    const cacheKey = `theory:${id}:${renderLatex}`;
    let theory = Cache.get<any>(cacheKey);

    if (!theory) {
      const db = getDatabase();

      try {
        const stmt = db.prepare(`
          SELECT * FROM theories
          WHERE id = ? OR filename = ?
        `);

        theory = stmt.get(id, id) as any;

        if (!theory) {
          throw new AppError('Theory not found', 404);
        }

        // Render LaTeX if requested
        if (renderLatex && theory.content) {
          theory.rendered_content = await ContentRenderer.renderMarkdown(theory.content);
          theory.equations = ContentRenderer.extractEquations(theory.content);
        }
      } finally {
        db.close();
      }

      Cache.set(cacheKey, theory, 3600);
    }

    res.json({
      success: true,
      data: theory,
    });
  }),

  /**
   * Search theories
   */
  search: asyncHandler(async (req: Request, res: Response) => {
    const { q } = req.query;

    if (!q || typeof q !== 'string') {
      throw new AppError('Query parameter "q" is required', 400);
    }

    const db = getDatabase();

    try {
      const stmt = db.prepare(`
        SELECT t.id, t.title, t.filename, t.summary, t.keywords,
               snippet(theories_fts, 1, '<mark>', '</mark>', '...', 32) as snippet,
               rank
        FROM theories_fts
        JOIN theories t ON theories_fts.rowid = t.id
        WHERE theories_fts MATCH ?
        ORDER BY rank
        LIMIT 50
      `);

      const results = stmt.all(q) as any[];

      res.json({
        success: true,
        data: results,
        count: results.length,
        query: q,
      });
    } finally {
      db.close();
    }
  }),

  /**
   * Get theory statistics
   */
  getStats: asyncHandler(async (req: Request, res: Response) => {
    const cacheKey = 'theories:stats';
    let stats = Cache.get<any>(cacheKey);

    if (!stats) {
      const db = getDatabase();

      try {
        const countStmt = db.prepare('SELECT COUNT(*) as count FROM theories');
        const { count } = countStmt.get() as { count: number };

        stats = {
          total: count,
          lastUpdated: new Date().toISOString(),
        };
      } finally {
        db.close();
      }

      Cache.set(cacheKey, stats, 600); // Cache for 10 minutes
    }

    res.json({
      success: true,
      data: stats,
    });
  }),
};
