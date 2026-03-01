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

// Prompt exports
export {
  formatTemplate,
  PROMPTS,
  GET_IMPORTANT_BASE_PROMPT_INFO,
  STORY_ELEMENTS_PROMPT,
  INITIAL_OUTLINE_PROMPT,
  CHAPTER_COUNT_PROMPT,
  SCENE_OUTLINE_PROMPT,
  GENERATE_SCENE_PROMPT,
  CRITIQUE_CHAPTER_PROMPT,
  CHECK_CHAPTER_COMPLETE_PROMPT,
  REVISE_CHAPTER_PROMPT,
  FINAL_STORY_PROMPT,
  STORY_INFO_PROMPT,
  REVISE_BUZZ_TERMS_PROMPT,
  DETECT_BUZZ_TERMS_PROMPT,
  TRANSLATE_PROMPT,
} from './prompts.js';

// Narrative Intelligence exports
export {
  EmotionCategory,
  Universe,
  NCPAwareStoryGenerator,
  CharacterArcTracker,
  createStoryBeat,
  createCharacterArcState,
  createNCPState,
} from './narrative-intelligence.js';
export type {
  StoryBeat as NarrativeStoryBeat,
  CharacterArcState as NarrativeCharacterArcState,
  Gap as NarrativeGap,
  NCPState as NarrativeNCPState,
  EmotionalAnalysis,
  UniverseAnalysis,
  ThreeUniverseAnalysis,
  GapSeverity,
} from './narrative-intelligence.js';

// Emotional Beat Enricher exports
export {
  EmotionalBeatEnricher,
  QualityThreshold,
  ENRICHMENT_TECHNIQUES,
} from './emotional-beat-enricher.js';
export type { EnrichedBeatResult } from './emotional-beat-enricher.js';

// Analytical Feedback Loop exports
export {
  AnalyticalFeedbackLoop,
  GapType,
  GapDimension,
  GAP_ROUTING,
} from './analytical-feedback-loop.js';
export type {
  CharacterAnalysisResult,
  ThematicAnalysisResult,
  MultiDimensionalAnalysis,
  FeedbackIteration,
} from './analytical-feedback-loop.js';

// Role Tooling exports
export {
  Role,
  RoleUniverse,
  ROLE_UNIVERSE_MAP,
  ToolRegistry,
  Architect,
  Structurist,
  Storyteller,
  Editor,
  Reader,
  Collaborator,
  Witness,
  createDefaultRegistry,
} from './role-tooling.js';
export type { RoleTool, RoleContext, RoleInterface } from './role-tooling.js';

// Narrative Story Graph exports
export {
  NodeStatus,
  NarrativeAwareStoryGraph,
  createGraphState,
  createDefaultPipeline,
  createNCPLoadNode,
  createBeatGenerationNode,
  createAnalysisNode,
  createEnrichmentNode,
  createCommitNode,
} from './narrative-story-graph.js';
export type { NodeResult, GraphState, GraphNode } from './narrative-story-graph.js';

// Ceremonial Diary exports
export {
  CeremonialPhase,
  EntryType,
  CeremonialDiary,
  DiaryManager,
  createDiaryEntry,
} from './ceremonial-diary.js';
export type { DiaryEntry } from './ceremonial-diary.js';

// Narrative Tracing exports
export {
  STORYTELLING_EVENT_TYPES,
  EVENT_GLYPHS,
  StorytellingTracer,
} from './narrative-tracing.js';
export type {
  StorytellingEventType,
  TraceSpan,
} from './narrative-tracing.js';

// Type exports (original types.ts — data models and MCP)
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
export const VERSION = '0.2.0';
