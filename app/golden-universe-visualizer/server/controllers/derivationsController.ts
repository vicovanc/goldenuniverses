import { Request, Response } from 'express';
import { AppError, asyncHandler } from '../middleware/errorHandler';
import * as fs from 'fs';
import * as path from 'path';
import config from '../config/config';
import { contentService } from '../contentService';

// Helper function to parse derivation folder name
function parseDerivationFolder(folderName: string) {
  const match = folderName.match(/^(\d+)_(.+)$/);
  if (match) {
    const [, number, name] = match;
    return {
      number: parseInt(number),
      name: name.replace(/_/g, ' '),
      title: `Law ${number}: ${name.replace(/_/g, ' ')}`
    };
  }
  return null;
}

// Helper function to get category from folder name
function getCategoryFromFolder(folderName: string): string {
  const upperName = folderName.toUpperCase();
  if (upperName.includes('PARTICLE') || upperName.includes('MASS')) return 'Particle Physics';
  if (upperName.includes('COSMOLOGY') || upperName.includes('UNIVERSE')) return 'Cosmology';
  if (upperName.includes('QUANTUM')) return 'Quantum Mechanics';
  if (upperName.includes('FIELD')) return 'Field Theory';
  if (upperName.includes('GEOMETRY') || upperName.includes('SPACE')) return 'Geometry';
  if (upperName.includes('INFORMATION') || upperName.includes('ENTROPY')) return 'Information Theory';
  return 'General Physics';
}

export const derivationsController = {
  /**
   * Get all derivations dynamically from content service
   */
  getAll: asyncHandler(async (req: Request, res: Response) => {
    try {
      // Use content service to get derivations
      const derivations = await contentService.getDerivations();

      res.json({
        success: true,
        data: derivations,
        count: derivations.length,
        source: contentService.isGitHubMode() ? 'github' : 'local',
        config: contentService.getConfig(),
      });
    } catch (error) {
      console.error('Error in derivations getAll:', error);
      throw new AppError('Failed to fetch derivations', 500);
    }
  }),

  /**
   * Get derivation by number
   */
  getByNumber: asyncHandler(async (req: Request, res: Response) => {
    const numberParam = Array.isArray(req.params.number) ? req.params.number[0] : req.params.number;
    const number = parseInt(numberParam, 10);

    if (isNaN(number) || number < 1 || number > 42) {
      throw new AppError('Invalid derivation number (must be 1-42)', 400);
    }

    const derivationsPath = config.content.derivationsPath;

    // Find the folder for this derivation number
    const folders = fs.readdirSync(derivationsPath, { withFileTypes: true })
      .filter(dirent => dirent.isDirectory())
      .filter(dirent => {
        const match = dirent.name.match(/^(\d+)_/);
        return match && parseInt(match[1]) === number;
      });

    if (folders.length === 0) {
      throw new AppError(`Derivation ${number} not found`, 404);
    }

    const folder = folders[0].name;
    const parsed = parseDerivationFolder(folder);
    const folderPath = path.join(derivationsPath, folder);
    const files = fs.readdirSync(folderPath);

    const derivation = {
      id: number,
      number: number,
      title: parsed ? parsed.title : `Law ${number}`,
      name: parsed ? parsed.name : folder.replace(/_/g, ' '),
      folder_path: folderPath,
      folderName: folder,
      category: getCategoryFromFolder(folder),
      file_list: files.map((file) => ({
        name: file,
        path: path.join(folderPath, file),
        extension: path.extname(file),
        size: fs.statSync(path.join(folderPath, file)).size,
      })),
    };

    res.json({
      success: true,
      data: derivation,
    });
  }),

  /**
   * Get derivation file content
   */
  getFile: asyncHandler(async (req: Request, res: Response) => {
    const numberParam = Array.isArray(req.params.number) ? req.params.number[0] : req.params.number;
    const number = parseInt(numberParam, 10);
    const filename = Array.isArray(req.params.filename) ? req.params.filename[0] : req.params.filename;

    if (isNaN(number) || number < 1 || number > 42) {
      throw new AppError('Invalid derivation number', 400);
    }

    const derivationsPath = config.content.derivationsPath;

    // Find the folder for this derivation number
    const folders = fs.readdirSync(derivationsPath, { withFileTypes: true })
      .filter(dirent => dirent.isDirectory())
      .filter(dirent => {
        const match = dirent.name.match(/^(\d+)_/);
        return match && parseInt(match[1]) === number;
      });

    if (folders.length === 0) {
      throw new AppError(`Derivation ${number} not found`, 404);
    }

    const folder = folders[0].name;
    const folderPath = path.join(derivationsPath, folder);
    const filePath = path.join(folderPath, filename);

    // Security check: ensure file is within derivation folder
    if (!filePath.startsWith(folderPath)) {
      throw new AppError('Invalid file path', 403);
    }

    if (!fs.existsSync(filePath)) {
      throw new AppError('File not found', 404);
    }

    const content = fs.readFileSync(filePath, 'utf-8');
    const extension = path.extname(filename).toLowerCase();

    res.json({
      success: true,
      data: {
        filename,
        content,
        extension,
        size: content.length,
      },
    });
  }),

  /**
   * Get derivation statistics
   */
  getStats: asyncHandler(async (req: Request, res: Response) => {
    const derivationsPath = config.content.derivationsPath;

    // Count all derivation folders
    const folders = fs.readdirSync(derivationsPath, { withFileTypes: true })
      .filter(dirent => dirent.isDirectory())
      .filter(dirent => /^\d+_/.test(dirent.name));

    const stats = {
      total: folders.length,
      expected: 42,
      completion: (folders.length / 42) * 100,
    };

    res.json({
      success: true,
      data: stats,
    });
  }),

  /**
   * Get files list for a specific derivation folder
   */
  getFolderFiles: asyncHandler(async (req: Request, res: Response) => {
    const folderName = Array.isArray(req.params.folderName) ? req.params.folderName[0] : req.params.folderName;

    try {
      const files = await contentService.getDerivationFiles(folderName);

      // Organize files by type
      const pythonFiles = files.filter(f => f.name.endsWith('.py'));
      const markdownFiles = files.filter(f => f.name.endsWith('.md'));
      const otherFiles = files.filter(f =>
        !f.name.endsWith('.py') &&
        !f.name.endsWith('.md') &&
        f.type === 'file'
      );

      res.json({
        success: true,
        data: {
          folderName,
          pythonFiles: pythonFiles.map(f => ({ filename: f.name, extension: '.py' })),
          markdownFiles: markdownFiles.map(f => ({ filename: f.name, extension: '.md' })),
          otherFiles: otherFiles.map(f => ({ filename: f.name, extension: path.extname(f.name) })),
          allFiles: files,
        },
        source: contentService.isGitHubMode() ? 'github' : 'local',
      });
    } catch (error) {
      console.error('Error fetching folder files:', error);
      throw new AppError('Failed to fetch derivation files', 500);
    }
  }),

  /**
   * Get specific file content from a derivation folder
   */
  getFolderFile: asyncHandler(async (req: Request, res: Response) => {
    const folderName = Array.isArray(req.params.folderName) ? req.params.folderName[0] : req.params.folderName;
    const filename = Array.isArray(req.params.filename) ? req.params.filename[0] : req.params.filename;

    try {
      const content = await contentService.getFileContent(`derivations/${folderName}/${filename}`);
      const extension = path.extname(filename).toLowerCase();

      res.json({
        success: true,
        data: {
          filename,
          content,
          extension,
          size: content.length,
        },
        source: contentService.isGitHubMode() ? 'github' : 'local',
      });
    } catch (error) {
      console.error('Error fetching file content:', error);
      throw new AppError('File not found', 404);
    }
  }),
};
