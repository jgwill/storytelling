# Implementation Plan: BaseContext Extraction Integration

**Status**: 🔴 REQUIRED - High Priority
**Target**: `/src/storytelling/storytelling/` package
**Specification Source**: `/src/storytelling/rispecs/ProceduralLogic.md` (lines 68-70), `/src/storytelling/rispecs/ApplicationLogic.md` (lines 38-42)

## Structural Tension

**Desired Outcome**: User meta-instructions (chapter length, tone, formatting preferences, creative vision) from prompts are extracted and injected into all generation stages, ensuring the LLM respects user preferences throughout story creation.

**Current Reality**: The `GET_IMPORTANT_BASE_PROMPT_INFO` prompt exists in `storytelling/prompts.py:4-24` but is **never invoked**. The `{_BaseContext}` placeholder appears in chapter generation prompts (lines 213, 238, 274, 512) but receives no data. User instructions about chapter length, formatting, and creative vision are **completely ignored**.

**Natural Progression**: Add a BaseContext extraction step before story element generation in the LangGraph workflow, store the result in graph state, and inject it into all prompts that reference `{_BaseContext}`.

---

## Implementation Steps

### 1. Update StoryState TypedDict

**File**: `/src/storytelling/storytelling/graph.py`
**Location**: Find the `StoryState` TypedDict definition (likely near the top of the file)

**Action**: Add `base_context` field to capture extracted meta-instructions

```python
class StoryState(TypedDict):
    # ... existing fields ...
    base_context: str  # Meta-instructions extracted from user prompt (chapter length, tone, formatting)
    # ... existing fields ...
```

---

### 2. Create BaseContext Extraction Node

**File**: `/src/storytelling/storytelling/graph.py`
**Location**: Add new node function before or near `generate_story_elements_node`

**Action**: Create a new node that extracts BaseContext from the user prompt

```python
def extract_base_context_node(state: StoryState) -> dict:
    """
    Extract meta-instructions from the user prompt.

    Captures guidance about chapter length, tone, formatting preferences,
    and overall creative vision that should guide all generation stages.
    """
    logger = state["logger"]
    config = state["config"]
    user_prompt = state["user_prompt"]

    logger.log("Extracting meta-instructions from user prompt", 5)

    # Get the LLM for base context extraction
    llm = get_model_for_task(config, "initial_outline_writer")

    # Import the prompt
    from storytelling.prompts import GET_IMPORTANT_BASE_PROMPT_INFO

    # Create the chain
    chain = GET_IMPORTANT_BASE_PROMPT_INFO | llm | StrOutputParser()

    # Extract base context
    base_context = chain.invoke({"_Prompt": user_prompt})

    logger.log(f"Extracted BaseContext: {base_context[:200]}...", 4)

    return {"base_context": base_context}
```

---

### 3. Update Story Elements Node to Use BaseContext

**File**: `/src/storytelling/storytelling/graph.py`
**Location**: Find `generate_story_elements_node` function

**Action**: The story elements prompt already has the user prompt, but BaseContext should be available for future use. No changes needed here unless the prompt template changes to explicitly use BaseContext.

---

### 4. Update Chapter Generation Stages to Inject BaseContext

**File**: `/src/storytelling/storytelling/graph.py`
**Location**: Find chapter generation functions (e.g., `generate_single_chapter_scene_by_scene_node` or similar)

**Action**: Ensure all chapter generation prompt invocations include `_BaseContext` parameter

**Example Pattern**:
```python
# When invoking CHAPTER_GENERATION_STAGE1, STAGE2, STAGE3, STAGE4
chain = prompt_template | llm | StrOutputParser()

result = chain.invoke({
    "_Outline": state["outline"],
    "_BaseContext": state["base_context"],  # ← Add this line
    "_ChapterNum": current_chapter,
    # ... other parameters ...
})
```

**Files to check**:
- Any function that invokes `CHAPTER_GENERATION_STAGE1`
- Any function that invokes `CHAPTER_GENERATION_STAGE2`
- Any function that invokes `CHAPTER_GENERATION_STAGE3`
- Any function that invokes `CHAPTER_GENERATION_STAGE4`
- Any scene generation prompts that reference `{_BaseContext}`

---

### 5. Update LangGraph Workflow to Include New Node

**File**: `/src/storytelling/storytelling/graph.py`
**Location**: Find the graph definition (likely near the end where nodes are added)

**Action**: Add the BaseContext extraction node as the **first step** after initialization

```python
# Build the graph
workflow = StateGraph(StoryState)

# Add nodes
workflow.add_node("extract_base_context", extract_base_context_node)  # ← NEW NODE (FIRST)
workflow.add_node("generate_story_elements", generate_story_elements_node)
workflow.add_node("generate_initial_outline", generate_initial_outline_node)
# ... other nodes ...

# Define edges
workflow.set_entry_point("extract_base_context")  # ← Start here
workflow.add_edge("extract_base_context", "generate_story_elements")  # ← Then go to story elements
workflow.add_edge("generate_story_elements", "generate_initial_outline")
# ... other edges ...
```

---

### 6. Update JSON Output to Include BaseContext

**File**: `/src/storytelling/storytelling/graph.py`
**Location**: Find where the final JSON output is created (likely in `generate_final_story_node` or similar)

**Action**: Include `base_context` in the saved JSON metadata

```python
story_info_json = {
    "outline": state["outline"],
    "story_elements": state["story_elements"],
    "base_context": state["base_context"],  # ← Add this line
    # ... other fields ...
}
```

---

## Verification Steps

After implementation, verify:

1. ✅ BaseContext is extracted at the start of the workflow
2. ✅ BaseContext appears in graph state throughout execution
3. ✅ Chapter generation stages receive BaseContext parameter
4. ✅ Final JSON output includes BaseContext field
5. ✅ Test with a prompt containing explicit instructions:
   ```
   Write a story about a space explorer.

   IMPORTANT: Each chapter must be at least 2000 words.
   Use a serious, scientific tone throughout.
   Format dialogue with em-dashes instead of quotation marks.
   ```
6. ✅ Verify the generated chapters respect these meta-instructions

---

## Files to Modify

1. `/src/storytelling/storytelling/graph.py` - Main graph definition
   - Add `base_context` field to `StoryState`
   - Create `extract_base_context_node` function
   - Update graph workflow to include new node as first step
   - Update chapter generation invocations to pass `_BaseContext`
   - Update JSON output to include BaseContext

2. `/src/storytelling/storytelling/prompts.py` - Already contains the prompt (no changes needed)

---

## Reference Implementation

See original implementation in `/src/WillWrite/`:
- `/src/WillWrite/Write.py:269-271` - How BaseContext is returned from outline generation
- `/src/WillWrite/Writer/Prompts.py:87-108` - The GET_IMPORTANT_BASE_PROMPT_INFO prompt
- `/src/WillWrite/Writer/Prompts.py:110-132` - How BaseContext is injected into STAGE1
- `/src/WillWrite/Writer/Prompts.py:134-167` - How BaseContext is injected into STAGE2
- `/src/WillWrite/Writer/Prompts.py:169-202` - How BaseContext is injected into STAGE3

---

## Expected Impact

✅ **Outcome**: User meta-instructions will be consistently applied throughout story generation
✅ **Benefit**: Chapter length requirements, tone preferences, and formatting instructions will be respected
✅ **Alignment**: Brings `/src/storytelling/` implementation into parity with `/src/WillWrite/` specifications
