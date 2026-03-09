import { Request, Response } from 'express';
import { AppError, asyncHandler } from '../middleware/errorHandler';
import * as fs from 'fs';
import * as path from 'path';
import axios from 'axios';

// Environment configuration
const CONTENT_SOURCE = process.env.NEXT_PUBLIC_CONTENT_SOURCE || 'local';
const CONTENT_BASE_PATH = process.env.CONTENT_BASE_PATH || '../../';
const GITHUB_OWNER = process.env.GITHUB_OWNER || 'vicovanc';
const GITHUB_REPO = process.env.GITHUB_REPO || 'goldenuniverses'; // Public repo with 's'
const GITHUB_BRANCH = process.env.GITHUB_BRANCH || 'main';

// Path to explanatory folder for local development
const EXPLANATORY_PATH = path.join(__dirname, CONTENT_BASE_PATH, 'explanatory');

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
      let files: string[] = [];

      if (CONTENT_SOURCE === 'github') {
        // Fetch from GitHub API
        try {
          const url = `https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/explanatory?ref=${GITHUB_BRANCH}`;
          const response = await axios.get(url, {
            headers: {
              'Accept': 'application/vnd.github.v3+json',
              ...(process.env.GITHUB_TOKEN && {
                'Authorization': `token ${process.env.GITHUB_TOKEN}`
              })
            }
          });

          files = response.data
            .filter((item: any) => item.type === 'file' && item.name.endsWith('.md'))
            .map((item: any) => item.name);
        } catch (err) {
          console.error('Error fetching from GitHub:', err);
          throw new AppError('Failed to fetch explanations from GitHub', 500);
        }
      } else {
        // Read from local file system
        if (!fs.existsSync(EXPLANATORY_PATH)) {
          throw new AppError('Explanatory folder not found', 500);
        }
        files = fs.readdirSync(EXPLANATORY_PATH)
          .filter(file => file.endsWith('.md'));
      }

      const topics = await Promise.all(files.map(async (file) => {
        const name = file.replace('.md', '').toLowerCase().replace(/_/g, '-');

        // Read first few lines to get a description
        let description = '';
        try {
          let content = '';

          if (CONTENT_SOURCE === 'github') {
            const url = `https://raw.githubusercontent.com/${GITHUB_OWNER}/${GITHUB_REPO}/${GITHUB_BRANCH}/explanatory/${file}`;
            const response = await axios.get(url);
            content = response.data;
          } else {
            const filePath = path.join(EXPLANATORY_PATH, file);
            content = fs.readFileSync(filePath, 'utf-8');
          }

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
      }));

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
      let content = '';
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

        // Check GitHub or local based on environment
        if (CONTENT_SOURCE === 'github') {
          // Try each possible filename on GitHub
          for (const name of possibleNames) {
            try {
              const url = `https://raw.githubusercontent.com/${GITHUB_OWNER}/${GITHUB_REPO}/${GITHUB_BRANCH}/explanatory/${name}`;
              const response = await axios.get(url);
              if (response.status === 200) {
                content = response.data;
                fileName = name;
                break;
              }
            } catch (err) {
              // Try next filename
              continue;
            }
          }
        } else {
          // Local file system
          for (const name of possibleNames) {
            const filePath = path.join(EXPLANATORY_PATH, name);
            if (fs.existsSync(filePath)) {
              fileName = name;
              content = fs.readFileSync(filePath, 'utf-8');
              break;
            }
          }
        }
      }

      // If fileName was found but content not loaded yet
      if (fileName && !content) {
        if (CONTENT_SOURCE === 'github') {
          const url = `https://raw.githubusercontent.com/${GITHUB_OWNER}/${GITHUB_REPO}/${GITHUB_BRANCH}/explanatory/${fileName}`;
          try {
            const response = await axios.get(url);
            content = response.data;
          } catch (err) {
            throw new AppError(`Failed to fetch explanation from GitHub: ${fileName}`, 500);
          }
        } else {
          const filePath = path.join(EXPLANATORY_PATH, fileName);
          if (fs.existsSync(filePath)) {
            content = fs.readFileSync(filePath, 'utf-8');
          }
        }
      }

      if (!content || !fileName) {
        throw new AppError(
          `Topic "${topic}" not found`,
          404
        );
      }

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