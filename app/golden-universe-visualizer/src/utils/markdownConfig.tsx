/**
 * Shared Markdown Configuration
 * Provides consistent markdown rendering settings across the app
 */

import React from 'react';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import type { Components } from 'react-markdown';

// Export the standard plugins for ReactMarkdown
export const remarkPlugins = [remarkGfm, remarkMath];
export const rehypePlugins = [rehypeKatex];

// Export a standard set of component overrides for consistent rendering
export const markdownComponents: Components = {
  // Headings
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

  // Paragraphs and text
  p: ({ children }) => (
    <p className="paragraph">{children}</p>
  ),

  // Lists
  ul: ({ children }) => (
    <ul className="bullet-list">{children}</ul>
  ),
  ol: ({ children }) => (
    <ol className="numbered-list">{children}</ol>
  ),
  li: ({ children }) => (
    <li className="list-item">{children}</li>
  ),

  // Code blocks
  code: ({ inline, className, children }) => {
    if (inline) {
      return <code className="inline-code">{children}</code>;
    }

    const language = className?.replace('language-', '') || '';

    // Special handling for ASCII art and diagrams
    if (language === 'diagram' || language === 'ascii' || language === 'text') {
      return (
        <div className="code-block">
          {language && <div className="code-language">{language.toUpperCase()}</div>}
          <pre>
            <code>{children}</code>
          </pre>
        </div>
      );
    }

    return (
      <div className="code-block">
        {language && <div className="code-language">{language.toUpperCase()}</div>}
        <pre>
          <code className={className}>{children}</code>
        </pre>
      </div>
    );
  },

  pre: ({ children }) => {
    // Return children directly as we handle the pre wrapper in the code component
    return <>{children}</>;
  },

  // Tables with GitHub Flavored Markdown support
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

  // Blockquotes
  blockquote: ({ children }) => (
    <blockquote className="quote-block">{children}</blockquote>
  ),

  // Links
  a: ({ href, children }) => (
    <a
      href={href}
      className="external-link"
      target="_blank"
      rel="noopener noreferrer"
    >
      {children}
    </a>
  ),

  // Images
  img: ({ src, alt }) => (
    <figure className="image-figure">
      <img src={src} alt={alt || ''} />
      {alt && <figcaption>{alt}</figcaption>}
    </figure>
  ),
};

// Helper function to get all markdown props at once
export const getMarkdownProps = (customComponents?: Partial<Components>) => ({
  remarkPlugins,
  rehypePlugins,
  components: customComponents
    ? { ...markdownComponents, ...customComponents }
    : markdownComponents,
});