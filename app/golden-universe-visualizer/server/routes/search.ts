import { Router } from 'express';
import { Request, Response } from 'express';
import { getDatabase } from '../database/schema';
import { AppError, asyncHandler } from '../middleware/errorHandler';
import { searchLimiter } from '../middleware/rateLimiter';
import { validators } from '../middleware/validation';

const router = Router();

// Full-text search across all content
router.get(
  '/',
  searchLimiter,
  validators.searchQuery,
  asyncHandler(async (req: Request, res: Response) => {
    const { q } = req.query as { q: string };

    const db = getDatabase();

    try {
      // Search theories
      const theoriesStmt = db.prepare(`
        SELECT 'theory' as type, t.id, t.title, t.filename,
               snippet(theories_fts, 1, '<mark>', '</mark>', '...', 32) as snippet
        FROM theories_fts
        JOIN theories t ON theories_fts.rowid = t.id
        WHERE theories_fts MATCH ?
        LIMIT 20
      `);

      const theories = theoriesStmt.all(q);

      // Search equations
      const equationsStmt = db.prepare(`
        SELECT 'equation' as type, id, name, category, description
        FROM equations
        WHERE name LIKE ? OR description LIKE ?
        LIMIT 20
      `);

      const searchTerm = `%${q}%`;
      const equations = equationsStmt.all(searchTerm, searchTerm);

      // Search derivations
      const derivationsStmt = db.prepare(`
        SELECT 'derivation' as type, id, number, title, description
        FROM derivations
        WHERE title LIKE ? OR description LIKE ?
        LIMIT 20
      `);

      const derivations = derivationsStmt.all(searchTerm, searchTerm);

      const results = [
        ...theories,
        ...equations,
        ...derivations,
      ];

      res.json({
        success: true,
        data: {
          query: q,
          results,
          counts: {
            theories: theories.length,
            equations: equations.length,
            derivations: derivations.length,
            total: results.length,
          },
        },
      });
    } finally {
      db.close();
    }
  })
);

export default router;
