# Outline-Level RAG Integration Specification

**Status**: Ready for Implementation  
**Date**: 2025-08-15  
**Version**: 1.0  
**Dependencies**: RAG_Implementation_Specification.md, ApplicationLogic.md

---

## 1. Overview

This specification defines the implementation of RAG (Retrieval-Augmented Generation) integration at the outline generation stage, extending the existing scene-level RAG system to provide knowledge-aware story foundation creation.

### 1.1 Current State
- ✅ **Scene-Level RAG**: Functional during chapter generation with context injection
- ❌ **Outline-Level RAG**: Not implemented - outlines generated without knowledge base awareness
- ✅ **Infrastructure**: RAG system (`src/willwrite/rag.py`) ready for extension

### 1.2 Strategic Importance
Outline-level RAG ensures that story foundations are grounded in established world-building from the start, creating more consistent and coherent narrative structures that naturally incorporate knowledge base content throughout the entire generation pipeline.

---

## 2. Architecture Design

### 2.1 Integration Points

#### 2.1.1 Initial Outline Generation
**Location**: `generate_initial_outline` workflow node  
**Trigger**: After prompt analysis, before outline creation  
**Purpose**: Inject relevant world-building context for foundational story structure

#### 2.1.2 Outline Critique/Revision
**Location**: `critique_outline` and `revise_outline` workflow nodes  
**Trigger**: During outline quality assessment and revision cycles  
**Purpose**: Ensure outline consistency with established knowledge base content

#### 2.1.3 Chapter Count Determination  
**Location**: `determine_chapter_count` workflow node  
**Trigger**: When determining story scope based on outline  
**Purpose**: Consider knowledge base complexity in pacing decisions

### 2.2 Retrieval Strategy

#### 2.2.1 Query Construction
**Primary Query Sources**:
- User's initial story prompt (full text)
- Extracted entities (characters, locations, concepts)
- Genre and theme keywords
- Conflict and plot elements

**Query Processing**:
```python
def construct_outline_queries(initial_prompt: str, story_elements: dict) -> List[str]:
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
        
    return queries
```

#### 2.2.2 Retrieval Parameters
- **Top-k Results**: 5 documents per query (configurable)
- **Context Token Limit**: 1,000 tokens maximum for outline stage
- **Semantic Filtering**: High-relevance threshold (0.7+ similarity)
- **Document Types**: Prioritize character sheets, world-building, magic systems

#### 2.2.3 Context Aggregation
**Deduplication**: Remove overlapping content between retrieved documents  
**Prioritization**: Rank by relevance and recency  
**Formatting**: Structure as labeled context blocks

### 2.3 Context Injection Format

#### 2.3.1 RAG-Outline-Context Block
```
<RAG-OUTLINE-CONTEXT>
# Relevant World Knowledge

## Characters
[Retrieved character information]

## World & Setting  
[Retrieved world-building content]

## Rules & Systems
[Retrieved magic/technology/social systems]

## Themes & Lore
[Retrieved thematic and background content]
</RAG-OUTLINE-CONTEXT>
```

#### 2.3.2 Prompt Integration
**Injection Point**: Between system instructions and user prompt  
**Labeling**: Clear separation with retrieval metadata  
**Token Management**: Truncate if exceeding limits, prioritize by relevance

---

## 3. Implementation Specification

### 3.1 New Functions Required

#### 3.1.1 Core Retrieval Function
```python
def retrieve_outline_context(
    retriever: VectorStoreRetriever,
    initial_prompt: str,
    story_elements: Optional[dict] = None,
    max_context_tokens: int = 1000,
    top_k_per_query: int = 5
) -> str:
    """
    Retrieve and format knowledge base context for outline generation.
    
    Args:
        retriever: Initialized knowledge base retriever
        initial_prompt: User's story prompt
        story_elements: Extracted characters, setting, themes
        max_context_tokens: Maximum tokens for retrieved context
        top_k_per_query: Number of documents per query
        
    Returns:
        Formatted RAG-Outline-Context string
    """
```

#### 3.1.2 Query Construction Function
```python
def construct_outline_queries(
    initial_prompt: str,
    story_elements: Optional[dict] = None
) -> List[str]:
    """
    Generate optimized queries for outline-stage knowledge retrieval.
    
    Args:
        initial_prompt: User's story prompt
        story_elements: Parsed story components
        
    Returns:
        List of targeted queries for knowledge base
    """
```

#### 3.1.3 Context Formatting Function
```python
def format_outline_context(
    retrieved_docs: List[Document],
    max_tokens: int = 1000
) -> str:
    """
    Format retrieved documents into structured outline context.
    
    Args:
        retrieved_docs: List of retrieved knowledge base documents
        max_tokens: Maximum token limit for context
        
    Returns:
        Formatted RAG-Outline-Context block
    """
```

### 3.2 Integration Points Modification

#### 3.2.1 Initial Outline Generation Enhancement
**File**: `src/willwrite/graph.py` (or appropriate workflow module)  
**Function**: `generate_initial_outline_node`

**Current Flow**:
```
User Prompt → LLM → Initial Outline
```

**Enhanced Flow**:
```
User Prompt → RAG Context Retrieval → Enhanced Prompt → LLM → Initial Outline
```

**Implementation**:
```python
def generate_initial_outline_node(state: StoryState) -> dict:
    retriever = state.get('retriever')
    config = state['config']
    logger = state['logger']
    initial_prompt = state['initial_prompt']
    
    # Enhanced: RAG context retrieval
    outline_context = ""
    if retriever:
        logger.info("Retrieving knowledge base context for outline generation")
        outline_context = retrieve_outline_context(
            retriever=retriever,
            initial_prompt=initial_prompt,
            story_elements=state.get('story_elements'),
            max_context_tokens=1000
        )
        logger.debug(f"Retrieved outline context: {len(outline_context)} characters")
    
    # Create enhanced prompt with context
    llm = get_llm_from_uri(config.initial_outline_model)
    context = {
        "initial_prompt": initial_prompt,
        "rag_context": outline_context,  # New context injection
        "genre": state.get('genre', ''),
        "style_preferences": state.get('style_preferences', '')
    }
    
    prompt = prompts.INITIAL_OUTLINE_PROMPT.format_messages(**context)
    response = llm.invoke(prompt)
    
    # ... rest of existing logic
```

#### 3.2.2 Outline Critique Enhancement
**Function**: `critique_outline_node`

**Implementation**:
```python
def critique_outline_node(state: StoryState) -> dict:
    retriever = state.get('retriever')
    current_outline = state['current_outline']
    
    # Enhanced: Include RAG context in critique
    critique_context = ""
    if retriever:
        # Use outline content as query for relevant knowledge
        critique_context = retrieve_outline_context(
            retriever=retriever,
            initial_prompt=current_outline,  # Use outline as query
            max_context_tokens=500  # Smaller limit for critique
        )
    
    # ... rest of critique logic with enhanced context
```

### 3.3 Prompt Template Updates

#### 3.3.1 Enhanced Initial Outline Prompt
**File**: `src/willwrite/prompts.py`

```python
INITIAL_OUTLINE_PROMPT_WITH_RAG = ChatPromptTemplate.from_messages([
    ("system", """You are an expert story outliner creating narrative foundations.

{rag_context}

Using the above knowledge base context (if provided), create a detailed story outline that:
1. Incorporates relevant world-building elements naturally
2. Maintains consistency with established characters and settings
3. Respects the rules and systems described in the knowledge base
4. Builds upon existing lore while advancing the new narrative

The outline should feel organic to the established world while exploring new territory."""),
    
    ("user", """{initial_prompt}

Create a comprehensive story outline that incorporates the relevant knowledge base elements while staying true to the creative vision in the prompt above.""")
])
```

#### 3.3.2 Enhanced Critique Prompt
```python
OUTLINE_CRITIQUE_PROMPT_WITH_RAG = ChatPromptTemplate.from_messages([
    ("system", """You are critiquing a story outline for consistency and quality.

{rag_context}

Evaluate the outline against:
1. Internal logical consistency
2. Alignment with established world knowledge (above)
3. Character consistency with known profiles
4. Adherence to established rules and systems
5. Natural integration of world elements"""),
    
    ("user", """Outline to critique:
{current_outline}

Provide specific feedback on consistency with the knowledge base and suggest improvements.""")
])
```

### 3.4 Configuration Extensions

#### 3.4.1 New Configuration Parameters
**File**: `src/willwrite/config.py`

```python
class WillWriteConfig(BaseModel):
    # ... existing fields ...
    
    # Outline-level RAG configuration
    outline_rag_enabled: bool = Field(True, alias='OutlineRagEnabled', 
        description="Enable RAG context injection during outline generation")
    outline_context_max_tokens: int = Field(1000, alias='OutlineContextMaxTokens',
        description="Maximum tokens for outline-stage RAG context")
    outline_rag_top_k: int = Field(5, alias='OutlineRagTopK',
        description="Number of documents to retrieve per query for outline stage")
    outline_rag_similarity_threshold: float = Field(0.7, alias='OutlineRagSimilarityThreshold',
        description="Minimum similarity threshold for outline-stage document retrieval")
```

---

## 4. Validation & Testing

### 4.1 Unit Tests

#### 4.1.1 Retrieval Function Tests
```python
def test_retrieve_outline_context():
    """Test outline context retrieval with various prompts"""
    
def test_construct_outline_queries():
    """Test query construction from prompts and story elements"""
    
def test_format_outline_context():
    """Test context formatting and token limiting"""
```

#### 4.1.2 Integration Tests
```python
def test_outline_generation_with_rag():
    """Test complete outline generation with RAG integration"""
    
def test_outline_critique_with_rag():
    """Test critique enhancement with knowledge base context"""
```

### 4.2 Functional Validation

#### 4.2.1 Test Scenarios
1. **Character Consistency**: Outline references established character traits
2. **World Adherence**: Setting details match knowledge base geography
3. **System Integration**: Magic/technology systems used correctly
4. **Thematic Alignment**: Story themes incorporate established lore

#### 4.2.2 Validation Metrics
- **Context Relevance**: Percentage of retrieved context used in outline
- **Knowledge Integration**: Count of knowledge base elements referenced
- **Consistency Score**: Automated consistency checking against knowledge base
- **Token Efficiency**: Context utilization within token limits

### 4.3 Performance Testing

#### 4.3.1 Retrieval Performance
- **Query Response Time**: Sub-second retrieval target
- **Context Size Management**: Adherence to token limits
- **Memory Usage**: Efficient document handling

#### 4.3.2 Generation Quality
- **Outline Coherence**: Logical narrative structure
- **Knowledge Integration**: Natural incorporation of context
- **Creative Balance**: Maintains user intent while adding knowledge

---

## 5. Deployment Strategy

### 5.1 Implementation Phases

#### 5.1.1 Phase 1: Core Retrieval Functions
1. Implement `retrieve_outline_context()` function
2. Create query construction logic
3. Add context formatting utilities
4. Unit test all core functions

#### 5.1.2 Phase 2: Workflow Integration  
1. Modify outline generation nodes
2. Update prompt templates
3. Add configuration parameters
4. Integration testing

#### 5.1.3 Phase 3: Optimization & Validation
1. Performance tuning
2. User experience testing
3. Documentation updates
4. Production deployment

### 5.2 Backward Compatibility

#### 5.2.1 Graceful Degradation
- System functions normally when `retriever` is None
- Existing prompts work without RAG context
- Configuration parameters have sensible defaults

#### 5.2.2 Optional Activation
- RAG integration controlled by `outline_rag_enabled` flag
- Users can disable outline-level RAG while keeping scene-level RAG
- Clear logging indicates when RAG context is used

---

## 6. Success Criteria

### 6.1 Functional Requirements ✅
- [ ] Outline generation incorporates relevant knowledge base content
- [ ] Retrieved context stays within token limits
- [ ] Knowledge integration feels natural, not forced
- [ ] System maintains performance with large knowledge bases

### 6.2 Quality Requirements ✅  
- [ ] Generated outlines reference established characters appropriately
- [ ] World-building elements appear consistently in narrative structure
- [ ] Magic/system rules are respected in plot development
- [ ] User creative intent is preserved and enhanced, not overridden

### 6.3 Technical Requirements ✅
- [ ] Sub-second retrieval performance
- [ ] Memory-efficient context handling
- [ ] Robust error handling for missing or invalid knowledge bases
- [ ] Comprehensive logging for debugging and optimization

### 6.4 User Experience Requirements ✅
- [ ] Seamless integration - users notice improved consistency, not complexity
- [ ] Clear configuration options for customization
- [ ] Helpful error messages and guidance
- [ ] Optional activation preserves existing workflows

---

## 7. Future Enhancements

### 7.1 Advanced Retrieval
- **Semantic Clustering**: Group related knowledge base content
- **Temporal Awareness**: Consider story timeline in retrieval
- **Relationship Mapping**: Understand character and location connections

### 7.2 Interactive Refinement
- **Context Review**: Allow users to review retrieved context before generation
- **Selective Integration**: Choose which knowledge elements to include
- **Dynamic Queries**: Refine queries based on outline development

### 7.3 Cross-Story Memory
- **Series Continuity**: Link outlines across multiple stories in same world
- **Character Development**: Track character growth across narratives
- **World Evolution**: Update knowledge base based on story events

---

**Implementation Priority**: HIGH - Completes the RAG pipeline and provides significant value for consistent world-building

**Estimated Effort**: 2-3 development phases, building on existing RAG infrastructure

**Dependencies**: Requires existing RAG system and workflow architecture to be operational