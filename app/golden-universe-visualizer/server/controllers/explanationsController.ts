import { Request, Response } from 'express';
import { AppError, asyncHandler } from '../middleware/errorHandler';
import * as fs from 'fs';
import * as path from 'path';

// Path to explanatory folder
const EXPLANATORY_PATH = '/Users/Cristiana_1/Documents/Golden Universe/explanatory';

// Map of topics to their markdown files
const TOPIC_FILES: Record<string, string> = {
  'consciousness': 'CONSCIOUSNESS.md',
  'gravity': 'WHAT_IS_GRAVITY.md',
  'electron': 'WHAT_IS_THE_ELECTRON.md',
  'proton': 'WHAT_IS_THE_PROTON.md',
  'consciousness-readme': 'README_GU_CONSCIOUSNESS.md'
};

export const explanationsController = {
  /**
   * Get list of available explanation topics
   */
  getTopics: asyncHandler(async (req: Request, res: Response) => {
    try {
      // Read all markdown files from the explanatory folder
      if (!fs.existsSync(EXPLANATORY_PATH)) {
        throw new AppError('Explanatory folder not found', 500);
      }

      const files = fs.readdirSync(EXPLANATORY_PATH)
        .filter(file => file.endsWith('.md'));

      const topics = files.map(file => {
        const name = file.replace('.md', '').toLowerCase().replace(/_/g, '-');
        const filePath = path.join(EXPLANATORY_PATH, file);

        // Read first few lines to get a description
        let description = '';
        try {
          const content = fs.readFileSync(filePath, 'utf-8');
          const lines = content.split('\n').filter(line => line.trim());

          // Find the first non-header line as description
          for (const line of lines) {
            if (!line.startsWith('#') && line.trim().length > 10) {
              description = line.trim().substring(0, 150) + '...';
              break;
            }
          }
        } catch (err) {
          console.error('Error reading file for description:', file, err);
        }

        return {
          id: name,
          file: file,
          title: formatTitle(file),
          description: description || `Explanation of ${formatTitle(file)}`,
          category: getCategory(file)
        };
      });

      res.json({
        success: true,
        data: topics
      });
    } catch (error) {
      console.error('Error getting explanation topics:', error);
      throw error;
    }
  }),

  /**
   * Get content for a specific explanation topic
   */
  getTopic: asyncHandler(async (req: Request, res: Response) => {
    const topicParam = req.params.topic;
    const topic = Array.isArray(topicParam) ? topicParam[0] : topicParam;

    try {
      // Find the markdown file for this topic
      let fileName = '';

      // Check if it's a known topic
      if (TOPIC_FILES[topic]) {
        fileName = TOPIC_FILES[topic];
      } else {
        // Try to find by converting topic to filename format
        const possibleNames = [
          `${topic.toUpperCase().replace(/-/g, '_')}.md`,
          `WHAT_IS_THE_${topic.toUpperCase().replace(/-/g, '_')}.md`,
          `README_GU_${topic.toUpperCase().replace(/-/g, '_')}.md`,
          `GU_${topic.toUpperCase().replace(/-/g, '_')}.md`
        ];

        for (const name of possibleNames) {
          const filePath = path.join(EXPLANATORY_PATH, name);
          if (fs.existsSync(filePath)) {
            fileName = name;
            break;
          }
        }
      }

      if (!fileName) {
        // List available files for debugging
        const availableFiles = fs.readdirSync(EXPLANATORY_PATH)
          .filter(f => f.endsWith('.md'));

        throw new AppError(
          `Topic "${topic}" not found. Available topics: ${availableFiles.join(', ')}`,
          404
        );
      }

      const filePath = path.join(EXPLANATORY_PATH, fileName);

      if (!fs.existsSync(filePath)) {
        throw new AppError(`Explanation file not found: ${fileName}`, 404);
      }

      const content = fs.readFileSync(filePath, 'utf-8');

      // Extract metadata from content
      const lines = content.split('\n');
      let title = formatTitle(fileName);

      // Try to get title from first # heading
      for (const line of lines) {
        if (line.startsWith('# ')) {
          title = line.substring(2).trim();
          break;
        }
      }

      res.json({
        success: true,
        data: {
          id: topic,
          title: title,
          fileName: fileName,
          content: content,
          category: getCategory(fileName)
        }
      });
    } catch (error) {
      console.error('Error getting explanation topic:', error);
      throw error;
    }
  }),

  /**
   * Search explanations for a keyword
   */
  search: asyncHandler(async (req: Request, res: Response) => {
    const { q } = req.query;

    if (!q || typeof q !== 'string') {
      throw new AppError('Search query is required', 400);
    }

    try {
      const searchTerm = q.toLowerCase();
      const results = [];

      // Read all markdown files
      const files = fs.readdirSync(EXPLANATORY_PATH)
        .filter(file => file.endsWith('.md'));

      for (const file of files) {
        const filePath = path.join(EXPLANATORY_PATH, file);
        const content = fs.readFileSync(filePath, 'utf-8');

        if (content.toLowerCase().includes(searchTerm)) {
          // Find matching lines
          const lines = content.split('\n');
          const matches = [];

          lines.forEach((line, index) => {
            if (line.toLowerCase().includes(searchTerm)) {
              matches.push({
                line: index + 1,
                text: line.trim().substring(0, 200)
              });
            }
          });

          results.push({
            file: file,
            title: formatTitle(file),
            topic: file.replace('.md', '').toLowerCase().replace(/_/g, '-'),
            matches: matches.slice(0, 5) // Limit to 5 matches per file
          });
        }
      }

      res.json({
        success: true,
        query: q,
        results: results
      });
    } catch (error) {
      console.error('Error searching explanations:', error);
      throw error;
    }
  })
};

// Helper function to format file name into title
function formatTitle(fileName: string): string {
  return fileName
    .replace('.md', '')
    .replace(/_/g, ' ')
    .replace(/\b\w/g, char => char.toUpperCase())
    .replace('Gu ', 'GU ')
    .replace(' Is ', ' is ')
    .replace(' The ', ' the ')
    .replace(/^What Is The/, 'What is the')
    .replace(/^Readme /, '');
}

// Helper function to determine category
function getCategory(fileName: string): string {
  const name = fileName.toLowerCase();

  if (name.includes('consciousness')) return 'consciousness';
  if (name.includes('gravity')) return 'physics';
  if (name.includes('electron') || name.includes('proton')) return 'particles';
  if (name.includes('readme')) return 'overview';

  return 'general';
}