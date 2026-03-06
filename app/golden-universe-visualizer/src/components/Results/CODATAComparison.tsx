/**
 * CODATAComparison - CODATA integration
 * GU-039: CODATA Integration
 * - Import CODATA 2022 values
 * - Automatic comparison with theoretical values
 * - Show differences in ppm/percentage
 * - Reference links to CODATA sources
 */

import React, { useState } from 'react';
import type { ResultData, CODATAValue } from './types';
import { codataValues } from './resultsData';

interface CODATAComparisonProps {
  results: ResultData[];
}

export const CODATAComparison: React.FC<CODATAComparisonProps> = ({
  results,
}) => {
  const [selectedResult, setSelectedResult] = useState<string | null>(null);
  const [showDetails, setShowDetails] = useState(false);

  // Match results with CODATA values
  const matchedResults = results.map(result => {
    const codata = codataValues.find(c =>
      c.name.toLowerCase() === result.name.toLowerCase()
    );
    return { result, codata };
  }).filter(m => m.codata !== undefined);

  const getCODATASource = (codata: CODATAValue): string => {
    if (codata.doi) {
      return `https://doi.org/${codata.doi}`;
    }
    if (codata.year === 2022) {
      return 'https://physics.nist.gov/cuu/Constants/';
    }
    return 'https://physics.nist.gov/cuu/Constants/archive2018.html';
  };

  const calculateRelativeError = (theoretical: number, experimental: number): number => {
    return ((theoretical - experimental) / experimental) * 100;
  };

  const calculateSigmaDeviation = (
    theoretical: number,
    experimental: number,
    uncertainty: number
  ): number => {
    return Math.abs((theoretical - experimental) / uncertainty);
  };

  const formatUncertainty = (value: number, uncertainty: number): string => {
    // Determine significant figures based on uncertainty
    const orderOfMagnitude = Math.floor(Math.log10(Math.abs(uncertainty)));
    const decimals = Math.max(0, -orderOfMagnitude + 1);

    return `${value.toExponential(decimals)} ± ${uncertainty.toExponential(1)}`;
  };

  return (
    <div className="codata-comparison">
      <div className="codata-header">
        <h3>CODATA Comparison</h3>
        <button
          className="details-toggle"
          onClick={() => setShowDetails(!showDetails)}
        >
          {showDetails ? 'Hide Details' : 'Show Details'}
        </button>
      </div>

      <div className="codata-info">
        <p>
          Comparing {matchedResults.length} Golden Universe predictions with
          experimental values from the{' '}
          <a
            href="https://physics.nist.gov/cuu/Constants/"
            target="_blank"
            rel="noopener noreferrer"
          >
            CODATA database
          </a>
          .
        </p>
      </div>

      <div className="codata-grid">
        {matchedResults.map(({ result, codata }, idx) => {
          if (!codata) return null;

          const isSelected = selectedResult === result.id;
          const relativeError = calculateRelativeError(
            result.theoretical,
            codata.value
          );
          const sigmaDeviation = calculateSigmaDeviation(
            result.theoretical,
            codata.value,
            codata.uncertainty
          );

          const isWithinUncertainty = Math.abs(sigmaDeviation) < 1;

          return (
            <div
              key={idx}
              className={`codata-card ${isSelected ? 'selected' : ''} ${isWithinUncertainty ? 'within-uncertainty' : ''}`}
              onClick={() => setSelectedResult(isSelected ? null : result.id)}
            >
              <div className="codata-card-header">
                <h4>{result.name}</h4>
                <span className={`category-badge ${result.category}`}>
                  {result.category}
                </span>
              </div>

              <div className="codata-values">
                <div className="value-row">
                  <span className="value-label">GU Theory:</span>
                  <span className="value-data theoretical">
                    {result.theoretical.toExponential(10)}
                  </span>
                </div>
                <div className="value-row">
                  <span className="value-label">CODATA {codata.year}:</span>
                  <span className="value-data experimental">
                    {showDetails
                      ? formatUncertainty(codata.value, codata.uncertainty)
                      : codata.value.toExponential(10)}
                  </span>
                </div>
              </div>

              <div className="codata-metrics">
                <div className="metric">
                  <span className="metric-label">Error:</span>
                  <span className="metric-value">
                    {Math.abs(result.errorPpm) < 0.01
                      ? '< 0.01 ppm'
                      : Math.abs(result.errorPpm) < 1000
                      ? `${Math.abs(result.errorPpm).toFixed(2)} ppm`
                      : `${Math.abs(relativeError).toFixed(4)}%`}
                  </span>
                </div>
                {showDetails && (
                  <div className="metric">
                    <span className="metric-label">σ deviation:</span>
                    <span
                      className={`metric-value ${isWithinUncertainty ? 'good' : 'warning'}`}
                    >
                      {sigmaDeviation.toFixed(2)}σ
                    </span>
                  </div>
                )}
              </div>

              {showDetails && isSelected && (
                <div className="codata-details">
                  <div className="detail-row">
                    <span>Absolute difference:</span>
                    <span>{Math.abs(result.theoretical - codata.value).toExponential(4)}</span>
                  </div>
                  <div className="detail-row">
                    <span>Relative error:</span>
                    <span>{relativeError.toFixed(6)}%</span>
                  </div>
                  <div className="detail-row">
                    <span>CODATA uncertainty:</span>
                    <span>{codata.uncertainty.toExponential(2)}</span>
                  </div>
                  <div className="detail-row">
                    <span>Within uncertainty:</span>
                    <span className={isWithinUncertainty ? 'yes' : 'no'}>
                      {isWithinUncertainty ? 'Yes' : 'No'}
                    </span>
                  </div>
                  <div className="reference-link">
                    <a
                      href={getCODATASource(codata)}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      View CODATA Source →
                    </a>
                  </div>
                </div>
              )}

              {isWithinUncertainty && (
                <div className="uncertainty-badge">
                  Within experimental uncertainty
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Summary Statistics */}
      <div className="codata-summary">
        <h4>Comparison Summary</h4>
        <div className="summary-grid">
          <div className="summary-item">
            <div className="summary-value">
              {matchedResults.filter(({ result, codata }) => {
                if (!codata) return false;
                const sigma = calculateSigmaDeviation(
                  result.theoretical,
                  codata.value,
                  codata.uncertainty
                );
                return Math.abs(sigma) < 1;
              }).length}
            </div>
            <div className="summary-label">Within 1σ</div>
          </div>
          <div className="summary-item">
            <div className="summary-value">
              {matchedResults.filter(({ result }) =>
                Math.abs(result.errorPpm) < 100
              ).length}
            </div>
            <div className="summary-label">Sub-100 ppm</div>
          </div>
          <div className="summary-item">
            <div className="summary-value">
              {matchedResults.filter(({ result }) =>
                Math.abs(result.errorPpm) < 10
              ).length}
            </div>
            <div className="summary-label">Sub-10 ppm</div>
          </div>
          <div className="summary-item">
            <div className="summary-value">
              {matchedResults.filter(({ result }) =>
                Math.abs(result.errorPpm) < 1
              ).length}
            </div>
            <div className="summary-label">Sub-1 ppm</div>
          </div>
        </div>
      </div>

      {/* CODATA Info */}
      <div className="codata-about">
        <h4>About CODATA</h4>
        <p>
          The Committee on Data for Science and Technology (CODATA) provides
          internationally recommended values of fundamental physical constants
          based on a least-squares adjustment of all available data.
        </p>
        <p>
          The most recent adjustment was published in 2018. CODATA 2022 values
          are expected to be released soon.
        </p>
      </div>
    </div>
  );
};
