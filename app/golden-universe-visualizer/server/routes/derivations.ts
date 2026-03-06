import { Router } from 'express';
import { derivationsController } from '../controllers/derivationsController';

const router = Router();

// Get all derivations
router.get('/', derivationsController.getAll);

// Get derivation statistics
router.get('/stats', derivationsController.getStats);

// Get derivation by number
router.get('/:number', derivationsController.getByNumber);

// Get derivation file
router.get('/:number/files/:filename', derivationsController.getFile);

// Get files for a derivation folder (dynamic)
router.get('/folder/:folderName/files', derivationsController.getFolderFiles);

// Get file content from a derivation folder
router.get('/folder/:folderName/file/:filename', derivationsController.getFolderFile);

export default router;
