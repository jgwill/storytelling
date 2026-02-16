/**
 * storytellingjs - Core Story Class
 * 
 * Parity with Python storytelling/core.py
 */

import type { Story as StoryInterface } from './types.js';

/**
 * A basic story class for storytelling applications.
 * Matches Python storytelling/core.py Story class.
 */
export class Story implements StoryInterface {
  title: string;
  content: string;
  metadata: Record<string, string>;

  /**
   * Initialize a new story.
   * @param title - The title of the story
   * @param content - The content of the story
   */
  constructor(title: string, content: string = '') {
    this.title = title;
    this.content = content;
    this.metadata = {};
  }

  /**
   * Add content to the story.
   * @param content - Content to add to the story
   */
  addContent(content: string): void {
    if (this.content) {
      this.content += `\n\n${content}`;
    } else {
      this.content = content;
    }
  }

  /**
   * Set metadata for the story.
   * @param key - Metadata key
   * @param value - Metadata value
   */
  setMetadata(key: string, value: string): void {
    this.metadata[key] = value;
  }

  /**
   * Get metadata value by key.
   * @param key - Metadata key
   * @returns Metadata value or undefined
   */
  getMetadata(key: string): string | undefined {
    return this.metadata[key];
  }

  /**
   * String representation of the story.
   */
  toString(): string {
    return `Story: ${this.title}`;
  }

  /**
   * Get content preview (first n characters).
   */
  getPreview(length: number = 100): string {
    if (this.content.length <= length) {
      return this.content;
    }
    return `${this.content.substring(0, length)}...`;
  }

  /**
   * Export story to markdown format.
   */
  toMarkdown(): string {
    let md = `# ${this.title}\n\n`;
    
    // Add metadata if present
    if (Object.keys(this.metadata).length > 0) {
      md += '---\n';
      for (const [key, value] of Object.entries(this.metadata)) {
        md += `${key}: ${value}\n`;
      }
      md += '---\n\n';
    }
    
    md += this.content;
    return md;
  }

  /**
   * Create a Story from markdown content.
   */
  static fromMarkdown(markdown: string): Story {
    const lines = markdown.split('\n');
    let title = 'Untitled';
    let content = '';
    const metadata: Record<string, string> = {};
    
    let inFrontmatter = false;
    let contentStart = 0;
    
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      
      // Check for title (first h1)
      if (line.startsWith('# ') && title === 'Untitled') {
        title = line.substring(2).trim();
        contentStart = i + 1;
        continue;
      }
      
      // Check for frontmatter
      if (line === '---') {
        if (!inFrontmatter) {
          inFrontmatter = true;
          continue;
        } else {
          inFrontmatter = false;
          contentStart = i + 1;
          continue;
        }
      }
      
      // Parse frontmatter
      if (inFrontmatter) {
        const colonIdx = line.indexOf(':');
        if (colonIdx > 0) {
          const key = line.substring(0, colonIdx).trim();
          const value = line.substring(colonIdx + 1).trim();
          metadata[key] = value;
        }
        continue;
      }
    }
    
    content = lines.slice(contentStart).join('\n').trim();
    
    const story = new Story(title, content);
    story.metadata = metadata;
    return story;
  }
}
