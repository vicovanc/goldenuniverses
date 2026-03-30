/**
 * Service for fetching derivations data from static JSON files
 * This replaces the API calls with static data fetching
 */

interface DerivationFile {
  id?: string;
  filename: string;
  path: string;
  content?: string;
}

interface DerivationFolder {
  id: string;
  folderName: string;
  path: string;
  displayName: string;
  readme?: {
    id: string;
    path: string;
    filename: string;
    title: string;
    content: string;
  };
  pythonScripts?: DerivationFile[];
  markdownFiles?: DerivationFile[];
  status?: string;
  fileCount?: number;
}

interface DerivationsData {
  derivations: DerivationFolder[];
}

/**
 * Fetch the derivations map from static JSON
 */
export async function fetchDerivations(): Promise<DerivationFolder[]> {
  try {
    // Add cache-busting version parameter
    const version = '1.0.5';
    const response = await fetch(`/data/derivations-map.json?v=${version}`);
    if (!response.ok) {
      throw new Error(`Failed to fetch derivations: ${response.status}`);
    }
    const data: DerivationsData = await response.json();
    return data.derivations || [];
  } catch (error) {
    console.error('Error fetching derivations:', error);
    return [];
  }
}

/**
 * Get files for a specific derivation folder
 */
export async function fetchDerivationFiles(folderName: string): Promise<DerivationFile[]> {
  try {
    const derivations = await fetchDerivations();
    const folder = derivations.find(d => d.folderName === folderName);

    if (!folder) return [];

    const files: DerivationFile[] = [];

    // Add README if it exists
    if (folder.readme) {
      files.push({
        id: folder.readme.id,
        filename: folder.readme.filename,
        path: folder.readme.path,
        content: folder.readme.content
      });
    }

    // Add Python scripts
    if (folder.pythonScripts) {
      files.push(...folder.pythonScripts);
    }

    // Add Markdown files
    if (folder.markdownFiles) {
      files.push(...folder.markdownFiles);
    }

    return files;
  } catch (error) {
    console.error(`Error fetching files for ${folderName}:`, error);
    return [];
  }
}

/**
 * Get content of a specific file in a derivation folder
 */
export async function fetchDerivationFileContent(
  folderName: string,
  fileName: string
): Promise<string | null> {
  try {
    const files = await fetchDerivationFiles(folderName);
    const file = files.find(f => f.filename === fileName);

    if (file?.content) {
      return file.content;
    }

    // If content is not embedded, try to fetch from the file path
    if (file?.path) {
      // Ensure the path starts with a forward slash
      const filePath = file.path.startsWith('/') ? file.path : `/${file.path}`;
      const response = await fetch(filePath);
      if (response.ok) {
        return await response.text();
      }
    }

    return null;
  } catch (error) {
    console.error(`Error fetching content for ${folderName}/${fileName}:`, error);
    return null;
  }
}

/**
 * Search derivations by keyword
 */
export async function searchDerivations(keyword: string): Promise<DerivationFolder[]> {
  try {
    const derivations = await fetchDerivations();
    const lowerKeyword = keyword.toLowerCase();

    return derivations.filter(folder => {
      // Check folder name
      if (folder.folderName.toLowerCase().includes(lowerKeyword)) {
        return true;
      }

      // Check display name
      if (folder.displayName?.toLowerCase().includes(lowerKeyword)) {
        return true;
      }

      // Check file names
      const allFiles = [
        ...(folder.pythonScripts || []),
        ...(folder.markdownFiles || [])
      ];

      return allFiles.some(file =>
        file.filename.toLowerCase().includes(lowerKeyword)
      );
    });
  } catch (error) {
    console.error('Error searching derivations:', error);
    return [];
  }
}

/**
 * Get derivation by ID (folder name)
 */
export async function getDerivationById(id: string): Promise<DerivationFolder | null> {
  try {
    const derivations = await fetchDerivations();
    return derivations.find(d => d.folderName === id) || null;
  } catch (error) {
    console.error(`Error getting derivation ${id}:`, error);
    return null;
  }
}

/**
 * Mock API response format for backward compatibility
 */
export function createApiResponse(data: any): Response {
  return new Response(JSON.stringify(data), {
    status: 200,
    headers: {
      'Content-Type': 'application/json',
    },
  });
}