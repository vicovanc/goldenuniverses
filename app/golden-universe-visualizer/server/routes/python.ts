import { Router } from 'express';
import { pythonController } from '../controllers/pythonController';

const router = Router();

// Execute Python code directly
router.post('/exec', pythonController.exec);

// Execute a Python file from derivations
router.post('/execFile', pythonController.execFile);

// Test Python availability
router.get('/test', pythonController.test);

export default router;