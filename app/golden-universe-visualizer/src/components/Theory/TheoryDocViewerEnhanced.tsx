import React, { useState, useEffect, useRef, useCallback } from 'react';
import { marked } from 'marked';
import hljs from 'highlight.js';
import katex from 'katex';
import 'highlight.js/styles/github-dark.css';
import 'katex/dist/katex.min.css';
import { TheoryDocument, DocumentSection } from '@/types/theory';
import DOMPurify from 'dompurify';

interface TheoryDocViewerProps {
  documentPath?: string;
  initialContent?: string;
}

const TheoryDocViewerEnhanced: React.FC<TheoryDocViewerProps> = ({ documentPath, initialContent }) => {
  const [content, setContent] = useState<string>(initialContent || '');
  const [sections, setSections] = useState<DocumentSection[]>([]);
  const [activeSection, setActiveSection] = useState<string>('');
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<{ section: string; matches: number }[]>([]);
  const [isPrintView, setIsPrintView] = useState(false);
  const contentRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(false);
  const observerRef = useRef<IntersectionObserver | null>(null);

  // Process LaTeX equations in markdown
  const processLatexInMarkdown = (text: string): string => {
    // Process display math blocks ($$...$$)
    text = text.replace(/\$\$([\s\S]*?)\$\$/g, (match, equation) => {
      try {
        const html = katex.renderToString(equation.trim(), {
          displayMode: true,
          throwOnError: false,
          errorColor: '#F59E0B',
          strict: false,
          trust: false,
        });
        return `<div class="math-display">${html}</div>`;
      } catch (e) {
        console.error('KaTeX error:', e);
        return `<div class="math-error">Error rendering: ${equation}</div>`;
      }
    });

    // Process inline math ($...$)
    text = text.replace(/\$([^\$\n]+?)\$/g, (match, equation) => {
      try {
        const html = katex.renderToString(equation.trim(), {
          displayMode: false,
          throwOnError: false,
          errorColor: '#F59E0B',
          strict: false,
          trust: false,
        });
        return `<span class="math-inline">${html}</span>`;
      } catch (e) {
        console.error('KaTeX error:', e);
        return `<span class="math-error">Error: ${equation}</span>`;
      }
    });

    // Process equations in common formats
    // M_P = √(ℏc/G) format
    text = text.replace(/M_P\s*=\s*√\(ℏc\/G\)/g, () => {
      try {
        const html = katex.renderToString('M_P = \\sqrt{\\frac{\\hbar c}{G}}', {
          displayMode: false,
          throwOnError: false,
        });
        return `<span class="math-inline">${html}</span>`;
      } catch (e) {
        return 'M_P = √(ℏc/G)';
      }
    });

    // Process S₀ = φⁿ format
    text = text.replace(/S₀\s*=\s*φⁿ/g, () => {
      try {
        const html = katex.renderToString('S_0 = \\varphi^n', {
          displayMode: false,
          throwOnError: false,
        });
        return `<span class="math-inline">${html}</span>`;
      } catch (e) {
        return 'S₀ = φⁿ';
      }
    });

    // Process subscripts and superscripts (e.g., m_e, x^2)
    text = text.replace(/([a-zA-Z])_([a-zA-Z0-9]+)/g, (match, base, sub) => {
      try {
        const html = katex.renderToString(`${base}_${sub}`, {
          displayMode: false,
          throwOnError: false,
        });
        return `<span class="math-inline">${html}</span>`;
      } catch (e) {
        return match;
      }
    });

    text = text.replace(/([a-zA-Z0-9]+)\^([a-zA-Z0-9]+)/g, (match, base, sup) => {
      try {
        const html = katex.renderToString(`${base}^{${sup}}`, {
          displayMode: false,
          throwOnError: false,
        });
        return `<span class="math-inline">${html}</span>`;
      } catch (e) {
        return match;
      }
    });

    return text;
  };

  // Configure marked with syntax highlighting and custom renderer for headers
  useEffect(() => {
    const renderer = new marked.Renderer();

    // Override the heading renderer to add section IDs
    renderer.heading = (text: string, level: number) => {
      const id = text.toLowerCase().replace(/[^a-z0-9]+/g, '-');
      return `<h${level} id="section-${id}">${text}</h${level}>`;
    };

    // Override paragraph renderer to process LaTeX
    const originalParagraph = renderer.paragraph.bind(renderer);
    renderer.paragraph = (text: string) => {
      const processedText = processLatexInMarkdown(text);
      return originalParagraph(processedText);
    };

    // Override list item renderer to process LaTeX
    const originalListItem = renderer.listitem.bind(renderer);
    renderer.listitem = (text: string, task: boolean, checked: boolean) => {
      const processedText = processLatexInMarkdown(text);
      return originalListItem(processedText, task, checked);
    };

    marked.setOptions({
      renderer: renderer,
      highlight: (code, lang) => {
        if (lang && hljs.getLanguage(lang)) {
          try {
            return hljs.highlight(code, { language: lang }).value;
          } catch (err) {
            console.error('Highlight error:', err);
          }
        }
        return hljs.highlightAuto(code).value;
      },
      breaks: true,
      gfm: true,
    });
  }, []);

  // Load document
  useEffect(() => {
    if (documentPath) {
      setLoading(true);
      fetch(documentPath)
        .then((response) => response.text())
        .then((text) => {
          setContent(text);
          extractSections(text);
          setLoading(false);
        })
        .catch((error) => {
          console.error('Error loading document:', error);
          setContent('# Error Loading Document\n\nCould not load the requested document.');
          setLoading(false);
        });
    } else if (initialContent) {
      extractSections(initialContent);
    }
  }, [documentPath, initialContent]);

  // Set up intersection observer for active section tracking
  useEffect(() => {
    if (!sections.length) return;

    if (observerRef.current) {
      observerRef.current.disconnect();
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const sectionId = entry.target.id.replace('section-', '');
            setActiveSection(sectionId);
          }
        });
      },
      {
        rootMargin: '-80px 0px -70% 0px',
        threshold: 0
      }
    );

    observerRef.current = observer;

    // Observe all section headers after content is rendered
    setTimeout(() => {
      sections.forEach(section => {
        const element = document.getElementById(`section-${section.id}`);
        if (element && observerRef.current) {
          observerRef.current.observe(element);
        }
      });
    }, 100);

    return () => {
      if (observerRef.current) {
        observerRef.current.disconnect();
      }
    };
  }, [sections]);

  // Extract sections from markdown content
  const extractSections = (text: string) => {
    const headerRegex = /^(#{1,6})\s+(.+)$/gm;
    const extractedSections: DocumentSection[] = [];
    let match;

    while ((match = headerRegex.exec(text)) !== null) {
      const level = match[1].length;
      const title = match[2];
      const id = title.toLowerCase().replace(/[^a-z0-9]+/g, '-');

      extractedSections.push({
        id,
        title,
        level,
        content: '',
      });
    }

    setSections(extractedSections);
  };

  // Scroll to a specific section
  const scrollToSection = (sectionId: string) => {
    const element = document.getElementById(`section-${sectionId}`);
    if (element) {
      const offset = 100;
      const elementPosition = element.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - offset;

      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth',
      });
    }
  };

  // Handle search
  const handleSearch = useCallback((query: string) => {
    setSearchQuery(query);
    if (!query.trim()) {
      setSearchResults([]);
      return;
    }

    const results: { section: string; matches: number }[] = [];
    const lowerQuery = query.toLowerCase();

    sections.forEach((section) => {
      const sectionElement = document.getElementById(`section-${section.id}`);
      if (sectionElement) {
        const text = sectionElement.textContent || '';
        const lowerText = text.toLowerCase();
        const matches = (lowerText.match(new RegExp(lowerQuery, 'g')) || []).length;

        if (matches > 0) {
          results.push({ section: section.title, matches });
        }
      }
    });

    setSearchResults(results);
  }, [sections]);

  // Highlight search terms
  const highlightSearchTerms = (html: string): string => {
    if (!searchQuery.trim()) return html;

    const searchRegex = new RegExp(`(${searchQuery})`, 'gi');
    return html.replace(searchRegex, '<mark class="search-highlight">$1</mark>');
  };

  // Parse markdown to HTML with LaTeX processing
  const getHtmlContent = () => {
    try {
      // First process LaTeX in the markdown
      const processedContent = processLatexInMarkdown(content);

      // Then parse with marked
      let html = marked.parse(processedContent) as string;

      // Highlight search terms if needed
      if (searchQuery.trim()) {
        html = highlightSearchTerms(html);
      }

      // Sanitize HTML to prevent XSS, but keep KaTeX classes and styles
      const sanitized = DOMPurify.sanitize(html, {
        ADD_TAGS: ['span', 'div'],
        ADD_ATTR: ['class', 'style'],
        ADD_DATA_URI_TAGS: ['span', 'div'],
        ALLOW_DATA_ATTR: false,
        KEEP_CONTENT: true,
        FORBID_TAGS: ['script', 'iframe', 'object', 'embed', 'form'],
        FORBID_ATTR: ['onerror', 'onload', 'onclick']
      });

      return sanitized;
    } catch (error) {
      console.error('Markdown parsing error:', error);
      return '<p>Error parsing document</p>';
    }
  };

  // Handle print
  const handlePrint = () => {
    setIsPrintView(true);
    setTimeout(() => {
      window.print();
      setIsPrintView(false);
    }, 100);
  };

  // Render table of contents
  const renderTOC = () => {
    return (
      <div className="doc-toc">
        <h3>Table of Contents</h3>
        <ul className="toc-list">
          {sections.map((section) => (
            <li
              key={section.id}
              className={`toc-item level-${section.level} ${activeSection === section.id ? 'active' : ''}`}
              style={{ paddingLeft: `${(section.level - 1) * 12}px` }}
            >
              <button
                onClick={() => scrollToSection(section.id)}
                className="toc-link"
                aria-label={`Navigate to ${section.title}`}
              >
                {section.title}
              </button>
            </li>
          ))}
        </ul>
      </div>
    );
  };

  return (
    <div className={`theory-doc-viewer ${isPrintView ? 'print-view' : ''}`}>
      {!isPrintView && (
        <div className="doc-controls">
          <div className="search-box">
            <input
              type="text"
              placeholder="Search in document..."
              value={searchQuery}
              onChange={(e) => handleSearch(e.target.value)}
              className="doc-search-input"
            />
            {searchQuery && (
              <div className="search-results-count">
                {searchResults.length} {searchResults.length === 1 ? 'section' : 'sections'} found
              </div>
            )}
          </div>

          <div className="doc-actions">
            <button onClick={handlePrint} className="doc-action-button" aria-label="Print document">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
                <path d="M5 2h10a1 1 0 0 1 1 1v4h1a2 2 0 0 1 2 2v6a2 2 0 0 1-2 2h-1v1a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-1H3a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h1V3a1 1 0 0 1 1-1zm0 2v3h10V4H5zm10 9v3H5v-3h10z" />
              </svg>
              Print
            </button>
          </div>
        </div>
      )}

      <div className="doc-layout">
        {!isPrintView && sections.length > 0 && <div className="doc-sidebar">{renderTOC()}</div>}

        <div className="doc-main">
          {loading ? (
            <div className="doc-loading">
              <div className="loading-spinner"></div>
              <p>Loading document...</p>
            </div>
          ) : (
            <>
              {searchResults.length > 0 && searchQuery && (
                <div className="search-results-panel">
                  <h4>Search Results for "{searchQuery}"</h4>
                  <ul className="search-results-list">
                    {searchResults.map((result, index) => (
                      <li key={index} className="search-result-item">
                        <button
                          className="search-result-link"
                          onClick={() => {
                            const sectionId = result.section.toLowerCase().replace(/[^a-z0-9]+/g, '-');
                            scrollToSection(sectionId);
                          }}
                        >
                          {result.section}
                          <span className="match-count">({result.matches} matches)</span>
                        </button>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              <div
                ref={contentRef}
                className="doc-content"
                dangerouslySetInnerHTML={{ __html: getHtmlContent() }}
              />
            </>
          )}
        </div>
      </div>

      {/* Add KaTeX CSS for equation styling */}
      <style>{`
        .math-display {
          margin: 1.5rem 0;
          text-align: center;
          overflow-x: auto;
        }

        .math-inline {
          display: inline-block;
          vertical-align: middle;
        }

        .math-error {
          color: #F59E0B;
          font-family: monospace;
          background: rgba(245, 158, 11, 0.1);
          padding: 0.2rem 0.4rem;
          border-radius: 4px;
        }

        .katex {
          font-size: 1.1em;
        }

        .katex-display {
          margin: 1rem 0;
        }
      `}</style>

      {/* Print styles */}
      {isPrintView && (
        <style>{`
          @media print {
            body {
              background: white;
              color: black;
            }
            .doc-controls,
            .doc-sidebar {
              display: none !important;
            }
            .doc-content {
              max-width: 100%;
              padding: 0;
              box-shadow: none;
            }
          }
        `}</style>
      )}
    </div>
  );
};

export default TheoryDocViewerEnhanced;