/**
 * storytellingjs - Analytical Feedback Loop
 *
 * Parity with Python storytelling/analytical_feedback_loop.py
 * Closed-loop analysis with gap identification and routing.
 */

import type {
  StoryBeat,
  CharacterArcState,
  Gap,
  NCPState,
  EmotionalAnalysis,
} from './narrative-intelligence.js';
import { EmotionalBeatEnricher, QualityThreshold } from './emotional-beat-enricher.js';
import type { EnrichedBeatResult } from './emotional-beat-enricher.js';

// =============================================================================
// Gap Types and Routing
// =============================================================================

export enum GapType {
  EMOTIONAL_WEAK = 'emotional_weak',
  EMOTIONAL_MISMATCH = 'emotional_mismatch',
  CHARACTER_INCONSISTENT = 'character_inconsistent',
  CHARACTER_STATIC = 'character_static',
  THEME_MISSING = 'theme_missing',
  THEME_CONTRADICTION = 'theme_contradiction',
  PACING_ISSUE = 'pacing_issue',
  DIALOGUE_WEAK = 'dialogue_weak',
}

export enum GapDimension {
  EMOTIONAL = 'emotional',
  CHARACTER = 'character',
  THEMATIC = 'thematic',
  STRUCTURAL = 'structural',
}

// Gap type → target role routing
export const GAP_ROUTING: Record<GapType, string> = {
  [GapType.EMOTIONAL_WEAK]: 'storyteller',
  [GapType.EMOTIONAL_MISMATCH]: 'storyteller',
  [GapType.CHARACTER_INCONSISTENT]: 'storyteller',
  [GapType.CHARACTER_STATIC]: 'structurist',
  [GapType.THEME_MISSING]: 'structurist',
  [GapType.THEME_CONTRADICTION]: 'structurist',
  [GapType.PACING_ISSUE]: 'architect',
  [GapType.DIALOGUE_WEAK]: 'storyteller',
};

// =============================================================================
// Analysis Results
// =============================================================================

export interface CharacterAnalysisResult {
  playerId: string;
  consistencyScore: number;
  arcDirection: string;
  issues: string[];
  suggestions: string[];
}

export interface ThematicAnalysisResult {
  threadId: string;
  presenceScore: number;
  development: string;
  issues: string[];
}

export interface MultiDimensionalAnalysis {
  analysisId: string;
  timestamp: string;

  // Per-dimension results
  emotionalAnalysis: EmotionalAnalysis[];
  characterAnalysis: CharacterAnalysisResult[];
  thematicAnalysis: ThematicAnalysisResult[];

  // Aggregated
  gaps: Gap[];
  overallScore: number;
  recommendations: string[];
}

// =============================================================================
// Feedback Loop Iteration
// =============================================================================

export interface FeedbackIteration {
  iterationNumber: number;
  timestamp: string;
  gapsAddressed: number;
  gapsRemaining: number;
  qualityDelta: number;
  actions: string[];
}

// =============================================================================
// Analytical Feedback Loop
// =============================================================================

export class AnalyticalFeedbackLoop {
  private enricher: EmotionalBeatEnricher;
  private maxIterations: number;
  private qualityTarget: number;
  private iterations: FeedbackIteration[] = [];

  constructor(options?: {
    maxIterations?: number;
    qualityTarget?: number;
    generateFn?: (prompt: string) => Promise<string>;
  }) {
    this.maxIterations = options?.maxIterations ?? 3;
    this.qualityTarget = options?.qualityTarget ?? QualityThreshold.GOOD;
    this.enricher = new EmotionalBeatEnricher({
      generateFn: options?.generateFn,
    });
  }

  /**
   * Run multi-dimensional analysis on a set of beats.
   */
  analyze(
    beats: StoryBeat[],
    characterArcs: CharacterArcState[],
    themes: string[],
  ): MultiDimensionalAnalysis {
    const analysisId = `analysis-${Date.now()}`;
    const gaps: Gap[] = [];
    const recommendations: string[] = [];

    // 1. Emotional dimension
    const emotionalAnalysis = beats.map((beat) => this.enricher.analyzeBeat(beat));
    const emotionalGaps = this.enricher.identifyGaps(beats);
    gaps.push(...emotionalGaps);

    // 2. Character dimension
    const characterAnalysis: CharacterAnalysisResult[] = characterArcs.map((arc) => {
      const arcBeats = beats.filter((b) => b.characterId === arc.characterId);
      const issues: string[] = [];
      const suggestions: string[] = [];

      if (arcBeats.length === 0) {
        issues.push(`No beats found for character ${arc.characterName}`);
        suggestions.push('Add scenes featuring this character');
      }

      if (arcBeats.length > 0 && arcBeats.length < 3) {
        issues.push(`Character ${arc.characterName} is underdeveloped (${arcBeats.length} beats)`);
        suggestions.push('Expand character presence across more beats');
      }

      const consistencyScore = arcBeats.length > 0 ? Math.min(1, arcBeats.length / 8) : 0;

      if (consistencyScore < 0.5) {
        gaps.push({
          type: GapType.CHARACTER_STATIC,
          severity: 'major',
          description: `Character ${arc.characterName} shows minimal development`,
          affectedBeats: arcBeats.map((b) => b.beatId),
          suggestion: 'Add key development moments',
          dimension: GapDimension.CHARACTER,
        });
      }

      return {
        playerId: arc.characterId,
        consistencyScore,
        arcDirection: arc.arcType,
        issues,
        suggestions,
      };
    });

    // 3. Thematic dimension
    const thematicAnalysis: ThematicAnalysisResult[] = themes.map((theme) => {
      const presenceScore = beats.filter(
        (b) => b.themeResonance?.includes(theme) ?? false,
      ).length / Math.max(1, beats.length);

      if (presenceScore < 0.2) {
        gaps.push({
          type: GapType.THEME_MISSING,
          severity: 'minor',
          description: `Theme "${theme}" is underrepresented`,
          suggestion: 'Weave theme into character actions and dialogue',
          dimension: GapDimension.THEMATIC,
        });
      }

      return {
        threadId: theme,
        presenceScore,
        development: presenceScore > 0.5 ? 'strong' : presenceScore > 0.2 ? 'developing' : 'weak',
        issues: presenceScore < 0.2 ? [`Theme "${theme}" needs more presence`] : [],
      };
    });

    // Aggregate score
    const emotionalAvg =
      emotionalAnalysis.reduce((sum, a) => sum + a.confidence, 0) /
      Math.max(1, emotionalAnalysis.length);
    const characterAvg =
      characterAnalysis.reduce((sum, a) => sum + a.consistencyScore, 0) /
      Math.max(1, characterAnalysis.length);
    const thematicAvg =
      thematicAnalysis.reduce((sum, a) => sum + a.presenceScore, 0) /
      Math.max(1, thematicAnalysis.length);
    const overallScore = (emotionalAvg + characterAvg + thematicAvg) / 3;

    // Recommendations
    if (overallScore < QualityThreshold.ADEQUATE) {
      recommendations.push('Overall quality below threshold — prioritize critical gaps');
    }
    if (gaps.filter((g) => g.severity === 'critical').length > 0) {
      recommendations.push('Address critical gaps before proceeding to next generation phase');
    }

    return {
      analysisId,
      timestamp: new Date().toISOString(),
      emotionalAnalysis,
      characterAnalysis,
      thematicAnalysis,
      gaps,
      overallScore,
      recommendations,
    };
  }

  /**
   * Route gaps to appropriate enrichment flows.
   */
  routeGaps(gaps: Gap[]): Record<string, Gap[]> {
    const routed: Record<string, Gap[]> = {};

    for (const gap of gaps) {
      const target = GAP_ROUTING[gap.type as GapType] ?? 'architect';
      if (!routed[target]) routed[target] = [];
      routed[target].push(gap);
    }

    return routed;
  }

  /**
   * Run the full feedback loop: analyze → enrich → re-analyze.
   */
  async runLoop(
    beats: StoryBeat[],
    characterArcs: CharacterArcState[],
    themes: string[],
  ): Promise<{
    finalAnalysis: MultiDimensionalAnalysis;
    iterations: FeedbackIteration[];
    enrichedBeats: EnrichedBeatResult[];
  }> {
    let currentBeats = [...beats];
    let enrichedResults: EnrichedBeatResult[] = [];

    for (let i = 0; i < this.maxIterations; i++) {
      const analysis = this.analyze(currentBeats, characterArcs, themes);

      if (analysis.overallScore >= this.qualityTarget || analysis.gaps.length === 0) {
        this.iterations.push({
          iterationNumber: i + 1,
          timestamp: new Date().toISOString(),
          gapsAddressed: 0,
          gapsRemaining: analysis.gaps.length,
          qualityDelta: 0,
          actions: ['Quality target met — loop complete'],
        });
        return { finalAnalysis: analysis, iterations: this.iterations, enrichedBeats: enrichedResults };
      }

      // Enrich beats with quality gaps
      const results = await this.enricher.enrichBeats(currentBeats);
      enrichedResults = results;
      currentBeats = results.map((r) => r.finalBeat);

      this.iterations.push({
        iterationNumber: i + 1,
        timestamp: new Date().toISOString(),
        gapsAddressed: results.filter((r) => r.wasEnriched).length,
        gapsRemaining: analysis.gaps.length,
        qualityDelta: results.reduce((sum, r) => sum + r.improvementDelta, 0) / Math.max(1, results.length),
        actions: [`Enriched ${results.filter((r) => r.wasEnriched).length} beats`],
      });
    }

    const finalAnalysis = this.analyze(currentBeats, characterArcs, themes);
    return { finalAnalysis, iterations: this.iterations, enrichedBeats: enrichedResults };
  }

  getIterations(): FeedbackIteration[] {
    return [...this.iterations];
  }
}
