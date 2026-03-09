/**
 * Content Service for dual environment support
 * Handles both local file system access (development) and GitHub API (production)
 */

import fs from 'fs/promises';
import path from 'path';

// Environment configuration
const CONTENT_SOURCE = process.env.NEXT_PUBLIC_CONTENT_SOURCE || 'local';
const CONTENT_BASE_PATH = process.env.CONTENT_BASE_PATH || '../../';
const GITHUB_OWNER = process.env.GITHUB_OWNER || 'vicovanc';
const GITHUB_REPO = process.env.GITHUB_REPO || 'goldenuniverse';
const GITHUB_BRANCH = process.env.GITHUB_BRANCH || 'main';

interface ContentFile {
  path: string;
  name: string;
  type: 'file' | 'directory';
  content?: string;
}

interface DerivationInfo {
  id: number;
  number: number;
  title: string;
  name: string;
  description: string;
  category: 'fundamental' | 'particles' | 'constants' | 'advanced';
  folderName: string;
  folder_path: string;
  pythonCount: number;
  markdownCount: number;
  totalFiles: number;
  files: {
    python: string[];
    markdown: string[];
    all: string[];
  };
}

class ContentService {
  private githubApiBase = 'https://api.github.com';
  private githubRawBase = 'https://raw.githubusercontent.com';

  /**
   * Get the list of derivations from either local file system or GitHub
   */
  async getDerivations(): Promise<DerivationInfo[]> {
    if (CONTENT_SOURCE === 'github') {
      return this.getDerivationsFromGitHub();
    } else {
      return this.getDerivationsFromLocal();
    }
  }

  /**
   * Get derivation files from either local file system or GitHub
   */
  async getDerivationFiles(folderName: string): Promise<ContentFile[]> {
    if (CONTENT_SOURCE === 'github') {
      return this.getDerivationFilesFromGitHub(folderName);
    } else {
      return this.getDerivationFilesFromLocal(folderName);
    }
  }

  /**
   * Get file content from either local file system or GitHub
   */
  async getFileContent(relativePath: string): Promise<string> {
    if (CONTENT_SOURCE === 'github') {
      return this.getFileContentFromGitHub(relativePath);
    } else {
      return this.getFileContentFromLocal(relativePath);
    }
  }

  // Local file system methods
  private async getDerivationsFromLocal(): Promise<DerivationInfo[]> {
    const derivationsPath = path.join(__dirname, CONTENT_BASE_PATH, 'derivations');
    const derivations: DerivationInfo[] = [];

    try {
      const folders = await fs.readdir(derivationsPath);
      let id = 1;

      for (const folder of folders) {
        const folderPath = path.join(derivationsPath, folder);
        const stats = await fs.stat(folderPath);

        if (stats.isDirectory()) {
          const derivationInfo = await this.parseDerivationFolder(folderPath, folder, id);
          if (derivationInfo) {
            derivations.push(derivationInfo);
            id++;
          }
        }
      }

      return derivations.sort((a, b) => a.number - b.number);
    } catch (error) {
      console.error('Error reading local derivations:', error);
      return [];
    }
  }

  private async parseDerivationFolder(folderPath: string, folderName: string, id: number): Promise<DerivationInfo | null> {
    try {
      const files = await fs.readdir(folderPath);
      const pythonFiles = files.filter(f => f.endsWith('.py'));
      const markdownFiles = files.filter(f => f.endsWith('.md'));

      // Parse law number from folder name
      const lawMatch = folderName.match(/law[-_]?(\d+)/i);
      const number = lawMatch ? parseInt(lawMatch[1]) : id;

      // Read the first markdown file to get title and description
      let title = folderName;
      let description = 'Mathematical derivation and proofs';

      if (markdownFiles.length > 0) {
        try {
          const firstMdPath = path.join(folderPath, markdownFiles[0]);
          const mdContent = await fs.readFile(firstMdPath, 'utf-8');
          const lines = mdContent.split('\n');

          // Extract title from first heading
          const titleLine = lines.find(line => line.startsWith('# '));
          if (titleLine) {
            title = titleLine.replace('# ', '').trim();
          }

          // Extract description from first paragraph
          const descLine = lines.find(line => line.trim() && !line.startsWith('#') && !line.startsWith('```'));
          if (descLine) {
            description = descLine.trim();
          }
        } catch (err) {
          // Ignore errors reading individual files
        }
      }

      // Categorize based on law number or folder name
      let category: DerivationInfo['category'] = 'fundamental';
      if (number <= 10) category = 'fundamental';
      else if (number <= 20 || folderName.toLowerCase().includes('particle') || folderName.toLowerCase().includes('mass')) category = 'particles';
      else if (number <= 30 || folderName.toLowerCase().includes('constant')) category = 'constants';
      else category = 'advanced';

      return {
        id,
        number,
        title,
        name: title.replace(/^Law \d+:?\s*/i, ''),
        description,
        category,
        folderName,
        folder_path: folderPath,
        pythonCount: pythonFiles.length,
        markdownCount: markdownFiles.length,
        totalFiles: files.length,
        files: {
          python: pythonFiles,
          markdown: markdownFiles,
          all: files
        }
      };
    } catch (error) {
      console.error(`Error parsing derivation folder ${folderName}:`, error);
      return null;
    }
  }

  private async getDerivationFilesFromLocal(folderName: string): Promise<ContentFile[]> {
    const derivationPath = path.join(__dirname, CONTENT_BASE_PATH, 'derivations', folderName);
    const files: ContentFile[] = [];

    try {
      const dirContents = await fs.readdir(derivationPath);

      for (const item of dirContents) {
        const itemPath = path.join(derivationPath, item);
        const stats = await fs.stat(itemPath);

        files.push({
          path: item,
          name: item,
          type: stats.isDirectory() ? 'directory' : 'file'
        });
      }

      return files;
    } catch (error) {
      console.error('Error reading derivation files:', error);
      return [];
    }
  }

  private async getFileContentFromLocal(relativePath: string): Promise<string> {
    const fullPath = path.join(__dirname, CONTENT_BASE_PATH, relativePath);
    try {
      return await fs.readFile(fullPath, 'utf-8');
    } catch (error) {
      console.error('Error reading file content:', error);
      throw error;
    }
  }

  // GitHub API methods
  private async getDerivationsFromGitHub(): Promise<DerivationInfo[]> {
    const derivations: DerivationInfo[] = [];

    try {
      // Fetch the derivations folder structure from GitHub
      const response = await fetch(
        `${this.githubApiBase}/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/derivations?ref=${GITHUB_BRANCH}`,
        {
          headers: {
            'Accept': 'application/vnd.github.v3+json',
            // Add GitHub token if available for higher rate limits
            ...(process.env.GITHUB_TOKEN && { 'Authorization': `token ${process.env.GITHUB_TOKEN}` })
          }
        }
      );

      if (!response.ok) {
        throw new Error(`GitHub API error: ${response.status}`);
      }

      const folders = await response.json();
      let id = 1;

      for (const folder of folders) {
        if (folder.type === 'dir') {
          const derivationInfo = await this.parseGitHubDerivationFolder(folder.name, folder.path, id);
          if (derivationInfo) {
            derivations.push(derivationInfo);
            id++;
          }
        }
      }

      return derivations.sort((a, b) => a.number - b.number);
    } catch (error) {
      console.error('Error fetching derivations from GitHub:', error);
      return [];
    }
  }

  private async parseGitHubDerivationFolder(folderName: string, folderPath: string, id: number): Promise<DerivationInfo | null> {
    try {
      // Fetch folder contents from GitHub
      const response = await fetch(
        `${this.githubApiBase}/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/${folderPath}?ref=${GITHUB_BRANCH}`,
        {
          headers: {
            'Accept': 'application/vnd.github.v3+json',
            ...(process.env.GITHUB_TOKEN && { 'Authorization': `token ${process.env.GITHUB_TOKEN}` })
          }
        }
      );

      if (!response.ok) {
        throw new Error(`GitHub API error: ${response.status}`);
      }

      const files = await response.json();
      const pythonFiles = files.filter((f: any) => f.name.endsWith('.py')).map((f: any) => f.name);
      const markdownFiles = files.filter((f: any) => f.name.endsWith('.md')).map((f: any) => f.name);
      const allFiles = files.map((f: any) => f.name);

      // Parse law number from folder name
      const lawMatch = folderName.match(/law[-_]?(\d+)/i);
      const number = lawMatch ? parseInt(lawMatch[1]) : id;

      // Default title and description
      let title = folderName;
      let description = 'Mathematical derivation and proofs';

      // Try to fetch the first markdown file for title and description
      if (markdownFiles.length > 0) {
        try {
          const mdUrl = `${this.githubRawBase}/${GITHUB_OWNER}/${GITHUB_REPO}/${GITHUB_BRANCH}/${folderPath}/${markdownFiles[0]}`;
          const mdResponse = await fetch(mdUrl);

          if (mdResponse.ok) {
            const mdContent = await mdResponse.text();
            const lines = mdContent.split('\n');

            // Extract title from first heading
            const titleLine = lines.find(line => line.startsWith('# '));
            if (titleLine) {
              title = titleLine.replace('# ', '').trim();
            }

            // Extract description from first paragraph
            const descLine = lines.find(line => line.trim() && !line.startsWith('#') && !line.startsWith('```'));
            if (descLine) {
              description = descLine.trim();
            }
          }
        } catch (err) {
          // Ignore errors reading individual files
        }
      }

      // Categorize based on law number or folder name
      let category: DerivationInfo['category'] = 'fundamental';
      if (number <= 10) category = 'fundamental';
      else if (number <= 20 || folderName.toLowerCase().includes('particle') || folderName.toLowerCase().includes('mass')) category = 'particles';
      else if (number <= 30 || folderName.toLowerCase().includes('constant')) category = 'constants';
      else category = 'advanced';

      return {
        id,
        number,
        title,
        name: title.replace(/^Law \d+:?\s*/i, ''),
        description,
        category,
        folderName,
        folder_path: folderPath,
        pythonCount: pythonFiles.length,
        markdownCount: markdownFiles.length,
        totalFiles: allFiles.length,
        files: {
          python: pythonFiles,
          markdown: markdownFiles,
          all: allFiles
        }
      };
    } catch (error) {
      console.error(`Error parsing GitHub derivation folder ${folderName}:`, error);
      return null;
    }
  }

  private async getDerivationFilesFromGitHub(folderName: string): Promise<ContentFile[]> {
    try {
      const response = await fetch(
        `${this.githubApiBase}/repos/${GITHUB_OWNER}/${GITHUB_REPO}/contents/derivations/${folderName}?ref=${GITHUB_BRANCH}`,
        {
          headers: {
            'Accept': 'application/vnd.github.v3+json',
            ...(process.env.GITHUB_TOKEN && { 'Authorization': `token ${process.env.GITHUB_TOKEN}` })
          }
        }
      );

      if (!response.ok) {
        throw new Error(`GitHub API error: ${response.status}`);
      }

      const items = await response.json();

      return items.map((item: any) => ({
        path: item.name,
        name: item.name,
        type: item.type === 'dir' ? 'directory' : 'file'
      }));
    } catch (error) {
      console.error('Error fetching derivation files from GitHub:', error);
      return [];
    }
  }

  private async getFileContentFromGitHub(relativePath: string): Promise<string> {
    try {
      const url = `${this.githubRawBase}/${GITHUB_OWNER}/${GITHUB_REPO}/${GITHUB_BRANCH}/${relativePath}`;
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(`GitHub fetch error: ${response.status}`);
      }

      return await response.text();
    } catch (error) {
      console.error('Error fetching file content from GitHub:', error);
      throw error;
    }
  }

  /**
   * Check if the service is configured for GitHub
   */
  isGitHubMode(): boolean {
    return CONTENT_SOURCE === 'github';
  }

  /**
   * Get configuration info
   */
  getConfig() {
    return {
      source: CONTENT_SOURCE,
      ...(CONTENT_SOURCE === 'github' ? {
        owner: GITHUB_OWNER,
        repo: GITHUB_REPO,
        branch: GITHUB_BRANCH
      } : {
        basePath: CONTENT_BASE_PATH
      })
    };
  }
}

// Export singleton instance
export const contentService = new ContentService();