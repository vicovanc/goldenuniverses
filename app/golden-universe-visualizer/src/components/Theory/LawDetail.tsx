import React from 'react';
import { TheoryLaw } from '@/types/theory';
import { getLawDependencies, getLawDependents } from '@/data/theoryLaws';
import EquationRenderer from './EquationRenderer';

interface LawDetailProps {
  law: TheoryLaw;
  onNavigate?: (lawId: number) => void;
}

const LawDetail: React.FC<LawDetailProps> = ({ law, onNavigate }) => {
  const dependencies = getLawDependencies(law.id);
  const dependents = getLawDependents(law.id);

  const getStatusBadge = (status: string) => {
    const statusMap: { [key: string]: { label: string; className: string } } = {
      'fully-defined': { label: 'Fully Defined', className: 'status-fully-defined' },
      'partially-defined': { label: 'Partially Defined', className: 'status-partially-defined' },
      'form-defined': { label: 'Form Defined', className: 'status-form-defined' },
      schematic: { label: 'Schematic', className: 'status-schematic' },
      derived: { label: 'Derived', className: 'status-derived' },
      validated: { label: 'Validated', className: 'status-validated' },
    };

    const statusInfo = statusMap[status] || { label: status, className: 'status-default' };

    return <span className={`status-badge ${statusInfo.className}`}>{statusInfo.label}</span>;
  };

  const getCategoryBadge = (category: string) => {
    const categoryMap: { [key: string]: { label: string; className: string } } = {
      foundation: { label: 'Foundation', className: 'category-foundation' },
      symmetry: { label: 'Symmetry', className: 'category-symmetry' },
      particles: { label: 'Particles', className: 'category-particles' },
      advanced: { label: 'Advanced', className: 'category-advanced' },
    };

    const categoryInfo = categoryMap[category] || { label: category, className: 'category-default' };

    return <span className={`category-badge ${categoryInfo.className}`}>{categoryInfo.label}</span>;
  };

  return (
    <div className="law-detail">
      <div className="law-header">
        <div className="law-title-section">
          <h2 className="law-number">Law {law.id}</h2>
          <h1 className="law-title">{law.title}</h1>
        </div>
        <div className="law-badges">
          {getStatusBadge(law.status)}
          {getCategoryBadge(law.category)}
        </div>
      </div>

      <div className="law-statement">
        <h3>Statement</h3>
        <p>{law.statement}</p>
      </div>

      {law.equations && law.equations.length > 0 && (
        <div className="law-equations">
          <h3>Equations</h3>
          <div className="equations-list">
            {law.equations.map((equation, index) => (
              <div key={index} className="equation-item">
                <EquationRenderer equation={equation} displayMode={true} />
              </div>
            ))}
          </div>
        </div>
      )}

      {law.subLaws && law.subLaws.length > 0 && (
        <div className="law-sublaws">
          <h3>Sub-Laws</h3>
          {law.subLaws.map((subLaw) => (
            <div key={subLaw.id} className="sublaw-item">
              <h4>
                Law {law.id}
                {subLaw.id}: {subLaw.title}
              </h4>
              <p className="sublaw-description">{subLaw.description}</p>
              {subLaw.equations && subLaw.equations.length > 0 && (
                <div className="sublaw-equations">
                  {subLaw.equations.map((equation, index) => (
                    <EquationRenderer key={index} equation={equation} displayMode={true} />
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {law.content && (
        <div className="law-content">
          <h3>Details</h3>
          <div className="content-text">{law.content}</div>
        </div>
      )}

      {law.validationResults && law.validationResults.length > 0 && (
        <div className="law-validation">
          <h3>Validation Results</h3>
          <div className="validation-list">
            {law.validationResults.map((result, index) => (
              <div key={index} className={`validation-item ${result.validated ? 'validated' : 'not-validated'}`}>
                <div className="validation-icon">{result.validated ? '✓' : '✗'}</div>
                <div className="validation-content">
                  <div className="validation-description">{result.description}</div>
                  <div className="validation-value">{result.value}</div>
                  {result.error && <div className="validation-error">Error: {result.error}</div>}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {law.gaps && law.gaps.length > 0 && (
        <div className="law-gaps">
          <h3>Known Gaps</h3>
          <ul className="gaps-list">
            {law.gaps.map((gap, index) => (
              <li key={index} className="gap-item">
                {gap}
              </li>
            ))}
          </ul>
        </div>
      )}

      {law.pythonImplementations && law.pythonImplementations.length > 0 && (
        <div className="law-implementations">
          <h3>Python Implementations</h3>
          <ul className="implementations-list">
            {law.pythonImplementations.map((file, index) => (
              <li key={index} className="implementation-item">
                <code>{file}</code>
              </li>
            ))}
          </ul>
        </div>
      )}

      {(dependencies.length > 0 || dependents.length > 0) && (
        <div className="law-dependencies">
          {dependencies.length > 0 && (
            <div className="dependencies-section">
              <h3>Depends On</h3>
              <div className="dependency-links">
                {dependencies.map((depId) => (
                  <button
                    key={depId}
                    className="dependency-link"
                    onClick={() => onNavigate?.(depId)}
                    aria-label={`Navigate to Law ${depId}`}
                  >
                    Law {depId}
                  </button>
                ))}
              </div>
            </div>
          )}

          {dependents.length > 0 && (
            <div className="dependents-section">
              <h3>Used By</h3>
              <div className="dependency-links">
                {dependents.map((depId) => (
                  <button
                    key={depId}
                    className="dependency-link"
                    onClick={() => onNavigate?.(depId)}
                    aria-label={`Navigate to Law ${depId}`}
                  >
                    Law {depId}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default LawDetail;
