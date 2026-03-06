import { Router } from 'express';
import { equationsController } from '../controllers/equationsController';
import { searchLimiter } from '../middleware/rateLimiter';

const router = Router();

// Get all equations
router.get('/', equationsController.getAll);

// Get equation categories
router.get('/categories', equationsController.getCategories);

// Search equations
router.get('/search', searchLimiter, equationsController.search);

// Get equation by ID
router.get('/:id', equationsController.getById);

export default router;
