import { Router } from 'express';
import { theoriesController } from '../controllers/theoriesController';
import { searchLimiter } from '../middleware/rateLimiter';

const router = Router();

// Get all theories
router.get('/', theoriesController.getAll);

// Search theories
router.get('/search', searchLimiter, theoriesController.search);

// Get theory statistics
router.get('/stats', theoriesController.getStats);

// Get theory by ID or filename
router.get('/:id', theoriesController.getById);

export default router;
