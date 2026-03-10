/**
 * Vercel Serverless Function to serve explanatory markdown files
 * Endpoint: /api/explanatory/[filename]
 * Example: /api/explanatory/WHAT_IS_THE_ELECTRON.md
 *
 * In production (Vercel), fetches from GitHub raw content
 * In local testing, reads from filesystem
 */

const fs = require('fs');
const path = require('path');

// GitHub repository configuration
const GITHUB_OWNER = 'vicovanc';
const GITHUB_REPO = 'goldenuniverses'; // Public repo for Vercel
const GITHUB_BRANCH = 'main';
const GITHUB_RAW_BASE = `https://raw.githubusercontent.com/${GITHUB_OWNER}/${GITHUB_REPO}/${GITHUB_BRANCH}`;

module.exports = async (req, res) => {
  const { filename } = req.query;

  // Security: Only allow .md files
  if (!filename || !filename.endsWith('.md')) {
    return res.status(400).json({
      error: 'Invalid filename. Only .md files are allowed.'
    });
  }

  // Security: Prevent directory traversal
  if (filename.includes('..') || filename.includes('/') || filename.includes('\\')) {
    return res.status(400).json({
      error: 'Invalid filename format.'
    });
  }

  try {
    let content;
    const isProduction = process.env.VERCEL === '1' || process.env.NODE_ENV === 'production';

    if (isProduction) {
      // In production (Vercel), fetch from GitHub
      const githubUrl = `${GITHUB_RAW_BASE}/explanatory/${filename}`;
      console.log('Fetching from GitHub:', githubUrl);

      const response = await fetch(githubUrl);

      if (!response.ok) {
        return res.status(404).json({
          error: `File not found on GitHub: ${filename}`,
          url: githubUrl,
          status: response.status
        });
      }

      content = await response.text();
    } else {
      // In local development, read from filesystem
      const explanatoryPath = path.join(process.cwd(), '..', '..', 'explanatory', filename);

      if (!fs.existsSync(explanatoryPath)) {
        return res.status(404).json({
          error: `File not found locally: ${filename}`,
          path: explanatoryPath
        });
      }

      content = fs.readFileSync(explanatoryPath, 'utf-8');
    }

    // Set appropriate headers
    res.setHeader('Content-Type', 'text/markdown; charset=utf-8');
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Cache-Control', 'public, max-age=3600'); // Cache for 1 hour

    // Return the content
    return res.status(200).send(content);
  } catch (error) {
    console.error('Error serving explanatory file:', error);
    return res.status(500).json({
      error: 'Failed to load explanatory file',
      message: error.message,
      stack: process.env.NODE_ENV === 'development' ? error.stack : undefined
    });
  }
};
