/**
 * storytellingjs - Emotional Beat Enricher
 *
 * Parity with Python storytelling/emotional_beat_enricher.py
 * Quality assessment and iterative enrichment of story beats.
 */

import type { StoryBeat, EmotionalAnalysis, Gap } from './narrative-intelligence.js';
import { EmotionCategory } from './narrative-intelligence.js';

// =============================================================================
// Quality Thresholds
// =============================================================================

export const QualityThreshold = {
  EXCELLENT: 0.85,
  GOOD: 0.75,
  ADEQUATE: 0.60,
  WEAK: 0.40,
} as const;

// =============================================================================
// Enrichment Result
// =============================================================================

export interface EnrichedBeatResult {
  originalBeat: StoryBeat;
  finalBeat: StoryBeat;
  initialAnalysis: EmotionalAnalysis;
  finalAnalysis?: EmotionalAnalysis;
  iterations: number;
  wasEnriched: boolean;
  improvementDelta: number;
  enrichmentNotes: string[];
}

// =============================================================================
// Enrichment Techniques
// =============================================================================

export const ENRICHMENT_TECHNIQUES: Record<string, string[]> = {
  stakes: [
    'Make what the character stands to lose/gain clearer',
    'Add ticking clock or deadline pressure',
    'Show irreversibility of the moment',
  ],
  sensory: [
    'Add specific physical sensations',
    'Include environmental details that reflect emotion',
    'Show body language and involuntary reactions',
  ],
  internal: [
    "Show character's internal conflict more visibly",
    'Add thought fragments or memory triggers',
    'Reveal what the character is trying NOT to feel',
  ],
  contrast: [
    'Juxtapose expected vs actual emotional response',
    'Show gap between what character says and feels',
    'Place emotional intensity against mundane backdrop',
  ],
  dialogue: [
    'Add subtext — what is NOT being said?',
    'Use interrupted speech or trailing off',
    'Show emotional leakage through word choice',
  ],
};

// =============================================================================
// Emotional Beat Enricher
// =============================================================================

export class EmotionalBeatEnricher {
  private maxIterations: number;
  private targetQuality: number;
  private generateFn?: (prompt: string) => Promise<string>;

  constructor(options?: {
    maxIterations?: number;
    targetQuality?: number;
    generateFn?: (prompt: string) => Promise<string>;
  }) {
    this.maxIterations = options?.maxIterations ?? 3;
    this.targetQuality = options?.targetQuality ?? QualityThreshold.GOOD;
    this.generateFn = options?.generateFn;
  }

  /**
   * Analyze a beat's emotional quality.
   */
  analyzeBeat(beat: StoryBeat): EmotionalAnalysis {
    // Heuristic analysis when no LLM is available
    const hasDialogue = !!beat.dialogue;
    const hasInternal = !!beat.internal;
    const hasAction = !!beat.action;
    const textLength = beat.rawText.length;

    let confidence = 0.3;
    if (hasDialogue) confidence += 0.15;
    if (hasInternal) confidence += 0.2;
    if (hasAction) confidence += 0.1;
    if (textLength > 200) confidence += 0.1;
    if (textLength > 500) confidence += 0.1;

    const primaryEmotion = (beat.emotionalTone as EmotionCategory) || EmotionCategory.ANTICIPATION;

    return {
      primaryEmotion,
      confidence: Math.min(1, confidence),
      emotionalArc: 'developing',
      intensityLevel: Math.min(1, confidence * 1.2),
    };
  }

  /**
   * Determine which enrichment techniques apply to a beat.
   */
  selectTechniques(analysis: EmotionalAnalysis): string[] {
    const techniques: string[] = [];

    if (analysis.intensityLevel < 0.5) {
      techniques.push('stakes');
    }
    if (analysis.confidence < 0.6) {
      techniques.push('sensory', 'internal');
    }
    if (analysis.intensityLevel >= 0.5 && analysis.confidence >= 0.6) {
      techniques.push('contrast');
    }

    return techniques;
  }

  /**
   * Enrich a single beat through iterative improvement.
   */
  async enrichBeat(beat: StoryBeat): Promise<EnrichedBeatResult> {
    const initialAnalysis = this.analyzeBeat(beat);

    const result: EnrichedBeatResult = {
      originalBeat: { ...beat },
      finalBeat: { ...beat },
      initialAnalysis,
      iterations: 0,
      wasEnriched: false,
      improvementDelta: 0,
      enrichmentNotes: [],
    };

    if (initialAnalysis.confidence >= this.targetQuality) {
      result.enrichmentNotes.push('Beat meets quality threshold — no enrichment needed');
      return result;
    }

    let currentBeat = { ...beat };
    let currentAnalysis = initialAnalysis;

    for (let i = 0; i < this.maxIterations; i++) {
      const techniques = this.selectTechniques(currentAnalysis);
      if (techniques.length === 0) break;

      result.iterations++;
      result.enrichmentNotes.push(
        `Iteration ${i + 1}: applying ${techniques.join(', ')}`,
      );

      // Track enrichment
      currentBeat.enrichmentsApplied.push(...techniques);
      currentBeat.qualityScore = Math.min(1, currentBeat.qualityScore + 0.1);

      currentAnalysis = this.analyzeBeat(currentBeat);
      if (currentAnalysis.confidence >= this.targetQuality) break;
    }

    result.finalBeat = currentBeat;
    result.finalAnalysis = currentAnalysis;
    result.wasEnriched = result.iterations > 0;
    result.improvementDelta = currentAnalysis.confidence - initialAnalysis.confidence;

    return result;
  }

  /**
   * Enrich a batch of beats.
   */
  async enrichBeats(beats: StoryBeat[]): Promise<EnrichedBeatResult[]> {
    const results: EnrichedBeatResult[] = [];
    for (const beat of beats) {
      results.push(await this.enrichBeat(beat));
    }
    return results;
  }

  /**
   * Identify emotional gaps across a sequence of beats.
   */
  identifyGaps(beats: StoryBeat[]): Gap[] {
    const gaps: Gap[] = [];

    for (let i = 1; i < beats.length; i++) {
      const prev = this.analyzeBeat(beats[i - 1]);
      const curr = this.analyzeBeat(beats[i]);

      // Check for emotional flatness
      if (
        prev.primaryEmotion === curr.primaryEmotion &&
        Math.abs(prev.intensityLevel - curr.intensityLevel) < 0.1
      ) {
        gaps.push({
          type: 'emotional_flatness',
          severity: 'minor',
          description: `Beats ${i - 1} and ${i} share same emotion (${curr.primaryEmotion}) at similar intensity`,
          affectedBeats: [beats[i - 1].beatId, beats[i].beatId],
          suggestion: 'Introduce emotional variation or contrast',
        });
      }

      // Check for abrupt shifts
      if (
        prev.primaryEmotion !== curr.primaryEmotion &&
        Math.abs(prev.intensityLevel - curr.intensityLevel) > 0.6
      ) {
        gaps.push({
          type: 'emotional_whiplash',
          severity: 'major',
          description: `Abrupt shift from ${prev.primaryEmotion} to ${curr.primaryEmotion}`,
          affectedBeats: [beats[i - 1].beatId, beats[i].beatId],
          suggestion: 'Add transitional beat to smooth emotional shift',
        });
      }
    }

    return gaps;
  }
}
