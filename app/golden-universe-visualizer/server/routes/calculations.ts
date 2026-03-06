import { Router } from 'express';
import { calculationsController } from '../controllers/calculationsController';
import { calculationLimiter } from '../middleware/rateLimiter';
import { validators } from '../middleware/validation';

const router = Router();

// Get calculation history
router.get('/', calculationsController.getHistory);

// Get precision results table
router.get('/results', calculationsController.getResults);

// Execute calculation
router.post(
  '/',
  calculationLimiter,
  validators.calculateRequest,
  calculationsController.execute
);

// Get calculation status
router.get('/:jobId', calculationsController.getStatus);

// Get calculation result
router.get('/:jobId/result', calculationsController.getResult);

// Cancel current calculation
router.post('/cancel', calculationsController.cancel);

export default router;
