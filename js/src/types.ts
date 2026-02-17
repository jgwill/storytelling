/**
 * storytellingjs - Core Type Definitions
 * 
 * Parity with Python storytelling/data_models.py and related types
 */

import { z } from 'zod';

// =============================================================================
// ENUMS
// =============================================================================

/** Session status states */
export type SessionStatus = 'in_progress' | 'completed' | 'failed' | 'interrupted';

/** Model provider schemes */
export type ModelProvider = 'google' | 'ollama' | 'openrouter' | 'myflowise';

/** Workflow node names */
export type WorkflowNode = 
  | 'generate_story_elements'
  | 'generate_initial_outline'
  | 'determine_chapter_count'
  | 'generate_single_chapter_scene_by_scene'
  | 'critique_chapter'
  | 'check_chapter_complete'
  | 'revise_chapter'
  | 'increment_chapter_index'
  | 'generate_final_story';

/** Style glossary enforcement levels */
export type EnforcementLevel = 'strict' | 'moderate' | 'lenient';

// =============================================================================
// DATA MODELS (matching Python data_models.py)
// =============================================================================

/** Chapter count schema - determines total chapters */
export interface ChapterCount {
  totalChapters: number;
}

/** Completion check schema - validates content quality */
export interface CompletionCheck {
  isComplete: boolean;
}

/** Summary check schema - verifies chapter follows outline */
export interface SummaryCheck {
  didFollowOutline: boolean;
  suggestions: string;
}

/** Story metadata schema */
export interface StoryInfo {
  title: string;
  summary: string;
  tags: string;
  overallRating: number;
}

/** Scene list for a chapter */
export interface SceneList {
  scenes: string[];
}

// =============================================================================
// SESSION TYPES (matching Python session_manager.py)
// =============================================================================

/** Checkpoint state representation */
export interface SessionCheckpoint {
  checkpointId: string;
  nodeName: WorkflowNode;
  timestamp: string;
  state: Record<string, unknown>;
  metadata: Record<string, unknown>;
}

/** Complete session information */
export interface SessionInfo {
  sessionId: string;
  createdAt: string;
  lastCheckpoint: string;
  status: SessionStatus;
  promptFile: string;
  outputFile: string;
  checkpoints: SessionCheckpoint[];
  configuration: Record<string, unknown>;
}

// =============================================================================
// CONFIGURATION TYPES (matching Python config.py)
// =============================================================================

/** Style glossary for buzz term detection */
export interface StyleGlossary {
  avoidTerms: string[];
  preferredAlternatives: Record<string, string[]>;
  customAvoidPhrases: string[];
  toneWords: Record<string, string[]>;
  enforcementLevel: EnforcementLevel;
}

/** Main configuration options */
export interface StorytellingConfig {
  // Core Parameters
  promptFile?: string;
  outputFile?: string;
  
  // Model Selection
  initialOutlineModel: string;
  chapterOutlineModel: string;
  chapterS1Model: string;
  chapterS2Model: string;
  chapterS3Model: string;
  chapterS4Model: string;
  chapterRevisionModel: string;
  revisionModel: string;
  evalModel: string;
  infoModel: string;
  scrubModel: string;
  checkerModel: string;
  translatorModel: string;
  
  // Knowledge Base / RAG
  knowledgeBasePath?: string;
  embeddingModel?: string;
  ollamaBaseUrl: string;
  
  // Outline-level RAG
  outlineRagEnabled: boolean;
  outlineContextMaxTokens: number;
  outlineRagTopK: number;
  outlineRagSimilarityThreshold: number;
  
  // Chapter-level RAG
  chapterRagEnabled: boolean;
  chapterContextMaxTokens: number;
  chapterRagTopK: number;
  
  // Workflow Control
  expandOutline: boolean;
  enableFinalEditPass: boolean;
  noScrubChapters: boolean;
  sceneGenerationPipeline: boolean;
  
  // Revision Control
  outlineMinRevisions: number;
  outlineMaxRevisions: number;
  chapterMinRevisions: number;
  chapterMaxRevisions: number;
  noChapterRevision: boolean;
  
  // Translation
  translate?: string;
  translatePrompt?: string;
  
  // Style Glossary
  styleGlossaryPath?: string;
  styleGlossary?: StyleGlossary;
  enableBuzzTermRevision: boolean;
  
  // Miscellaneous
  seed: number;
  sleepTime: number;
  debug: boolean;
  mockMode: boolean;
}

// =============================================================================
// CORE TYPES (matching Python core.py)
// =============================================================================

/** Basic story representation */
export interface Story {
  title: string;
  content: string;
  metadata: Record<string, string>;
}

// =============================================================================
// NCP INTEGRATION TYPES (matching narrative_intelligence_integration.py)
// =============================================================================

/** Story beat with optional universe analysis */
export interface StoryBeat {
  id: string;
  text: string;
  timestamp: string;
  emotionalTone?: string;
  thematicRelevance?: string[];
  characterInvolved?: string[];
  universeAnalysis?: {
    engineer?: string;
    ceremony?: string;
    storyEngine?: string;
  };
}

/** Character arc state */
export interface CharacterArcState {
  characterId: string;
  characterName: string;
  currentPosition: number;
  arcType: string;
  keyMoments: string[];
  developmentNotes: string[];
}

/** Gap identified in quality analysis */
export interface Gap {
  type: string;
  severity: 'critical' | 'major' | 'minor';
  description: string;
  affectedBeats?: string[];
  suggestion?: string;
}

/** NCP state container */
export interface NCPState {
  beats: StoryBeat[];
  characterArcs: CharacterArcState[];
  gaps: Gap[];
  currentPhase: string;
}

// =============================================================================
// MCP TYPES (matching storytelling_mcp/server.py)
// =============================================================================

/** Tool definition for MCP */
export interface ToolDefinition {
  name: string;
  description: string;
  inputSchema: {
    type: 'object';
    properties: Record<string, PropertySchema>;
    required?: string[];
  };
}

/** Property schema for tool inputs */
export interface PropertySchema {
  type: 'string' | 'number' | 'boolean' | 'array' | 'object';
  description?: string;
  enum?: string[];
  items?: PropertySchema;
  minimum?: number;
  maximum?: number;
  default?: unknown;
}

/** Tool execution handler */
export interface ToolHandler {
  definition: ToolDefinition;
  execute: (args: Record<string, unknown>) => Promise<ToolResult>;
}

/** Tool execution result */
export interface ToolResult {
  content: Array<{
    type: 'text' | 'image' | 'resource';
    text?: string;
    data?: string;
    mimeType?: string;
  }>;
  isError?: boolean;
}

// =============================================================================
// ZOD SCHEMAS (for runtime validation)
// =============================================================================

export const ChapterCountSchema = z.object({
  totalChapters: z.number().int().positive(),
});

export const CompletionCheckSchema = z.object({
  isComplete: z.boolean(),
});

export const SummaryCheckSchema = z.object({
  didFollowOutline: z.boolean(),
  suggestions: z.string(),
});

export const StoryInfoSchema = z.object({
  title: z.string(),
  summary: z.string(),
  tags: z.string(),
  overallRating: z.number().int().min(1).max(10),
});

export const SessionInfoSchema = z.object({
  sessionId: z.string(),
  createdAt: z.string(),
  lastCheckpoint: z.string(),
  status: z.enum(['in_progress', 'completed', 'failed', 'interrupted']),
  promptFile: z.string(),
  outputFile: z.string(),
  checkpoints: z.array(z.object({
    checkpointId: z.string(),
    nodeName: z.string(),
    timestamp: z.string(),
    state: z.record(z.unknown()),
    metadata: z.record(z.unknown()),
  })),
  configuration: z.record(z.unknown()),
});

export const ModelUriSchema = z.string().regex(
  /^(google|ollama|openrouter|myflowise):\/\/.+$/,
  'Invalid model URI format. Expected: provider://model-name[@host:port]'
);
