from typing import Any, Dict

from langgraph.graph import END, StateGraph

from . import prompts
from .llm_providers import get_llm_from_uri
from .rag import construct_outline_queries, retrieve_outline_context
from .session_manager import SessionManager

# Type alias for the story state dictionary
StoryState = Dict[str, Any]


def generate_single_chapter_scene_by_scene_node(state: StoryState) -> dict:
    logger = state.get("logger")
    config = state.get("config")
    index = state.get("current_chapter_index", 0)

    if logger:
        logger.info(f"=== NODE: Chapter {index + 1}, Scene-by-Scene Generation ===")

    try:
        if config is None:
            rough_chapter = f"Mock Chapter {index + 1}\n\nConfig was not preserved. Using mock content."
        elif config.mock_mode:
            rough_chapter = f"Mock Chapter {index + 1}\n\nThis is a mock chapter generated for testing purposes. The chapter follows the outline and develops the story further."
            if logger:
                logger.info(f"Using mock chapter {index + 1}")
        else:
            # Simplified chapter generation - just generate a basic chapter
            llm = get_llm_from_uri(config.chapter_s4_model)

            # Create a simple chapter prompt
            chapter_prompt = f"""Generate Chapter {index + 1} for the following story:

Story Elements: {state.get('story_elements', '')}

Outline: {state.get('outline', '')}

Chapter Requirements:
- Continue the story from where it left off
- Include character development and plot progression
- Make it engaging and well-written
- Keep it to a reasonable length (3-5 paragraphs)

Generate the chapter content now:"""

            if logger:
                logger.info(f"Generating chapter {index + 1}...")

            # Generate the chapter
            rough_chapter = llm.invoke(chapter_prompt).content

            if logger:
                logger.save_interaction(
                    f"Chapter_{index+1}_Generation",
                    [{"prompt": chapter_prompt}, {"content": rough_chapter}],
                )

        # Store the generated chapter
        chapters = state.get("chapters", [])
        chapter_data = {
            "content": rough_chapter,
            "current_chapter_text": rough_chapter,
            "chapter_index": state.get("current_chapter_index", 0),
            "chapter_revision_count": 0,
        }
        chapters.append(chapter_data)

        result = {
            "chapters": chapters,
            "current_chapter_text": rough_chapter,
            "chapter_revision_count": 0,
            # Preserve ALL state from previous nodes
            "story_elements": state.get("story_elements", ""),
            "base_context": state.get("base_context", ""),
            "outline": state.get("outline", ""),
            "total_chapters": state.get("total_chapters", 1),
            "current_chapter_index": state.get("current_chapter_index", 0),
            "session_manager": state.get("session_manager"),
            "session_id": state.get("session_id"),
            "config": state.get("config"),
            "logger": state.get("logger"),
            "initial_prompt": state.get("initial_prompt"),
            "retriever": state.get("retriever"),
        }

        # Save checkpoint after successful completion
        session_manager = state.get("session_manager")
        session_id = state.get("session_id")
        if session_manager and session_id and logger:
            session_manager.save_checkpoint(
                session_id,
                "generate_single_chapter_scene_by_scene",
                result,
                metadata={
                    "node_type": "chapter_generation",
                    "success": True,
                    "chapter_index": state.get("current_chapter_index", 0),
                    "chapter_count": len(chapters),
                },
            )
            logger.info(
                f"Checkpoint saved: chapter {state.get('current_chapter_index', 0) + 1} generation"
            )

        return result

    except Exception as e:
        if logger:
            logger.error(f"An error occurred during scene-by-scene generation: {e}")
        chapters = state.get("chapters", [])
        error_chapter = {
            "content": "Could not connect to LLM.",
            "current_chapter_text": "Could not connect to LLM.",
            "chapter_index": state.get("current_chapter_index", 0),
            "chapter_revision_count": 0,
            "error": str(e),
        }
        chapters.append(error_chapter)
        return {
            "chapters": chapters,
            "current_chapter_text": "Could not connect to LLM.",
            "chapter_revision_count": 0,
            "errors": state.get("errors", []) + [str(e)],
            # Preserve ALL state from previous nodes
            "story_elements": state.get("story_elements", ""),
            "base_context": state.get("base_context", ""),
            "outline": state.get("outline", ""),
            "total_chapters": state.get("total_chapters", 1),
            "current_chapter_index": state.get("current_chapter_index", 0),
            "config": state.get("config"),
            "logger": state.get("logger"),
            "initial_prompt": state.get("initial_prompt"),
            "retriever": state.get("retriever"),
            "session_manager": state.get("session_manager"),
            "session_id": state.get("session_id"),
        }


def should_use_scene_generation_pipeline(state: StoryState) -> str:
    return (
        "scene_by_scene"
        if state["config"].scene_generation_pipeline
        else "staged_generation"
    )


def get_chapter_context(state: StoryState) -> dict:
    """Helper function to get context for chapter generation"""
    chapters = state.get("chapters", [])
    last_chapter_summary = ""
    if chapters:
        last_chapter = chapters[-1]
        last_chapter_summary = f"Previous chapter summary: {last_chapter.get('summary', last_chapter.get('content', '')[:200])}"

    return {
        "FormattedLastChapterSummary": last_chapter_summary,
        "_BaseContext": state.get("story_elements", ""),
        "outline": state.get("outline", ""),
        "chapters": chapters,
    }


def generate_story_elements_node(state: StoryState) -> dict:
    """Generate story elements from initial prompt"""
    try:
        logger = state.get("logger")
        config = state.get("config")
        session_manager = state.get("session_manager")
        session_id = state.get("session_id")

        if not logger or not config:
            return {
                "story_elements": "Missing logger or config",
                "errors": state.get("errors", []) + ["Missing logger or config"],
            }

        logger.info("=== NODE: Generating story elements ===")

        if config.mock_mode:
            story_elements = (
                f"Mock Story Elements for: {state['initial_prompt'][:50]}..."
            )
            logger.info("Using mock story elements")
        else:
            llm = get_llm_from_uri(config.initial_outline_model)
            prompt = prompts.STORY_ELEMENTS_PROMPT.format_messages(
                _OutlinePrompt=state["initial_prompt"]
            )
            story_elements = llm.invoke(prompt).content
            logger.save_interaction(
                "01_StoryElements",
                [p.dict() for p in prompt] + [{"content": story_elements}],
            )

        # CRITICAL: Preserve all state from input, add new data
        result = {
            "story_elements": story_elements,
            "base_context": story_elements,
            # Preserve essential state for next nodes
            "config": state["config"],
            "logger": state["logger"],
            "initial_prompt": state["initial_prompt"],
            "retriever": state.get("retriever"),
            "errors": state.get("errors", []),
            "session_manager": state.get("session_manager"),
            "session_id": state.get("session_id"),
        }

        # Save checkpoint after successful completion
        if session_manager and session_id:
            session_manager.save_checkpoint(
                session_id,
                "generate_story_elements",
                result,
                metadata={"node_type": "story_foundation", "success": True},
            )
            logger.info("Checkpoint saved: generate_story_elements")

        return result
    except Exception as e:
        error_msg = f"Error generating story elements: {e}"
        if state.get("logger"):
            state["logger"].error(error_msg)
            state["logger"].error(f"Exception type: {type(e)}")
        import traceback

        traceback.print_exc()
        return {
            "story_elements": "Error generating story elements",
            "errors": state.get("errors", []) + [str(e)],
            # Preserve essential state even on error
            "config": state.get("config"),
            "logger": state.get("logger"),
            "initial_prompt": state.get("initial_prompt"),
            "retriever": state.get("retriever"),
        }


def generate_initial_outline_node(state: StoryState) -> dict:
    """Generate initial story outline"""
    try:
        logger = state.get("logger")
        config = state.get("config")
        retriever = state.get("retriever")

        if not logger or not config:
            return {
                "outline": "Missing logger or config",
                "errors": state.get("errors", []) + ["Missing logger or config"],
            }

        logger.info("=== NODE: Generating initial outline ===")

        if config.mock_mode:
            outline = "Mock Outline\n\nChapter 1: Introduction\nThe story begins...\n\nChapter 2: Development\nThe plot thickens..."
            logger.info("Using mock outline")
        else:
            llm = get_llm_from_uri(config.initial_outline_model)

            # Build prompt context
            context = {
                "_OutlinePrompt": state["initial_prompt"],
                "StoryElements": state.get("story_elements", ""),
                "_BaseContext": state.get("base_context", ""),
                "story_elements": state.get("story_elements", ""),
            }

            # Add RAG context if available
            if retriever and config.outline_rag_enabled:
                try:
                    # Construct queries from prompt and story elements
                    queries = construct_outline_queries(
                        state["initial_prompt"],
                        state.get("story_elements")
                    )
                    
                    # Retrieve context using the queries
                    outline_context = retrieve_outline_context(
                        retriever=retriever,
                        queries=queries,
                        max_tokens=config.outline_context_max_tokens,
                        top_k=config.outline_rag_top_k,
                        similarity_threshold=config.outline_rag_similarity_threshold
                    )
                    
                    if outline_context:
                        context["rag_context"] = outline_context
                        logger.info("Added RAG context to outline generation")
                    else:
                        logger.warning("RAG retrieval returned empty context")
                        
                except Exception as e:
                    error_msg = f"RAG context failed: {e}"
                    logger.error(error_msg)
                    
                    # If knowledge base was explicitly configured, this is a critical error
                    if config.knowledge_base_path and config.embedding_model:
                        logger.error("Knowledge base was configured but RAG failed - aborting generation")
                        return {
                            "outline": "",
                            "errors": state.get("errors", []) + [error_msg],
                            "story_elements": state.get("story_elements", ""),
                            "base_context": state.get("base_context", ""),
                            "config": state["config"],
                            "logger": state["logger"],
                            "initial_prompt": state["initial_prompt"],
                            "retriever": state.get("retriever"),
                            "session_manager": state.get("session_manager"),
                        }
                    else:
                        # If RAG was opportunistic (not explicitly configured), continue without it
                        logger.warning(f"{error_msg} - continuing without RAG context")

            # Generate outline using the correct prompt template
            prompt_template = prompts.INITIAL_OUTLINE_PROMPT
            prompt = prompt_template.format_messages(**context)
            outline = llm.invoke(prompt).content
            logger.save_interaction(
                "02_InitialOutline", [p.dict() for p in prompt] + [{"content": outline}]
            )

        result = {
            "outline": outline,
            # Preserve ALL essential state from previous nodes
            "story_elements": state.get("story_elements", ""),
            "base_context": state.get("base_context", ""),
            "config": state["config"],
            "logger": state["logger"],
            "initial_prompt": state["initial_prompt"],
            "retriever": state.get("retriever"),
            "errors": state.get("errors", []),
            "session_manager": state.get("session_manager"),
            "session_id": state.get("session_id"),
        }

        # Save checkpoint after successful completion
        session_manager = state.get("session_manager")
        session_id = state.get("session_id")
        if session_manager and session_id:
            session_manager.save_checkpoint(
                session_id,
                "generate_initial_outline",
                result,
                metadata={
                    "node_type": "story_structure",
                    "success": True,
                    "rag_enabled": config.outline_rag_enabled,
                },
            )
            if logger:
                logger.info("Checkpoint saved: generate_initial_outline")

        return result
    except Exception as e:
        error_msg = f"Error generating outline: {e}"
        if state.get("logger"):
            state["logger"].error(error_msg)
            state["logger"].error(f"Exception type: {type(e)}")
        import traceback

        traceback.print_exc()
        return {
            "outline": "Error generating outline",
            "errors": state.get("errors", []) + [str(e)],
            # Preserve essential state even on error
            "story_elements": state.get("story_elements", ""),
            "base_context": state.get("base_context", ""),
            "config": state.get("config"),
            "logger": state.get("logger"),
            "initial_prompt": state.get("initial_prompt"),
            "retriever": state.get("retriever"),
        }


def determine_chapter_count_node(state: StoryState) -> dict:
    """Determine how many chapters the story should have"""
    try:
        logger = state.get("logger")

        if logger:
            logger.info("=== NODE: Determining chapter count ===")

        # More sophisticated chapter count determination
        outline = state.get("outline", "")
        chapter_count = 0

        # Look for various chapter/section markers
        import re

        # Count "Chapter X" patterns
        chapter_count = max(
            chapter_count, len(re.findall(r"Chapter\s*\d+", outline, re.IGNORECASE))
        )
        # Count "# Chapter" markdown headers
        chapter_count = max(
            chapter_count, len(re.findall(r"#+\s*Chapter", outline, re.IGNORECASE))
        )
        # Count "Act" markers (3-act structure)
        act_count = len(re.findall(r"Act\s*[IVX\d]+", outline, re.IGNORECASE))
        if act_count > 0 and chapter_count == 0:
            chapter_count = act_count
        # Count numbered sections like "1.", "2.", etc. at start of lines
        numbered_sections = len(re.findall(r"^\s*\d+\.", outline, re.MULTILINE))
        if numbered_sections > chapter_count:
            chapter_count = numbered_sections
        # Count markdown headers with Roman numerals
        roman_count = len(re.findall(r"#+\s*[IVX]+\.", outline))
        if roman_count > chapter_count:
            chapter_count = roman_count
        # Look for "Part" markers
        part_count = len(re.findall(r"Part\s*[IVX\d]+", outline, re.IGNORECASE))
        if part_count > chapter_count:
            chapter_count = part_count

        # Default to 3 chapters if nothing found (reasonable story length)
        if chapter_count == 0:
            chapter_count = 3

        if logger:
            logger.info(f"Determined chapter count: {chapter_count}")
        result = {
            "total_chapters": chapter_count,
            "current_chapter_index": 0,
            "chapters": [],
            # Preserve state from previous nodes
            "story_elements": state.get("story_elements", ""),
            "base_context": state.get("base_context", ""),
            "outline": state.get("outline", ""),
            "session_manager": state.get("session_manager"),
            "session_id": state.get("session_id"),
            "config": state.get("config"),
            "logger": state.get("logger"),
            "initial_prompt": state.get("initial_prompt"),
            "retriever": state.get("retriever"),
        }

        # Save checkpoint after successful completion
        session_manager = state.get("session_manager")
        session_id = state.get("session_id")
        if session_manager and session_id and logger:
            session_manager.save_checkpoint(
                session_id,
                "determine_chapter_count",
                result,
                metadata={
                    "node_type": "story_planning",
                    "success": True,
                    "chapter_count": chapter_count,
                },
            )
            logger.info(
                f"Checkpoint saved: determine_chapter_count (chapters: {chapter_count})"
            )

        return result
    except Exception as e:
        if state.get("logger"):
            state["logger"].error(f"Error determining chapter count: {e}")
        return {
            "total_chapters": 1,
            "current_chapter_index": 0,
            "chapters": [],
            "errors": state.get("errors", []) + [str(e)],
            # Preserve state from previous nodes
            "story_elements": state.get("story_elements", ""),
            "base_context": state.get("base_context", ""),
            "outline": state.get("outline", ""),
        }


def generate_final_story_node(state: StoryState) -> dict:
    """Combine all chapters into final story"""
    logger = state.get("logger")
    if logger:
        logger.info("Generating final story...")

    try:
        chapters = state.get("chapters", [])
        story_elements = state.get("story_elements", "")
        outline = state.get("outline", "")

        # Combine all chapters
        final_story = f"# Story\n\n{story_elements}\n\n## Outline\n{outline}\n\n"

        for i, chapter in enumerate(chapters):
            final_story += f"## Chapter {i+1}\n\n"
            chapter_content = chapter.get(
                "content", chapter.get("current_chapter_text", "")
            )
            final_story += chapter_content + "\n\n"

        # Generate story metadata
        story_info = {
            "title": "Generated Story",
            "summary": "A story generated by WillWrite",
            "tags": "fiction, generated",
            "overall_rating": 7,
        }

        return {
            "final_story_markdown": final_story,
            "story_info": story_info,
            "is_complete": True,
        }
    except Exception as e:
        logger.error(f"Error generating final story: {e}")
        return {"errors": state.get("errors", []) + [str(e)]}


def check_if_more_chapters_needed(state: StoryState) -> str:
    """Check if we need to generate more chapters"""
    current_index = state.get("current_chapter_index", 0)
    total_chapters = state.get("total_chapters", 3)
    chapters = state.get("chapters", [])

    # Debug logging
    logger = state.get("logger")
    if logger:
        logger.info(
            f"Checking chapters: current={current_index}, total={total_chapters}, chapters_generated={len(chapters)}"
        )

    # Safety check - prevent infinite loops
    if current_index > 20:  # Safety limit - increased for longer stories
        if logger:
            logger.error(f"Safety limit reached: current_index={current_index}")
        return "finalize"

    if current_index >= total_chapters:
        if logger:
            logger.info(
                f"Finished generating all chapters: {current_index} >= {total_chapters}"
            )
        return "finalize"
    else:
        if logger:
            logger.info(f"Need more chapters: {current_index} < {total_chapters}")
        return "generate_chapter"


def increment_chapter_index_node(state: StoryState) -> dict:
    """Move to the next chapter"""
    current_index = state.get("current_chapter_index", 0)
    new_index = current_index + 1

    logger = state.get("logger")
    if logger:
        logger.info(
            f"=== NODE: Incrementing chapter index: {current_index} -> {new_index} ==="
        )

    # IMPORTANT: Preserve all necessary state, not just the new index
    result = {
        "current_chapter_index": new_index,
        "total_chapters": state.get("total_chapters", 1),
        "chapters": state.get("chapters", []),
        "story_elements": state.get("story_elements", ""),
        "outline": state.get("outline", ""),
        "base_context": state.get("base_context", ""),
        "session_manager": state.get("session_manager"),
        "session_id": state.get("session_id"),
        "config": state.get("config"),
        "logger": state.get("logger"),
        "initial_prompt": state.get("initial_prompt"),
        "retriever": state.get("retriever"),
    }

    # Save checkpoint after index increment
    session_manager = state.get("session_manager")
    session_id = state.get("session_id")
    if session_manager and session_id and logger:
        session_manager.save_checkpoint(
            session_id,
            "increment_chapter_index",
            result,
            metadata={
                "node_type": "chapter_progression",
                "success": True,
                "new_chapter_index": new_index,
                "total_chapters": state.get("total_chapters", 1),
            },
        )
        logger.info(
            f"Checkpoint saved: increment_chapter_index (now at chapter {new_index + 1})"
        )

    return result


def create_graph(config=None, session_id=None, session_manager=None, retriever=None):
    """Create the main story generation workflow graph"""

    workflow = StateGraph(dict)

    # Add nodes
    workflow.add_node("generate_story_elements", generate_story_elements_node)
    workflow.add_node("generate_initial_outline", generate_initial_outline_node)
    workflow.add_node("determine_chapter_count", determine_chapter_count_node)
    workflow.add_node(
        "generate_single_chapter_scene_by_scene",
        generate_single_chapter_scene_by_scene_node,
    )
    workflow.add_node("increment_chapter_index", increment_chapter_index_node)
    workflow.add_node("generate_final_story", generate_final_story_node)

    # Set entry point
    workflow.set_entry_point("generate_story_elements")

    # Add edges
    workflow.add_edge("generate_story_elements", "generate_initial_outline")
    workflow.add_edge("generate_initial_outline", "determine_chapter_count")
    workflow.add_edge(
        "determine_chapter_count", "generate_single_chapter_scene_by_scene"
    )
    workflow.add_edge(
        "generate_single_chapter_scene_by_scene", "increment_chapter_index"
    )

    # Add conditional edge for chapter generation
    workflow.add_conditional_edges(
        "increment_chapter_index",
        check_if_more_chapters_needed,
        {
            "generate_chapter": "generate_single_chapter_scene_by_scene",
            "finalize": "generate_final_story",
        },
    )

    workflow.add_edge("generate_final_story", END)

    return workflow.compile()


def create_resume_graph(
    session_manager: SessionManager, session_id: str, resume_from_node: str = None
):
    """Create a graph configured for resuming from a specific checkpoint"""

    # Get resume entry point
    if resume_from_node is None:
        resume_from_node = session_manager.get_resume_entry_point(session_id)

    workflow = StateGraph(dict)

    # Add all nodes
    workflow.add_node("generate_story_elements", generate_story_elements_node)
    workflow.add_node("generate_initial_outline", generate_initial_outline_node)
    workflow.add_node("determine_chapter_count", determine_chapter_count_node)
    workflow.add_node(
        "generate_single_chapter_scene_by_scene",
        generate_single_chapter_scene_by_scene_node,
    )
    workflow.add_node("increment_chapter_index", increment_chapter_index_node)
    workflow.add_node("generate_final_story", generate_final_story_node)

    # Set dynamic entry point based on resume location
    workflow.set_entry_point(resume_from_node)

    # Add conditional edges based on entry point
    if resume_from_node in [
        "generate_story_elements",
        "generate_initial_outline",
        "determine_chapter_count",
    ]:
        # Standard workflow from the resume point
        if resume_from_node != "generate_initial_outline":
            workflow.add_edge("generate_story_elements", "generate_initial_outline")
        if resume_from_node != "determine_chapter_count":
            workflow.add_edge("generate_initial_outline", "determine_chapter_count")
        workflow.add_edge(
            "determine_chapter_count", "generate_single_chapter_scene_by_scene"
        )
    elif resume_from_node in [
        "generate_single_chapter_scene_by_scene",
        "increment_chapter_index",
    ]:
        # Resume from chapter generation
        workflow.add_edge(
            "generate_single_chapter_scene_by_scene", "increment_chapter_index"
        )
        workflow.add_conditional_edges(
            "increment_chapter_index",
            check_if_more_chapters_needed,
            {
                "generate_chapter": "generate_single_chapter_scene_by_scene",
                "finalize": "generate_final_story",
            },
        )

    # Always add edge to final story generation
    workflow.add_edge("increment_chapter_index", "generate_final_story")
    workflow.add_edge("generate_final_story", END)

    return workflow.compile()


def load_state_from_session(
    session_manager: SessionManager, session_id: str, config, logger, retriever=None
) -> Dict[str, Any]:
    """Load and reconstruct state from a saved session"""

    try:
        # Load session info
        session_info = session_manager.load_session_info(session_id)

        # Load the latest checkpoint state
        checkpoint_state = session_manager.load_session_state(session_id)

        # Reconstruct full state for resume
        resume_state = {
            # Add runtime objects that can't be serialized
            "config": config,
            "logger": logger,
            "session_manager": session_manager,
            "session_id": session_id,
            "retriever": retriever,
            # Load saved state
            **checkpoint_state,
        }

        # Ensure we have essential fields
        if "initial_prompt" not in resume_state:
            # Try to reconstruct from session configuration
            resume_state["initial_prompt"] = f"Resumed from session {session_id}"

        logger.info(
            f"Loaded state from session {session_id} with {len(session_info.checkpoints)} checkpoints"
        )
        return resume_state

    except Exception as e:
        logger.error(f"Failed to load state from session {session_id}: {e}")
        raise
