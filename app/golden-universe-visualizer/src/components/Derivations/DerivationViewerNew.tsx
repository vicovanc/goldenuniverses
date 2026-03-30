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
import { fetchDerivations, fetchDerivationFileContent } from '@/services/derivationsService';
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
  const [isMaximized, setIsMaximized] = useState(false);

  // Use the folder prop directly - it contains the correct folder name from the data
  const actualFolderName = folder;

  useEffect(() => {
    loadDerivationData();
  }, [derivationId, actualFolderName]);

  const loadDerivationData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Load from static JSON using the service
      const derivations = await fetchDerivations();

      // Find the matching derivation by folder name
      const derivation = derivations.find(d =>
        d.folderName === actualFolderName ||
        d.path?.includes(actualFolderName)
      );

      if (derivation) {
        // Create derivation data structure
        const derivationData: DerivationData = {
          id: derivationId,
          folderName: derivation.folderName,
          path: derivation.path || derivation.folderName,
          displayName: title || derivation.displayName || derivation.folderName,
          pythonScripts: derivation.pythonScripts?.map((f, idx) => ({
            id: f.id || `py-${idx}`,
            filename: f.filename,
            path: f.path || f.filename,
            content: f.content,
          })),
          markdownFiles: derivation.markdownFiles?.filter(f => f.filename !== 'README.md').map((f, idx) => ({
            id: f.id || `md-${idx}`,
            filename: f.filename,
            path: f.path || f.filename,
            content: f.content,
          })),
        };

        // Check for README
        if (derivation.readme) {
          derivationData.readme = {
            content: derivation.readme.content || '',
            lastModified: new Date().toISOString(),
          };
        } else {
          // Try to find README in markdown files
          const readmeFile = derivation.markdownFiles?.find(f => f.filename === 'README.md');
          if (readmeFile && readmeFile.content) {
            derivationData.readme = {
              content: readmeFile.content,
              lastModified: new Date().toISOString(),
            };
          }
        }

        setDerivationData(derivationData);

        // Select the first Python file by default
        if (derivationData.pythonScripts && derivationData.pythonScripts.length > 0) {
          const firstPythonFile = derivationData.pythonScripts[0];
          setSelectedFile(firstPythonFile);
          if (firstPythonFile.content) {
            setFileContent(firstPythonFile.content);
          }
          setActiveTab('python');
        } else if (derivationData.readme) {
          setActiveTab('readme');
        } else if (derivationData.markdownFiles && derivationData.markdownFiles.length > 0) {
          const firstMarkdown = derivationData.markdownFiles[0];
          setSelectedFile(firstMarkdown);
          if (firstMarkdown.content) {
            setFileContent(firstMarkdown.content);
          }
          setActiveTab('markdown');
        }
      } else {
        console.warn(`No derivation found for folder: ${actualFolderName}`);
        setError(`Unable to load derivation for ${actualFolderName}`);
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

      // Try to load from service
      const folderName = derivationData?.folderName || actualFolderName;
      const content = await fetchDerivationFileContent(folderName, file.filename);

      if (content) {
        setFileContent(content);
      } else {
        // If no content found, show a message
        setFileContent(`# File Not Available\n\n` +
          `The file "${file.filename}" is not available in the static data.\n\n` +
          `This may be because:\n` +
          `- The derivations-map.json file needs to be regenerated\n` +
          `- The file content is not included in the static export\n\n` +
          `Please check that the derivation files are properly included in the build.`);
      }
    } catch (err) {
      console.error('Error loading file content:', err);
      setFileContent(`# Error Loading File\n\n` +
        `Failed to load: ${file.filename}\n\n` +
        `Error: ${err}\n\n` +
        `Please ensure the derivation files are properly configured.`);
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
    <div className={`derivation-viewer-new ${isMaximized ? 'maximized' : ''}`}>
      <div className="viewer-header">
        <div className="header-content">
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
        <button
          className="maximize-button"
          onClick={() => setIsMaximized(!isMaximized)}
          title={isMaximized ? 'Minimize view' : 'Maximize view'}
        >
          {isMaximized ? (
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M8 3v3a2 2 0 0 1-2 2H3m18 0h-3a2 2 0 0 1-2-2V3m0 18v-3a2 2 0 0 1 2-2h3M3 16h3a2 2 0 0 1 2 2v3" />
            </svg>
          ) : (
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3" />
            </svg>
          )}
        </button>
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
                  <>
                    {/* Only pass to PythonExecutor if content looks like Python */}
                    {(fileContent.includes('import ') || fileContent.includes('def ') || fileContent.includes('print(') || fileContent.startsWith('#!')) && !fileContent.startsWith('# ') ? (
                      <PythonExecutor
                        code={fileContent}
                        autoRun={true}
                        title={selectedFile.filename}
                        showCode={true}
                      />
                    ) : (
                      <div className="file-content-display">
                        <h4>{selectedFile.filename}</h4>
                        {fileContent.startsWith('#') && fileContent.includes('\n\n') ? (
                          /* Looks like markdown, render it */
                          <ReactMarkdown
                            remarkPlugins={[remarkGfm, remarkMath]}
                            rehypePlugins={[rehypeKatex]}
                          >
                            {fileContent}
                          </ReactMarkdown>
                        ) : (
                          /* Show as code block */
                          <pre className="code-block">
                            <code>{fileContent}</code>
                          </pre>
                        )}
                      </div>
                    )}
                  </>
                )}
                {selectedFile && !fileContent && (
                  <div className="no-content-message">
                    <p>No content available for {selectedFile.filename}</p>
                    <p className="hint">The file may need to be regenerated in the derivations map.</p>
                  </div>
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