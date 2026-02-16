/**
 * storytellingjs - LLM Provider Abstraction
 * 
 * Model URI parsing and provider interface.
 */

import { parseModelUri, isValidModelUri } from './config.js';

export type ModelProvider = 'google' | 'ollama' | 'openrouter' | 'myflowise';

export interface ParsedModelUri {
  provider: ModelProvider;
  model: string;
  host?: string;
  port?: number;
}

export interface LLMProvider {
  name: ModelProvider;
  generateText(prompt: string, options?: GenerateOptions): Promise<string>;
  generateStructured<T>(prompt: string, schema: unknown, options?: GenerateOptions): Promise<T>;
}

export interface GenerateOptions {
  temperature?: number;
  maxTokens?: number;
  seed?: number;
  stopSequences?: string[];
}

/**
 * Parse a model URI into components.
 */
export function parseUri(uri: string): ParsedModelUri {
  const result = parseModelUri(uri);
  return {
    provider: result.provider as ModelProvider,
    model: result.model,
    host: result.host,
    port: result.port,
  };
}

/**
 * Validate a model URI.
 */
export function validateUri(uri: string): { valid: boolean; error?: string } {
  if (!uri) {
    return { valid: false, error: 'Model URI is required' };
  }
  
  if (!isValidModelUri(uri)) {
    return { 
      valid: false, 
      error: `Invalid model URI format. Expected: provider://model[@host:port]. Valid providers: google, ollama, openrouter, myflowise` 
    };
  }
  
  return { valid: true };
}

/**
 * Get the base URL for a provider.
 */
export function getProviderBaseUrl(parsed: ParsedModelUri): string {
  switch (parsed.provider) {
    case 'google':
      return 'https://generativelanguage.googleapis.com';
    case 'ollama':
      const host = parsed.host ?? 'localhost';
      const port = parsed.port ?? 11434;
      return `http://${host}:${port}`;
    case 'openrouter':
      return 'https://openrouter.ai/api';
    case 'myflowise':
      return process.env.FLOWISE_API_URL ?? 'http://localhost:3000/api/v1';
    default:
      throw new Error(`Unknown provider: ${parsed.provider}`);
  }
}

/**
 * Format example model URIs for help text.
 */
export function getModelUriExamples(): string {
  return `
Model URI Format Examples:
  - google://gemini-2.5-flash
  - google://gemini-pro
  - ollama://qwen3:latest@localhost:11434
  - ollama://mistral@localhost:11434
  - openrouter://anthropic/claude-3-sonnet
  - myflowise://flow-id

Supported Providers:
  - google:// - Google Gemini models (requires GOOGLE_API_KEY)
  - ollama:// - Ollama local models (specify host:port)
  - openrouter:// - OpenRouter API (requires OPENROUTER_API_KEY)
  - myflowise:// - Flowise flow execution
`.trim();
}

/**
 * Suggest model combinations for different story types.
 */
export function suggestModelCombination(
  storyType: string = 'general',
  speedPriority: boolean = false
): { recommendation: string; details: Record<string, string> } {
  const recommendations: Record<string, Record<string, string>> = {
    general: {
      balanced: 'Use google://gemini-2.5-flash for all stages (fastest, good quality)',
      quality: 'Use google://gemini-pro for planning, gemini-2.5-flash for prose generation',
      local: 'Use ollama://mistral for planning, ollama://neural-chat for prose',
    },
    fantasy: {
      balanced: 'Gemini Flash throughout - handles worldbuilding well',
      quality: 'Gemini Pro for outline, Flash for scenes',
      local: 'Mistral for outline, Llama2 for prose (better for descriptive text)',
    },
    scifi: {
      balanced: 'Gemini Flash - good with technical concepts',
      quality: 'Gemini Pro for outline, Flash for scenes',
      local: 'Neural Chat (good with technical details) for all stages',
    },
    mystery: {
      balanced: 'Gemini Pro for all stages (better plot coherence)',
      quality: 'Gemini Pro for everything',
      local: 'Mistral for planning, Neural Chat for prose',
    },
    romance: {
      balanced: 'Gemini Flash - handles dialogue well',
      quality: 'Gemini Pro for all stages',
      local: 'Neural Chat for better character voice',
    },
  };

  const key = storyType.toLowerCase();
  const recs = recommendations[key] ?? recommendations['general'];
  
  return {
    recommendation: speedPriority ? recs.balanced : recs.quality,
    details: recs,
  };
}
