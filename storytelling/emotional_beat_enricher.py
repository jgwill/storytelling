"""
Emotional Beat Enrichment for Storytelling Package

This module provides emotional quality assessment and iterative enrichment
of story beats to ensure consistent emotional resonance.

Implements specification from:
- rispecs/Emotional_Beat_Enrichment_Specification.md
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from .narrative_intelligence_integration import (
    StoryBeat,
    EmotionalAnalysis,
    EmotionCategory,
    Gap,
)

logger = logging.getLogger(__name__)


# ============================================================================
# Quality Thresholds
# ============================================================================

class QualityThreshold:
    """Quality threshold constants."""
    EXCELLENT = 0.85
    GOOD = 0.75
    ADEQUATE = 0.60
    WEAK = 0.40


# ============================================================================
# Enrichment Result
# ============================================================================

@dataclass
class EnrichedBeatResult:
    """Result container for enrichment process."""
    original_beat: StoryBeat
    final_beat: StoryBeat
    
    # Analysis
    initial_analysis: EmotionalAnalysis
    final_analysis: Optional[EmotionalAnalysis] = None
    
    # Process tracking
    iterations: int = 0
    was_enriched: bool = False
    improvement_delta: float = 0.0
    
    # Notes
    enrichment_notes: List[str] = field(default_factory=list)


# ============================================================================
# Enrichment Techniques
# ============================================================================

ENRICHMENT_TECHNIQUES = {
    "stakes": [
        "Make what the character stands to lose/gain clearer",
        "Add ticking clock or deadline pressure",
        "Show irreversibility of the moment",
    ],
    "sensory": [
        "Add specific physical sensations",
        "Include environmental details that reflect emotion",
        "Show body language and involuntary reactions",
    ],
    "internal": [
        "Show character's internal conflict more visibly",
        "Add thought fragments or memory triggers",
        "Include cognitive dissonance or realization",
    ],
    "dialogue": [
        "Add specificity and emotional subtext to speech",
        "Use meaningful pauses or interruptions",
        "Let silence carry emotional weight",
    ],
    "action": [
        "Use telling gestures that reveal emotion",
        "Show involuntary movements or reactions",
        "Add meaningful physical actions",
    ],
    "pacing": [
        "Vary sentence length for emotional rhythm",
        "Use white space and breathing room",
        "Apply repetition for emphasis",
    ],
}


# ============================================================================
# Emotional Beat Enricher
# ============================================================================

class EmotionalBeatEnricher:
    """
    Analyze and enrich story beats for emotional quality.
    
    Implements specification from Emotional_Beat_Enrichment_Specification.md
    """
    
    def __init__(
        self,
        llm_provider: Any,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize enricher with LLM provider.
        
        Args:
            llm_provider: LLM provider for analysis and enrichment
            config: Configuration options
        """
        self.llm_provider = llm_provider
        self.config = config or {}
        
        # Configuration
        self.quality_threshold = self.config.get(
            'emotional_quality_threshold', QualityThreshold.GOOD
        )
        self.max_iterations = self.config.get('enrichment_max_iterations', 3)
        self.min_improvement = self.config.get('enrichment_min_improvement', 0.05)
        self.length_tolerance = self.config.get('preserve_length_tolerance', 0.20)
        
        logger.info(f"EmotionalBeatEnricher initialized (threshold={self.quality_threshold})")
    
    async def analyze_and_enrich(
        self,
        beat: StoryBeat,
        target_threshold: Optional[float] = None,
        max_iterations: Optional[int] = None,
    ) -> EnrichedBeatResult:
        """
        Complete analysis → enrichment pipeline.
        
        Args:
            beat: The story beat to analyze and potentially enrich
            target_threshold: Quality threshold to achieve (default from config)
            max_iterations: Maximum enrichment iterations (default from config)
        
        Returns:
            EnrichedBeatResult with original and enriched beat
        """
        threshold = target_threshold or self.quality_threshold
        max_iter = max_iterations or self.max_iterations
        
        # Initial analysis
        initial_analysis = await self.classify_emotion(beat)
        
        # Check if enrichment needed
        if initial_analysis.quality_score >= threshold:
            return EnrichedBeatResult(
                original_beat=beat,
                final_beat=beat,
                initial_analysis=initial_analysis,
                final_analysis=initial_analysis,
                iterations=0,
                was_enriched=False,
                enrichment_notes=["Beat met quality threshold, no enrichment needed"],
            )
        
        # Enrichment loop
        current_beat = beat
        current_analysis = initial_analysis
        iteration = 0
        notes = []
        
        while iteration < max_iter:
            iteration += 1
            
            # Check if we should continue
            if not self._should_continue_enrichment(
                current_analysis, threshold, iteration, max_iter
            ):
                notes.append(f"Stopped at iteration {iteration}")
                break
            
            # Enrich the beat
            enriched_beat = await self._enrich_beat(
                current_beat, current_analysis
            )
            
            # Re-analyze
            new_analysis = await self.classify_emotion(enriched_beat)
            
            # Check improvement
            improvement = new_analysis.quality_score - current_analysis.quality_score
            notes.append(
                f"Iteration {iteration}: {current_analysis.quality_score:.2f} → "
                f"{new_analysis.quality_score:.2f} (Δ{improvement:+.2f})"
            )
            
            if improvement < self.min_improvement:
                notes.append("Improvement below threshold, stopping")
                break
            
            current_beat = enriched_beat
            current_analysis = new_analysis
            
            if current_analysis.quality_score >= threshold:
                notes.append("Quality threshold achieved")
                break
        
        return EnrichedBeatResult(
            original_beat=beat,
            final_beat=current_beat,
            initial_analysis=initial_analysis,
            final_analysis=current_analysis,
            iterations=iteration,
            was_enriched=iteration > 0,
            improvement_delta=current_analysis.quality_score - initial_analysis.quality_score,
            enrichment_notes=notes,
        )
    
    async def classify_emotion(self, beat: StoryBeat) -> EmotionalAnalysis:
        """
        Classify emotional content of a beat.
        
        Args:
            beat: Story beat to analyze
        
        Returns:
            EmotionalAnalysis with classification and quality metrics
        """
        # Build analysis prompt
        prompt = self._build_classification_prompt(beat)
        
        # Get LLM analysis
        try:
            response = await self._async_generate(prompt)
            analysis = self._parse_classification_response(response, beat.beat_id)
        except Exception as e:
            logger.error(f"Classification failed: {e}")
            analysis = EmotionalAnalysis(
                beat_id=beat.beat_id,
                primary_emotion="unclassified",
                confidence=0.0,
            )
        
        # Calculate overall quality
        analysis.calculate_quality()
        
        return analysis
    
    def _build_classification_prompt(self, beat: StoryBeat) -> str:
        """Build prompt for emotional classification."""
        return f"""Analyze the following story beat for emotional content and quality.

=== Story Beat ===
{beat.raw_text}

=== Analysis Required ===
Provide analysis in the following format:

PRIMARY_EMOTION: [single emotion word]
SECONDARY_EMOTIONS: [comma-separated list]
CONFIDENCE: [0.0-1.0]

RESONANCE_SCORE: [0.0-1.0] How strongly the emotion connects with reader
SPECIFICITY_SCORE: [0.0-1.0] How specific vs abstract the emotional expression
AUTHENTICITY_SCORE: [0.0-1.0] How genuine vs forced the emotion feels

IMPROVEMENT_AREAS: [comma-separated list of: stakes, sensory, internal, dialogue, action, pacing]
SUGGESTED_TECHNIQUES: [comma-separated specific techniques]
"""
    
    def _parse_classification_response(
        self, response: str, beat_id: str
    ) -> EmotionalAnalysis:
        """Parse LLM response into EmotionalAnalysis."""
        analysis = EmotionalAnalysis(beat_id=beat_id, primary_emotion="neutral")
        
        for line in response.split('\n'):
            line = line.strip()
            if ':' not in line:
                continue
            
            key, value = line.split(':', 1)
            key = key.strip().upper()
            value = value.strip()
            
            if key == "PRIMARY_EMOTION":
                analysis.primary_emotion = value.lower()
            elif key == "SECONDARY_EMOTIONS":
                analysis.secondary_emotions = [e.strip() for e in value.split(',')]
            elif key == "CONFIDENCE":
                analysis.confidence = self._parse_float(value, 0.5)
            elif key == "RESONANCE_SCORE":
                analysis.resonance_score = self._parse_float(value, 0.5)
            elif key == "SPECIFICITY_SCORE":
                analysis.specificity_score = self._parse_float(value, 0.5)
            elif key == "AUTHENTICITY_SCORE":
                analysis.authenticity_score = self._parse_float(value, 0.5)
            elif key == "IMPROVEMENT_AREAS":
                analysis.improvement_areas = [a.strip() for a in value.split(',')]
            elif key == "SUGGESTED_TECHNIQUES":
                analysis.suggested_techniques = [t.strip() for t in value.split(',')]
        
        return analysis
    
    def _parse_float(self, value: str, default: float) -> float:
        """Parse float from string with default."""
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    async def _enrich_beat(
        self,
        beat: StoryBeat,
        analysis: EmotionalAnalysis,
    ) -> StoryBeat:
        """
        Enrich a beat to strengthen emotional resonance.
        
        Args:
            beat: Beat to enrich
            analysis: Current emotional analysis
        
        Returns:
            Enriched StoryBeat
        """
        prompt = self._build_enrichment_prompt(beat, analysis)
        
        try:
            response = await self._async_generate(prompt)
            
            # Create enriched beat
            enriched = StoryBeat(
                beat_id=beat.beat_id,
                beat_index=beat.beat_index,
                raw_text=response,
                character_id=beat.character_id,
                character_name=beat.character_name,
                emotional_tone=analysis.primary_emotion,
                ncp_metadata=beat.ncp_metadata.copy(),
                enrichments_applied=beat.enrichments_applied + analysis.improvement_areas,
            )
            
            return enriched
            
        except Exception as e:
            logger.error(f"Enrichment failed: {e}")
            return beat
    
    def _build_enrichment_prompt(
        self,
        beat: StoryBeat,
        analysis: EmotionalAnalysis,
    ) -> str:
        """Build prompt for emotional enrichment."""
        # Gather techniques for improvement areas
        techniques = []
        for area in analysis.improvement_areas[:3]:  # Focus on top 3 areas
            if area in ENRICHMENT_TECHNIQUES:
                techniques.extend(ENRICHMENT_TECHNIQUES[area])
        
        return f"""=== Emotional Enrichment Request ===

The following story beat was analyzed for emotional quality:

--- Original Beat ---
{beat.raw_text}

--- Analysis Results ---
Primary Emotion: {analysis.primary_emotion}
Confidence: {analysis.confidence:.2f}
Quality Score: {analysis.quality_score:.2f}

Areas Needing Improvement:
{', '.join(analysis.improvement_areas)}

--- Enrichment Guidelines ---
To strengthen emotional resonance, apply these techniques:

{chr(10).join(f"- {t}" for t in techniques[:6])}

--- Task ---
Rewrite this beat to achieve stronger {analysis.primary_emotion} resonance.
Preserve the narrative content while deepening emotional impact.
Keep approximately the same length (within 20%).

Output ONLY the rewritten beat, no explanations.
"""
    
    def _should_continue_enrichment(
        self,
        analysis: EmotionalAnalysis,
        threshold: float,
        iteration: int,
        max_iterations: int,
    ) -> bool:
        """Determine if enrichment should continue."""
        if analysis.quality_score >= threshold:
            return False
        if iteration >= max_iterations:
            return False
        return True
    
    async def _async_generate(self, prompt: str) -> str:
        """Generate LLM response (async wrapper)."""
        # Handle both sync and async LLM providers
        import asyncio
        
        if hasattr(self.llm_provider, 'agenerate'):
            return await self.llm_provider.agenerate(prompt)
        elif hasattr(self.llm_provider, 'generate'):
            # Wrap sync in executor
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None, self.llm_provider.generate, prompt
            )
        else:
            raise ValueError("LLM provider must have 'generate' or 'agenerate' method")
    
    def validate_enrichment(
        self,
        original: StoryBeat,
        enriched: StoryBeat,
    ) -> Dict[str, Any]:
        """
        Validate that enrichment preserved narrative content.
        
        Args:
            original: Original beat
            enriched: Enriched beat
        
        Returns:
            Validation result with score and issues
        """
        issues = []
        
        # Check length preservation
        orig_len = len(original.raw_text)
        new_len = len(enriched.raw_text)
        length_ratio = new_len / orig_len if orig_len > 0 else 1.0
        
        if abs(1.0 - length_ratio) > self.length_tolerance:
            issues.append(f"Length changed by {(length_ratio - 1) * 100:.0f}%")
        
        # Check character consistency
        if original.character_id != enriched.character_id:
            issues.append("Character ID changed")
        
        return {
            "is_valid": len(issues) == 0,
            "issues": issues,
            "length_ratio": length_ratio,
        }


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    "QualityThreshold",
    "EnrichedBeatResult",
    "ENRICHMENT_TECHNIQUES",
    "EmotionalBeatEnricher",
]
