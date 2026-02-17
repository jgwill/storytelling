/**
 * storytellingjs - Main Library Export
 * 
 * TypeScript story generation library with CLI and MCP server.
 * Full parity with Python storytelling package.
 */

// Core exports
export { Story } from './core.js';
export { SessionManager, migrateExistingSession } from './session-manager.js';
export { Logger, createConsoleLogger } from './logger.js';
export type { LogLevel, LogEntry } from './logger.js';

// Configuration exports
export { 
  DEFAULT_CONFIG, 
  createConfig, 
  getDefaultStyleGlossary,
  parseModelUri,
  isValidModelUri,
  CONFIG_OPTIONS,
} from './config.js';

// LLM Provider exports
export {
  parseUri,
  validateUri,
  getProviderBaseUrl,
  getModelUriExamples,
  suggestModelCombination,
} from './llm-providers.js';
export type { 
  ParsedModelUri, 
  LLMProvider, 
  GenerateOptions,
  ModelProvider,
} from './llm-providers.js';

// Type exports
export type {
  // Session types
  SessionStatus,
  WorkflowNode,
  SessionCheckpoint,
  SessionInfo,
  
  // Data model types
  ChapterCount,
  CompletionCheck,
  SummaryCheck,
  StoryInfo,
  SceneList,
  
  // Configuration types
  StorytellingConfig,
  StyleGlossary,
  EnforcementLevel,
  
  // Core types
  Story as StoryInterface,
  
  // NCP types
  StoryBeat,
  CharacterArcState,
  Gap,
  NCPState,
  
  // MCP types
  ToolDefinition,
  PropertySchema,
  ToolHandler,
  ToolResult,
} from './types.js';

// Zod schemas for runtime validation
export {
  ChapterCountSchema,
  CompletionCheckSchema,
  SummaryCheckSchema,
  StoryInfoSchema,
  SessionInfoSchema,
  ModelUriSchema,
} from './types.js';

// Package version
export const VERSION = '0.1.0';
