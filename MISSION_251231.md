# 🌟 Storytelling System: Narrative Intelligence Integration (2025-12-31)

**Reference**: See main unified mission at `/workspace/langgraph/MISSION_251231.md`

## Your Role in the Stack

The Storytelling System is the **narrative generation engine** that produces the raw stories. Your job is to make it narrative-intelligent: aware of NCP structures, responsive to analytical feedback, and open to agent enrichment.

## Current Status

✅ **Strengths**:
- Story generation graph complete and functional
- RAG integration with knowledge base retrieval
- Session management with checkpoints
- Multiple LLM providers supported
- Indigenous-inspired prompts with rich narrative context
- COAIA fusion for ceremonial integration
- 55KB of sophisticated narrative prompts

❌ **Gaps**:
- Doesn't understand NCP structure (generates freestyle)
- No emotional beat analysis of generated content
- No feedback loop from analysis back to generation
- No character arc tracking across beats
- Agentic enrichment not integrated
- Story checkpointing not connected to narrative state persistence

## Integration Tasks for This Codebase

### **Phase 1-3: Unified Graph Integration** (Your Primary Responsibility)

#### Task 1: NCP-Aware Story Generation
**File**: `storytelling/narrative_intelligence_integration.py` (NEW)

```python
"""
Enhance story generation to be NCP-aware from the start.

Current: Generate beats, hope they're coherent
New: Generate beats with NCP structure, track state, enable analysis

Key insight: Instead of generating raw text, generate:
- StoryBeat objects with metadata
- Character perspective tracking
- Theme thread references
- Emotional tone expectations

This makes analysis and enrichment possible.
"""

from narrative_intelligence import StoryBeat, NCPState, Player, Perspective

class NCPAwareStoryGenerator:
    def __init__(self, llm_provider, graph_executor):
        self.llm = llm_provider
        self.graph = graph_executor
        self.ncp_state = NCPState()
    
    def generate_beat_with_ncp(self, 
        context: str,
        character_state: Player,
        thematic_focus: str,
        emotional_target: str
    ) -> StoryBeat:
        """
        Generate story beat with full NCP context:
        
        1. Pass character state, theme, emotion target to LLM
        2. LLM generates dialogue/action
        3. Parse as structured StoryBeat (not just text)
        4. Track in NCPState for continuity
        5. Return beat ready for analysis
        """
        # Construct context-aware prompt
        prompt = self._build_ncp_prompt(
            context=context,
            character=character_state,
            theme=thematic_focus,
            emotion=emotional_target
        )
        
        # Generate with LLM
        response = self.llm.generate(prompt)
        
        # Parse into StoryBeat structure
        beat = self._parse_beat(response, character_state)
        
        # Update NCP state
        self.ncp_state.add_beat(beat)
        
        return beat
    
    def _build_ncp_prompt(self, context, character, theme, emotion):
        """
        Example prompt that respects narrative structure:
        
        "You are writing for [PERSPECTIVE] of [CHARACTER].
        
        Character state:
        - Arc: [CHARACTER_ARC_SO_FAR]
        - Emotional state: [CURRENT_EMOTION]
        - Goals: [CHARACTER_GOALS]
        
        Narrative moment:
        - Phase: [SETUP/CRISIS/RESOLUTION]
        - Theme focus: [THEME]
        - Emotional beat needed: [EMOTION_TARGET]
        - Dramatic tension: [TENSION_LEVEL]
        
        Context: [STORY_CONTEXT]
        
        Write dialogue and action that:
        1. Advances [CHARACTER]'s arc from [STATE_A] toward [STATE_B]
        2. Explores the theme of [THEME]
        3. Creates [EMOTION_TARGET] tone
        4. Is consistent with what came before
        
        Response format:
        <beat>
        <dialogue>...</dialogue>
        <action>...</action>
        <emotional_tone>[tone]</emotional_tone>
        <theme_resonance>[how it connects to theme]</theme_resonance>
        </beat>"
        """
        pass
    
    def _parse_beat(self, response: str, character: Player) -> StoryBeat:
        """Parse LLM response into StoryBeat structure"""
        pass
```

#### Task 2: Emotional Beat Analysis & Feedback Loop
**File**: `storytelling/emotional_beat_enricher.py` (NEW)

```python
"""
Analyze generated beats for emotional quality and feed back to generation.

Pipeline:
1. Beat generated → Send to Emotional Classifier
2. Classifier returns: emotion_detected, confidence, quality_score
3. If quality_score < threshold: Route to enrichment
4. Enrichment: "Please strengthen the emotional resonance of this beat"
5. Result: Regenerated beat with better emotional impact
6. Repeat until quality threshold met
"""

from narrative_intelligence import EmotionalBeatClassifierNode, StoryBeat

class EmotionalBeatEnricher:
    def __init__(self, classifier_node: EmotionalBeatClassifierNode, llm_provider):
        self.classifier = classifier_node
        self.llm = llm_provider
    
    async def analyze_and_enrich(self, beat: StoryBeat, max_iterations: int = 3) -> StoryBeat:
        """
        Analyze beat emotionally, enrich if needed.
        
        Returns:
        - Same beat if quality sufficient
        - Enriched beat if quality improved
        """
        current_beat = beat
        
        for iteration in range(max_iterations):
            # Analyze emotional quality
            analysis = await self.classifier.classify(current_beat)
            
            emotion_quality = analysis.confidence  # 0-1 score
            
            if emotion_quality >= 0.75:
                # Good enough
                return current_beat
            
            # Quality too low, enrich
            enrichment_prompt = self._build_enrichment_prompt(
                beat=current_beat,
                analysis=analysis,
                iteration=iteration
            )
            
            enriched_text = await self.llm.generate(enrichment_prompt)
            current_beat = self._update_beat_content(current_beat, enriched_text)
        
        return current_beat
    
    def _build_enrichment_prompt(self, beat: StoryBeat, analysis, iteration: int) -> str:
        """
        Prompt to strengthen emotional resonance.
        
        Example:
        "The beat you wrote was detected as having emotion: [EMOTION]
        with confidence: [CONFIDENCE].
        
        But it could be stronger. The current emotional quality score is [SCORE].
        
        To improve:
        - Make the stakes clearer
        - Strengthen the sensory details
        - Make the internal conflict more visible
        - Add more specificity to dialogue
        
        Rewrite this beat to have stronger emotional resonance:
        [BEAT_TEXT]"
        """
        pass
    
    def _update_beat_content(self, beat: StoryBeat, enriched_text: str) -> StoryBeat:
        """Update beat with enriched content"""
        pass
```

#### Task 3: Character Arc Continuity Tracking
**File**: `storytelling/character_arc_tracker.py` (NEW)

```python
"""
Track character development across generated beats.

Current: Each beat generated independently
New: Each beat aware of character's arc so far

This prevents:
- Character behaving inconsistently
- Arc regressing suddenly  
- Growth not being cumulative
- Personality contradictions
"""

from narrative_intelligence import Player, CharacterArcState

class CharacterArcTracker:
    def __init__(self):
        self.character_states: Dict[str, CharacterArcState] = {}
    
    def initialize_character(self, character: Player):
        """Set up tracking for a character"""
        self.character_states[character.id] = CharacterArcState(
            player=character,
            initial_state=character.initial_state,
            arc_points=[]
        )
    
    def record_beat_impact(self, beat: StoryBeat, character: Player):
        """
        After beat generated, analyze its impact on character arc.
        
        Extract from beat:
        - What does character learn/realize?
        - How does this change their perspective?
        - What new capability/emotional state emerged?
        - Does this move toward or away from their goal?
        """
        arc_state = self.character_states[character.id]
        
        # Analyze beat for character impact
        impact = self._analyze_impact(beat, character, arc_state)
        
        # Record in arc
        arc_state.arc_points.append(impact)
    
    def get_character_arc_context(self, character: Player) -> str:
        """
        Generate context for next beat generation.
        
        Returns: "Here's what [CHARACTER] has experienced so far:
        - Started as: [INITIAL_STATE]
        - Learned: [LESSONS]
        - Grew from: [STATE_A] → [STATE_B]
        - Current emotional state: [EMOTION]
        - Unresolved goals: [GOALS]"
        """
        arc_state = self.character_states[character.id]
        return self._format_arc_summary(arc_state)
    
    def check_arc_consistency(self, beat: StoryBeat, character: Player) -> ConsistencyReport:
        """
        Before finalizing beat, check if it's consistent with character arc.
        
        Returns:
        - Is character behaving consistently?
        - Does beat advance arc or contradict it?
        - Are dialogue/actions aligned with growth so far?
        - Suggestions for corrections if inconsistent
        """
        arc_state = self.character_states[character.id]
        return self._validate_consistency(beat, arc_state)
    
    def _analyze_impact(self, beat: StoryBeat, character: Player, arc_state: CharacterArcState) -> ArcPoint:
        """Extract narrative impact on character"""
        pass
    
    def _format_arc_summary(self, arc_state: CharacterArcState) -> str:
        """Format arc history as context"""
        pass
    
    def _validate_consistency(self, beat: StoryBeat, arc_state: CharacterArcState) -> ConsistencyReport:
        """Check beat against arc"""
        pass
```

#### Task 4: Analytical Feedback Integration
**File**: `storytelling/analytical_feedback_loop.py` (NEW)

```python
"""
Close the loop: Analysis insights drive story improvements.

Flow:
1. Beat generated
2. Beat analyzed (emotional quality, character arc impact, theme resonance)
3. Gaps identified ("emotional beat weak", "character inconsistent", "theme unclear")
4. For each gap: Route to appropriate agent flow
5. Agent returns enrichment
6. Beat updated with enrichment
7. Story continues from enriched beat

This is the core of the narrative intelligence loop.
"""

from narrative_intelligence import NCPState, CharacterArcState, ThematicAnalysisState
from agentic_flywheel import NarrativeFlowRouter, NarrativeIntentClassifier

class AnalyticalFeedbackLoop:
    def __init__(self, 
        character_arc_analyzer,
        thematic_analyzer,
        emotional_classifier,
        flow_router: NarrativeFlowRouter,
        llm_provider
    ):
        self.character_arc_analyzer = character_arc_analyzer
        self.thematic_analyzer = thematic_analyzer
        self.emotional_classifier = emotional_classifier
        self.flow_router = flow_router
        self.llm = llm_provider
    
    async def process_beat_with_analysis(self, 
        beat: StoryBeat,
        ncp_state: NCPState
    ) -> EnrichedBeat:
        """
        Complete analysis → gap identification → enrichment loop.
        
        Returns: Enriched beat ready for next generation phase
        """
        
        # STEP 1: Analyze beat from multiple angles
        character_analysis = await self.character_arc_analyzer.analyze_impact(beat, ncp_state)
        thematic_analysis = await self.thematic_analyzer.analyze_resonance(beat, ncp_state)
        emotional_analysis = await self.emotional_classifier.classify(beat)
        
        # STEP 2: Identify gaps (where does beat need improvement?)
        gaps = self._identify_gaps(
            character_analysis,
            thematic_analysis, 
            emotional_analysis
        )
        
        if not gaps:
            # Beat is high quality, no enrichment needed
            return EnrichedBeat(beat=beat, enrichments=[], analyses=[
                character_analysis, thematic_analysis, emotional_analysis
            ])
        
        # STEP 3: Route gaps to appropriate flows
        enriched_beat = beat
        
        for gap in gaps:
            # Get appropriate flow(s) for this gap
            flows = self.flow_router.select_flows(
                narrative_state=ncp_state,
                gap_analysis=gap
            )
            
            # Execute each flow
            for flow in flows:
                enrichment = await self._execute_enrichment_flow(
                    beat=enriched_beat,
                    flow=flow,
                    gap=gap
                )
                
                # Update beat with enrichment
                enriched_beat = self._apply_enrichment(enriched_beat, enrichment)
        
        return EnrichedBeat(
            beat=enriched_beat,
            enrichments=[enrichment],
            analyses=[character_analysis, thematic_analysis, emotional_analysis]
        )
    
    def _identify_gaps(self, character_analysis, thematic_analysis, emotional_analysis) -> List[Gap]:
        """
        From analysis results, identify what needs improvement.
        
        Examples:
        - Gap: "character_motivation_unclear" 
          Identified by: Character arc score < 0.6
          
        - Gap: "emotional_beat_weak"
          Identified by: Emotional quality < 0.5
          
        - Gap: "theme_not_resonant"
          Identified by: Theme score < 0.7
        """
        pass
    
    async def _execute_enrichment_flow(self, beat: StoryBeat, flow: FlowRoute, gap: Gap) -> Enrichment:
        """
        Execute Flowise flow to address a specific gap.
        
        Example:
        Gap: emotional_beat_weak
        Flow: sentiment_enhancer
        Input: beat + context + emotional target
        Output: Enriched dialogue/action with stronger emotion
        """
        pass
    
    def _apply_enrichment(self, beat: StoryBeat, enrichment: Enrichment) -> StoryBeat:
        """Update beat with enrichment while preserving narrative continuity"""
        pass

class Gap:
    gap_type: str  # "character_arc", "emotional_quality", "theme_resonance", etc
    score: float  # 0-1, where low = needs improvement
    suggested_flows: List[str]
    context: dict

class EnrichedBeat:
    beat: StoryBeat
    enrichments: List[Enrichment]
    analyses: List[AnalysisResult]
```

#### Task 5: Enhanced Story Generation Graph
**File**: `storytelling/narrative_aware_story_graph.py` (NEW)

```python
"""
New story graph that integrates all components:
- NCP-aware generation
- Emotional analysis & enrichment
- Character arc tracking
- Analytical feedback loop
- Langfuse instrumentation

This is the unified orchestration for story creation.
"""

from langgraph.graph import StateGraph
from narrative_intelligence import NCPState, StoryBeat

class NarrativeAwareStoryGraph:
    def __init__(self, config):
        self.graph = StateGraph(NCPState)
        
        # Initialize all components
        self.ncp_generator = NCPAwareStoryGenerator(config.llm, self)
        self.beat_enricher = EmotionalBeatEnricher(config.classifier, config.llm)
        self.arc_tracker = CharacterArcTracker()
        self.feedback_loop = AnalyticalFeedbackLoop(...)
        self.tracer = NarrativeTracingHandler()
    
    def _build_graph(self):
        """
        Graph flow:
        
        setup_story → 
        [
            generate_beat → 
            analyze_and_enrich_beat → 
            track_character_impact → 
            [
                for each character/theme: update arc/theme state
            ] →
            should_continue?
        ] (loop) →
        finalize_story
        """
        
        self.graph.add_node("setup_story", self.setup_story_node)
        self.graph.add_node("generate_beat", self.generate_beat_node)
        self.graph.add_node("analyze_beat", self.analyze_beat_node)
        self.graph.add_node("track_character", self.track_character_node)
        self.graph.add_node("finalize_story", self.finalize_story_node)
        
        self.graph.set_entry_point("setup_story")
        
        self.graph.add_edge("setup_story", "generate_beat")
        self.graph.add_edge("generate_beat", "analyze_beat")
        self.graph.add_edge("analyze_beat", "track_character")
        
        self.graph.add_conditional_edges(
            "track_character",
            self.should_continue_story,
            {
                "continue": "generate_beat",
                "finish": "finalize_story"
            }
        )
    
    async def setup_story_node(self, state: NCPState) -> NCPState:
        """Initialize story with NCP structure"""
        with self.tracer.create_story_generation_root_trace(state.story_id) as root_span:
            # Load NCP schema for this story
            # Initialize characters, themes, perspectives
            # Set up knowledge base context
            return state
    
    async def generate_beat_node(self, state: NCPState) -> NCPState:
        """Generate next story beat with NCP awareness"""
        current_character = state.get_current_perspective().player
        emotional_target = state.determine_emotional_beat_needed()
        thematic_focus = state.get_active_theme()
        
        beat = await self.ncp_generator.generate_beat_with_ncp(
            context=state.build_context_prompt(),
            character_state=current_character,
            thematic_focus=thematic_focus,
            emotional_target=emotional_target
        )
        
        state.add_beat(beat)
        return state
    
    async def analyze_beat_node(self, state: NCPState) -> NCPState:
        """Analyze beat and enrich if needed"""
        beat = state.get_last_beat()
        
        enriched_beat = await self.feedback_loop.process_beat_with_analysis(
            beat=beat,
            ncp_state=state
        )
        
        state.update_last_beat(enriched_beat)
        return state
    
    async def track_character_node(self, state: NCPState) -> NCPState:
        """Update character arc based on beat"""
        beat = state.get_last_beat()
        character = state.get_current_perspective().player
        
        self.arc_tracker.record_beat_impact(beat, character)
        
        return state
    
    def should_continue_story(self, state: NCPState) -> str:
        """Determine if story should continue"""
        # Check: have we reached resolution?
        # Check: character arcs complete?
        # Check: themes resolved?
        if state.should_conclude():
            return "finish"
        return "continue"
    
    async def finalize_story_node(self, state: NCPState) -> NCPState:
        """Complete story with final analysis"""
        # Extract final metrics
        metrics = state.calculate_final_metrics()
        
        # Close Langfuse trace with metrics
        self.tracer.finalize_story_trace(
            trace_id=state.trace_id,
            story=state.get_full_story(),
            metrics=metrics
        )
        
        return state
```

## Implementation Sequence

### **Step 1: Foundation** (Phase 1)
- [ ] Create `narrative_intelligence_integration.py`
  - [ ] NCPAwareStoryGenerator class
  - [ ] NCP prompt building
  - [ ] Beat parsing and structuring

- [ ] Create `character_arc_tracker.py`
  - [ ] Character state initialization
  - [ ] Impact analysis
  - [ ] Arc context generation
  - [ ] Consistency checking

### **Step 2: Quality & Analysis** (Phase 2)
- [ ] Create `emotional_beat_enricher.py`
  - [ ] Integration with classifier node
  - [ ] Enrichment prompt building
  - [ ] Iterative quality improvement

- [ ] Create `analytical_feedback_loop.py`
  - [ ] Gap identification logic
  - [ ] Flow routing
  - [ ] Enrichment application

### **Step 3: Orchestration** (Phase 3)
- [ ] Create `narrative_aware_story_graph.py`
  - [ ] Graph structure with nodes
  - [ ] State transitions
  - [ ] Conditional routing

### **Step 4: Integration** (Phase 3)
- [ ] Integrate with Langfuse tracing
- [ ] Test end-to-end generation → analysis → enrichment
- [ ] Document usage and examples

## Key Integration Points

1. **From Narrative Intelligence Toolkit**:
   - Import NCP data models
   - Use CharacterArcGenerator for analysis
   - Use EmotionalBeatClassifier for quality assessment
   - Use ThematicTensionAnalyzer for theme tracking

2. **From Agentic Flywheel**:
   - Send beat analysis to flow router
   - Receive enriched beats back
   - Integrate routing decisions into story flow

3. **To Langfuse**:
   - Trace each beat generation
   - Log analysis results
   - Log enrichment flows
   - Store final metrics

## Testing Strategy

```python
# Test 1: Single beat generation
beat = await generator.generate_beat_with_ncp(...)
assert beat.character == expected_character
assert beat.emotional_tone == expected_emotion

# Test 2: Emotional enrichment
enriched = await enricher.analyze_and_enrich(beat)
assert enriched.emotional_quality > 0.75

# Test 3: Character consistency
assert tracker.check_arc_consistency(beat, character).is_consistent

# Test 4: Full story generation
story_state = await graph.invoke(initial_state)
assert len(story_state.beats) > 0
assert story_state.metrics.coherence > 0.8

# Test 5: Trace completeness
traces = langfuse_client.get_traces(story_id)
assert traces.beat_count == story_state.beat_count
assert traces.enrichment_flows_used > 0
```

## Success Criteria

- [ ] Stories generated with NCP-aware structure
- [ ] Character arcs persistent and consistent across beats
- [ ] Emotional beats automatically improved when quality is low
- [ ] Analytical gaps drive agent flow selection
- [ ] End-to-end story: generation → analysis → enrichment → next beat
- [ ] Full trace in Langfuse showing decision tree
- [ ] Quality metrics improve with agentic enrichment

## Remember

> The storytelling system isn't just generating text anymore—it's orchestrating a complex dance of generation, analysis, and intelligent enhancement. Each beat gets smarter because the system learns from what works.

---

**Last Updated**: 2025-12-31
**Your Focus**: Making story generation narrative-intelligent and feedback-aware
**Success Metric**: Generated stories improve in coherence and emotional resonance through analytical feedback loop
