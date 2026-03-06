/**
 * ExportOptions - Data export functionality
 * GU-040: Results Export
 * - CSV export with all data
 * - Excel export with formatting
 * - JSON export for programmatic use
 * - LaTeX table export for papers
 * - Copy to clipboard functionality
 */

import React, { useState } from 'react';
import type { ResultData, ExportFormat } from './types';

interface ExportOptionsProps {
  results: ResultData[];
  filename?: string;
}

export const ExportOptions: React.FC<ExportOptionsProps> = ({
  results,
  filename = 'golden-universe-results',
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [copied, setCopied] = useState(false);

  const formatCSV = (data: ResultData[]): string => {
    const headers = [
      'Name',
      'Category',
      'Theoretical Value',
      'Experimental Value',
      'Unit',
      'Error (ppm)',
      'Error (%)',
      'Precision Level',
      'Formula',
      'Derivation',
      'Breakthrough',
      'Discovery Date',
      'CODATA Year',
    ];

    const rows = data.map(r => [
      r.name,
      r.category,
      r.theoretical.toString(),
      r.experimental.toString(),
      r.unit,
      r.errorPpm.toString(),
      r.errorPercent.toString(),
      r.precision,
      r.formula || '',
      r.derivation || '',
      r.breakthrough ? 'Yes' : 'No',
      r.discoveryDate || '',
      r.codataYear?.toString() || '',
    ]);

    return [
      headers.join(','),
      ...rows.map(row => row.map(cell => `"${cell}"`).join(',')),
    ].join('\n');
  };

  const formatJSON = (data: ResultData[]): string => {
    return JSON.stringify(
      {
        metadata: {
          source: 'Golden Universe Theory',
          exportDate: new Date().toISOString(),
          resultCount: data.length,
        },
        results: data,
      },
      null,
      2
    );
  };

  const formatLaTeX = (data: ResultData[]): string => {
    const rows = data.map(r => {
      const escapedName = r.name.replace(/_/g, '\\_').replace(/%/g, '\\%');
      const precision = Math.abs(r.errorPpm) < 0.01 ? '<0.01' : Math.abs(r.errorPpm).toFixed(2);

      return `${escapedName} & ${r.theoretical.toExponential(6)} & ${r.experimental.toExponential(6)} & ${precision} & ${r.unit.replace(/_/g, '\\_')} \\\\`;
    });

    return `\\begin{table}[h]
\\centering
\\caption{Golden Universe Theoretical Predictions vs. Experimental Values}
\\label{tab:gu-results}
\\begin{tabular}{lcccc}
\\hline
\\textbf{Quantity} & \\textbf{Theoretical} & \\textbf{Experimental} & \\textbf{Error (ppm)} & \\textbf{Unit} \\\\
\\hline
${rows.join('\n')}
\\hline
\\end{tabular}
\\end{table}`;
  };

  const formatExcel = (data: ResultData[]): string => {
    // Simple TSV format that Excel can open
    const headers = [
      'Name',
      'Category',
      'Theoretical',
      'Experimental',
      'Error (ppm)',
      'Error (%)',
      'Precision',
      'Unit',
      'Formula',
      'Breakthrough',
    ];

    const rows = data.map(r => [
      r.name,
      r.category,
      r.theoretical,
      r.experimental,
      r.errorPpm,
      r.errorPercent,
      r.precision,
      r.unit,
      r.formula || '',
      r.breakthrough ? 'Yes' : 'No',
    ]);

    return [
      headers.join('\t'),
      ...rows.map(row => row.join('\t')),
    ].join('\n');
  };

  const downloadFile = (content: string, format: ExportFormat['type']) => {
    const extensions = {
      csv: 'csv',
      excel: 'tsv',
      json: 'json',
      latex: 'tex',
    };

    const mimeTypes = {
      csv: 'text/csv',
      excel: 'text/tab-separated-values',
      json: 'application/json',
      latex: 'text/x-tex',
    };

    const blob = new Blob([content], { type: mimeTypes[format] });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${filename}.${extensions[format]}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handleExport = (format: ExportFormat['type']) => {
    let content = '';

    switch (format) {
      case 'csv':
        content = formatCSV(results);
        break;
      case 'excel':
        content = formatExcel(results);
        break;
      case 'json':
        content = formatJSON(results);
        break;
      case 'latex':
        content = formatLaTeX(results);
        break;
    }

    downloadFile(content, format);
    setIsOpen(false);
  };

  const handleCopyToClipboard = async () => {
    const content = formatCSV(results);
    try {
      await navigator.clipboard.writeText(content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy to clipboard:', err);
    }
  };

  return (
    <div className="export-options">
      <button
        className="export-trigger-btn"
        onClick={() => setIsOpen(!isOpen)}
      >
        Export Results
      </button>

      {isOpen && (
        <div className="export-menu">
          <div className="export-menu-header">
            <h4>Export Options</h4>
            <button
              className="close-btn"
              onClick={() => setIsOpen(false)}
              aria-label="Close"
            >
              ×
            </button>
          </div>

          <div className="export-options-list">
            <button
              className="export-option-btn"
              onClick={() => handleExport('csv')}
            >
              <div className="option-icon">📄</div>
              <div className="option-content">
                <div className="option-title">CSV Export</div>
                <div className="option-description">
                  Comma-separated values for Excel/Sheets
                </div>
              </div>
            </button>

            <button
              className="export-option-btn"
              onClick={() => handleExport('excel')}
            >
              <div className="option-icon">📊</div>
              <div className="option-content">
                <div className="option-title">Excel Export</div>
                <div className="option-description">
                  Tab-separated format with formatting
                </div>
              </div>
            </button>

            <button
              className="export-option-btn"
              onClick={() => handleExport('json')}
            >
              <div className="option-icon">🔧</div>
              <div className="option-content">
                <div className="option-title">JSON Export</div>
                <div className="option-description">
                  Programmatic access with metadata
                </div>
              </div>
            </button>

            <button
              className="export-option-btn"
              onClick={() => handleExport('latex')}
            >
              <div className="option-icon">📝</div>
              <div className="option-content">
                <div className="option-title">LaTeX Export</div>
                <div className="option-description">
                  Ready-to-use table for papers
                </div>
              </div>
            </button>

            <button
              className={`export-option-btn ${copied ? 'copied' : ''}`}
              onClick={handleCopyToClipboard}
            >
              <div className="option-icon">{copied ? '✓' : '📋'}</div>
              <div className="option-content">
                <div className="option-title">
                  {copied ? 'Copied!' : 'Copy to Clipboard'}
                </div>
                <div className="option-description">
                  Copy data as CSV format
                </div>
              </div>
            </button>
          </div>

          <div className="export-info">
            <p>
              Exporting {results.length} result{results.length !== 1 ? 's' : ''}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};
