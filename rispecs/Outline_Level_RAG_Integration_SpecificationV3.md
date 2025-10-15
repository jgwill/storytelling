# Outline-Level RAG Integration Specification

**Status**: Under Revision (Integrating Unified Creative Orientation Framework)  
**Date**: 2025-08-25  
**Version**: 1.1  
**Dependencies**: RAG_Implementation_Specification.md, ApplicationLogic.md, Unified_Creative_Orientation_Framework.md

------
RESERVATION on IMPLEMENTATION by Claude
------
  🎭 Gemini's Enhancement: Creative Orientation Integration

  Strengths:
  - Sophisticated Framework Integration: Transforms basic RAG into "Event-Driven Adaptive RAG" with bidirectional
  feedback and dynamic adaptation
  - Creative Orientation Alignment: Integrates RISE principles (Advancing Patterns, Structural Tension Resolution) rather
   than just static knowledge retrieval
  - Advanced Contextual Intelligence: Introduces "Semantic Adaptation Layer" for contextual transposition, going beyond
  simple document retrieval to intelligent content adaptation

  Key Innovations:
  - Dynamic Query Construction: Queries adapt based on outline evolution, critic feedback, and LLM output analysis
  - RISE-Aware Prioritization: Documents tagged with creative orientation patterns get priority
  - Bidirectional Synchronization: Outline generation informs knowledge base evolution via coaia-memory

------







---

## 1. Overview

This specification defines the implementation of an **Event-Driven Adaptive RAG (Retrieval-Augmented Generation)** system at the outline generation stage. It extends the existing scene-level RAG to provide **dynamically knowledge-aware story foundation creation**, deeply integrated within the overarching **Unified Creative Orientation Framework**. This marks a significant shift from static context injection to a responsive, intelligent system that actively participates in the recursive creative process.

### 1.1 Current State
- ✅ **Scene-Level RAG**: Functional during chapter generation with context injection.
- ❌ **Outline-Level RAG (Static)**: Initial implementation for outline generation without dynamic adaptation.
- ✅ **Infrastructure**: Core RAG system (`src/willwrite/rag.py`) and Unified Creative Orientation Framework components (e.g., `coaia-memory`, `mcp-coaia-sequential-thinking`, `co-lint`) are ready for advanced integration.

### 1.2 Strategic Importance
Outline-level RAG is critical for ensuring that story foundations are not only grounded in established world-building but also **actively guided towards creative orientation and advancing patterns from the outset**. By integrating with the Unified Creative Orientation Framework, this system will:
*   Enable **recursive creative system design** by providing dynamically adapted knowledge.
*   Facilitate **bidirectional synchronization** where outline evolution informs and refines the knowledge retrieval process.
*   Foster **consistent and coherent narrative structures** that naturally incorporate knowledge base content, while mitigating reactive biases and promoting structural tension resolution.
*   Serve as a core component for `WillWrite` to function as a sophisticated "Creative Writing Assistant" within the Event-Driven Creative Orientation Ecosystem (EDCOE).

---

## 2. Architecture Design

### 2.1 Integration Points (Dynamic Adaptation & Feedback)

The Outline-Level RAG system integrates at key points within the `WillWrite` workflow, serving not just as injection points but as nodes for **dynamic adaptation and bidirectional feedback** within the recursive creative system.

#### 2.1.1 Initial Outline Generation
**Location**: `generate_initial_outline` workflow node  
**Trigger**: After prompt analysis, before initial outline creation  
**Purpose**: Inject relevant world-building context, dynamically adapted for foundational story structure, and establish initial structural tension.

#### 2.1.2 Outline Critique/Revision
**Location**: `critique_outline` and `revise_outline` workflow nodes  
**Trigger**: During outline quality assessment and revision cycles, and upon detection of oscillating patterns.  
**Purpose**: Provide dynamically re-adapted knowledge to guide revisions, ensure consistency with established knowledge, and actively steer the outline towards advancing patterns. This is a critical point for **bidirectional synchronization** with `coaia-memory`.

#### 2.1.3 Chapter Count Determination
**Location**: `determine_chapter_count` workflow node  
**Trigger**: When determining story scope based on outline.  
**Purpose**: Consider knowledge base complexity and structural tension dynamics in pacing decisions, ensuring the proposed chapter count aligns with the narrative's natural progression.

### 2.2 Retrieval Strategy (Event-Driven & Contextually Transposed)

The retrieval strategy is enhanced to be **event-driven and contextually aware**, leveraging insights from the Unified Conceptual Framework to provide intelligently adapted knowledge.

#### 2.2.1 Dynamic Query Construction
Queries are constructed not only from static sources but also dynamically, adapting to the evolving outline, LLM outputs, and critic feedback. This leverages advanced prompting strategies for optimal query formulation.

**Primary Query Sources**:
- User's initial story prompt (full text)
- Extracted entities (characters, locations, concepts)
- Genre and theme keywords
- Conflict and plot elements
- **Evolving Outline Content**: Sections of the outline currently being critiqued or revised.
- **Critic Feedback**: Specific points of feedback from the `critique_outline` node.
- **LLM Output Analysis**: Analysis of previous LLM generations to identify areas of ambiguity or inconsistency.

**Query Processing**:
```python
def construct_outline_queries(
    initial_prompt: str,
    story_elements: dict,
    current_outline_segment: Optional[str] = None, # New: for dynamic queries
    critic_feedback: Optional[str] = None,         # New: for dynamic queries
    llm_output_analysis: Optional[str] = None      # New: for dynamic queries
) -> List[str]:
    queries = []
    
    # Primary prompt-based query
    queries.append(initial_prompt)
    
    # Entity-specific queries
    if story_elements.get('characters'):
        queries.append(f"Characters: {', '.join(story_elements['characters'])}")
    
    if story_elements.get('setting'):
        queries.append(f"Setting and world: {story_elements['setting']}")
    
    # Theme and conflict queries
    if story_elements.get('theme'):
        queries.append(f"Themes: {story_elements['theme']}")
    
    # New: Dynamic queries based on current state and feedback
    if current_outline_segment:
        queries.append(f"Context for outline segment: {current_outline_segment}")
    if critic_feedback:
        queries.append(f"Knowledge to address critique: {critic_feedback}")
    if llm_output_analysis:
        queries.append(f"Refine based on LLM output analysis: {llm_output_analysis}")
        
    # Apply advanced prompting strategies (e.g., Goal-Oriented, Role-Based, Narrative-of-Thought)
    # to refine queries for optimal retrieval. (Conceptual, implemented in helper functions)
    
    return queries
```

#### 2.2.2 Dynamic Retrieval Parameters
Retrieval parameters are dynamically adjusted based on the context and the stage of outline generation/revision.

-   **Top-k Results**: 5-10 documents per query (configurable, dynamically adjustable based on query complexity).
-   **Context Token Limit**: 1,000-2,000 tokens maximum for outline stage (dynamically adjustable, potentially higher for initial generation, lower for focused critique).
-   **Semantic Filtering**: High-relevance threshold (0.7+ similarity), with dynamic adjustment based on the need for broader exploration vs. precise focus.
-   **Document Types**: Prioritize character sheets, world-building, magic systems, **and RISE-tagged documents (e.g., Advancing Pattern examples, Structural Tension resolution strategies)**.
-   **Re-retrieval Frequency**: Parameters for controlling how often RAG context is re-evaluated and updated during iterative revision cycles.
-   **Adaptation Thresholds**: Define criteria for triggering dynamic re-retrieval (e.g., significant change in outline segment, critical feedback received).

#### 2.2.3 Context Aggregation & Semantic Adaptation Layer (Contextual Transposition Intelligence)
Beyond simple deduplication and prioritization, a **Semantic Adaptation Layer** (part of "Contextual Transposition Intelligence") processes and semantically adapts retrieved content.

-   **Deduplication**: Remove overlapping content between retrieved documents.
-   **Prioritization**: Rank by relevance, recency, and **RISE-alignment (e.g., prioritizing Advancing Pattern examples)**.
-   **Semantic Adaptation**: Apply contextual transposition principles to transform raw retrieved content into a format that is semantically aligned and creatively relevant to the current outline context. This may involve:
    *   **Style Adaptation**: Adjusting the tone or style of retrieved information to match the desired narrative style.
    *   **Structural Pattern Extraction**: Identifying and highlighting underlying structural dynamics (e.g., cause-effect relationships, character arcs) within the retrieved content.
    *   **Concept Transposition**: Adapting abstract concepts from the knowledge base to concrete narrative elements relevant to the outline.
-   **Formatting**: Structure as labeled context blocks, potentially including metadata about the "structural dynamics" or "patterns" identified by the Semantic Adaptation Layer.

### 2.3 Context Injection Format (Transposed & RISE-Aware)

The injected context reflects the output of the "Contextual Transposition Intelligence," providing not just raw knowledge but semantically adapted and RISE-aware insights.

#### 2.3.1 RAG-Outline-Context Block
```
<RAG-OUTLINE-CONTEXT>
# Relevant World Knowledge (Contextually Transposed)

## Characters
[Semantically adapted character information, potentially highlighting character arcs or motivations relevant to current outline segment]

## World & Setting  
[Transposed world-building content, emphasizing structural elements or thematic relevance]

## Rules & Systems
[Adapted magic/technology/social systems, with focus on their impact on narrative progression or structural tension]

## Themes & Lore
[Semantically adapted thematic and background content, emphasizing Advancing Patterns or resolution of structural tension]

## Structural Insights (RISE-Aligned)
[Metadata or distilled insights from the Semantic Adaptation Layer, e.g., "This context suggests an Advancing Pattern for character development here."]
</RAG-OUTLINE-CONTEXT>
```

#### 2.3.2 Prompt Integration (Advanced Prompting Strategies)
The injection point remains between system instructions and user prompt, but the integration leverages advanced prompting strategies to maximize the LLM's utilization of the transposed and RISE-aware context.

**Injection Point**: Between system instructions and user prompt.  
**Labeling**: Clear separation with retrieval metadata and explicit labels for transposed content and structural insights.  
**Token Management**: Truncate if exceeding limits, prioritize by relevance and **RISE-alignment**.  
**Advanced Prompting**: Prompts will be designed using strategies like:
*   **Goal-Oriented Prompting**: Explicitly guiding the LLM on the desired outcome for integrating the RAG context.
*   **Role-Based Prompting**: Assigning the LLM a role (e.g., "expert world-builder," "narrative architect") that aligns with the type of context provided.
*   **Narrative-of-Thought (NoT)**: Encouraging the LLM to generate internal narratives or reasoning steps that incorporate the transposed context.
*   **MAPO Insights**: Prompts will be optimized based on insights from Model-Adaptive Prompt Optimization (MAPO) to ensure they are tailored to the specific LLM being used, maximizing the effectiveness of context utilization.

---

## 3. Implementation Specification

### 3.1 New Functions Required (Dynamic & Contextually Intelligent RAG)

To support the Event-Driven Adaptive RAG and Contextual Transposition Intelligence, several new or significantly modified functions will be required.

#### 3.1.1 Core Retrieval & Adaptation Function (`retrieve_and_transpose_outline_context`)
This function orchestrates dynamic query generation, retrieval, and the semantic adaptation process.

```python
def retrieve_and_transpose_outline_context(
    retriever: VectorStoreRetriever,
    initial_prompt: str,
    story_elements: Optional[dict] = None,
    current_outline_segment: Optional[str] = None, # For dynamic queries
    critic_feedback: Optional[str] = None,         # For dynamic queries
    llm_output_analysis: Optional[str] = None,     # For dynamic queries
    max_context_tokens: int = 2000,                # Increased limit
    top_k_per_query: int = 10,                     # Increased k
    rise_prioritization_enabled: bool = False      # New: RISE-aware retrieval
) -> str:
    """
    Dynamically retrieves, semantically adapts, and formats knowledge base context for outline generation,
    integrating Contextual Transposition Intelligence and RISE-aware prioritization.
    
    Args:
        retriever: Initialized knowledge base retriever.
        initial_prompt: User's story prompt.
        story_elements: Extracted characters, setting, themes.
        current_outline_segment: Current part of the outline being processed (for dynamic queries).
        critic_feedback: Feedback from the critic (for dynamic queries).
        llm_output_analysis: Analysis of previous LLM output (for dynamic queries).
        max_context_tokens: Maximum tokens for retrieved and transposed context.
        top_k_per_query: Number of documents to retrieve per query.
        rise_prioritization_enabled: If True, prioritizes documents tagged with RISE patterns.
        
    Returns:
        Formatted RAG-Outline-Context string with transposed and RISE-aware insights.
    """
    # 1. Construct dynamic queries (using construct_outline_queries)
    queries = construct_outline_queries(initial_prompt, story_elements, 
                                        current_outline_segment, critic_feedback, llm_output_analysis)
    
    # 2. Perform retrieval (potentially with RISE-aware prioritization)
    retrieved_docs = []
    for query in queries:
        docs = retriever.invoke(query)
        # Apply RISE-aware prioritization if enabled (conceptual, implemented in helper)
        if rise_prioritization_enabled:
            docs = prioritize_rise_docs(docs) # New helper function
        retrieved_docs.extend(docs)
    
    # 3. Apply Semantic Adaptation Layer (Contextual Transposition Intelligence)
    transposed_context = apply_semantic_adaptation_layer(retrieved_docs, max_context_tokens) # New helper function
    
    # 4. Format into RAG-Outline-Context block
    formatted_context = format_outline_context(transposed_context, max_context_tokens) # Modified to take transposed_context
    
    return formatted_context
```

#### 3.1.2 Dynamic Query Construction Function (`construct_outline_queries`)
This function will be enhanced to generate queries based on the evolving state of the outline and feedback.

```python
# (Function signature updated in Section 2.2.1)
# Implementation will include logic to combine static and dynamic elements,
# and potentially apply advanced prompting strategies to the queries themselves.
```

#### 3.1.3 Semantic Adaptation Layer Function (`apply_semantic_adaptation_layer`)
This new core function will implement the "Contextual Transposition Intelligence."

```python
def apply_semantic_adaptation_layer(
    retrieved_docs: List[Document],
    max_tokens: int
) -> List[TransposedContent]: # New return type or structured string
    """
    Processes retrieved documents to semantically adapt and transpose content,
    extracting structural patterns and aligning with creative context.
    
    Args:
        retrieved_docs: List of raw retrieved knowledge base documents.
        max_tokens: Maximum token limit for the adapted content.
        
    Returns:
        A structured representation of the transposed content, potentially including
        extracted structural insights (e.g., Advancing Patterns, Structural Tension points).
    """
    # This function will contain the core logic for:
    # - Style Adaptation (e.g., using LLM calls or specialized models)
    # - Structural Pattern Extraction (e.g., identifying narrative arcs, character dynamics)
    # - Concept Transposition (adapting abstract KB concepts to concrete outline elements)
    # - Deduplication and intelligent summarization of adapted content.
    # - Potentially, LLM calls to perform the transposition based on specific instructions.
    pass # Placeholder for detailed implementation
```

#### 3.1.4 RISE Prioritization Helper (`prioritize_rise_docs`)
This new helper function will prioritize documents based on RISE-related tags.

```python
def prioritize_rise_docs(docs: List[Document]) -> List[Document]:
    """
    Prioritizes retrieved documents based on embedded RISE-related metadata or tags.
    Documents tagged as 'Advancing Pattern', 'Structural Tension Resolution', etc.,
    will be ranked higher.
    """
    # Implementation will involve checking document metadata/content for RISE tags
    # and re-ranking the documents accordingly.
    pass # Placeholder for detailed implementation
```

### 3.2 Integration Points Modification (Event-Driven & Bidirectional)

The workflow nodes will be updated to leverage the dynamic and contextually intelligent RAG, and to facilitate bidirectional synchronization.

#### 3.2.1 Initial Outline Generation Enhancement (`generate_initial_outline_node`)
The initial generation will now use the enhanced retrieval and adaptation function.

**File**: `src/willwrite/graph.py` (or appropriate workflow module)  
**Function**: `generate_initial_outline_node`

**Enhanced Flow**:
```
User Prompt → Dynamic RAG Context Retrieval & Transposition → Enhanced Prompt → LLM → Initial Outline
```

**Implementation**:
```python
def generate_initial_outline_node(state: StoryState) -> dict:
    retriever = state.get('retriever')
    config = state['config']
    logger = state['logger']
    initial_prompt = state['initial_prompt']
    
    # Enhanced: Dynamic RAG context retrieval and transposition
    outline_context = ""
    if retriever:
        logger.info("Retrieving and transposing knowledge base context for outline generation")
        outline_context = retrieve_and_transpose_outline_context( # NEW FUNCTION CALL
            retriever=retriever,
            initial_prompt=initial_prompt,
            story_elements=state.get('story_elements'),
            max_context_tokens=config.outline_context_max_tokens,
            top_k_per_query=config.outline_rag_top_k,
            rise_prioritization_enabled=config.outline_rise_prioritization_enabled # NEW CONFIG
        )
        logger.debug(f"Retrieved and transposed outline context: {len(outline_context)} characters")
    
    # Create enhanced prompt with context (using advanced prompting strategies)
    llm = get_llm_from_uri(config.initial_outline_model)
    context = {
        "initial_prompt": initial_prompt,
        "rag_context": outline_context,  # Now contains transposed and RISE-aware context
        "genre": state.get('genre', ''),
        "style_preferences": state.get('style_preferences', '')
    }
    
    # Apply advanced prompting strategies (e.g., Goal-Oriented, Role-Based, Narrative-of-Thought)
    # to the prompt template itself, potentially using a new template or dynamic construction.
    prompt_template = prompts.INITIAL_OUTLINE_PROMPT_WITH_RAG # This template will be updated
    prompt = prompt_template.format_messages(**context)
    
    response = llm.invoke(prompt)
    
    # ... rest of existing logic
    # After outline generation, consider feeding back to coaia-memory for bidirectional sync
    # (Conceptual, requires integration with coaia-memory system)
```

#### 3.2.2 Outline Critique Enhancement (`critique_outline_node`)
Critique will trigger adaptive RAG and guide feedback using RISE principles, enabling bidirectional synchronization.

**Function**: `critique_outline_node`

**Implementation**:
```python
def critique_outline_node(state: StoryState) -> dict:
    retriever = state.get('retriever')
    current_outline = state['current_outline']
    config = state['config'] # Access config for new parameters
    
    # Enhanced: Include dynamically adapted RAG context in critique, guided by RISE principles
    critique_context = ""
    if retriever:
        logger.info("Retrieving and transposing knowledge base context for outline critique")
        critique_context = retrieve_and_transpose_outline_context( # NEW FUNCTION CALL
            retriever=retriever,
            initial_prompt=current_outline,  # Use outline as query for relevant knowledge
            current_outline_segment=current_outline, # Pass current outline for dynamic query
            max_context_tokens=config.outline_critique_context_max_tokens, # NEW CONFIG
            top_k_per_query=config.outline_rag_top_k,
            rise_prioritization_enabled=config.outline_rise_prioritization_enabled
        )
        logger.debug(f"Retrieved and transposed critique context: {len(critique_context)} characters")
    
    # ... rest of critique logic with enhanced context (using updated prompt template)
    # After critique, consider feeding back to coaia-memory for bidirectional sync
    # (Conceptual, requires integration with coaia-memory system)
```

### 3.3 Prompt Template Updates (Advanced Prompting & RISE-Aware)

Prompt templates will be updated to leverage advanced prompting strategies and to guide the LLM in integrating transposed context and adhering to RISE principles.

#### 3.3.1 Enhanced Initial Outline Prompt (`INITIAL_OUTLINE_PROMPT_WITH_RAG`)
**File**: `src/willwrite/prompts.py`

```python
# (Existing template will be significantly expanded)
INITIAL_OUTLINE_PROMPT_WITH_RAG = ChatPromptTemplate.from_messages([
    ("system", """You are an expert story outliner and narrative architect, deeply versed in the principles of creative manifestation and structural tension. Your goal is to create a detailed, coherent, and creatively oriented story outline.

{rag_context}

Using the above **contextually transposed knowledge** (if provided), and adhering to the principles of **Advancing Patterns** (avoiding oscillating patterns), create a detailed story outline that:
1.  **Integrates relevant world-building elements naturally**, ensuring consistency with established characters, settings, rules, and systems.
2.  **Resolves structural tension forward**, guiding the narrative towards desired outcomes without creating unnecessary loops or contradictions.
3.  **Embodies creative orientation**, focusing on what the story enables users to create or experience, rather than merely solving problems.
4.  **Leverages structural insights** provided in the RAG context to build a robust and compelling narrative blueprint.

Think step-by-step, like a seasoned narrative architect. Consider the core conflict, character motivations, and the natural progression of events. Your outline should feel organic to the established world while exploring new territory.
"""),
    
    ("user", """{initial_prompt}

Create a comprehensive story outline that incorporates the relevant knowledge base elements while staying true to the creative vision in the prompt above. Ensure the outline clearly defines chapters and their content, focusing on character development and the natural evolution of the narrative.
""")
])
```

#### 3.3.2 Enhanced Critique Prompt (`OUTLINE_CRITIQUE_PROMPT_WITH_RAG`)
```python
# (Existing template will be significantly expanded)
OUTLINE_CRITIQUE_PROMPT_WITH_RAG = ChatPromptTemplate.from_messages([
    ("system", """You are a highly discerning narrative critic and structural consultant, specializing in identifying and transforming oscillating patterns into advancing patterns within story outlines. Your task is to provide precise, actionable feedback.

{rag_context}

Evaluate the outline against:
1.  **Internal logical consistency** and narrative coherence.
2.  **Alignment with established world knowledge** (provided above), specifically how well the outline integrates transposed insights.
3.  **Character consistency** with known profiles and their natural development arcs.
4.  **Adherence to established rules and systems**, ensuring they contribute to advancing patterns.
5.  **Presence of Advancing Patterns**: Identify areas where the narrative progresses naturally towards desired outcomes.
6.  **Detection of Oscillating Patterns**: Pinpoint any structural loops, contradictions, or elements that might lead to stagnation or regression.
7.  **Resolution of Structural Tension**: Assess how effectively the outline sets up and resolves narrative tension.

Provide specific feedback on consistency with the knowledge base, adherence to RISE principles, and suggest improvements to foster advancing patterns. Focus on *why* a change is needed in terms of structural dynamics.
"""),
    
    ("user", """Outline to critique:
{current_outline}

Provide specific feedback on consistency with the knowledge base and suggest improvements.
""")
])
```

### 3.4 Configuration Extensions (Dynamic RAG & RISE-Aware)

New configuration parameters will be added to control the behavior of the dynamic RAG, contextual transposition, and RISE-aware prioritization.

#### 3.4.1 New Configuration Parameters (`WillWriteConfig` in `src/willwrite/config.py`)

```python
class WillWriteConfig(BaseModel):
    # ... existing fields ...
    
    # Outline-level RAG configuration (Enhanced)
    outline_rag_enabled: bool = Field(True, alias='OutlineRagEnabled', 
        description="Enable RAG context injection during outline generation and critique.")
    outline_context_max_tokens: int = Field(2000, alias='OutlineContextMaxTokens', # Increased
        description="Maximum tokens for retrieved and transposed outline-stage RAG context.")
    outline_rag_top_k: int = Field(10, alias='OutlineRagTopK', # Increased
        description="Number of documents to retrieve per query for outline stage.")
    outline_rag_similarity_threshold: float = Field(0.7, alias='OutlineRagSimilarityThreshold',
        description="Minimum similarity threshold for outline-stage document retrieval.")
    
    # New: Dynamic RAG & Contextual Transposition parameters
    outline_dynamic_rag_enabled: bool = Field(True, alias='OutlineDynamicRagEnabled',
        description="Enable dynamic re-retrieval and adaptation of RAG context during revision cycles.")
    outline_critique_context_max_tokens: int = Field(1000, alias='OutlineCritiqueContextMaxTokens', # New
        description="Maximum tokens for retrieved and transposed RAG context during outline critique.")
    outline_semantic_adaptation_model: Optional[str] = Field(None, alias='OutlineSemanticAdaptationModel', # New
        description="Model to use for the Semantic Adaptation Layer (Contextual Transposition Intelligence).")
    
    # New: RISE-aware RAG parameters
    outline_rise_prioritization_enabled: bool = Field(True, alias='OutlineRisePrioritizationEnabled', # New
        description="Enable prioritization of knowledge base documents tagged with RISE patterns (Advancing, Structural Tension).")
    outline_rise_tag_model: Optional[str] = Field(None, alias='OutlineRiseTagModel', # New
        description="Model to use for identifying RISE patterns in knowledge base documents if not pre-tagged.")
```

---

## 4. Validation & Testing (Comprehensive & RISE-Aware)

Validation and testing will be expanded to rigorously assess the dynamic and contextually intelligent RAG system, focusing on its effectiveness in fostering creative orientation and avoiding oscillating patterns within the Unified Creative Orientation Framework.

### 4.1 Unit Tests

Unit tests will cover all new and modified functions, ensuring the reliability of dynamic query generation, semantic adaptation, and RISE-aware prioritization.

#### 4.1.1 Core Retrieval & Adaptation Function Tests
```python
def test_retrieve_and_transpose_outline_context_static_query():
    """Test core function with static queries and basic transposition."""
    
def test_retrieve_and_transpose_outline_context_dynamic_query():
    """Test core function with dynamic queries (e.g., based on critic feedback)."""

def test_retrieve_and_transpose_outline_context_rise_prioritization():
    """Test core function's ability to prioritize RISE-tagged documents."""
```

#### 4.1.2 Dynamic Query Construction Function Tests
```python
def test_construct_outline_queries_with_feedback():
    """Test query construction based on critic feedback and LLM output analysis."""
```

#### 4.1.3 Semantic Adaptation Layer Function Tests
```python
def test_apply_semantic_adaptation_layer_style_adaptation():
    """Test semantic adaptation for style transposition."""

def test_apply_semantic_adaptation_layer_structural_extraction():
    """Test semantic adaptation for extracting structural patterns (e.g., Advancing/Oscillating)."""

def test_apply_semantic_adaptation_layer_concept_transposition():
    """Test semantic adaptation for transposing abstract concepts to narrative elements."""
```

#### 4.1.4 RISE Prioritization Helper Tests
```python
def test_prioritize_rise_docs_ranking():
    """Test correct ranking of documents based on RISE tags."""
```

#### 4.1.5 Integration Tests
Integration tests will verify the end-to-end flow of dynamic RAG and its impact on outline generation and critique within the graph.

```python
def test_outline_generation_with_dynamic_rag_and_transposition():
    """Test complete outline generation with RAG and semantic adaptation."""
    
def test_outline_critique_with_adaptive_rag_and_rise_guidance():
    """Test critique enhancement with adaptive RAG and its guidance towards advancing patterns."""

def test_bidirectional_sync_with_coaia_memory_integration():
    """Test the feedback loop to coaia-memory for structural tension updates (conceptual)."""
```

### 4.2 Functional Validation (Creative Orientation & Structural Dynamics)

Functional validation will assess the system's ability to foster creative orientation, resolve structural tension, and avoid oscillating patterns, aligning with the Unified Creative Orientation Framework.

#### 4.2.1 Test Scenarios
1.  **Character Consistency & Development**: Outline references established character traits and demonstrates natural character development arcs.
2.  **World Adherence & Structural Integrity**: Setting details match knowledge base geography, and the narrative structure maintains integrity with established rules and systems.
3.  **Thematic Alignment & Creative Intent**: Story themes incorporate established lore and align with the user's core creative intent, demonstrating creative manifestation.
4.  **Structural Tension Resolution**: Scenarios designed to test the system's ability to set up and resolve narrative tension in an advancing manner.
5.  **Oscillating Pattern Transformation**: Scenarios where initial LLM outputs might exhibit oscillating patterns, and the system's ability to guide revisions towards advancing patterns is tested.
6.  **Bidirectional Synchronization Impact**: Assess how updates to `coaia-memory` (e.g., completed action steps from outline generation) influence subsequent creative processes.

#### 4.2.2 Validation Metrics
New metrics will be introduced to quantify creative orientation, contextual transposition effectiveness, and the impact of bidirectional synchronization.

-   **Context Relevance & Transposition Quality**:
    *   **Transposition Fidelity**: How accurately and creatively the retrieved context is adapted to the specific narrative context.
    *   **Structural Insight Utility**: Quantitative assessment of how often and effectively the "Structural Insights" from the RAG context are utilized by the LLM.
-   **Knowledge Integration & Consistency**:
    *   **Knowledge Integration Score**: Automated assessment of how well knowledge base elements are naturally and consistently integrated into the outline.
    *   **Consistency Score**: Automated consistency checking against knowledge base, including character and world-building adherence.
-   **Creative Orientation & Pattern Dynamics**:
    *   **Advancing Pattern Score**: Automated or human evaluation of the presence and strength of advancing patterns in the generated outline.
    *   **Oscillating Pattern Reduction**: Measurement of the reduction in oscillating patterns after revision cycles guided by the system.
    *   **Structural Tension Resolution Score**: Assessment of how effectively narrative tension is introduced and resolved.
-   **Bidirectional Synchronization Impact**:
    *   **Memory Update Accuracy**: Accuracy of updates pushed to `coaia-memory` based on outline generation progress.
    *   **Recursive Advancement Metric**: Quantify how feedback loops (e.g., from `coaia-memory`) contribute to improved creative output over multiple iterations.
-   **Token Efficiency**: Context utilization within token limits, considering the increased context size.

### 4.3 Performance Testing

Performance testing will ensure the system remains efficient despite the added complexity of dynamic RAG and semantic adaptation.

#### 4.3.1 Retrieval & Adaptation Performance
-   **Query Response Time**: Sub-second retrieval and transposition target.
-   **Context Size Management**: Adherence to token limits, including the expanded context.
-   **Memory Usage**: Efficient document handling and semantic adaptation processes.
-   **Semantic Adaptation Latency**: Measure the time taken for the `apply_semantic_adaptation_layer` function.

#### 4.3.2 Generation Quality & Efficiency
-   **Outline Coherence**: Logical narrative structure and flow.
-   **Knowledge Integration**: Natural incorporation of transposed context.
-   **Creative Balance**: Maintains user intent while adding knowledge and adhering to RISE principles.
-   **Overall Generation Time**: Monitor the total time taken for outline generation and revision cycles with the enhanced RAG.

---

## 5. Deployment Strategy (Phased Integration with Unified Framework)

The deployment of the enhanced Outline-Level RAG will follow a phased approach, ensuring stable integration with the existing `WillWrite` architecture and the broader Unified Creative Orientation Framework.

### 5.1 Implementation Phases

#### 5.1.1 Phase 1: Core Dynamic RAG & Contextual Transposition Functions
This phase focuses on building the foundational components for dynamic retrieval and semantic adaptation.
1.  Implement `retrieve_and_transpose_outline_context` function.
2.  Enhance `construct_outline_queries` for dynamic query generation.
3.  Implement `apply_semantic_adaptation_layer` for Contextual Transposition Intelligence.
4.  Implement `prioritize_rise_docs` for RISE-aware knowledge prioritization.
5.  Unit test all new core functions and helper utilities.

#### 5.1.2 Phase 2: Workflow Integration & Advanced Prompting
This phase integrates the new RAG capabilities into the `WillWrite` workflow and updates prompting strategies.
1.  Modify `generate_initial_outline_node` and `critique_outline_node` to use the new `retrieve_and_transpose_outline_context` function.
2.  Update prompt templates (`INITIAL_OUTLINE_PROMPT_WITH_RAG`, `OUTLINE_CRITIQUE_PROMPT_WITH_RAG`) to leverage advanced prompting strategies (CoT, Goal-Oriented, Role-Based) and guide the LLM in utilizing transposed and RISE-aware context.
3.  Add new configuration parameters to `WillWriteConfig` for dynamic RAG, contextual transposition, and RISE-aware features.
4.  Conduct integration testing for the enhanced outline generation and critique loops.

#### 5.1.3 Phase 3: Bidirectional Synchronization & Recursive Advancement
This phase focuses on integrating the RAG system with the broader Unified Creative Orientation Framework for recursive advancement.
1.  Implement mechanisms for **bidirectional synchronization** with `coaia-memory` (e.g., pushing outline progress, detected patterns, and completed action steps to the structural memory).
2.  Develop feedback loops from `coaia-memory` and `mcp-coaia-sequential-thinking` to dynamically influence RAG behavior (e.g., adjusting retrieval parameters based on detected oscillating patterns in the overall creative process).
3.  Perform comprehensive system-level validation, including end-to-end testing of recursive advancement spirals.
4.  Conduct user experience testing to ensure seamless integration and intuitive creative workflow.
5.  Update documentation to reflect the new capabilities and integration points within the Unified Creative Orientation Framework.
6.  Prepare for production deployment.

### 5.2 Backward Compatibility (Graceful Degradation)

The system will be designed for graceful degradation and optional activation, ensuring stability and flexibility.

#### 5.2.1 Graceful Degradation
-   The system will function normally if the `retriever` is not initialized or if new configuration parameters are not explicitly set (defaulting to disabled or sensible fallbacks).
-   Existing prompts will continue to work, though without the benefits of dynamic RAG and contextual transposition.

#### 5.2.2 Optional Activation
-   New RAG features (dynamic RAG, contextual transposition, RISE prioritization) will be controlled by dedicated configuration flags (e.g., `outline_dynamic_rag_enabled`, `outline_rise_prioritization_enabled`).
-   Users can selectively enable or disable these advanced features, allowing for incremental adoption and experimentation.
-   Clear logging will indicate when dynamic RAG and contextual transposition are active and how they are influencing the outline generation process.

---

## 6. Success Criteria (Unified Creative Orientation & Recursive Advancement)

The success of the enhanced Outline-Level RAG will be measured against its ability to contribute to the Unified Creative Orientation Framework, fostering recursive advancement and delivering a superior creative experience.

### 6.1 Functional Requirements ✅

-   [ ] **Dynamic Contextual Retrieval**: Outline generation dynamically incorporates relevant knowledge base content, adapted through Contextual Transposition Intelligence.
-   [ ] **RISE-Aware Integration**: Retrieved context is prioritized and integrated based on RISE principles (Advancing Patterns, Structural Tension resolution).
-   [ ] **Bidirectional Synchronization**: Outline generation progress and detected patterns are accurately fed back to `coaia-memory` for structural tension updates.
-   [ ] **Context Token Management**: Retrieved and transposed context consistently stays within defined token limits.
-   [ ] **Scalability**: System maintains performance with large knowledge bases and complex dynamic queries.

### 6.2 Quality Requirements ✅

-   [ ] **Creative Orientation**: Generated outlines consistently embody creative orientation, focusing on manifestation and natural progression.
-   [ ] **Advancing Pattern Dominance**: Significant reduction in oscillating patterns and a measurable increase in advancing patterns within generated outlines.
-   [ ] **Structural Tension Resolution**: Outlines effectively set up and resolve narrative tension in a compelling and advancing manner.
-   [ ] **Transposition Fidelity**: Semantically adapted knowledge is integrated naturally and creatively, enhancing narrative depth without feeling forced or artificial.
-   [ ] **Narrative Coherence**: Outlines demonstrate superior internal logical consistency, character development, and world adherence, directly attributable to the enhanced RAG.
-   [ ] **User Creative Intent Preservation**: User's core creative vision is preserved and enhanced, not overridden, by the system's guidance.

### 6.3 Technical Requirements ✅

-   [ ] **Sub-second Retrieval & Adaptation**: Query response time for retrieval and semantic adaptation remains sub-second.
-   [ ] **Memory & Compute Efficiency**: Efficient handling of documents and semantic adaptation processes, minimizing memory and computational overhead.
-   [ ] **Robustness**: Robust error handling for missing/invalid knowledge bases and during dynamic adaptation processes.
-   [ ] **Comprehensive Logging**: Detailed logging for debugging, optimization, and tracing recursive advancement spirals.
-   [ ] **Integration Stability**: Seamless and stable integration with `coaia-memory` and `mcp-coaia-sequential-thinking` components.

### 6.4 User Experience Requirements ✅

-   [ ] **Seamless Creative Flow**: Users perceive the system as a natural and intuitive creative partner, enhancing their creative flow.
-   [ ] **Improved Creative Output**: Users report a noticeable improvement in the consistency, depth, and creative quality of generated outlines.
-   [ ] **Clear Guidance**: Configuration options are clear and provide intuitive control over advanced RAG features.
-   [ ] **Actionable Feedback**: Critique feedback is precise, actionable, and effectively guides revisions towards advancing patterns.
-   [ ] **Optional Activation**: Advanced features can be optionally activated, preserving existing workflows for users who prefer simpler modes.

---

## 7. Future Enhancements (Recursive & Self-Improving Creative Ecosystem)

This section outlines future enhancements that will further deepen the integration of Outline-Level RAG within the Unified Creative Orientation Framework, fostering a truly recursive and self-improving creative ecosystem.

### 7.1 Advanced Retrieval & Knowledge Dynamics
-   **Semantic Clustering & Structural Graphing**: Beyond simple clustering, develop capabilities to identify and represent structural relationships within the knowledge base (e.g., character relationship graphs, plot dependency networks) to enable more intelligent retrieval.
-   **Temporal Awareness & Narrative Flow**: Integrate a deeper understanding of narrative timelines and pacing into retrieval, allowing the system to provide context relevant to specific temporal points in the story's progression.
-   **Relationship Mapping & Dynamic Evolution**: Continuously update and refine character and location relationships within the knowledge base based on the evolving narrative, feeding back into `coaia-memory` for dynamic knowledge evolution.
-   **Predictive Contextualization**: Develop models that can anticipate future narrative needs and proactively retrieve or generate relevant context, guiding the story towards compelling structural tension and resolution.

### 7.2 Interactive Refinement & Human-AI Co-Creation
-   **Context Review & Selective Integration**: Allow users to review the retrieved and transposed context before generation, providing feedback on relevance and enabling selective integration of knowledge elements.
-   **Dynamic Feedback Loops**: Implement more sophisticated human-in-the-loop feedback mechanisms that allow users to directly influence the semantic adaptation layer and RISE prioritization, refining the system's understanding of creative intent.
-   **Creative Control Interfaces**: Develop intuitive interfaces that allow users to directly manipulate structural tension, advancing patterns, and oscillating patterns within the outline, with the RAG system providing real-time, contextually transposed guidance.

### 7.3 Cross-Story Memory & Ecosystemic Learning
-   **Series Continuity & Recursive Learning**: Deepen the integration with `coaia-memory` to link outlines across multiple stories within the same world or series, allowing the system to learn and maintain continuity and character growth across narratives.
-   **World Evolution & Knowledge Base Refinement**: Enable the system to update and refine the knowledge base itself based on the outcomes of generated stories, creating a self-improving knowledge ecosystem.
-   **Meta-Cognitive Pattern Recognition**: Develop capabilities for the system to analyze its own creative processes, identify successful "recursive advancement spirals," and learn from failures to continuously improve its creative orientation.

---

**Implementation Priority**: CRITICAL - This enhanced RAG system is a foundational component for the Unified Creative Orientation Framework and its recursive creative system design.

**Estimated Effort**: 3-5 development phases, requiring significant research and development in AI, NLP, and systems architecture.

**Dependencies**: Requires robust implementation of the core Unified Creative Orientation Framework components (`coaia-memory`, `mcp-coaia-sequential-thinking`, `co-lint`) and their bidirectional synchronization capabilities.
