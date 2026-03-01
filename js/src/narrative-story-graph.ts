/**
 * storytellingjs - Narrative-Aware Story Graph
 *
 * Parity with Python storytelling/narrative_story_graph.py
 * Graph state and node definitions for NCP-aware generation.
 */

import { v4 as uuidv4 } from 'uuid';
import type {
  StoryBeat,
  CharacterArcState,
  NCPState,
  Gap,
  ThreeUniverseAnalysis,
} from './narrative-intelligence.js';
import { NCPAwareStoryGenerator, CharacterArcTracker, createNCPState } from './narrative-intelligence.js';
import { EmotionalBeatEnricher } from './emotional-beat-enricher.js';
import type { EnrichedBeatResult } from './emotional-beat-enricher.js';
import { AnalyticalFeedbackLoop } from './analytical-feedback-loop.js';
import type { MultiDimensionalAnalysis } from './analytical-feedback-loop.js';

// =============================================================================
// Graph State
// =============================================================================

export enum NodeStatus {
  PENDING = 'pending',
  RUNNING = 'running',
  COMPLETED = 'completed',
  FAILED = 'failed',
  SKIPPED = 'skipped',
}

export interface NodeResult {
  nodeId: string;
  status: NodeStatus;
  output?: unknown;
  error?: string;
  durationMs: number;
  timestamp: string;
}

export interface GraphState {
  // Identity
  graphId: string;
  sessionId?: string;

  // Input
  prompt: string;
  context: Record<string, unknown>;

  // NCP State
  ncpState: NCPState;

  // Beat management
  currentBeat?: StoryBeat;
  pendingBeats: StoryBeat[];
  completedBeats: StoryBeat[];

  // Analysis
  latestAnalysis?: MultiDimensionalAnalysis;
  analysisHistory: MultiDimensionalAnalysis[];

  // Graph execution
  currentNode: string;
  nodeResults: NodeResult[];
  errors: string[];

  // Metadata
  startedAt: string;
  updatedAt: string;
}

export function createGraphState(prompt: string, sessionId?: string): GraphState {
  return {
    graphId: uuidv4(),
    sessionId,
    prompt,
    context: {},
    ncpState: createNCPState(),
    pendingBeats: [],
    completedBeats: [],
    analysisHistory: [],
    currentNode: 'start',
    nodeResults: [],
    errors: [],
    startedAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };
}

// =============================================================================
// Graph Nodes
// =============================================================================

export type GraphNode = (state: GraphState) => Promise<GraphState>;

/**
 * NCP Load Node — loads NCP data and initializes state.
 */
export function createNCPLoadNode(): GraphNode {
  return async (state: GraphState): Promise<GraphState> => {
    const start = Date.now();
    state.currentNode = 'ncp_load';

    try {
      state.ncpState = createNCPState();
      state.ncpState.currentPhase = 'loaded';

      state.nodeResults.push({
        nodeId: 'ncp_load',
        status: NodeStatus.COMPLETED,
        durationMs: Date.now() - start,
        timestamp: new Date().toISOString(),
      });
    } catch (err) {
      const error = err instanceof Error ? err.message : String(err);
      state.errors.push(error);
      state.nodeResults.push({
        nodeId: 'ncp_load',
        status: NodeStatus.FAILED,
        error,
        durationMs: Date.now() - start,
        timestamp: new Date().toISOString(),
      });
    }

    state.updatedAt = new Date().toISOString();
    return state;
  };
}

/**
 * Beat Generation Node — generates story beats from prompt context.
 */
export function createBeatGenerationNode(
  generateFn?: (prompt: string) => Promise<string>,
): GraphNode {
  const generator = new NCPAwareStoryGenerator(generateFn);

  return async (state: GraphState): Promise<GraphState> => {
    const start = Date.now();
    state.currentNode = 'beat_generation';

    try {
      const beat = await generator.generateBeat(
        state.prompt,
        'protagonist',
        'Protagonist',
      );
      state.pendingBeats.push(beat);
      state.ncpState = generator.getState();

      state.nodeResults.push({
        nodeId: 'beat_generation',
        status: NodeStatus.COMPLETED,
        output: { beatId: beat.beatId },
        durationMs: Date.now() - start,
        timestamp: new Date().toISOString(),
      });
    } catch (err) {
      const error = err instanceof Error ? err.message : String(err);
      state.errors.push(error);
      state.nodeResults.push({
        nodeId: 'beat_generation',
        status: NodeStatus.FAILED,
        error,
        durationMs: Date.now() - start,
        timestamp: new Date().toISOString(),
      });
    }

    state.updatedAt = new Date().toISOString();
    return state;
  };
}

/**
 * Analysis Node — runs multi-dimensional analysis on beats.
 */
export function createAnalysisNode(): GraphNode {
  const feedbackLoop = new AnalyticalFeedbackLoop();

  return async (state: GraphState): Promise<GraphState> => {
    const start = Date.now();
    state.currentNode = 'analysis';

    try {
      const allBeats = [...state.completedBeats, ...state.pendingBeats];
      const themes = state.ncpState.thematicThreads;
      const arcs = state.ncpState.characterArcs;

      const analysis = feedbackLoop.analyze(allBeats, arcs, themes);
      state.latestAnalysis = analysis;
      state.analysisHistory.push(analysis);
      state.ncpState.gaps = analysis.gaps;
      state.ncpState.overallCoherence = analysis.overallScore;

      state.nodeResults.push({
        nodeId: 'analysis',
        status: NodeStatus.COMPLETED,
        output: { score: analysis.overallScore, gapCount: analysis.gaps.length },
        durationMs: Date.now() - start,
        timestamp: new Date().toISOString(),
      });
    } catch (err) {
      const error = err instanceof Error ? err.message : String(err);
      state.errors.push(error);
      state.nodeResults.push({
        nodeId: 'analysis',
        status: NodeStatus.FAILED,
        error,
        durationMs: Date.now() - start,
        timestamp: new Date().toISOString(),
      });
    }

    state.updatedAt = new Date().toISOString();
    return state;
  };
}

/**
 * Enrichment Node — enriches beats that are below quality threshold.
 */
export function createEnrichmentNode(
  generateFn?: (prompt: string) => Promise<string>,
): GraphNode {
  const enricher = new EmotionalBeatEnricher({ generateFn });

  return async (state: GraphState): Promise<GraphState> => {
    const start = Date.now();
    state.currentNode = 'enrichment';

    try {
      const results = await enricher.enrichBeats(state.pendingBeats);
      state.pendingBeats = results.map((r) => r.finalBeat);

      const enrichedCount = results.filter((r) => r.wasEnriched).length;

      state.nodeResults.push({
        nodeId: 'enrichment',
        status: NodeStatus.COMPLETED,
        output: { enrichedCount, totalBeats: results.length },
        durationMs: Date.now() - start,
        timestamp: new Date().toISOString(),
      });
    } catch (err) {
      const error = err instanceof Error ? err.message : String(err);
      state.errors.push(error);
      state.nodeResults.push({
        nodeId: 'enrichment',
        status: NodeStatus.FAILED,
        error,
        durationMs: Date.now() - start,
        timestamp: new Date().toISOString(),
      });
    }

    state.updatedAt = new Date().toISOString();
    return state;
  };
}

/**
 * Commit Node — moves pending beats to completed.
 */
export function createCommitNode(): GraphNode {
  return async (state: GraphState): Promise<GraphState> => {
    const start = Date.now();
    state.currentNode = 'commit';

    state.completedBeats.push(...state.pendingBeats);
    state.ncpState.beats = state.completedBeats;
    state.pendingBeats = [];

    state.nodeResults.push({
      nodeId: 'commit',
      status: NodeStatus.COMPLETED,
      output: { totalCompleted: state.completedBeats.length },
      durationMs: Date.now() - start,
      timestamp: new Date().toISOString(),
    });

    state.updatedAt = new Date().toISOString();
    return state;
  };
}

// =============================================================================
// Narrative-Aware Story Graph
// =============================================================================

/**
 * Orchestrates the NCP-aware story generation pipeline.
 */
export class NarrativeAwareStoryGraph {
  private nodes: Map<string, GraphNode> = new Map();
  private edges: Map<string, string[]> = new Map();

  addNode(name: string, node: GraphNode): void {
    this.nodes.set(name, node);
  }

  addEdge(from: string, to: string): void {
    const existing = this.edges.get(from) ?? [];
    existing.push(to);
    this.edges.set(from, existing);
  }

  /**
   * Execute the graph linearly through connected nodes.
   */
  async execute(state: GraphState): Promise<GraphState> {
    let currentNode = 'start';
    let current = state;

    while (true) {
      const nextNodes = this.edges.get(currentNode);
      if (!nextNodes || nextNodes.length === 0) break;

      const nextName = nextNodes[0]; // Linear execution
      const node = this.nodes.get(nextName);
      if (!node) {
        current.errors.push(`Node not found: ${nextName}`);
        break;
      }

      current = await node(current);
      currentNode = nextName;

      // Stop on failure
      const lastResult = current.nodeResults[current.nodeResults.length - 1];
      if (lastResult?.status === NodeStatus.FAILED) break;
    }

    return current;
  }
}

/**
 * Create a default narrative-aware pipeline.
 */
export function createDefaultPipeline(
  generateFn?: (prompt: string) => Promise<string>,
): NarrativeAwareStoryGraph {
  const graph = new NarrativeAwareStoryGraph();

  graph.addNode('ncp_load', createNCPLoadNode());
  graph.addNode('beat_generation', createBeatGenerationNode(generateFn));
  graph.addNode('analysis', createAnalysisNode());
  graph.addNode('enrichment', createEnrichmentNode(generateFn));
  graph.addNode('commit', createCommitNode());

  graph.addEdge('start', 'ncp_load');
  graph.addEdge('ncp_load', 'beat_generation');
  graph.addEdge('beat_generation', 'analysis');
  graph.addEdge('analysis', 'enrichment');
  graph.addEdge('enrichment', 'commit');

  return graph;
}
