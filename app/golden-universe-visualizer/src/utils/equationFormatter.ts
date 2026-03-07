/**
 * Converts plain text mathematical notation to LaTeX format
 * This handles the specific notation used in the Golden Universe theory equations
 */
export function convertToLatex(plainText: string): string {
  if (!plainText) return '';

  let latex = plainText;

  // Handle exponential notation exp(...) -> e^{...}
  latex = latex.replace(/exp\((.*?)\)/g, (match, content) => {
    // Recursively convert the content inside exp()
    const innerLatex = convertToLatex(content);
    return `e^{${innerLatex}}`;
  });

  // Convert multiplication dot to LaTeX cdot
  latex = latex.replace(/·/g, ' \\cdot ');
  latex = latex.replace(/\*/g, ' \\cdot ');

  // Handle fractions a/b -> \frac{a}{b}
  // This needs to be smart about what constitutes the numerator and denominator
  latex = latex.replace(/([a-zA-Z0-9φπθλμνρσωαβγδεζηκξτυχψΩΨΓΔΘΛΞΠΣΦΧΨΩ]+(?:\^[a-zA-Z0-9]+)?)\s*\/\s*([a-zA-Z0-9φπθλμνρσωαβγδεζηκξτυχψΩΨΓΔΘΛΞΠΣΦΧΨΩ]+(?:\^[a-zA-Z0-9]+)?)/g, '\\frac{$1}{$2}');

  // Handle complex fractions (1+√5)/2 -> \frac{1+\sqrt{5}}{2}
  latex = latex.replace(/\((.*?)\)\s*\/\s*([a-zA-Z0-9]+)/g, '\\frac{$1}{$2}');
  latex = latex.replace(/([a-zA-Z0-9]+)\s*\/\s*\((.*?)\)/g, '\\frac{$1}{$2}');
  latex = latex.replace(/\((.*?)\)\s*\/\s*\((.*?)\)/g, '\\frac{$1}{$2}');

  // Convert square roots
  latex = latex.replace(/√(\d+)/g, '\\sqrt{$1}');
  latex = latex.replace(/√([a-zA-Z])/g, '\\sqrt{$1}');
  latex = latex.replace(/sqrt\((.*?)\)/g, '\\sqrt{$1}');

  // Convert superscripts (must come before Greek letter conversion)
  latex = latex.replace(/\^(-?\d+)/g, '^{$1}');
  latex = latex.replace(/\^([a-zA-Z]+)/g, '^{$1}');
  latex = latex.replace(/\^([nmijtk])/g, '^{$1}');

  // Convert subscripts
  latex = latex.replace(/_([a-zA-Z0-9]+)/g, '_{$1}');

  // Greek letters (uppercase)
  latex = latex.replace(/Ω/g, '\\Omega');
  latex = latex.replace(/Ψ/g, '\\Psi');
  latex = latex.replace(/Φ/g, '\\Phi');
  latex = latex.replace(/Γ/g, '\\Gamma');
  latex = latex.replace(/Δ/g, '\\Delta');
  latex = latex.replace(/Θ/g, '\\Theta');
  latex = latex.replace(/Λ/g, '\\Lambda');
  latex = latex.replace(/Ξ/g, '\\Xi');
  latex = latex.replace(/Π/g, '\\Pi');
  latex = latex.replace(/Σ/g, '\\Sigma');

  // Greek letters (lowercase)
  latex = latex.replace(/α/g, '\\alpha');
  latex = latex.replace(/β/g, '\\beta');
  latex = latex.replace(/γ/g, '\\gamma');
  latex = latex.replace(/δ/g, '\\delta');
  latex = latex.replace(/ε/g, '\\varepsilon');
  latex = latex.replace(/ζ/g, '\\zeta');
  latex = latex.replace(/η/g, '\\eta');
  latex = latex.replace(/θ/g, '\\theta');
  latex = latex.replace(/κ/g, '\\kappa');
  latex = latex.replace(/λ/g, '\\lambda');
  latex = latex.replace(/μ/g, '\\mu');
  latex = latex.replace(/ν/g, '\\nu');
  latex = latex.replace(/ξ/g, '\\xi');
  latex = latex.replace(/π/g, '\\pi');
  latex = latex.replace(/ρ/g, '\\rho');
  latex = latex.replace(/σ/g, '\\sigma');
  latex = latex.replace(/τ/g, '\\tau');
  latex = latex.replace(/υ/g, '\\upsilon');
  latex = latex.replace(/φ/g, '\\varphi');
  latex = latex.replace(/χ/g, '\\chi');
  latex = latex.replace(/ψ/g, '\\psi');
  latex = latex.replace(/ω/g, '\\omega');

  // Special symbols
  latex = latex.replace(/∂/g, '\\partial');
  latex = latex.replace(/∇/g, '\\nabla');
  latex = latex.replace(/∫/g, '\\int');
  latex = latex.replace(/∑/g, '\\sum');
  latex = latex.replace(/∏/g, '\\prod');
  latex = latex.replace(/∞/g, '\\infty');
  latex = latex.replace(/±/g, '\\pm');
  latex = latex.replace(/≈/g, '\\approx');
  latex = latex.replace(/≡/g, '\\equiv');
  latex = latex.replace(/≠/g, '\\neq');
  latex = latex.replace(/≤/g, '\\leq');
  latex = latex.replace(/≥/g, '\\geq');
  latex = latex.replace(/×/g, '\\times');
  latex = latex.replace(/→/g, '\\rightarrow');
  latex = latex.replace(/←/g, '\\leftarrow');
  latex = latex.replace(/↔/g, '\\leftrightarrow');
  latex = latex.replace(/⇒/g, '\\Rightarrow');
  latex = latex.replace(/∈/g, '\\in');
  latex = latex.replace(/∉/g, '\\notin');
  latex = latex.replace(/⊂/g, '\\subset');
  latex = latex.replace(/⊃/g, '\\supset');
  latex = latex.replace(/∀/g, '\\forall');
  latex = latex.replace(/∃/g, '\\exists');

  // Special physics notation
  latex = latex.replace(/ℏ/g, '\\hbar');
  latex = latex.replace(/□/g, '\\Box'); // D'Alembertian

  // Handle functions
  latex = latex.replace(/sin\(/g, '\\sin(');
  latex = latex.replace(/cos\(/g, '\\cos(');
  latex = latex.replace(/tan\(/g, '\\tan(');
  latex = latex.replace(/log\(/g, '\\log(');
  latex = latex.replace(/ln\(/g, '\\ln(');

  // Handle integrals with limits
  latex = latex.replace(/∫_([a-zA-Z0-9]+)\^([a-zA-Z0-9∞]+)/g, '\\int_{$1}^{$2}');

  // Handle special Golden Universe notation
  latex = latex.replace(/S_0/g, 'S_0');
  latex = latex.replace(/N_e/g, 'N_e');
  latex = latex.replace(/C_e/g, 'C_e');
  latex = latex.replace(/m_e/g, 'm_e');
  latex = latex.replace(/X_e/g, 'X_e');
  latex = latex.replace(/L_([a-zA-Z]+)/g, 'L_{$1}');

  // Handle complex expressions like (1+√5)/2
  // This should already be handled above, but let's make sure
  latex = latex.replace(/\(1\+\\sqrt\{5\}\)\\cdot 2\^{-1}/g, '\\frac{1+\\sqrt{5}}{2}');

  // Clean up extra spaces
  latex = latex.replace(/\s+/g, ' ');
  latex = latex.trim();

  return latex;
}

/**
 * Check if a string is already in LaTeX format
 */
export function isLatexFormat(text: string): boolean {
  // Check for common LaTeX commands
  const latexPatterns = [
    /\\frac/,
    /\\sqrt/,
    /\\alpha/,
    /\\beta/,
    /\\gamma/,
    /\\theta/,
    /\\phi/,
    /\\varphi/,
    /\\psi/,
    /\\omega/,
    /\\Omega/,
    /\\Psi/,
    /\\cdot/,
    /\\times/,
    /\\partial/,
    /\\int/,
    /\\sum/,
    /\^{/,
    /_{/
  ];

  return latexPatterns.some(pattern => pattern.test(text));
}

/**
 * Smart conversion that only converts if not already LaTeX
 */
export function ensureLatexFormat(text: string): string {
  if (isLatexFormat(text)) {
    return text;
  }
  return convertToLatex(text);
}