/**
 * storytellingjs - Configuration System
 * 
 * Parity with Python storytelling/config.py
 */

import type { StorytellingConfig, StyleGlossary } from './types.js';

/** Default model URI */
const DEFAULT_MODEL = 'ollama://qwen3:latest@localhost:11434';

/** Default configuration values */
export const DEFAULT_CONFIG: StorytellingConfig = {
  // Core Parameters
  promptFile: undefined,
  outputFile: undefined,
  
  // Model Selection
  initialOutlineModel: DEFAULT_MODEL,
  chapterOutlineModel: DEFAULT_MODEL,
  chapterS1Model: DEFAULT_MODEL,
  chapterS2Model: DEFAULT_MODEL,
  chapterS3Model: DEFAULT_MODEL,
  chapterS4Model: DEFAULT_MODEL,
  chapterRevisionModel: DEFAULT_MODEL,
  revisionModel: DEFAULT_MODEL,
  evalModel: DEFAULT_MODEL,
  infoModel: DEFAULT_MODEL,
  scrubModel: DEFAULT_MODEL,
  checkerModel: DEFAULT_MODEL,
  translatorModel: DEFAULT_MODEL,
  
  // Knowledge Base / RAG
  knowledgeBasePath: undefined,
  embeddingModel: undefined,
  ollamaBaseUrl: 'http://localhost:11434',
  
  // Outline-level RAG
  outlineRagEnabled: true,
  outlineContextMaxTokens: 1000,
  outlineRagTopK: 5,
  outlineRagSimilarityThreshold: 0.7,
  
  // Chapter-level RAG
  chapterRagEnabled: true,
  chapterContextMaxTokens: 1500,
  chapterRagTopK: 8,
  
  // Workflow Control
  expandOutline: true,
  enableFinalEditPass: false,
  noScrubChapters: false,
  sceneGenerationPipeline: true,
  
  // Revision Control
  outlineMinRevisions: 1,
  outlineMaxRevisions: 3,
  chapterMinRevisions: 1,
  chapterMaxRevisions: 3,
  noChapterRevision: false,
  
  // Translation
  translate: undefined,
  translatePrompt: undefined,
  
  // Style Glossary
  styleGlossaryPath: undefined,
  styleGlossary: undefined,
  enableBuzzTermRevision: true,
  
  // Miscellaneous
  seed: 12,
  sleepTime: 31,
  debug: false,
  mockMode: false,
};

/** Default style glossary with common buzz terms */
export function getDefaultStyleGlossary(): StyleGlossary {
  return {
    avoidTerms: [
      'gap', 'journey', 'leverage', 'synergy', 'paradigm',
      'ecosystem', 'landscape', 'bandwidth', 'pivot',
      'very', 'really', 'just', 'basically', 'actually',
      'amazing', 'incredible', 'literally'
    ],
    preferredAlternatives: {
      'gap': ['distance', 'divide', 'separation', 'difference'],
      'journey': ['path', 'progression', 'evolution', 'experience'],
      'leverage': ['use', 'employ', 'apply', 'harness'],
      'very': ['extremely', 'remarkably', 'exceptionally'],
      'amazing': ['remarkable', 'extraordinary', 'striking'],
    },
    customAvoidPhrases: [
      'at the end of the day', 
      'moving forward', 
      'low-hanging fruit',
      'it was then that', 
      'suddenly realized', 
      'heart pounded'
    ],
    toneWords: {},
    enforcementLevel: 'moderate',
  };
}

/** Parse model URI and validate format */
export function parseModelUri(uri: string): {
  provider: string;
  model: string;
  host?: string;
  port?: number;
} {
  const match = uri.match(/^(google|ollama|openrouter|myflowise):\/\/(.+)$/);
  if (!match) {
    throw new Error(`Invalid model URI: ${uri}. Expected format: provider://model[@host:port]`);
  }
  
  const [, provider, rest] = match;
  
  // Check for host:port suffix (e.g., ollama://model@localhost:11434)
  const hostMatch = rest.match(/^(.+)@(.+):(\d+)$/);
  if (hostMatch) {
    const [, model, host, portStr] = hostMatch;
    return { provider, model, host, port: parseInt(portStr, 10) };
  }
  
  return { provider, model: rest };
}

/** Validate model URI format */
export function isValidModelUri(uri: string): boolean {
  try {
    parseModelUri(uri);
    return true;
  } catch {
    return false;
  }
}

/** Create configuration from partial options */
export function createConfig(options: Partial<StorytellingConfig> = {}): StorytellingConfig {
  const config = { ...DEFAULT_CONFIG, ...options };
  
  // Apply default style glossary if buzz term revision is enabled
  if (config.enableBuzzTermRevision && !config.styleGlossary) {
    config.styleGlossary = getDefaultStyleGlossary();
  }
  
  return config;
}

/** Configuration option metadata for CLI */
export const CONFIG_OPTIONS = [
  { name: 'prompt', alias: 'p', type: 'string', description: 'Path to prompt file', field: 'promptFile' },
  { name: 'output', alias: 'o', type: 'string', description: 'Output file path', field: 'outputFile' },
  { name: 'initial-outline-model', type: 'string', description: 'Model for initial outline', field: 'initialOutlineModel' },
  { name: 'chapter-outline-model', type: 'string', description: 'Model for chapter outline', field: 'chapterOutlineModel' },
  { name: 'chapter-s1-model', type: 'string', description: 'Model for scene 1', field: 'chapterS1Model' },
  { name: 'chapter-s2-model', type: 'string', description: 'Model for scene 2', field: 'chapterS2Model' },
  { name: 'chapter-s3-model', type: 'string', description: 'Model for scene 3', field: 'chapterS3Model' },
  { name: 'chapter-s4-model', type: 'string', description: 'Model for scene 4', field: 'chapterS4Model' },
  { name: 'chapter-revision-model', type: 'string', description: 'Model for chapter revision', field: 'chapterRevisionModel' },
  { name: 'revision-model', type: 'string', description: 'Model for final revision', field: 'revisionModel' },
  { name: 'knowledge-base-path', type: 'string', description: 'Path to knowledge base', field: 'knowledgeBasePath' },
  { name: 'embedding-model', type: 'string', description: 'Embedding model for RAG', field: 'embeddingModel' },
  { name: 'chapter-max-revisions', type: 'number', description: 'Max revisions per chapter', field: 'chapterMaxRevisions' },
  { name: 'expand-outline', type: 'boolean', description: 'Expand outline', field: 'expandOutline' },
  { name: 'debug', type: 'boolean', description: 'Enable debug mode', field: 'debug' },
  { name: 'mock-mode', type: 'boolean', description: 'Use mock responses', field: 'mockMode' },
] as const;
