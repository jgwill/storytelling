/**
 * storytellingjs - Narrative Tracing Adapter
 *
 * Parity with Python storytelling/narrative_tracing.py
 * Bridges storytelling operations to observability infrastructure.
 */

// =============================================================================
// Event Types for Storytelling
// =============================================================================

export const STORYTELLING_EVENT_TYPES = {
  // Beat lifecycle
  BEAT_GENERATED: 'storytelling.beat.generated',
  BEAT_ANALYZED: 'storytelling.beat.analyzed',
  BEAT_ENRICHED: 'storytelling.beat.enriched',
  BEAT_COMMITTED: 'storytelling.beat.committed',

  // Chapter lifecycle
  CHAPTER_STARTED: 'storytelling.chapter.started',
  CHAPTER_SCENE_GENERATED: 'storytelling.chapter.scene_generated',
  CHAPTER_CRITIQUED: 'storytelling.chapter.critiqued',
  CHAPTER_REVISED: 'storytelling.chapter.revised',
  CHAPTER_COMPLETED: 'storytelling.chapter.completed',

  // Graph lifecycle
  GRAPH_STARTED: 'storytelling.graph.started',
  GRAPH_NODE_ENTERED: 'storytelling.graph.node_entered',
  GRAPH_NODE_COMPLETED: 'storytelling.graph.node_completed',
  GRAPH_COMPLETED: 'storytelling.graph.completed',

  // Session lifecycle
  SESSION_STARTED: 'storytelling.session.started',
  SESSION_CHECKPOINT: 'storytelling.session.checkpoint',
  SESSION_RESUMED: 'storytelling.session.resumed',
  SESSION_COMPLETED: 'storytelling.session.completed',

  // Three-Universe
  THREE_UNIVERSE_ANALYSIS: 'storytelling.three_universe.analysis',

  // Ceremonial
  CEREMONY_PHASE_ENTERED: 'storytelling.ceremony.phase_entered',
  DIARY_ENTRY_CREATED: 'storytelling.diary.entry_created',
} as const;

export type StorytellingEventType = typeof STORYTELLING_EVENT_TYPES[keyof typeof STORYTELLING_EVENT_TYPES];

// =============================================================================
// Event Glyphs (from ava-langchain narrative-tracing)
// =============================================================================

export const EVENT_GLYPHS: Record<string, string> = {
  [STORYTELLING_EVENT_TYPES.BEAT_GENERATED]: '📝',
  [STORYTELLING_EVENT_TYPES.BEAT_ANALYZED]: '🔍',
  [STORYTELLING_EVENT_TYPES.BEAT_ENRICHED]: '✨',
  [STORYTELLING_EVENT_TYPES.BEAT_COMMITTED]: '✅',
  [STORYTELLING_EVENT_TYPES.CHAPTER_STARTED]: '📖',
  [STORYTELLING_EVENT_TYPES.CHAPTER_COMPLETED]: '📗',
  [STORYTELLING_EVENT_TYPES.GRAPH_STARTED]: '🔄',
  [STORYTELLING_EVENT_TYPES.GRAPH_COMPLETED]: '🏁',
  [STORYTELLING_EVENT_TYPES.SESSION_STARTED]: '🚀',
  [STORYTELLING_EVENT_TYPES.SESSION_COMPLETED]: '🎉',
  [STORYTELLING_EVENT_TYPES.THREE_UNIVERSE_ANALYSIS]: '🌐',
  [STORYTELLING_EVENT_TYPES.CEREMONY_PHASE_ENTERED]: '🙏',
  [STORYTELLING_EVENT_TYPES.DIARY_ENTRY_CREATED]: '📔',
};

// =============================================================================
// Trace Span
// =============================================================================

export interface TraceSpan {
  spanId: string;
  parentSpanId?: string;
  eventType: StorytellingEventType;
  name: string;
  startTime: string;
  endTime?: string;
  metadata: Record<string, unknown>;
  status: 'running' | 'completed' | 'failed';
}

// =============================================================================
// Storytelling Tracer
// =============================================================================

export class StorytellingTracer {
  private storyId: string;
  private sessionId: string;
  private spans: TraceSpan[] = [];
  private activeSpans: Map<string, TraceSpan> = new Map();
  private enabled: boolean;

  constructor(storyId: string, sessionId: string, enabled: boolean = true) {
    this.storyId = storyId;
    this.sessionId = sessionId;
    this.enabled = enabled;
  }

  /**
   * Start a new trace span.
   */
  startSpan(
    eventType: StorytellingEventType,
    name: string,
    metadata?: Record<string, unknown>,
    parentSpanId?: string,
  ): string {
    const spanId = `span-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;

    const span: TraceSpan = {
      spanId,
      parentSpanId,
      eventType,
      name,
      startTime: new Date().toISOString(),
      metadata: {
        storyId: this.storyId,
        sessionId: this.sessionId,
        ...metadata,
      },
      status: 'running',
    };

    this.spans.push(span);
    this.activeSpans.set(spanId, span);

    if (this.enabled) {
      const glyph = EVENT_GLYPHS[eventType] ?? '•';
      console.log(`${glyph} [${eventType}] ${name}`);
    }

    return spanId;
  }

  /**
   * End a trace span.
   */
  endSpan(spanId: string, status: 'completed' | 'failed' = 'completed'): void {
    const span = this.activeSpans.get(spanId);
    if (!span) return;

    span.endTime = new Date().toISOString();
    span.status = status;
    this.activeSpans.delete(spanId);
  }

  /**
   * Log an event without a span duration.
   */
  logEvent(
    eventType: StorytellingEventType,
    name: string,
    metadata?: Record<string, unknown>,
  ): void {
    const spanId = this.startSpan(eventType, name, metadata);
    this.endSpan(spanId);
  }

  // Convenience methods

  logBeatGenerated(beatId: string, characterId: string): void {
    this.logEvent(STORYTELLING_EVENT_TYPES.BEAT_GENERATED, `Beat ${beatId}`, {
      beatId,
      characterId,
    });
  }

  logBeatAnalyzed(beatId: string, score: number): void {
    this.logEvent(STORYTELLING_EVENT_TYPES.BEAT_ANALYZED, `Analyzed ${beatId}`, {
      beatId,
      score,
    });
  }

  logBeatEnriched(beatId: string, techniques: string[]): void {
    this.logEvent(STORYTELLING_EVENT_TYPES.BEAT_ENRICHED, `Enriched ${beatId}`, {
      beatId,
      techniques,
    });
  }

  logThreeUniverseAnalysis(
    beatId: string,
    engineer: string,
    ceremony: string,
    storyEngine: string,
  ): void {
    this.logEvent(STORYTELLING_EVENT_TYPES.THREE_UNIVERSE_ANALYSIS, `3U Analysis ${beatId}`, {
      beatId,
      engineer,
      ceremony,
      storyEngine,
    });
  }

  logCeremonialPhase(phase: string, participant: string): void {
    this.logEvent(STORYTELLING_EVENT_TYPES.CEREMONY_PHASE_ENTERED, `Phase: ${phase}`, {
      phase,
      participant,
    });
  }

  /**
   * Get all spans for export.
   */
  getSpans(): TraceSpan[] {
    return [...this.spans];
  }

  /**
   * Get correlation headers for cross-system tracing.
   */
  getCorrelationHeaders(): Record<string, string> {
    return {
      'X-Narrative-Trace-Id': `${this.storyId}-${this.sessionId}`,
      'X-Story-Id': this.storyId,
      'X-Session-Id': this.sessionId,
    };
  }
}
