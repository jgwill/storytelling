"""
Narrative Tracing Adapter for Storytelling Package

Bridges storytelling operations to the narrative-tracing library from LangChain fork.
Provides Langfuse integration for observability of story generation.

Implements specifications from:
- rispecs/Logging_And_Traceability_Specification.md Section 5
- narrative-tracing.langchain.rispec.md
"""

from __future__ import annotations

import logging
import os
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from functools import wraps
from typing import Any, Callable, Dict, Generator, List, Optional, TypeVar

logger = logging.getLogger(__name__)

# ============================================================================
# Graceful import of narrative-tracing from LangChain fork
# ============================================================================

try:
    from narrative_tracing import (
        NarrativeTracingHandler,
        NarrativeEventType,
        NarrativeSpan,
        BEAT_GENERATED,
        BEAT_ENRICHED,
        CHARACTER_ARC_UPDATED,
        STORY_GENERATED,
        SESSION_STARTED,
        SESSION_ENDED,
    )
    from narrative_tracing.adapters.storytelling_hooks import (
        StorytellingHooks,
        BeatTracer,
    )
    HAS_NARRATIVE_TRACING = True
except ImportError:
    HAS_NARRATIVE_TRACING = False
    NarrativeTracingHandler = None
    StorytellingHooks = None
    BeatTracer = None


# ============================================================================
# Event Types for Storytelling
# ============================================================================

STORYTELLING_EVENT_TYPES = {
    # Beat lifecycle
    "BEAT_GENERATED": "storytelling.beat.generated",
    "BEAT_ANALYZED": "storytelling.beat.analyzed",
    "BEAT_ENRICHED": "storytelling.beat.enriched",
    
    # Character events
    "CHARACTER_ARC_INITIALIZED": "storytelling.character.initialized",
    "CHARACTER_ARC_UPDATED": "storytelling.character.arc_updated",
    "CHARACTER_CONSISTENCY_CHECK": "storytelling.character.consistency",
    
    # Emotional analysis
    "EMOTIONAL_QUALITY_ASSESSED": "storytelling.emotion.assessed",
    "EMOTIONAL_ENRICHMENT_APPLIED": "storytelling.emotion.enriched",
    
    # Gap analysis
    "GAP_IDENTIFIED": "storytelling.gap.identified",
    "GAP_REMEDIATION_STARTED": "storytelling.gap.remediation_started",
    "GAP_REMEDIATION_COMPLETED": "storytelling.gap.remediation_completed",
    
    # Graph execution
    "GRAPH_NODE_STARTED": "storytelling.graph.node_started",
    "GRAPH_NODE_COMPLETED": "storytelling.graph.node_completed",
    "GRAPH_EXECUTION_STARTED": "storytelling.graph.started",
    "GRAPH_EXECUTION_COMPLETED": "storytelling.graph.completed",
    
    # Story lifecycle
    "STORY_GENERATION_STARTED": "storytelling.story.started",
    "STORY_GENERATION_COMPLETED": "storytelling.story.completed",
    "STORY_CHECKPOINT_SAVED": "storytelling.story.checkpoint",
}


# ============================================================================
# Trace Context
# ============================================================================

@dataclass
class TraceContext:
    """Context for a storytelling trace session."""
    
    trace_id: str
    session_id: str
    story_id: Optional[str] = None
    ceremony_uuid: Optional[str] = None
    
    # Metrics
    beats_generated: int = 0
    beats_enriched: int = 0
    gaps_identified: int = 0
    gaps_resolved: int = 0
    
    # Timing
    start_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging."""
        return {
            "trace_id": self.trace_id,
            "session_id": self.session_id,
            "story_id": self.story_id,
            "ceremony_uuid": self.ceremony_uuid,
            "beats_generated": self.beats_generated,
            "beats_enriched": self.beats_enriched,
            "gaps_identified": self.gaps_identified,
            "gaps_resolved": self.gaps_resolved,
            "duration_seconds": (datetime.now(timezone.utc) - self.start_time).total_seconds(),
        }


# ============================================================================
# Storytelling Tracer
# ============================================================================

class StorytellingTracer:
    """
    Narrative tracing for storytelling operations.
    
    Provides decorators and context managers for instrumenting:
    - Beat generation
    - Emotional analysis and enrichment
    - Character arc tracking
    - Gap identification and remediation
    - Graph execution
    
    Example:
        tracer = StorytellingTracer(session_id="story-001")
        
        with tracer.trace_beat_generation("beat_1") as span:
            beat = generator.generate(...)
            span.set_attribute("emotional_tone", beat.emotional_tone)
        
        # Or use decorator
        @tracer.trace_method("generate_beat")
        async def generate_beat(self, context):
            ...
    """
    
    def __init__(
        self,
        session_id: str,
        story_id: Optional[str] = None,
        ceremony_uuid: Optional[str] = None,
        public_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        host: Optional[str] = None,
    ) -> None:
        """
        Initialize storytelling tracer.
        
        Args:
            session_id: Unique session identifier.
            story_id: Optional story identifier for grouping.
            ceremony_uuid: Optional ceremony UUID for cross-system correlation.
            public_key: Langfuse public key (or from LANGFUSE_PUBLIC_KEY env).
            secret_key: Langfuse secret key (or from LANGFUSE_SECRET_KEY env).
            host: Langfuse host URL (or from LANGFUSE_HOST env).
        """
        self.session_id = session_id
        self.story_id = story_id
        self.ceremony_uuid = ceremony_uuid
        
        # Get credentials from env if not provided
        self.public_key = public_key or os.environ.get("LANGFUSE_PUBLIC_KEY")
        self.secret_key = secret_key or os.environ.get("LANGFUSE_SECRET_KEY")
        self.host = host or os.environ.get("LANGFUSE_HOST")
        
        # Initialize handler if available
        self._handler: Optional[NarrativeTracingHandler] = None
        self._hooks: Optional[StorytellingHooks] = None
        self._context: Optional[TraceContext] = None
        
        if HAS_NARRATIVE_TRACING and self.public_key and self.secret_key:
            try:
                self._handler = NarrativeTracingHandler(
                    session_id=session_id,
                    story_id=story_id,
                    public_key=self.public_key,
                    secret_key=self.secret_key,
                    host=self.host,
                )
                self._hooks = StorytellingHooks(self._handler)
                logger.info(f"Langfuse tracing enabled for session {session_id}")
            except Exception as e:
                logger.warning(f"Failed to initialize Langfuse: {e}")
                self._handler = None
        else:
            if not HAS_NARRATIVE_TRACING:
                logger.debug("narrative-tracing not available, using local logging")
            else:
                logger.debug("Langfuse credentials not provided, using local logging")
    
    @property
    def is_enabled(self) -> bool:
        """Check if tracing is enabled."""
        return self._handler is not None
    
    @property
    def context(self) -> Optional[TraceContext]:
        """Get current trace context."""
        return self._context
    
    # ========================================================================
    # Context Managers
    # ========================================================================
    
    @contextmanager
    def trace_story_generation(
        self,
        story_id: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Generator[TraceContext, None, None]:
        """
        Context manager for tracing entire story generation.
        
        Args:
            story_id: Story identifier.
            metadata: Optional metadata to attach.
            
        Yields:
            TraceContext for the generation session.
        """
        import uuid
        
        trace_id = str(uuid.uuid4())
        self._context = TraceContext(
            trace_id=trace_id,
            session_id=self.session_id,
            story_id=story_id,
            ceremony_uuid=self.ceremony_uuid,
        )
        
        self._log_event(
            STORYTELLING_EVENT_TYPES["STORY_GENERATION_STARTED"],
            {
                "story_id": story_id,
                "trace_id": trace_id,
                **(metadata or {}),
            },
        )
        
        try:
            yield self._context
        finally:
            self._log_event(
                STORYTELLING_EVENT_TYPES["STORY_GENERATION_COMPLETED"],
                self._context.to_dict(),
            )
            self._context = None
    
    @contextmanager
    def trace_beat_generation(
        self,
        beat_id: str,
        character_id: Optional[str] = None,
        phase: Optional[str] = None,
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Context manager for tracing beat generation.
        
        Args:
            beat_id: Beat identifier.
            character_id: Optional character perspective.
            phase: Optional dramatic phase.
            
        Yields:
            Dictionary to collect beat attributes.
        """
        span_data: Dict[str, Any] = {
            "beat_id": beat_id,
            "character_id": character_id,
            "phase": phase,
        }
        
        self._log_event(
            STORYTELLING_EVENT_TYPES["GRAPH_NODE_STARTED"],
            {"node": "beat_generation", "beat_id": beat_id},
        )
        
        try:
            yield span_data
        finally:
            if self._context:
                self._context.beats_generated += 1
            
            self._log_event(
                STORYTELLING_EVENT_TYPES["BEAT_GENERATED"],
                span_data,
            )
    
    @contextmanager
    def trace_emotional_analysis(
        self,
        beat_id: str,
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Context manager for tracing emotional analysis.
        
        Args:
            beat_id: Beat being analyzed.
            
        Yields:
            Dictionary to collect analysis results.
        """
        analysis_data: Dict[str, Any] = {"beat_id": beat_id}
        
        try:
            yield analysis_data
        finally:
            self._log_event(
                STORYTELLING_EVENT_TYPES["EMOTIONAL_QUALITY_ASSESSED"],
                analysis_data,
            )
    
    @contextmanager
    def trace_enrichment(
        self,
        beat_id: str,
        gap_type: Optional[str] = None,
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Context manager for tracing beat enrichment.
        
        Args:
            beat_id: Beat being enriched.
            gap_type: Type of gap being addressed.
            
        Yields:
            Dictionary to collect enrichment data.
        """
        enrichment_data: Dict[str, Any] = {
            "beat_id": beat_id,
            "gap_type": gap_type,
        }
        
        try:
            yield enrichment_data
        finally:
            if self._context:
                self._context.beats_enriched += 1
            
            self._log_event(
                STORYTELLING_EVENT_TYPES["BEAT_ENRICHED"],
                enrichment_data,
            )
    
    # ========================================================================
    # Decorators
    # ========================================================================
    
    F = TypeVar("F", bound=Callable[..., Any])
    
    def trace_method(self, name: str) -> Callable[[F], F]:
        """
        Decorator for tracing a method.
        
        Args:
            name: Span name for the method.
            
        Returns:
            Decorated function.
        """
        def decorator(func: F) -> F:
            @wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                self._log_event(
                    STORYTELLING_EVENT_TYPES["GRAPH_NODE_STARTED"],
                    {"node": name},
                )
                try:
                    result = await func(*args, **kwargs)
                    self._log_event(
                        STORYTELLING_EVENT_TYPES["GRAPH_NODE_COMPLETED"],
                        {"node": name, "success": True},
                    )
                    return result
                except Exception as e:
                    self._log_event(
                        STORYTELLING_EVENT_TYPES["GRAPH_NODE_COMPLETED"],
                        {"node": name, "success": False, "error": str(e)},
                    )
                    raise
            
            @wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                self._log_event(
                    STORYTELLING_EVENT_TYPES["GRAPH_NODE_STARTED"],
                    {"node": name},
                )
                try:
                    result = func(*args, **kwargs)
                    self._log_event(
                        STORYTELLING_EVENT_TYPES["GRAPH_NODE_COMPLETED"],
                        {"node": name, "success": True},
                    )
                    return result
                except Exception as e:
                    self._log_event(
                        STORYTELLING_EVENT_TYPES["GRAPH_NODE_COMPLETED"],
                        {"node": name, "success": False, "error": str(e)},
                    )
                    raise
            
            import asyncio
            if asyncio.iscoroutinefunction(func):
                return async_wrapper  # type: ignore
            return sync_wrapper  # type: ignore
        
        return decorator
    
    # ========================================================================
    # Direct Logging Methods
    # ========================================================================
    
    def log_beat_generated(
        self,
        beat_id: str,
        emotional_tone: str,
        character_id: Optional[str] = None,
        phase: Optional[str] = None,
        quality_score: Optional[float] = None,
    ) -> None:
        """Log beat generation event."""
        self._log_event(
            STORYTELLING_EVENT_TYPES["BEAT_GENERATED"],
            {
                "beat_id": beat_id,
                "emotional_tone": emotional_tone,
                "character_id": character_id,
                "phase": phase,
                "quality_score": quality_score,
            },
        )
        if self._context:
            self._context.beats_generated += 1
    
    def log_gap_identified(
        self,
        gap_type: str,
        beat_id: str,
        severity: str,
        score: float,
    ) -> None:
        """Log gap identification event."""
        self._log_event(
            STORYTELLING_EVENT_TYPES["GAP_IDENTIFIED"],
            {
                "gap_type": gap_type,
                "beat_id": beat_id,
                "severity": severity,
                "score": score,
            },
        )
        if self._context:
            self._context.gaps_identified += 1
    
    def log_gap_resolved(
        self,
        gap_type: str,
        beat_id: str,
        flow_used: str,
        improvement: float,
    ) -> None:
        """Log gap resolution event."""
        self._log_event(
            STORYTELLING_EVENT_TYPES["GAP_REMEDIATION_COMPLETED"],
            {
                "gap_type": gap_type,
                "beat_id": beat_id,
                "flow_used": flow_used,
                "improvement": improvement,
            },
        )
        if self._context:
            self._context.gaps_resolved += 1
    
    def log_character_arc_updated(
        self,
        character_id: str,
        beat_id: str,
        arc_progress: float,
        new_state: str,
    ) -> None:
        """Log character arc update event."""
        self._log_event(
            STORYTELLING_EVENT_TYPES["CHARACTER_ARC_UPDATED"],
            {
                "character_id": character_id,
                "beat_id": beat_id,
                "arc_progress": arc_progress,
                "new_state": new_state,
            },
        )
    
    def log_checkpoint(
        self,
        checkpoint_id: str,
        node_name: str,
        state_keys: List[str],
    ) -> None:
        """Log checkpoint save event."""
        self._log_event(
            STORYTELLING_EVENT_TYPES["STORY_CHECKPOINT_SAVED"],
            {
                "checkpoint_id": checkpoint_id,
                "node_name": node_name,
                "state_keys": state_keys,
            },
        )
    
    # ========================================================================
    # Internal Methods
    # ========================================================================
    
    def _log_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """
        Log an event to the tracing backend.
        
        Args:
            event_type: Type of event.
            data: Event data.
        """
        # Add context if available
        if self._context:
            data["trace_id"] = self._context.trace_id
            data["session_id"] = self._context.session_id
            if self._context.story_id:
                data["story_id"] = self._context.story_id
        
        # Log to Langfuse if available
        if self._handler:
            try:
                self._handler.log_event(event_type, data)
            except Exception as e:
                logger.warning(f"Failed to log to Langfuse: {e}")
        
        # Always log locally
        logger.debug(f"[TRACE] {event_type}: {data}")
    
    def flush(self) -> None:
        """Flush any pending traces to the backend."""
        if self._handler:
            try:
                self._handler.flush()
            except Exception as e:
                logger.warning(f"Failed to flush traces: {e}")


# ============================================================================
# Global Tracer Instance
# ============================================================================

_global_tracer: Optional[StorytellingTracer] = None


def get_tracer(
    session_id: Optional[str] = None,
    **kwargs: Any,
) -> StorytellingTracer:
    """
    Get or create the global storytelling tracer.
    
    Args:
        session_id: Session ID for new tracer.
        **kwargs: Additional arguments for StorytellingTracer.
        
    Returns:
        StorytellingTracer instance.
    """
    global _global_tracer
    
    if _global_tracer is None or session_id:
        import uuid
        _global_tracer = StorytellingTracer(
            session_id=session_id or str(uuid.uuid4()),
            **kwargs,
        )
    
    return _global_tracer


def reset_tracer() -> None:
    """Reset the global tracer."""
    global _global_tracer
    if _global_tracer:
        _global_tracer.flush()
    _global_tracer = None
