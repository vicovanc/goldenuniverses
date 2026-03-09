import { marked } from 'marked';
import katex from 'katex';
import hljs from 'highlight.js';

// Configure marked with simpler options
marked.setOptions({
  gfm: true,
  breaks: true
});

export interface RenderOptions {
  displayMode?: boolean;
  throwOnError?: boolean;
}

export class ContentRenderer {
  /**
   * Render LaTeX to HTML
   */
  static renderLatex(latex: string, options: RenderOptions = {}): string {
    try {
      return katex.renderToString(latex, {
        displayMode: options.displayMode ?? false,
        throwOnError: options.throwOnError ?? false,
        output: 'html',
        strict: false,
      });
    } catch (error) {
      console.error('LaTeX rendering error:', error);
      return `<span class="latex-error">LaTeX Error: ${latex}</span>`;
    }
  }

  /**
   * Render Markdown to HTML with LaTeX support
   */
  static async renderMarkdown(markdown: string): Promise<string> {
    // Replace inline LaTeX: $...$
    let processed = markdown.replace(/\$([^$]+)\$/g, (match, latex) => {
      return this.renderLatex(latex.trim(), { displayMode: false });
    });

    // Replace block LaTeX: $$...$$
    processed = processed.replace(/\$\$([^$]+)\$\$/g, (match, latex) => {
      return this.renderLatex(latex.trim(), { displayMode: true });
    });

    // Render markdown
    return await marked.parse(processed);
  }

  /**
   * Extract LaTeX equations from text
   */
  static extractEquations(text: string): Array<{ latex: string; displayMode: boolean; position: number }> {
    const equations: Array<{ latex: string; displayMode: boolean; position: number }> = [];

    // Find block equations
    const blockRegex = /\$\$([^$]+)\$\$/g;
    let match;
    while ((match = blockRegex.exec(text)) !== null) {
      equations.push({
        latex: match[1].trim(),
        displayMode: true,
        position: match.index,
      });
    }

    // Find inline equations
    const inlineRegex = /\$([^$]+)\$/g;
    while ((match = inlineRegex.exec(text)) !== null) {
      equations.push({
        latex: match[1].trim(),
        displayMode: false,
        position: match.index,
      });
    }

    return equations.sort((a, b) => a.position - b.position);
  }

  /**
   * Render code with syntax highlighting
   */
  static highlightCode(code: string, language: string): string {
    if (language && hljs.getLanguage(language)) {
      try {
        return hljs.highlight(code, { language }).value;
      } catch (err) {
        console.error('Highlight error:', err);
      }
    }
    return hljs.highlightAuto(code).value;
  }

  /**
   * Sanitize HTML (basic implementation)
   */
  static sanitizeHtml(html: string): string {
    // Basic sanitization - in production, use a library like DOMPurify
    return html
      .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
      .replace(/on\w+\s*=\s*["'][^"']*["']/gi, '')
      .replace(/javascript:/gi, '');
  }
}

export default ContentRenderer;
