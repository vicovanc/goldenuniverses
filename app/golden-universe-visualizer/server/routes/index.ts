import { Router } from 'express';
import theoriesRoutes from './theories';
import derivationsRoutes from './derivations';
import calculationsRoutes from './calculations';
import equationsRoutes from './equations';
import searchRoutes from './search';
import healthRoutes from './health';
import explanationsRoutes from './explanations';
import pythonRoutes from './python';

const router = Router();

// API routes
router.use('/theories', theoriesRoutes);
router.use('/derivations', derivationsRoutes);
router.use('/calculations', calculationsRoutes);
router.use('/equations', equationsRoutes);
router.use('/explanations', explanationsRoutes);
router.use('/search', searchRoutes);
router.use('/health', healthRoutes);
router.use('/python', pythonRoutes);

// API root
router.get('/', (_req, res) => {
  res.json({
    success: true,
    message: 'Golden Universe API',
    version: '1.0.0',
    endpoints: {
      theories: '/api/theories',
      derivations: '/api/derivations',
      calculations: '/api/calculations',
      equations: '/api/equations',
      explanations: '/api/explanations',
      search: '/api/search',
      health: '/api/health',
      python: '/api/python',
    },
  });
});

export default router;
