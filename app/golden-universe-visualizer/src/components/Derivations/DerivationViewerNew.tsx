/**
 * DerivationViewerNew - Enhanced derivation viewer with full file support
 * Loads actual derivation files from derivations-map.json
 * Supports both Python (.py) and Markdown (.md) files
 */

import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';
import { PythonExecutor } from '@/components/Calculations/PythonExecutor';
import './DerivationViewerNew.scss';

interface DerivationFile {
  id: string;
  filename: string;
  path: string;
  content?: string;
  lineCount?: number;
}

interface DerivationData {
  id: string;
  folderName: string;
  path: string;
  displayName: string;
  readme?: {
    content: string;
    lastModified: string;
  };
  pythonScripts?: DerivationFile[];
  markdownFiles?: DerivationFile[];
}

interface DerivationsMap {
  derivations: DerivationData[];
  metadata: {
    totalDerivations: number;
    totalPythonScripts: number;
    totalMarkdownFiles: number;
    lastGenerated: string;
  };
}

interface DerivationViewerProps {
  derivationId: string;
  title: string;
  folder: string;
}

// Map derivation IDs to folder names based on the actual folder structure
const DERIVATION_ID_TO_FOLDER: Record<string, string> = {
  '1': '01_FORCE_UNIFICATION',
  '2': '02_FUNDAMENTAL_CONSTANTS',
  '3': '03_PARTICLE_MASSES',
  '4': '04_COSMOLOGY',
  '5': '05_CHARGE_QUANTIZATION',
  '6': '06_COUPLING_CONSTANTS',
  '7': '07_PARTICLE_FAMILIES',
  '8': '08_NEUTRINO_MASSES',
  '9': '09_QCD_SCALE',
  '10': '10_HIGGS_MECHANISM',
  '11': '11_SYMMETRY_BREAKING',
  '12': '03_PARTICLE_MASSES',  // Duplicate mapping for particle masses
  '13': '13_DARK_MATTER',
  '14': '14_FINAL_ASSESSMENT',
  '15': '15_QUANTUM_GRAVITY',
  '16': '16_BLACK_HOLES',
  '17': '17_ALPHA_EM_DERIVATION',
  '18': '18_COSMOLOGICAL_CONSTANT',
  '19': '19_INFLATION',
  '20': '20_BARYON_ASYMMETRY',
  '21': '21_ENTROPY',
  '22': '17_ALPHA_EM_DERIVATION',  // Another mapping for alpha
  '23': '23_NEWTON_G',
  '24': '24_TIME_ARROW',
  '25': '03_PARTICLE_MASSES',  // Another particle masses mapping
  '26': '26_PLATONIC_SPACE',
  '27': '27_ENTANGLEMENT',
  '28': '28_MEASUREMENT',
  '29': '29_DECOHERENCE',
  '30': '30_QUANTUM_COMPUTATION',
  '31': '31_HOLOGRAPHIC_PRINCIPLE',
  '32': '32_EMERGENT_DIMENSIONS',
  '33': '33_PHASE_TRANSITIONS',
  '34': '34_CRITICAL_PHENOMENA',
  '35': '35_RENORMALIZATION',
  '36': '36_EFFECTIVE_THEORIES',
  '37': '37_ANOMALIES',
  '38': '38_INSTANTONS',
  '39': '39_MONOPOLES',
  '40': '14_FINAL_ASSESSMENT',  // Another final assessment mapping
  '41': '41_HAMILTONIAN',
  '42': '42_COMPLETE_FRAMEWORK'
};

export const DerivationViewerNew: React.FC<DerivationViewerProps> = ({
  derivationId,
  title,
  folder
}) => {
  const [derivationData, setDerivationData] = useState<DerivationData | null>(null);
  const [selectedFile, setSelectedFile] = useState<DerivationFile | null>(null);
  const [fileContent, setFileContent] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'readme' | 'python' | 'markdown'>('python');

  // Get the correct folder name for this derivation
  const actualFolderName = DERIVATION_ID_TO_FOLDER[derivationId] || folder;

  useEffect(() => {
    loadDerivationData();
  }, [derivationId, actualFolderName]);

  const loadDerivationData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Use the new API endpoint to get files for this folder
      const filesResponse = await fetch(`/api/derivations/folder/${actualFolderName}/files`);
      if (filesResponse.ok) {
        const filesResult = await filesResponse.json();
        if (filesResult.success && filesResult.data) {
          const { pythonFiles, markdownFiles, allFiles } = filesResult.data;

          // Create derivation data structure from API response
          const derivation: DerivationData = {
            id: derivationId,
            folderName: actualFolderName,
            path: actualFolderName,
            displayName: title,
            pythonScripts: pythonFiles.map((f: any, idx: number) => ({
              id: `py-${idx}`,
              filename: f.filename,
              path: f.filename,
            })),
            markdownFiles: markdownFiles.filter((f: any) => f.filename !== 'README.md').map((f: any, idx: number) => ({
              id: `md-${idx}`,
              filename: f.filename,
              path: f.filename,
            })),
          };

          // Check for README
          const readmeFile = markdownFiles.find((f: any) => f.filename === 'README.md');
          if (readmeFile) {
            // Load README content
            const readmeResponse = await fetch(`/api/derivations/folder/${actualFolderName}/file/README.md`);
            if (readmeResponse.ok) {
              const readmeResult = await readmeResponse.json();
              if (readmeResult.success && readmeResult.data) {
                derivation.readme = {
                  content: readmeResult.data.content,
                  lastModified: new Date().toISOString(),
                };
              }
            }
          }

          setDerivationData(derivation);

          // Select the first Python file by default
          if (derivation.pythonScripts && derivation.pythonScripts.length > 0) {
            const firstPythonFile = derivation.pythonScripts[0];
            setSelectedFile(firstPythonFile);
            await loadFileContent(firstPythonFile);
            setActiveTab('python');
          } else if (derivation.readme) {
            setActiveTab('readme');
          }
        }
      } else {
        // Fallback: Try to load from derivations-map.json
        const response = await fetch('/data/derivations-map.json');
        if (response.ok) {
          const data: DerivationsMap = await response.json();
          const derivation = data.derivations.find(d =>
            d.folderName === actualFolderName ||
            d.path.includes(actualFolderName)
          );

          if (derivation) {
            setDerivationData(derivation);

            if (derivation.pythonScripts && derivation.pythonScripts.length > 0) {
              const firstPythonFile = derivation.pythonScripts[0];
              setSelectedFile(firstPythonFile);
              await loadFileContent(firstPythonFile);
              setActiveTab('python');
            } else if (derivation.readme) {
              setActiveTab('readme');
            }
          }
        }
      }
    } catch (err) {
      console.error('Error loading derivation data:', err);
      setError('Failed to load derivation data');
    } finally {
      setLoading(false);
    }
  };

  const loadFromServer = async () => {
    try {
      // Try to fetch from the server using the API endpoint
      const response = await fetch(`/api/derivations/${derivationId}/files`);
      if (response.ok) {
        const files = await response.json();
        // Process server response
        console.log('Loaded from server:', files);
      }
    } catch (err) {
      console.error('Server fallback failed:', err);
    }
  };

  const loadFileContent = async (file: DerivationFile) => {
    try {
      // First check if content is embedded in the file object
      if (file.content) {
        setFileContent(file.content);
        return;
      }

      // Use the new API endpoint to load file directly from filesystem
      const apiPath = `/api/derivations/folder/${actualFolderName}/file/${file.filename}`;
      console.log('Loading file from API:', apiPath);

      const response = await fetch(apiPath);
      if (response.ok) {
        const result = await response.json();
        if (result.success && result.data) {
          setFileContent(result.data.content);
        } else {
          throw new Error('Invalid API response');
        }
      } else {
        // Fallback to try derivationData folder name if different
        if (derivationData?.folderName && derivationData.folderName !== actualFolderName) {
          const altApiPath = `/api/derivations/folder/${derivationData.folderName}/file/${file.filename}`;
          console.log('Trying alternative API path:', altApiPath);

          const altResponse = await fetch(altApiPath);
          if (altResponse.ok) {
            const altResult = await altResponse.json();
            if (altResult.success && altResult.data) {
              setFileContent(altResult.data.content);
            } else {
              throw new Error('Invalid API response from alternative path');
            }
          } else {
            throw new Error(`File not found: ${file.filename}`);
          }
        } else {
          throw new Error(`File not found: ${file.filename}`);
        }
      }
    } catch (err) {
      console.error('Error loading file content:', err);
      setFileContent(`# Error loading file\n\nFailed to load: ${file.filename}\n\nError: ${err}\n\n` +
        `This file should be loaded dynamically from the server's filesystem.\n` +
        `Please ensure the derivation files are properly configured on the server.`);
    }
  };

  const handleFileSelect = async (file: DerivationFile) => {
    setSelectedFile(file);
    await loadFileContent(file);
  };

  const renderTabs = () => {
    const hasPython = derivationData?.pythonScripts && derivationData.pythonScripts.length > 0;
    const hasMarkdown = derivationData?.markdownFiles && derivationData.markdownFiles.length > 0;
    const hasReadme = !!derivationData?.readme;

    return (
      <div className="derivation-tabs">
        {hasPython && (
          <button
            className={`tab ${activeTab === 'python' ? 'active' : ''}`}
            onClick={() => setActiveTab('python')}
          >
            Python Files ({derivationData.pythonScripts?.length})
          </button>
        )}
        {hasMarkdown && (
          <button
            className={`tab ${activeTab === 'markdown' ? 'active' : ''}`}
            onClick={() => setActiveTab('markdown')}
          >
            Documentation ({derivationData.markdownFiles?.length})
          </button>
        )}
        {hasReadme && (
          <button
            className={`tab ${activeTab === 'readme' ? 'active' : ''}`}
            onClick={() => setActiveTab('readme')}
          >
            README
          </button>
        )}
      </div>
    );
  };

  const renderFileList = (files: DerivationFile[], type: 'python' | 'markdown') => {
    if (!files || files.length === 0) return null;

    return (
      <div className="file-list">
        {files.map((file) => (
          <button
            key={file.id}
            className={`file-item ${selectedFile?.id === file.id ? 'active' : ''}`}
            onClick={() => handleFileSelect(file)}
          >
            <span className="file-name">{file.filename}</span>
            {file.lineCount && (
              <span className="file-meta">{file.lineCount} lines</span>
            )}
          </button>
        ))}
      </div>
    );
  };

  if (loading) {
    return (
      <div className="derivation-viewer loading">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading derivation files...</p>
        </div>
      </div>
    );
  }

  if (error && !derivationData) {
    return (
      <div className="derivation-viewer error">
        <div className="error-message">
          <h3>Error Loading Derivation</h3>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="derivation-viewer-new">
      <div className="viewer-header">
        <h2>{title}</h2>
        {derivationData && (
          <div className="derivation-meta">
            <span className="folder-name">{derivationData.folderName}</span>
            <span className="file-count">
              {derivationData.pythonScripts?.length || 0} Python files,
              {derivationData.markdownFiles?.length || 0} Markdown files
            </span>
          </div>
        )}
      </div>

      {renderTabs()}

      <div className="viewer-content">
        {activeTab === 'readme' && derivationData?.readme && (
          <div className="readme-content">
            <ReactMarkdown
              remarkPlugins={[remarkGfm, remarkMath]}
              rehypePlugins={[rehypeKatex]}
            >
              {derivationData.readme.content}
            </ReactMarkdown>
          </div>
        )}

        {activeTab === 'python' && derivationData?.pythonScripts && (
          <div className="python-content">
            <div className="content-layout">
              <aside className="file-sidebar">
                <h4>Python Files</h4>
                {renderFileList(derivationData.pythonScripts, 'python')}
              </aside>

              <main className="file-display">
                {selectedFile && fileContent && (
                  <PythonExecutor
                    code={fileContent}
                    autoRun={true}
                    title={selectedFile.filename}
                    showCode={true}
                  />
                )}
              </main>
            </div>
          </div>
        )}

        {activeTab === 'markdown' && derivationData?.markdownFiles && (
          <div className="markdown-content">
            <div className="content-layout">
              <aside className="file-sidebar">
                <h4>Documentation Files</h4>
                {renderFileList(derivationData.markdownFiles, 'markdown')}
              </aside>

              <main className="file-display">
                {selectedFile && fileContent && (
                  <div className="markdown-display">
                    <h3>{selectedFile.filename}</h3>
                    <ReactMarkdown
                      remarkPlugins={[remarkGfm, remarkMath]}
                      rehypePlugins={[rehypeKatex]}
                    >
                      {fileContent}
                    </ReactMarkdown>
                  </div>
                )}
              </main>
            </div>
          </div>
        )}
      </div>

      {!derivationData && (
        <div className="fallback-content">
          <div className="info-message">
            <p>
              Derivation files are being loaded. If this persists, please check:
            </p>
            <ul>
              <li>The derivations folder exists at the correct path</li>
              <li>The server has access to the derivation files</li>
              <li>The derivations-map.json file is up to date</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default DerivationViewerNew;