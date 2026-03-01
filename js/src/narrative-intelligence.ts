/**
 * storytellingjs - Narrative Intelligence Integration
 *
 * Parity with Python storytelling/narrative_intelligence_integration.py
 * NCP-aware story generation with Three-Universe analysis.
 */

// =============================================================================
// Emotional Taxonomy
// =============================================================================

export enum EmotionCategory {
  JOY = 'joy',
  SADNESS = 'sadness',
  ANGER = 'anger',
  FEAR = 'fear',
  SURPRISE = 'surprise',
  DISGUST = 'disgust',
  TRUST = 'trust',
  ANTICIPATION = 'anticipation',
  LOVE = 'love',
  SHAME = 'shame',
}

// =============================================================================
// Three-Universe Model
// =============================================================================

export enum Universe {
  ENGINEER = 'engineer',
  CEREMONY = 'ceremony',
  STORY_ENGINE = 'story_engine',
}

export interface UniverseAnalysis {
  engineer?: string;
  ceremony?: string;
  storyEngine?: string;
}

export interface ThreeUniverseAnalysis {
  engineerIntent: string;
  ceremonyIntent: string;
  storyEngineIntent: string;
  leadUniverse: Universe;
  coherenceScore: number;
}

// =============================================================================
// Story Beat
// =============================================================================

export interface StoryBeat {
  beatId: string;
  beatIndex: number;
  rawText: string;

  // Character and perspective
  characterId: string;
  characterName?: string;

  // Structured content
  dialogue?: string;
  action?: string;
  internal?: string;

  // Analysis results
  emotionalTone?: string;
  emotionConfidence: number;
  themeResonance?: string;

  // Three-Universe analysis
  universeAnalysis?: UniverseAnalysis;

  // Enrichment tracking
  enrichmentsApplied: string[];
  qualityScore: number;

  // Metadata
  ncpMetadata: Record<string, unknown>;
  timestamp: string;
}

export function createStoryBeat(
  beatId: string,
  beatIndex: number,
  rawText: string,
  characterId: string,
  overrides?: Partial<StoryBeat>,
): StoryBeat {
  return {
    beatId,
    beatIndex,
    rawText,
    characterId,
    emotionConfidence: 0,
    enrichmentsApplied: [],
    qualityScore: 0,
    ncpMetadata: {},
    timestamp: new Date().toISOString(),
    ...overrides,
  };
}

// =============================================================================
// Emotional Analysis
// =============================================================================

export interface EmotionalAnalysis {
  primaryEmotion: EmotionCategory;
  confidence: number;
  secondaryEmotion?: EmotionCategory;
  emotionalArc: string;
  intensityLevel: number;
  emotionalShift?: string;
}

// =============================================================================
// Character Arc State
// =============================================================================

export interface CharacterArcState {
  characterId: string;
  characterName: string;
  currentPosition: number;
  arcType: string;
  keyMoments: string[];
  developmentNotes: string[];
  activeBeats: string[];
  emotionalTrajectory: EmotionCategory[];
}

export function createCharacterArcState(
  characterId: string,
  characterName: string,
  arcType: string = 'growth',
): CharacterArcState {
  return {
    characterId,
    characterName,
    currentPosition: 0,
    arcType,
    keyMoments: [],
    developmentNotes: [],
    activeBeats: [],
    emotionalTrajectory: [],
  };
}

// =============================================================================
// Gap Analysis
// =============================================================================

export type GapSeverity = 'critical' | 'major' | 'minor';

export interface Gap {
  type: string;
  severity: GapSeverity;
  description: string;
  affectedBeats?: string[];
  suggestion?: string;
  dimension?: string;
}

// =============================================================================
// NCP State
// =============================================================================

export interface NCPState {
  beats: StoryBeat[];
  characterArcs: CharacterArcState[];
  gaps: Gap[];
  currentPhase: string;
  thematicThreads: string[];
  overallCoherence: number;
}

export function createNCPState(): NCPState {
  return {
    beats: [],
    characterArcs: [],
    gaps: [],
    currentPhase: 'initialization',
    thematicThreads: [],
    overallCoherence: 0,
  };
}

// =============================================================================
// NCP-Aware Story Generator
// =============================================================================

/**
 * Generates story beats with NCP awareness and Three-Universe analysis.
 */
export class NCPAwareStoryGenerator {
  private ncpState: NCPState;
  private generateFn?: (prompt: string) => Promise<string>;

  constructor(generateFn?: (prompt: string) => Promise<string>) {
    this.ncpState = createNCPState();
    this.generateFn = generateFn;
  }

  getState(): NCPState {
    return this.ncpState;
  }

  /**
   * Generate a beat from raw text, producing structured analysis.
   */
  async generateBeat(
    rawText: string,
    characterId: string,
    characterName?: string,
  ): Promise<StoryBeat> {
    const beatIndex = this.ncpState.beats.length;
    const beatId = `beat-${beatIndex}`;

    const beat = createStoryBeat(beatId, beatIndex, rawText, characterId, {
      characterName,
    });

    this.ncpState.beats.push(beat);
    this.ncpState.currentPhase = 'generation';

    return beat;
  }

  /**
   * Analyze a beat across Three Universes.
   */
  analyzeThreeUniverse(beat: StoryBeat): ThreeUniverseAnalysis {
    return {
      engineerIntent: `Structural function of beat ${beat.beatId} in narrative flow`,
      ceremonyIntent: `Relational significance of beat ${beat.beatId} to character ${beat.characterId}`,
      storyEngineIntent: `Narrative momentum from beat ${beat.beatId}`,
      leadUniverse: Universe.STORY_ENGINE,
      coherenceScore: beat.qualityScore,
    };
  }
}

// =============================================================================
// Character Arc Tracker
// =============================================================================

/**
 * Tracks character development across story beats.
 */
export class CharacterArcTracker {
  private arcs: Map<string, CharacterArcState> = new Map();

  registerCharacter(
    characterId: string,
    characterName: string,
    arcType: string = 'growth',
  ): CharacterArcState {
    const arc = createCharacterArcState(characterId, characterName, arcType);
    this.arcs.set(characterId, arc);
    return arc;
  }

  getArc(characterId: string): CharacterArcState | undefined {
    return this.arcs.get(characterId);
  }

  getAllArcs(): CharacterArcState[] {
    return Array.from(this.arcs.values());
  }

  /**
   * Record a beat's contribution to a character's arc.
   */
  recordBeat(characterId: string, beat: StoryBeat): void {
    const arc = this.arcs.get(characterId);
    if (!arc) return;

    arc.activeBeats.push(beat.beatId);
    if (beat.emotionalTone) {
      const emotion = beat.emotionalTone as EmotionCategory;
      if (Object.values(EmotionCategory).includes(emotion)) {
        arc.emotionalTrajectory.push(emotion);
      }
    }
    arc.currentPosition = arc.activeBeats.length;
  }

  /**
   * Assess arc consistency — returns a score from 0 to 1.
   */
  assessConsistency(characterId: string): number {
    const arc = this.arcs.get(characterId);
    if (!arc || arc.activeBeats.length === 0) return 0;
    // Simple heuristic: more beats = higher consistency base
    return Math.min(1, arc.activeBeats.length / 10);
  }
}
