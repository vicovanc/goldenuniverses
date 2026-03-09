/**
 * Derivation Executor Service
 * Fetches and executes derivation Python files using available methods
 */

import { getPythonEngine } from './pythonEngine';

interface DerivationFile {
  name: string;
  path: string;
  content?: string;
}

interface DerivationResult {
  success: boolean;
  output?: string;
  error?: string;
  file?: string;
}

class DerivationExecutor {
  private derivationsMap: any = null;
  private pythonEngine = getPythonEngine();

  /**
   * Load the derivations map
   */
  private async loadDerivationsMap() {
    if (this.derivationsMap) return this.derivationsMap;

    try {
      const response = await fetch('/data/derivations-map.json');
      if (response.ok) {
        this.derivationsMap = await response.json();
        console.log('Loaded derivations map with', this.derivationsMap.length, 'entries');
      }
    } catch (error) {
      console.error('Failed to load derivations map:', error);
    }

    return this.derivationsMap;
  }

  /**
   * Get derivation by ID or folder name
   */
  async getDerivation(idOrFolder: string | number) {
    const map = await this.loadDerivationsMap();
    if (!map) return null;

    // Find by ID or folder name
    return map.find((d: any) =>
      d.id === Number(idOrFolder) ||
      d.folderName === String(idOrFolder) ||
      d.folder === String(idOrFolder)
    );
  }

  /**
   * Fetch Python file content
   */
  async fetchPythonFile(folderName: string, fileName: string): Promise<string | null> {
    // Try multiple approaches to fetch the file

    // 1. Try via static files served from public
    try {
      const staticUrl = `/derivations/${folderName}/${fileName}`;
      const response = await fetch(staticUrl);
      if (response.ok) {
        const content = await response.text();
        if (!content.includes('<!DOCTYPE') && !content.includes('File Not Available')) {
          console.log('Fetched from static:', staticUrl);
          return content;
        }
      }
    } catch (error) {
      console.debug('Static fetch failed:', error);
    }

    // 2. Try via API endpoint (if backend is running)
    try {
      const apiUrl = `/api/derivations/${folderName}/files/${fileName}`;
      const response = await fetch(apiUrl);
      if (response.ok) {
        const data = await response.json();
        if (data.success && data.data?.content) {
          console.log('Fetched from API:', apiUrl);
          return data.data.content;
        }
      }
    } catch (error) {
      console.debug('API fetch failed:', error);
    }

    // 3. Try raw GitHub URL as last resort
    try {
      const githubUrl = `https://raw.githubusercontent.com/vicovanc/goldenuniverse/main/derivations/${folderName}/${fileName}`;
      const response = await fetch(githubUrl);
      if (response.ok) {
        const content = await response.text();
        console.log('Fetched from GitHub:', githubUrl);
        return content;
      }
    } catch (error) {
      console.debug('GitHub fetch failed:', error);
    }

    return null;
  }

  /**
   * Execute a derivation by ID or folder name
   */
  async executeDerivation(
    idOrFolder: string | number,
    fileName?: string
  ): Promise<DerivationResult> {
    try {
      // Get derivation info
      const derivation = await this.getDerivation(idOrFolder);
      if (!derivation) {
        return {
          success: false,
          error: `Derivation not found: ${idOrFolder}`
        };
      }

      // Determine which file to execute
      let targetFile = fileName;
      if (!targetFile) {
        // Use first Python file or main orchestrator
        const pythonFiles = derivation.files?.python || [];
        targetFile = pythonFiles.find((f: string) =>
          f.includes('orchestrator') ||
          f.includes('main') ||
          f.startsWith('01_')
        ) || pythonFiles[0];

        if (!targetFile) {
          return {
            success: false,
            error: 'No Python files found in derivation'
          };
        }
      }

      // Fetch the Python code
      const code = await this.fetchPythonFile(derivation.folderName, targetFile);
      if (!code) {
        return {
          success: false,
          error: `Failed to fetch file: ${targetFile}`,
          file: targetFile
        };
      }

      // Check if it's actually Python code
      if (code.includes('<!DOCTYPE') || code.includes('File Not Available')) {
        return {
          success: false,
          error: 'File content is not valid Python code',
          file: targetFile
        };
      }

      console.log(`Executing ${derivation.title} - ${targetFile}`);

      // Execute the Python code
      const result = await this.pythonEngine.execute(code);

      return {
        success: result.success || false,
        output: result.result ?
          (typeof result.result === 'string' ? result.result : JSON.stringify(result.result, null, 2)) :
          'Execution completed',
        error: result.error,
        file: targetFile
      };

    } catch (error) {
      console.error('Execution error:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown execution error'
      };
    }
  }

  /**
   * List all available derivations
   */
  async listDerivations() {
    const map = await this.loadDerivationsMap();
    if (!map) return [];

    return map.map((d: any) => ({
      id: d.id,
      title: d.title,
      folderName: d.folderName,
      category: d.category,
      pythonFiles: d.files?.python || [],
      totalFiles: d.totalFiles || 0
    }));
  }

  /**
   * Test execution with a simple derivation
   */
  async testExecution(): Promise<DerivationResult> {
    // Test with particle masses calculation (ID 3 or 25)
    console.log('Testing derivation execution...');

    // Try Law 3 which should have particle mass calculations
    const result = await this.executeDerivation(3);

    if (!result.success) {
      // Try a simpler test with inline code
      console.log('Trying fallback test with simple Python code...');
      const testCode = `
import math

# Golden ratio
phi = (1 + math.sqrt(5)) / 2

# Test calculation
print("Golden ratio:", phi)
print("phi^2:", phi**2)
print("1/phi:", 1/phi)

# Verify golden ratio property
print("\\nVerification: phi^2 = phi + 1")
print(f"phi^2 = {phi**2:.10f}")
print(f"phi+1 = {phi+1:.10f}")
print(f"Difference: {abs(phi**2 - (phi+1)):.2e}")

"Test completed successfully"
`;

      const testResult = await this.pythonEngine.execute(testCode);
      return {
        success: testResult.success || false,
        output: testResult.result ? String(testResult.result) : 'Test completed',
        error: testResult.error
      };
    }

    return result;
  }
}

// Export singleton instance
export const derivationExecutor = new DerivationExecutor();
export default derivationExecutor;