import { Request, Response } from 'express';
import { getDatabase } from '../database/schema';
import { AppError, asyncHandler } from '../middleware/errorHandler';
import ContentRenderer from '../utils/contentRenderer';
import Cache from '../utils/cache';

export const equationsController = {
  /**
   * Get all equations
   */
  getAll: asyncHandler(async (req: Request, res: Response) => {
    const category = req.query.category as string;
    const render = req.query.render === 'true';

    const cacheKey = `equations:${category || 'all'}:${render}`;
    let equations = Cache.get<any[]>(cacheKey);

    if (!equations) {
      const db = getDatabase();

      try {
        let stmt;
        if (category) {
          stmt = db.prepare(`
            SELECT * FROM equations
            WHERE category = ?
            ORDER BY id
          `);
          equations = stmt.all(category) as any[];
        } else {
          stmt = db.prepare(`
            SELECT * FROM equations
            ORDER BY category, id
          `);
          equations = stmt.all() as any[];
        }

        // Render LaTeX if requested
        if (render) {
          equations = equations.map((eq) => ({
            ...eq,
            rendered: ContentRenderer.renderLatex(eq.latex, { displayMode: true }),
          }));
        }

        // Parse variables JSON
        equations = equations.map((eq) => ({
          ...eq,
          variables: eq.variables ? JSON.parse(eq.variables) : [],
        }));
      } finally {
        db.close();
      }

      Cache.set(cacheKey, equations, 3600);
    }

    res.json({
      success: true,
      data: equations,
      count: equations.length,
    });
  }),

  /**
   * Get equation by ID
   */
  getById: asyncHandler(async (req: Request, res: Response) => {
    const idParam = Array.isArray(req.params.id) ? req.params.id[0] : req.params.id;
    const id = parseInt(idParam, 10);
    const render = req.query.render === 'true';

    if (isNaN(id)) {
      throw new AppError('Invalid equation ID', 400);
    }

    const cacheKey = `equation:${id}:${render}`;
    let equation = Cache.get<any>(cacheKey);

    if (!equation) {
      const db = getDatabase();

      try {
        const stmt = db.prepare('SELECT * FROM equations WHERE id = ?');
        equation = stmt.get(id) as any;

        if (!equation) {
          throw new AppError('Equation not found', 404);
        }

        // Parse variables
        if (equation.variables) {
          equation.variables = JSON.parse(equation.variables);
        }

        // Render LaTeX if requested
        if (render) {
          equation.rendered = ContentRenderer.renderLatex(equation.latex, { displayMode: true });
        }
      } finally {
        db.close();
      }

      Cache.set(cacheKey, equation, 3600);
    }

    res.json({
      success: true,
      data: equation,
    });
  }),

  /**
   * Get equations by category
   */
  getCategories: asyncHandler(async (req: Request, res: Response) => {
    const cacheKey = 'equations:categories';
    let categories = Cache.get<any[]>(cacheKey);

    if (!categories) {
      const db = getDatabase();

      try {
        const stmt = db.prepare(`
          SELECT category, COUNT(*) as count
          FROM equations
          WHERE category IS NOT NULL
          GROUP BY category
          ORDER BY category
        `);

        categories = stmt.all() as any[];
      } finally {
        db.close();
      }

      Cache.set(cacheKey, categories, 3600);
    }

    res.json({
      success: true,
      data: categories,
    });
  }),

  /**
   * Search equations
   */
  search: asyncHandler(async (req: Request, res: Response) => {
    const { q } = req.query;

    if (!q || typeof q !== 'string') {
      throw new AppError('Query parameter "q" is required', 400);
    }

    const db = getDatabase();

    try {
      const stmt = db.prepare(`
        SELECT * FROM equations
        WHERE name LIKE ? OR description LIKE ? OR latex LIKE ?
        ORDER BY name
        LIMIT 50
      `);

      const searchTerm = `%${q}%`;
      const equations = stmt.all(searchTerm, searchTerm, searchTerm) as any[];

      res.json({
        success: true,
        data: equations,
        count: equations.length,
        query: q,
      });
    } finally {
      db.close();
    }
  }),
};
