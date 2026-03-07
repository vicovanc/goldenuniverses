import React, { useEffect, useRef, useState } from 'react';
import katex from 'katex';
import 'katex/dist/katex.min.css';
import { ensureLatexFormat } from '@/utils/equationFormatter';

interface EquationRendererProps {
  equation: string;
  displayMode?: boolean;
  className?: string;
  allowCopy?: boolean;
  allowZoom?: boolean;
}

const EquationRenderer: React.FC<EquationRendererProps> = ({
  equation,
  displayMode = false,
  className = '',
  allowCopy = true,
  allowZoom = true,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [isZoomed, setIsZoomed] = useState(false);
  const [copied, setCopied] = useState(false);
  const [renderError, setRenderError] = useState<string | null>(null);

  useEffect(() => {
    if (containerRef.current && equation) {
      try {
        setRenderError(null);
        // First convert from plain text to LaTeX format if needed
        let processedEquation = ensureLatexFormat(equation)
          // Fix common LaTeX issues
          .replace(/\s+/g, ' ') // Normalize whitespace
          .replace(/\\bar\{([^}]+)\}/g, '\\overline{$1}') // Fix bar notation
          .replace(/\\tilde\{([^}]+)\}/g, '\\widetilde{$1}') // Fix tilde notation
          .replace(/Ω/g, '\\Omega') // Greek letter Omega
          .replace(/Ψ/g, '\\Psi') // Greek letter Psi
          .replace(/γ/g, '\\gamma') // Greek letter gamma
          .replace(/λ/g, '\\lambda') // Greek letter lambda
          .replace(/μ/g, '\\mu') // Greek letter mu
          .replace(/ν/g, '\\nu') // Greek letter nu
          .replace(/φ/g, '\\varphi') // Greek letter phi
          .replace(/σ/g, '\\sigma') // Greek letter sigma
          .replace(/τ/g, '\\tau') // Greek letter tau
          .replace(/ℏ/g, '\\hbar') // Reduced Planck constant
          .replace(/∂/g, '\\partial') // Partial derivative
          .replace(/∫/g, '\\int') // Integral
          .replace(/Σ/g, '\\sum') // Sum
          .replace(/□/g, '\\square') // D'Alembertian operator
          .replace(/≈/g, '\\approx') // Approximately equal
          .replace(/⋅/g, '\\cdot') // Dot product
          .replace(/×/g, '\\times') // Cross product
          .replace(/∞/g, '\\infty') // Infinity
          .replace(/√/g, '\\sqrt') // Square root
          .replace(/≡/g, '\\equiv') // Equivalent
          .replace(/≠/g, '\\neq') // Not equal
          .replace(/≤/g, '\\leq') // Less than or equal
          .replace(/≥/g, '\\geq') // Greater than or equal
          .replace(/→/g, '\\rightarrow') // Right arrow
          .replace(/←/g, '\\leftarrow') // Left arrow
          .replace(/↔/g, '\\leftrightarrow') // Bidirectional arrow
          .replace(/⇒/g, '\\Rightarrow') // Double right arrow
          .replace(/∈/g, '\\in') // Element of
          .replace(/∉/g, '\\notin') // Not element of
          .replace(/⊂/g, '\\subset') // Subset
          .replace(/⊃/g, '\\supset') // Superset
          .replace(/∀/g, '\\forall') // For all
          .replace(/∃/g, '\\exists') // Exists
          .replace(/∇/g, '\\nabla') // Nabla/gradient
          .replace(/·/g, '\\cdot') // Middle dot
          .replace(/π/g, '\\pi') // Pi
          .replace(/α/g, '\\alpha') // Alpha
          .replace(/β/g, '\\beta') // Beta
          .replace(/δ/g, '\\delta') // Delta
          .replace(/ε/g, '\\varepsilon') // Epsilon
          .replace(/θ/g, '\\theta') // Theta
          .replace(/κ/g, '\\kappa') // Kappa
          .replace(/ρ/g, '\\rho') // Rho
          .replace(/ω/g, '\\omega') // Omega (lowercase)
          .replace(/Γ/g, '\\Gamma') // Gamma (uppercase)
          .replace(/Δ/g, '\\Delta') // Delta (uppercase)
          .replace(/Λ/g, '\\Lambda') // Lambda (uppercase)
          .replace(/Φ/g, '\\Phi') // Phi (uppercase)
          .replace(/Θ/g, '\\Theta'); // Theta (uppercase)

        const html = katex.renderToString(processedEquation, {
          displayMode,
          throwOnError: false,
          errorColor: '#F59E0B', // Golden color for errors
          strict: false,
          trust: false,
          fleqn: false, // Center equations
          macros: {
            '\\Omega': '\\Omega',
            '\\bar': '\\overline',
            '\\tilde': '\\widetilde',
            '\\square': '\\Box',
            '\\Tr': '\\text{Tr}',
            '\\inv': '\\text{inv}',
            '\\eff': '\\text{eff}',
            '\\tot': '\\text{tot}',
            '\\int': '\\text{int}',
            '\\gauge': '\\text{gauge}',
            '\\kin': '\\text{kin}',
            '\\fullOmega': '\\text{full}\\Omega',
            '\\angularmod': '\\text{angular-mod}',
            '\\phasecoupler': '\\text{phase-couple}',
            '\\memcouple': '\\text{mem-couple}',
            '\\recursivemimic': '\\text{recursive-mimic}',
            '\\phasedriver': '\\text{phase-driver}',
            '\\target': '\\text{target}',
            '\\ang': '\\text{ang}',
            '\\lobes': '\\text{lobes}',
            '\\prim': '\\text{prim}',
            '\\SM': '\\text{SM}',
            '\\electron': '\\text{electron}',
            '\\rec': '\\text{rec}',
            '\\coupling': '\\text{coupling}',
            '\\NLDE': '\\text{NLDE}',
            '\\NonLinearTerms': '\\text{NonLinearTerms}',
            '\\Eff': '\\text{Eff}',
            '\\arg': '\\text{arg}',
            '\\History': '\\text{History}',
          },
        });
        containerRef.current.innerHTML = html;
      } catch (error) {
        setRenderError(error instanceof Error ? error.message : 'Rendering error');
        // Fallback: show the raw equation nicely formatted
        containerRef.current.innerHTML = `<span class="equation-fallback">${equation}</span>`;
      }
    }
  }, [equation, displayMode]);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(equation);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      console.error('Failed to copy equation:', error);
    }
  };

  const handleZoomToggle = () => {
    if (allowZoom) {
      setIsZoomed(!isZoomed);
    }
  };

  return (
    <div className={`equation-renderer ${className} ${isZoomed ? 'zoomed' : ''}`}>
      <div
        ref={containerRef}
        className={`equation-content ${displayMode ? 'display-mode' : 'inline-mode'}`}
        onClick={handleZoomToggle}
        style={{ cursor: allowZoom ? 'zoom-in' : 'default' }}
      />
      {renderError && <div className="equation-error-message">{renderError}</div>}
      <div className="equation-controls">
        {allowCopy && (
          <button
            className={`copy-button ${copied ? 'copied' : ''}`}
            onClick={handleCopy}
            title="Copy LaTeX source"
            aria-label="Copy LaTeX source"
          >
            {copied ? (
              <span className="icon">✓</span>
            ) : (
              <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <path d="M4 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2zm0 1a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V4a1 1 0 0 0-1-1H4z" />
                <path d="M6 0h6a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2v-1a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H6a1 1 0 0 0-1 1H4a2 2 0 0 1 2-2z" />
              </svg>
            )}
          </button>
        )}
      </div>
      {isZoomed && (
        <div className="equation-zoom-overlay" onClick={() => setIsZoomed(false)}>
          <div className="equation-zoom-content" onClick={(e) => e.stopPropagation()}>
            <div
              ref={(el) => {
                if (el && equation) {
                  try {
                    const html = katex.renderToString(equation, {
                      displayMode: true,
                      throwOnError: false,
                      errorColor: '#cc0000',
                      strict: false,
                    });
                    el.innerHTML = html;
                  } catch (error) {
                    console.error('Zoom render error:', error);
                  }
                }
              }}
              className="equation-zoomed"
            />
            <button className="close-zoom" onClick={() => setIsZoomed(false)} aria-label="Close zoom">
              ×
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default EquationRenderer;
