import { Router } from 'express';
import { explanationsController } from '../controllers/explanationsController';

const router = Router();

// Get all explanation topics
router.get('/topics', explanationsController.getTopics);

// Search explanations
router.get('/search', explanationsController.search);

// Get specific explanation topic
router.get('/topic/:topic', explanationsController.getTopic);

export default router;