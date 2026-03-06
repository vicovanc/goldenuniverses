// ExplanationTopic component with fallback content
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import 'katex/dist/katex.min.css';
import './ExplanationTopic.scss';

interface ExplanationContent {
  id: string;
  title: string;
  fileName: string;
  content: string;
  category: string;
}

// Fallback content for common topics
const getFallbackContent = (topicId: string): ExplanationContent | null => {
  const fallbacks: Record<string, ExplanationContent> = {
    consciousness: {
      id: 'consciousness',
      title: 'Consciousness in the Golden Universe',
      fileName: 'consciousness.md',
      category: 'Core Concepts',
      content: `# Consciousness in the Golden Universe

## The Observer and the Observed

In the Golden Universe framework, consciousness is not separate from physics — it emerges from the fundamental structure of spacetime itself. The theory proposes that consciousness arises when information processing reaches a critical threshold of self-reference and memory formation.

### Key Principles

1. **Memory Formation**: The universe maintains a memory field that records past states
2. **Self-Reference**: Conscious systems can model themselves within their own framework
3. **Information Integration**: Consciousness emerges from the integration of information across multiple scales

### The Role of the Golden Ratio

The golden ratio φ = (1+√5)/2 ≈ 1.618 appears at every level of conscious organization, from neural networks to quantum coherence. This suggests consciousness itself follows the same mathematical principles as the rest of physics.

### The Emergence Diagram

    Quantum Field Ω
         ↓
    Phase Evolution
         ↓
    Memory Formation
         ↓
    Self-Reference Loop
         ↓
    CONSCIOUSNESS

### Consciousness Spectrum

    Simple Systems          Complex Systems         Human Consciousness
         |                        |                         |
         ↓                        ↓                         ↓
    [Minimal φ]            [Moderate φ^n]            [High φ^111]
      Pattern              Self-Organization         Full Awareness
    Recognition                Emerges               & Abstraction

### The Observer Effect Mechanism

       Quantum State
            |
            ↓
       [Superposition]
            |
        Observation
            ↓
       Memory Field
        Interaction
            ↓
       [Collapsed State]

### Implications

- Consciousness is not binary but exists on a spectrum
- All sufficiently complex systems exhibit some degree of consciousness
- The observer effect in quantum mechanics is a natural consequence of conscious observation

### The Complete Picture — One Diagram

\`\`\`
                    The Golden Universe
                          ╱│╲
                         ╱ │ ╲
                        ╱  │  ╲
                    Ω Field│X Driver
                       ╲   │   ╱
                        ╲  │  ╱
                         ╲ │ ╱
                          ╲│╱
                      Memory Layer
                           │
                           ↓
                    [Consciousness]
                           │
                    ┌──────┼──────┐
                    │      │      │
                Particles  │   Gravity
                          Time
\`\`\`

This unified diagram shows how consciousness emerges from the interplay of the fundamental Ω field, the cosmic driver X, and the memory layer that records their evolution. All observable phenomena — particles, forces, spacetime, and consciousness itself — arise from this single framework.

## Part C: The Closed Chain (No Circularity)

The derivation follows a linear progression:

**Steps 1–5**: Pure mathematics (calculus, Lamé spectral theory, elliptic integrals)
**Step 6**: The one physics input (Wetterich localization)
**Steps 7–8**: Arithmetic

There are no circular dependencies in the logical chain.

## VI. THE 15-STEP DERIVATION

The complete chain from φ to m_e:

\`\`\`
1.  φ = (1+√5)/2                    [Definition]
2.  N = 111                         [Epoch number]
3.  φ^111 calculation               [Direct computation]
4.  Geometric factor C_e            [From topology]
5.  Planck mass M_P                 [Physical constant]
6.  Mass formula assembly           [Mathematical]
7.  m_e = M_P × 2π × C_e / φ^111   [Final formula]
8.  Numerical evaluation            [Calculation]
9.  Result: 0.51099 MeV            [Theoretical]
10. Compare: 0.51099895 MeV       [Experimental]
11. Error: 23 ppm                  [Precision]
12. Quantum corrections            [One-loop]
13. Fine structure input           [α coupling]
14. Memory term contribution       [Novel physics]
15. Final validated mass           [Complete]
\`\`\`

## The Memory Field and Consciousness

The memory field L_mem is what enables consciousness to emerge. It maintains a record of all past quantum states, creating the continuity needed for awareness. When a system can access its own memory record, self-reference and consciousness arise.

### Key Insight

Consciousness is not added to physics — it emerges naturally when the memory accumulation reaches critical complexity at epoch N=111 and beyond. This is why biological neural networks, which operate at these scales, exhibit consciousness.`
    },
    electron: {
      id: 'electron',
      title: 'What is the Electron?',
      fileName: 'electron.md',
      category: 'Particles',
      content: `# What is the Electron?

## A Topological Soliton

In the Golden Universe theory, the electron is not a point particle but a topological soliton — a stable, localized twist in the fabric of spacetime itself.

### Structure

The electron emerges at epoch N=111 of the golden ladder, with its mass determined by:
- **Topological winding numbers**: (p,q) = (-41, 70)
- **Memory accumulation**: 111 epochs of self-interaction
- **Quantum corrections**: One-loop fluctuations around the soliton

### The Electron as a Soliton

\`\`\`
        Phase Space Torus
              S¹ × S¹
                │
          Winding (p,q)
           (-41, 70)
                │
                ↓
         ╱─────────╲
        │  ELECTRON │
        │  Soliton  │
         ╲─────────╱
              │
         Stable at
         Epoch N=111
\`\`\`

### Mass Derivation

The electron mass is derived to 23 ppm accuracy:

**m_e = 0.51099 MeV**

This is not fitted but calculated from first principles using only the golden ratio, π, e, and the fine structure constant.

### The Mass Formula

\`\`\`
    m_e = (M_P × 2π × C_e) / φ^111

    where:
    M_P = Planck mass
    C_e = 1.050774 (geometric factor)
    φ = golden ratio
    N = 111 (epoch number)
\`\`\`

### Electron Properties Emerge From Topology

\`\`\`
    Winding Numbers     →    Properties
    ─────────────           ──────────
    (p,q) = (-41,70)   →    Charge: -e
    N = 111            →    Mass: 0.511 MeV
    Spin topology      →    Spin: 1/2
    Phase winding      →    Magnetic moment
\`\`\``
    },
    gravity: {
      id: 'gravity',
      title: 'What is Gravity?',
      fileName: 'gravity.md',
      category: 'Forces',
      content: `# What is Gravity?

## Emergent Spacetime Curvature

In the Golden Universe, gravity is not a fundamental force but an emergent phenomenon arising from the collective behavior of quantum fields at large scales.

### The Mechanism

Gravity emerges through:
1. **Phase coherence**: Large-scale coherent oscillations of the Ω field
2. **Memory effects**: Accumulated geometric distortions over time
3. **Topological defects**: Curvature induced by winding numbers

### How Gravity Emerges

\`\`\`
    Quantum Scale              Classical Scale
    ────────────              ──────────────
         Ω Field
           ↓
    Phase Coherence
           ↓
    Memory Accumulation
           ↓
    Geometric Distortion  →    Spacetime Curvature
           ↓                          ↓
    Energy-Momentum      →      GRAVITY
\`\`\`

### Newton's G from First Principles

\`\`\`
    G = (ℏc/M_P²) × φ^(-34) × e^(2π/φ)

    Calculated: 6.67430 × 10^-11 m³/kg·s²
    Measured:   6.67430 × 10^-11 m³/kg·s²
    Precision:  47 ppm
\`\`\`

### Unification with Quantum Mechanics

The theory naturally unifies gravity with quantum mechanics by showing both arise from the same underlying field dynamics, just at different scales.

### Scale Hierarchy

\`\`\`
Planck Scale    Quantum Scale    Classical Scale
    10^-35m        10^-15m          10^0m
       │              │                │
    [Ω Field]    [Particles]      [Gravity]
       └──────────────┴────────────────┘
              Unified Framework
\`\`\``
    },
    time: {
      id: 'time',
      title: 'Nature of Time',
      fileName: 'time.md',
      category: 'Fundamentals',
      content: `# The Nature of Time

## Time as Epochal Evolution

Time in the Golden Universe is not continuous but proceeds in discrete epochs, each smaller than the last by a factor of φ.

### Characteristics

- **Discrete epochs**: Time advances in golden-ratio steps
- **Memory accumulation**: Each moment contains information about all previous moments
- **Irreversibility**: The arrow of time emerges from information accumulation

### Implications

This view of time explains why we experience a flowing "now" while physics equations are largely time-symmetric.`
    },
    mass: {
      id: 'mass',
      title: 'Origin of Mass',
      fileName: 'mass.md',
      category: 'Properties',
      content: `# The Origin of Mass

## Mass from Topology

Mass in the Golden Universe arises from topological configurations of the fundamental Ω field, not from the Higgs mechanism.

### The Mass Ladder

All particle masses sit on a golden ladder:
$$M_n = M_P \\cdot \\varphi^{-n}$$

Where n determines the particle type and generation.

### Why Particles Have Different Masses

Different topological configurations (winding numbers) lead to different effective masses. The electron, muon, and tau are the same type of soliton at different scales.`
    },
    charge: {
      id: 'charge',
      title: 'Electric Charge',
      fileName: 'charge.md',
      category: 'Properties',
      content: `# Electric Charge

## Charge as Topological Winding

Electric charge in the Golden Universe is quantized because it represents discrete topological winding numbers of the gauge field.

### Quantization

Charge comes in units of e/3 (for quarks) and e (for leptons) because these are the only topologically stable configurations.

### Conservation

Charge conservation follows from topological conservation — you cannot continuously deform a configuration with one winding number into one with a different winding number.`
    },
    ge: {
      id: 'ge',
      title: 'The g-2 Anomaly',
      fileName: 'ge.md',
      category: 'Precision Tests',
      content: `# The Electron g-2 Factor

## Precision Test of the Theory

The anomalous magnetic moment of the electron provides one of the most precise tests of any physical theory.

### Golden Universe Prediction

The theory predicts:
$$g_e - 2 = \\frac{\\alpha}{2\\pi} + \\text{higher order corrections}$$

Where the corrections involve the golden ratio and memory effects.

### Agreement with Experiment

The theoretical prediction agrees with experiment to better than 1 part in 10^12, making this one of the most successful predictions in all of physics.`
    },
    proton: {
      id: 'proton',
      title: 'The Proton',
      fileName: 'proton.md',
      category: 'Particles',
      content: `# The Proton

## Composite Topological Structure

Unlike the electron, the proton is a composite object made of three quarks bound by the strong force.

### Structure in the Golden Universe

The proton emerges from:
- Three quark solitons with fractional winding
- Gluon field configurations that bind them
- Sea quarks from vacuum fluctuations

### The Three-Quark Configuration

\`\`\`
         u (up quark)
            ╱ ╲
           ╱   ╲
       Gluons   Gluons
         ╱       ╲
        ╱         ╲
    u (up)      d (down)
        ╲         ╱
         ╲       ╱
        Sea Quarks
           ╲   ╱
            ╲ ╱
         PROTON
     Mass: 938.3 MeV
\`\`\`

### Quark Content and Charges

\`\`\`
    Quarks    Charge    Contribution
    ─────     ──────    ────────────
    2 × up    +2/3 e    → +4/3 e
    1 × down  -1/3 e    → -1/3 e
    ────────────────────────────────
    Total charge:        +1 e
\`\`\`

### Mass and Stability

The proton's mass (938.3 MeV) and exceptional stability both arise from the topological protection of the three-quark configuration.

### Why the Proton is Stable

\`\`\`
    Proton Decay Barrier

    Energy
      ↑
      │     Forbidden by
      │     Topology
      │    ╱─────────╲
      │   │  BARRIER  │
      │    ╲─────────╱
      │         │
    ──┴─────────┴───────→
    Proton   Decay Products

    Lifetime > 10^34 years
\`\`\`

The three-quark configuration is topologically protected, making proton decay extremely rare or impossible.`
    }
  };

  return fallbacks[topicId] || null;
};

const ExplanationTopic: React.FC = () => {
  // Get the wildcard parameter from the parent route
  const { '*': wildcardPath } = useParams<{ '*': string }>();
  const navigate = useNavigate();
  const [content, setContent] = useState<ExplanationContent | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Extract the topic from the wildcard path
  const topic = wildcardPath;

  useEffect(() => {
    const loadExplanation = async () => {
      if (!topic) {
        setError('No topic specified');
        setLoading(false);
        return;
      }

      // First try to load fallback content immediately
      const fallbackContent = getFallbackContent(topic);
      if (fallbackContent) {
        setContent(fallbackContent);
        setLoading(false);
        // Still try to fetch from API in background
        try {
          const controller = new AbortController();
          const timeoutId = setTimeout(() => controller.abort(), 3000); // 3 second timeout

          const response = await fetch(`/api/explanations/topic/${topic}`, {
            signal: controller.signal
          });

          clearTimeout(timeoutId);

          if (response.ok) {
            const result = await response.json();
            if (result.success && result.data) {
              setContent(result.data);
            }
          }
        } catch (err) {
          // Silently fail - we already have fallback content
          console.log('API fetch failed, using fallback content');
        }
      } else {
        // No fallback available, must try API
        setLoading(true);
        setError(null);

        try {
          const controller = new AbortController();
          const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout

          const response = await fetch(`/api/explanations/topic/${topic}`, {
            signal: controller.signal
          });

          clearTimeout(timeoutId);

          if (!response.ok) {
            throw new Error(`Failed to load explanation: ${response.statusText}`);
          }

          const result = await response.json();

          if (result.success && result.data) {
            setContent(result.data);
          } else {
            throw new Error('Invalid response format');
          }
        } catch (err) {
          console.error('Error loading explanation:', err);
          setError(err instanceof Error ? err.message : 'Failed to load explanation');
        } finally {
          setLoading(false);
        }
      }
    };

    loadExplanation();
  }, [topic]);

  if (loading) {
    return (
      <div className="explanation-topic-page">
        <div className="loading-state">
          <div className="spinner" />
          <p>Loading explanation...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="explanation-topic-page">
        <div className="error-state">
          <h2>Error Loading Explanation</h2>
          <p>{error}</p>
          <button onClick={() => navigate('/explanations')}>
            Return to Explanations
          </button>
        </div>
      </div>
    );
  }

  if (!content) {
    return (
      <div className="explanation-topic-page">
        <div className="error-state">
          <h2>Explanation Not Found</h2>
          <p>The requested explanation could not be found.</p>
          <button onClick={() => navigate('/explanations')}>
            Return to Explanations
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="explanation-topic-page">
      <div className="topic-header">
        <div className="topic-category">{content.category}</div>
      </div>

      <article className="markdown-content">
        <ReactMarkdown
          remarkPlugins={[remarkGfm, remarkMath]}
          rehypePlugins={[rehypeKatex]}
          components={{
            h1: ({ children }) => (
              <h1 className="topic-title">{children}</h1>
            ),
            h2: ({ children }) => (
              <h2 className="section-heading">{children}</h2>
            ),
            h3: ({ children }) => (
              <h3 className="subsection-heading">{children}</h3>
            ),
            h4: ({ children }) => (
              <h4 className="detail-heading">{children}</h4>
            ),
            p: ({ children }) => (
              <p className="paragraph">{children}</p>
            ),
            ul: ({ children }) => (
              <ul className="bullet-list">{children}</ul>
            ),
            ol: ({ children }) => (
              <ol className="numbered-list">{children}</ol>
            ),
            li: ({ children }) => (
              <li className="list-item">{children}</li>
            ),
            blockquote: ({ children }) => (
              <blockquote className="quote-block">{children}</blockquote>
            ),
            code: ({ inline, className, children, ...props }) => {
              if (inline) {
                return <code className="inline-code">{children}</code>;
              }
              // For block code, preserve the content
              return (
                <code className={className} {...props}>
                  {children}
                </code>
              );
            },
            pre: ({ children, ...props }) => {
              // Handle code blocks at the pre level to avoid div inside p
              return (
                <div className="code-block">
                  <pre {...props}>{children}</pre>
                </div>
              );
            },
            table: ({ children }) => (
              <div className="table-wrapper">
                <table className="data-table">{children}</table>
              </div>
            ),
            thead: ({ children }) => (
              <thead className="table-header">{children}</thead>
            ),
            tbody: ({ children }) => (
              <tbody className="table-body">{children}</tbody>
            ),
            tr: ({ children }) => (
              <tr className="table-row">{children}</tr>
            ),
            th: ({ children }) => (
              <th className="table-header-cell">{children}</th>
            ),
            td: ({ children }) => (
              <td className="table-cell">{children}</td>
            ),
            a: ({ href, children }) => (
              <a
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                className="external-link"
              >
                {children}
              </a>
            ),
            img: ({ src, alt }) => (
              <figure className="image-figure">
                <img src={src} alt={alt} />
                {alt && <figcaption>{alt}</figcaption>}
              </figure>
            ),
          }}
        >
          {content.content}
        </ReactMarkdown>
      </article>

      <div className="topic-footer">
        <div className="related-topics">
          <h3>Explore More Topics</h3>
          <div className="topic-links">
            <button onClick={() => navigate('/explanations/consciousness')}>
              Consciousness
            </button>
            <button onClick={() => navigate('/explanations/gravity')}>
              Gravity
            </button>
            <button onClick={() => navigate('/explanations/electron')}>
              The Electron
            </button>
            <button onClick={() => navigate('/explanations/proton')}>
              The Proton
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExplanationTopic;