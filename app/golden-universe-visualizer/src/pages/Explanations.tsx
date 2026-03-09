import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';
import { THEORY_LAWS, EXPERIMENTAL_VALIDATIONS, DERIVATION_FILES } from '@/data/theoryContentExports';
import { lagrangianTerms } from '../data/theoryLaws';
import EquationRenderer from '../components/Theory/EquationRenderer';
import ExplanationTopic from '@/components/Explanations/ExplanationTopic';
import './Explanations.scss';

interface ExplanationCategory {
  id: string;
  title: string;
  icon: string;
  description: string;
}

const categories: ExplanationCategory[] = [
  {
    id: 'documents',
    title: 'Complete Theory Papers',
    icon: '📚',
    description: 'Comprehensive theoretical papers and documentation'
  },
  {
    id: 'overview',
    title: 'Theory Overview',
    icon: '🌌',
    description: 'Introduction to the Golden Universe theory and its foundations'
  },
  {
    id: 'foundation',
    title: 'Foundation Laws (0-5)',
    icon: '🏗️',
    description: 'Action principle, Lagrangian structure, and fundamental symmetries'
  },
  {
    id: 'symmetry',
    title: 'Symmetry Laws (6-15)',
    icon: '🔄',
    description: 'Symmetry breaking cascade, charge quantization, and gauge theories'
  },
  {
    id: 'particles',
    title: 'Particle Laws (16-25)',
    icon: '⚛️',
    description: 'Particle masses, generations, and fundamental constants'
  },
  {
    id: 'cosmology',
    title: 'Cosmological Laws (26-30)',
    icon: '🌍',
    description: 'Universe expansion, dark matter, and cosmic evolution'
  },
  {
    id: 'advanced',
    title: 'Advanced Laws (31-38)',
    icon: '🔬',
    description: 'Quantum corrections, CP violation, and unification'
  },
  {
    id: 'lagrangian',
    title: 'Lagrangian Structure',
    icon: '∫',
    description: 'The six fundamental terms of the master Lagrangian'
  },
  {
    id: 'validations',
    title: 'Experimental Validations',
    icon: '✅',
    description: 'Precision measurements confirming theoretical predictions'
  },
  {
    id: 'calculations',
    title: 'Python Calculations',
    icon: '🐍',
    description: '371+ derivations and numerical calculations'
  },
  {
    id: 'concepts',
    title: 'Key Concepts',
    icon: '💡',
    description: 'Electron, gravity, consciousness, time, mass, and charge explained'
  }
];

// Theory document metadata
interface TheoryDocument {
  id: string;
  title: string;
  filename: string;
  category: 'core' | 'physics' | 'cosmology' | 'explanatory' | 'technical';
  description?: string;
}

// List of all theory documents
const THEORY_DOCUMENTS: TheoryDocument[] = [
  // Core Theory Documents
  {
    id: 'complete-theory',
    title: 'The Complete Golden Universe Theory',
    filename: 'COMPLETE_GOLDEN_UNIVERSE_THEORY.md',
    category: 'core',
    description: 'Complete derivation from three numbers to all of reality',
  },
  {
    id: 'formation',
    title: 'The Golden Universe Formation',
    filename: 'The Golden Universe Formation.md',
    category: 'core',
    description: 'Core formation principles and mechanisms',
  },
  {
    id: 'demonstration',
    title: 'Cosmological and Symmetrical Genesis',
    filename: 'The Golden Universe- A Demonstration of Cosmological and Symmetrical Genesis.md',
    category: 'core',
    description: 'Mathematical demonstration of the theory',
  },
  {
    id: 'first-principles',
    title: 'Emergent Reality from Geometric First Principles',
    filename: 'The Golden Universe- A Theory of Emergent Reality from Geometric First Principles - V2.md',
    category: 'core',
    description: 'Geometric foundations of reality',
  },

  // Physics Documents
  {
    id: 'particles',
    title: 'Calculation of Particles',
    filename: 'Golden Universe Theory for the Calculation of Particles v2.md',
    category: 'physics',
    description: 'Complete particle mass derivations',
  },
  {
    id: 'electron',
    title: 'What is the Electron?',
    filename: 'WHAT_IS_THE_ELECTRON.md',
    category: 'physics',
    description: 'Deep dive into electron physics',
  },
  {
    id: 'proton',
    title: 'What is the Proton?',
    filename: 'WHAT_IS_THE_PROTON.md',
    category: 'physics',
    description: 'Understanding proton structure',
  },
  {
    id: 'gravity',
    title: 'What is Gravity?',
    filename: 'WHAT_IS_GRAVITY.md',
    category: 'physics',
    description: 'Gravity in the Golden Universe framework',
  },

  // Cosmology Documents
  {
    id: 'cosmological-closure',
    title: 'Cosmological Closure Analysis',
    filename: 'GU_COSMOLOGICAL_CLOSURE.md',
    category: 'cosmology',
    description: 'Complete cosmological framework closure',
  },
  {
    id: 'formation-en',
    title: 'GU Formation (English)',
    filename: 'GU_Formation_0_EN.md',
    category: 'cosmology',
    description: 'Formation theory in detail',
  },

  // Explanatory Documents
  {
    id: 'consciousness',
    title: 'Consciousness and the Golden Universe',
    filename: 'CONSCIOUSNESS.md',
    category: 'explanatory',
    description: 'How consciousness emerges from the framework',
  },
  {
    id: 'consciousness-readme',
    title: 'Understanding GU Consciousness',
    filename: 'README_GU_CONSCIOUSNESS.md',
    category: 'explanatory',
    description: 'Introduction to consciousness in GU',
  },

  // Technical Documents
  {
    id: 'laws-333',
    title: 'The 333 Laws',
    filename: 'GU_Laws_333.md',
    category: 'technical',
    description: 'Complete set of theoretical laws',
  },
  {
    id: 'theory-laws',
    title: 'Theory Laws',
    filename: 'theory-laws.md',
    category: 'technical',
    description: 'Core theoretical laws',
  },
  {
    id: 'theory-laws-updated',
    title: 'Updated Theory Laws',
    filename: 'THEORY_LAWS_UPDATED.md',
    category: 'technical',
    description: 'Latest version of theory laws',
  },
  {
    id: 'derived-laws',
    title: 'Derived Laws',
    filename: 'derived-laws.md',
    category: 'technical',
    description: 'Laws derived from core principles',
  },
  {
    id: 'memory-regime',
    title: 'Memory Regime Map',
    filename: 'GU_MEMORY_REGIME_MAP.md',
    category: 'technical',
    description: 'Memory mechanisms across scales',
  },
  {
    id: 'notation',
    title: 'Notation Standard',
    filename: 'NOTATION_STANDARD.md',
    category: 'technical',
    description: 'Standard notation and conventions',
  },
];

const Explanations: React.FC = () => {
  const { '*': topic } = useParams<{ '*': string }>();
  const navigate = useNavigate();
  const category = topic; // Use topic as category
  const [selectedLaw, setSelectedLaw] = useState<number | null>(null);
  const [selectedDoc, setSelectedDoc] = useState<string>('complete-theory');
  const [markdownContent, setMarkdownContent] = useState<string>('');
  const [loadingDoc, setLoadingDoc] = useState(false);
  const [docError, setDocError] = useState<string | null>(null);

  const PHI = 1.618033988749895;

  // Load markdown document
  useEffect(() => {
    if (category === 'documents' && selectedDoc) {
      const loadMarkdown = async () => {
        const doc = THEORY_DOCUMENTS.find(d => d.id === selectedDoc);
        if (!doc) return;

        setLoadingDoc(true);
        setDocError(null);

        try {
          // Try loading from /explanatory/ folder first
          let response = await fetch(`/explanatory/${doc.filename}`);
          if (!response.ok) {
            // Fallback to /data/theory/ if not found
            response = await fetch(`/data/theory/${doc.filename}`);
            if (!response.ok) {
              throw new Error(`Failed to load document: ${doc.filename}`);
            }
          }
          const content = await response.text();
          setMarkdownContent(content);
        } catch (err) {
          console.error('Error loading markdown:', err);
          setDocError(err instanceof Error ? err.message : 'Failed to load document');
          setMarkdownContent('');
        } finally {
          setLoadingDoc(false);
        }
      };

      loadMarkdown();
    }
  }, [category, selectedDoc]);

  const renderOverview = () => (
    <div className="explanation-section">
      <h2>The Golden Universe Theory</h2>
      <p className="intro-text">
        A comprehensive theory of quantum gravity and particle physics based on the golden ratio φ = {PHI.toFixed(15)}
      </p>

      <h3>Core Principles</h3>
      <div className="principles-grid">
        <div className="principle-card">
          <h4>🌀 Golden Ratio Foundation</h4>
          <p>The universe begins with perfect symmetry at the Planck scale, broken by the golden ratio φ = (1+√5)/2</p>
        </div>
        <div className="principle-card">
          <h4>🎭 Action Principle</h4>
          <p>All dynamics follow from extremizing a single action S = ∫ L_total d⁴x</p>
        </div>
        <div className="principle-card">
          <h4>🔄 Recursive Epochs</h4>
          <p>Universe evolves through recursive epochs scaled by φ, with particles forming at specific resonances</p>
        </div>
        <div className="principle-card">
          <h4>🌐 Phase Torus Topology</h4>
          <p>Phase space has topology S¹ × S¹ with golden ratio winding numbers determining particle properties</p>
        </div>
      </div>

      <h3>Key Predictions</h3>
      <ul className="predictions-list">
        <li>✅ Electron mass: 0.510121 MeV (0.17% error)</li>
        <li>✅ Newton's G from first principles (47 ppm)</li>
        <li>✅ Fine structure constant α = 1/137.03599913</li>
        <li>✅ Three particle generations from topology</li>
        <li>📊 Muon mass: 105.7 MeV (predicted)</li>
        <li>📊 Tau mass: 1777 MeV (predicted)</li>
        <li>📊 Proton lifetime &gt; 10³⁴ years</li>
        <li>📊 Dark matter ratio: 5.35</li>
      </ul>
    </div>
  );

  const renderLawsByCategory = (categoryId: string) => {
    const laws = THEORY_LAWS.filter(law => law.category === categoryId);

    return (
      <div className="laws-section">
        <h2>{categories.find(c => c.id === categoryId)?.title}</h2>
        <div className="laws-grid">
          {laws.map(law => (
            <div
              key={law.id}
              className={`law-card ${selectedLaw === law.id ? 'selected' : ''}`}
              onClick={() => setSelectedLaw(selectedLaw === law.id ? null : law.id)}
            >
              <div className="law-header">
                <span className="law-id">Law {law.id}</span>
                <span className={`law-status ${law.status}`}>{law.status}</span>
              </div>
              <h3>{law.name}</h3>
              <p className="law-description">{law.description}</p>

              {law.formula && (
                <div className="law-formula">
                  <EquationRenderer equation={law.formula} />
                </div>
              )}

              {selectedLaw === law.id && (
                <div className="law-details">
                  <h4>Derivation</h4>
                  <p>{law.derivation}</p>

                  {law.precision && (
                    <div className="precision-badge">
                      Precision: {law.precision}
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    );
  };

  const renderLagrangian = () => (
    <div className="lagrangian-section">
      <h2>The Master Lagrangian</h2>
      <p className="intro-text">
        The total Lagrangian decomposes into six fundamental terms that govern all physics:
      </p>

      <div className="lagrangian-equation">
        <EquationRenderer equation="L_{total} = L_Ω + L_X + L_{int} + L_{gauge} + L_{lock} + L_{mem}" />
      </div>

      <div className="lagrangian-terms">
        {lagrangianTerms.map((term, index) => (
          <div key={index} className="lagrangian-term-card">
            <div className="term-header">
              <span className="term-symbol">{term.symbol}</span>
              <h3>{term.name}</h3>
            </div>
            <p className="term-description">{term.description}</p>

            <div className="term-equation">
              <EquationRenderer equation={term.equation} />
            </div>

            {term.components && term.components.length > 0 && (
              <div className="term-components">
                <h4>Components:</h4>
                {term.components.map((comp, idx) => (
                  <div key={idx} className="component">
                    <h5>{comp.name}</h5>
                    <p>{comp.description}</p>
                    <EquationRenderer equation={comp.equation} />
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );

  const renderValidations = () => (
    <div className="validations-section">
      <h2>Experimental Validations</h2>
      <p className="intro-text">
        High-precision measurements confirming theoretical predictions:
      </p>

      <div className="validations-grid">
        {Object.entries(EXPERIMENTAL_VALIDATIONS).map(([key, validation]) => (
          <div key={key} className="validation-card">
            <h3>{key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}</h3>
            <div className="validation-values">
              <div className="value-row">
                <span className="label">Theoretical:</span>
                <span className="value">{validation.theoretical}</span>
              </div>
              <div className="value-row">
                <span className="label">Experimental:</span>
                <span className="value">{validation.experimental}</span>
              </div>
              <div className="value-row">
                <span className="label">Precision:</span>
                <span className="precision">{validation.precision}</span>
              </div>
              <div className={`status ${validation.status.toLowerCase()}`}>
                {validation.status}
              </div>
            </div>
          </div>
        ))}
      </div>

      <h3>Key Achievements</h3>
      <ul className="achievements-list">
        <li>🎯 Electron mass derived from first principles with 0.17% accuracy</li>
        <li>🎯 Newton's gravitational constant G predicted to 47 ppm</li>
        <li>🎯 Fine structure constant α matches experiment to 0.15 ppm</li>
        <li>🎯 Proton mass prediction within 15 ppm</li>
        <li>🎯 Three generations explained topologically</li>
        <li>🎯 Charge quantization from winding numbers</li>
      </ul>
    </div>
  );

  const renderCalculations = () => (
    <div className="calculations-section">
      <h2>Python Implementation Files</h2>
      <p className="intro-text">
        371 Python scripts implementing the theoretical calculations and derivations:
      </p>

      <div className="calculations-grid">
        {Object.entries(DERIVATION_FILES).map(([category, files]) => (
          <div key={category} className="calculation-category">
            <h3>{category.replace(/_/g, ' ').replace(/^\d+\s/, '')}</h3>
            <div className="file-list">
              {files.map((file, idx) => (
                <div key={idx} className="file-item">
                  <span className="file-icon">📄</span>
                  <span className="file-name">{file}</span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="implementation-stats">
        <h3>Implementation Coverage</h3>
        <div className="progress-bars">
          <div className="progress-item">
            <span>Laws Implemented</span>
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: '85%' }}>85%</div>
            </div>
          </div>
          <div className="progress-item">
            <span>Numerical Validations</span>
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: '92%' }}>92%</div>
            </div>
          </div>
          <div className="progress-item">
            <span>Precision Calculations</span>
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: '78%' }}>78%</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderDocuments = () => {
    const DOC_CATEGORIES = [
      { id: 'core', title: 'Core Theory', icon: '🌌' },
      { id: 'physics', title: 'Physics', icon: '⚛️' },
      { id: 'cosmology', title: 'Cosmology', icon: '🌠' },
      { id: 'explanatory', title: 'Explanatory', icon: '💡' },
      { id: 'technical', title: 'Technical', icon: '🔧' },
    ];

    const currentDoc = THEORY_DOCUMENTS.find(d => d.id === selectedDoc);

    return (
      <div className="documents-section">
        <div className="documents-header">
          <h2>Complete Theory Documentation</h2>
          <p className="intro-text">
            Comprehensive theoretical papers, detailed explanations, and technical documentation
          </p>
        </div>

        <div className="documents-container">
          {/* Document Sidebar */}
          <aside className="documents-sidebar">
            <h3>Documents</h3>
            {DOC_CATEGORIES.map(cat => {
              const categoryDocs = THEORY_DOCUMENTS.filter(doc => doc.category === cat.id);
              if (categoryDocs.length === 0) return null;

              return (
                <div key={cat.id} className="doc-category">
                  <h4>
                    {cat.icon} {cat.title}
                  </h4>
                  <div className="doc-list">
                    {categoryDocs.map(doc => (
                      <button
                        key={doc.id}
                        className={`doc-item ${selectedDoc === doc.id ? 'active' : ''}`}
                        onClick={() => setSelectedDoc(doc.id)}
                      >
                        <strong>{doc.title}</strong>
                        {doc.description && <small>{doc.description}</small>}
                      </button>
                    ))}
                  </div>
                </div>
              );
            })}
          </aside>

          {/* Document Content */}
          <main className="document-content">
            {loadingDoc && (
              <div className="loading">
                <div className="spinner" />
                <p>Loading document...</p>
              </div>
            )}

            {docError && (
              <div className="error">
                <h3>Error Loading Document</h3>
                <p>{docError}</p>
                <button onClick={() => setSelectedDoc('complete-theory')}>
                  Return to Main Theory
                </button>
              </div>
            )}

            {!loadingDoc && !docError && markdownContent && (
              <>
                <div className="doc-header">
                  {currentDoc?.description && <p className="doc-description">{currentDoc.description}</p>}
                </div>

                <article className="markdown-content">
                  <ReactMarkdown
                    remarkPlugins={[remarkMath]}
                    rehypePlugins={[rehypeKatex]}
                    components={{
                      // Custom components for better rendering
                      h1: ({ children }) => (
                        <h1 className="theory-heading-1">{children}</h1>
                      ),
                      h2: ({ children }) => (
                        <h2 className="theory-heading-2">{children}</h2>
                      ),
                      h3: ({ children }) => (
                        <h3 className="theory-heading-3">{children}</h3>
                      ),
                      table: ({ children }) => (
                        <div className="table-wrapper">
                          <table>{children}</table>
                        </div>
                      ),
                      code: ({ className, children, ...props }: any) => {
                        const inline = (props as any).inline;
                        if (inline) {
                          return <code className="inline-code">{children}</code>;
                        }
                        const language = className?.replace('language-', '');
                        return (
                          <div className="code-block">
                            {language && (
                              <div className="code-language">{language}</div>
                            )}
                            <pre>
                              <code className={className}>{children}</code>
                            </pre>
                          </div>
                        );
                      },
                      blockquote: ({ children }) => (
                        <blockquote className="theory-quote">{children}</blockquote>
                      ),
                      a: ({ href, children }) => (
                        <a href={href} target="_blank" rel="noopener noreferrer">
                          {children}
                        </a>
                      ),
                    }}
                  >
                    {markdownContent}
                  </ReactMarkdown>
                </article>
              </>
            )}
          </main>
        </div>
      </div>
    );
  };

  const renderConcepts = () => (
    <div className="concepts-section">
      <h2>Fundamental Concepts Explained</h2>

      <div className="concept-card">
        <h3>⚛️ The Electron</h3>
        <p>
          In the Golden Universe theory, the electron emerges as a fundamental soliton - a stable, localized
          wave packet in the substrate field Ω. Its mass (0.510121 MeV) arises from the energy functional
          of the soliton configuration at epoch N=111, with geometric factor C_e = 1.050774.
        </p>
        <div className="formula-box">
          <EquationRenderer equation="m_e = \frac{M_P c^2 \cdot 2\pi C_e}{\phi^{111}}" />
        </div>
      </div>

      <div className="concept-card">
        <h3>🌍 Gravity</h3>
        <p>
          Gravity emerges as a collective phenomenon from the interaction between the cosmic driver field X
          and the substrate field Ω. Newton's gravitational constant is derived from first principles:
        </p>
        <div className="formula-box">
          <EquationRenderer equation="G = \frac{\hbar c}{M_P^2} \cdot \phi^{-34} \cdot e^{2\pi/\phi}" />
        </div>
      </div>

      <div className="concept-card">
        <h3>🧘 Consciousness and Memory</h3>
        <p>
          The memory term L_mem in the Lagrangian encodes the history of field interactions.
          Conscious observation couples to this memory sector, creating irreversible records that
          break quantum superposition. The memory integral takes the form:
        </p>
        <div className="formula-box">
          <EquationRenderer equation="L_{mem} = -\lambda_{rec}(X) \cdot \int_{\tau_0}^t d\tau \, G(X; t,\tau) \cdot H[\Omega(x,\tau)]" />
        </div>
      </div>

      <div className="concept-card">
        <h3>⏰ The Nature of Time</h3>
        <p>
          Time is not fundamental but emerges from the evolution of the phase driver θ(t) and memory
          accumulation. The arrow of time comes from the irreversible accumulation of memory in L_mem.
          Proper time along a worldline is the accumulated phase change ∫ dθ.
        </p>
      </div>

      <div className="concept-card">
        <h3>⚖️ Origin of Mass</h3>
        <p>
          Mass is not a fundamental property but emerges from the energy functional of localized field
          configurations (solitons). The mass hierarchy of particles follows a φ-based pattern:
        </p>
        <div className="mass-hierarchy">
          <div>Electron: m_e = 0.511 MeV (N=111)</div>
          <div>Muon: m_μ ≈ 206.8 m_e (N=100)</div>
          <div>Tau: m_τ ≈ 3477 m_e (N=94)</div>
        </div>
      </div>

      <div className="concept-card">
        <h3>⚡ Electric Charge</h3>
        <p>
          Charge emerges from the topological structure of the complex substrate field Ω.
          The quantization Q = n·e/3 (where n ∈ ℤ) comes from winding numbers on the phase torus.
          Conservation is automatic due to U(1) gauge symmetry.
        </p>
      </div>
    </div>
  );

  const renderContent = () => {
    if (!category) {
      return (
        <div className="explanations-home">
          <div className="explanations-header">
            <h1>Golden Universe Theory - Complete Documentation</h1>
            <p>Explore all 39 fundamental laws, 6 Lagrangian terms, and comprehensive theoretical framework</p>
          </div>

          <div className="categories-grid">
            {categories.map((cat) => (
              <div
                key={cat.id}
                className="category-card"
                onClick={() => {
                  console.log(`Navigating to: /explanations/${cat.id}`);
                  navigate(`/explanations/${cat.id}`);
                }}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    navigate(`/explanations/${cat.id}`);
                  }
                }}
                style={{ cursor: 'pointer' }}
              >
                <div className="category-icon">{cat.icon}</div>
                <h3>{cat.title}</h3>
                <p>{cat.description}</p>
              </div>
            ))}
          </div>

          {/* Add quick links to individual explanation topics */}
          <div className="explanation-topics">
            <h2>Featured Explanations</h2>
            <div className="topics-grid">
              <div className="topic-card" onClick={() => navigate('/explanations/consciousness')}>
                <h3>🧘 Consciousness</h3>
                <p>How consciousness emerges from the quantum substrate</p>
              </div>
              <div className="topic-card" onClick={() => navigate('/explanations/gravity')}>
                <h3>🌍 What is Gravity?</h3>
                <p>Understanding gravity through the Golden Universe framework</p>
              </div>
              <div className="topic-card" onClick={() => navigate('/explanations/electron')}>
                <h3>⚛️ The Electron</h3>
                <p>Deep dive into the nature of the electron</p>
              </div>
              <div className="topic-card" onClick={() => navigate('/explanations/proton')}>
                <h3>⚡ The Proton</h3>
                <p>Understanding proton structure and properties</p>
              </div>
            </div>
          </div>
        </div>
      );
    }

    // Handle individual explanation topics from the explanatory folder
    if (category === 'electron' || category === 'gravity' || category === 'consciousness' || category === 'proton') {
      // Return the ExplanationTopic component which loads from API
      return <ExplanationTopic />;
    }

    // Handle direct submenu items for other concepts
    if (category === 'time' || category === 'mass' || category === 'charge') {
      // Show concepts section but with focus on specific topic
      return renderConcepts();
    }

    switch (category) {
      case 'documents':
        return renderDocuments();
      case 'overview':
        return renderOverview();
      case 'foundation':
      case 'symmetry':
      case 'particles':
      case 'cosmology':
      case 'advanced':
        return renderLawsByCategory(category);
      case 'lagrangian':
        return renderLagrangian();
      case 'validations':
        return renderValidations();
      case 'calculations':
        return renderCalculations();
      case 'concepts':
        return renderConcepts();
      default:
        return (
          <div className="category-not-found">
            <h2>Category Not Found</h2>
            <p>The category "{category}" does not exist.</p>
            <button className="back-button-large" onClick={() => navigate('/explanations')}>
              ← Return to Categories
            </button>
          </div>
        );
    }
  };

  return (
    <div className="explanations-page">
      {category && (
        <button className="back-button" onClick={() => navigate('/explanations')}>
          ← Back to Categories
        </button>
      )}

      <div className="explanations-content">
        {renderContent()}
      </div>
    </div>
  );
};

export default Explanations;