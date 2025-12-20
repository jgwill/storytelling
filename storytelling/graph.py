from typing import Any, Dict

from langgraph.graph import END, StateGraph

from . import prompts
from .llm_providers import get_llm_from_uri
from .rag import construct_outline_queries, retrieve_outline_context, retrieve_chapter_context
from .session_manager import SessionManager

# Type alias for the story state dictionary
StoryState = Dict[str, Any]


def generate_single_chapter_scene_by_scene_node(state: StoryState) -> dict:
    logger = state.get("logger")
    config = state.get("config")
    retriever = state.get("retriever")
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
            llm = get_llm_from_uri(config.chapter_s4_model)

            # Retrieve chapter-specific RAG context
            chapter_context = ""
            if retriever and getattr(config, 'chapter_rag_enabled', True):
                if logger:
                    logger.info(f"Retrieving knowledge base context for chapter {index + 1}")

                # Get previous chapter summary for continuity
                previous_summary = ""
                chapters = state.get("chapters", [])
                if chapters and index > 0:
                    prev_chapter = chapters[index - 1]
                    previous_summary = prev_chapter.get("summary", prev_chapter.get("content", "")[:300])

                try:
                    chapter_context = retrieve_chapter_context(
                        retriever=retriever,
                        chapter_outline=state.get("outline", ""),
                        chapter_number=index + 1,
                        previous_chapter_summary=previous_summary,
                        story_elements=state.get("story_elements"),
                        max_tokens=getattr(config, 'chapter_context_max_tokens', 1500),
                        top_k=getattr(config, 'chapter_rag_top_k', 8),
                    )

                    if chapter_context and logger:
                        logger.info(f"Retrieved chapter context: {len(chapter_context)} characters")
                except Exception as e:
                    if logger:
                        logger.warning(f"Failed to retrieve chapter context: {e}")

            # Create a chapter prompt with RAG context
            rag_instruction = ""
            if chapter_context:
                rag_instruction = f"""
## Knowledge Base Context
Use the following knowledge base content to ground your narrative in established lore, character details, and world-building. Integrate these elements naturally into the story:

{chapter_context}

---
"""

            chapter_prompt = f"""Generate Chapter {index + 1} for the following story:

{rag_instruction}
Story Elements: {state.get('story_elements', '')}

Outline: {state.get('outline', '')}

Chapter Requirements:
- Continue the story from where it left off
- Include character development and plot progression
- Integrate knowledge base themes and elements naturally into the narrative
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


def critique_chapter_node(state: StoryState) -> dict:
    """Critique the current chapter using CRITIC_CHAPTER_PROMPT with optional RAG context"""
    logger = state.get("logger")
    config = state.get("config")
    retriever = state.get("retriever")

    if logger:
        chapter_index = state.get("current_chapter_index", 0)
        revision_count = state.get("chapter_revision_count", 0)
        logger.info(f"=== NODE: Critiquing Chapter {chapter_index + 1} (revision {revision_count}) ===")

    try:
        current_chapter = state.get("current_chapter_text", "")

        if not current_chapter:
            if logger:
                logger.warning("No chapter content to critique")
            return {
                **_preserve_state(state, exclude=["chapter_feedback"]),
                "chapter_feedback": "",
            }

        if config and config.mock_mode:
            feedback = "Mock feedback: The chapter is well-written with good pacing."
            if logger:
                logger.info("Using mock chapter feedback")
        else:
            # Retrieve RAG context for critique
            critique_context = ""
            if retriever and getattr(config, 'chapter_rag_enabled', True):
                try:
                    critique_context = retrieve_chapter_context(
                        retriever=retriever,
                        chapter_outline=current_chapter[:500],  # Use beginning of chapter
                        chapter_number=state.get("current_chapter_index", 0) + 1,
                        story_elements=state.get("story_elements"),
                        max_tokens=1000,  # Smaller context for critique
                        top_k=5,
                    )
                    if critique_context and logger:
                        logger.info(f"Retrieved critique context: {len(critique_context)} characters")
                except Exception as e:
                    if logger:
                        logger.warning(f"Failed to retrieve critique context: {e}")

            llm = get_llm_from_uri(config.chapter_revision_model)
            
            # Build critique prompt with RAG context
            if critique_context:
                enhanced_chapter = f"""<RAG_REFERENCE>
{critique_context}
</RAG_REFERENCE>

{current_chapter}"""
                prompt = prompts.CRITIC_CHAPTER_PROMPT.format_messages(_Chapter=enhanced_chapter)
            else:
                prompt = prompts.CRITIC_CHAPTER_PROMPT.format_messages(_Chapter=current_chapter)
            
            feedback = llm.invoke(prompt).content

            if logger:
                logger.save_interaction(
                    f"Chapter_{state.get('current_chapter_index', 0) + 1}_Critique_Rev{state.get('chapter_revision_count', 0)}",
                    [p.dict() for p in prompt] + [{"content": feedback}],
                )

        result = {
            **_preserve_state(state, exclude=["chapter_feedback"]),
            "chapter_feedback": feedback,
        }

        # Save checkpoint
        session_manager = state.get("session_manager")
        session_id = state.get("session_id")
        if session_manager and session_id and logger:
            session_manager.save_checkpoint(
                session_id,
                "critique_chapter",
                result,
                metadata={
                    "node_type": "chapter_critique",
                    "success": True,
                    "chapter_index": state.get("current_chapter_index", 0),
                    "revision_count": state.get("chapter_revision_count", 0),
                },
            )
            logger.info(f"Checkpoint saved: chapter critique")

        return result

    except Exception as e:
        if logger:
            logger.error(f"Error critiquing chapter: {e}")
        return {
            **_preserve_state(state, exclude=["chapter_feedback"]),
            "chapter_feedback": "",
            "errors": state.get("errors", []) + [str(e)],
        }


def check_chapter_complete_node(state: StoryState) -> dict:
    """Check if chapter meets completion criteria using CHAPTER_COMPLETE_PROMPT"""
    logger = state.get("logger")
    config = state.get("config")

    if logger:
        logger.info("=== NODE: Checking chapter completion ===")

    try:
        current_chapter = state.get("current_chapter_text", "")

        if config and config.mock_mode:
            is_complete = True
            if logger:
                logger.info("Mock mode: chapter marked complete")
        else:
            import json
            llm = get_llm_from_uri(config.chapter_revision_model)
            prompt = prompts.CHAPTER_COMPLETE_PROMPT.format_messages(_Chapter=current_chapter)
            response = llm.invoke(prompt).content

            # Parse JSON response
            try:
                # Handle potential markdown code blocks
                response_clean = response.strip()
                if response_clean.startswith("```"):
                    response_clean = response_clean.split("```")[1]
                    if response_clean.startswith("json"):
                        response_clean = response_clean[4:]
                    response_clean = response_clean.strip()

                result_json = json.loads(response_clean)
                is_complete = result_json.get("is_complete", False)
            except json.JSONDecodeError:
                if logger:
                    logger.warning(f"Failed to parse completion response: {response}")
                is_complete = False

            if logger:
                logger.save_interaction(
                    f"Chapter_{state.get('current_chapter_index', 0) + 1}_Complete_Check",
                    [p.dict() for p in prompt] + [{"content": response}],
                )

        result = {
            **_preserve_state(state, exclude=["chapter_is_complete"]),
            "chapter_is_complete": is_complete,
        }

        if logger:
            logger.info(f"Chapter completion check: {is_complete}")

        return result

    except Exception as e:
        if logger:
            logger.error(f"Error checking chapter completion: {e}")
        return {
            **_preserve_state(state, exclude=["chapter_is_complete"]),
            "chapter_is_complete": True,  # Default to complete on error to prevent infinite loops
            "errors": state.get("errors", []) + [str(e)],
        }


def revise_chapter_node(state: StoryState) -> dict:
    """Revise the current chapter based on feedback using CHAPTER_REVISION prompt with optional RAG context"""
    logger = state.get("logger")
    config = state.get("config")
    retriever = state.get("retriever")
    revision_count = state.get("chapter_revision_count", 0)

    if logger:
        chapter_index = state.get("current_chapter_index", 0)
        logger.info(f"=== NODE: Revising Chapter {chapter_index + 1} (revision {revision_count + 1}) ===")

    try:
        current_chapter = state.get("current_chapter_text", "")
        feedback = state.get("chapter_feedback", "")

        if not feedback:
            if logger:
                logger.warning("No feedback provided for revision")
            return {
                **_preserve_state(state),
                "chapter_revision_count": revision_count,
            }

        if config and config.mock_mode:
            revised_chapter = f"{current_chapter}\n\n[Mock revision {revision_count + 1} applied based on feedback]"
            if logger:
                logger.info(f"Using mock chapter revision {revision_count + 1}")
        else:
            # Retrieve RAG context for revision
            revision_context = ""
            if retriever and getattr(config, 'chapter_rag_enabled', True):
                try:
                    revision_context = retrieve_chapter_context(
                        retriever=retriever,
                        chapter_outline=current_chapter[:500],
                        chapter_number=state.get("current_chapter_index", 0) + 1,
                        story_elements=state.get("story_elements"),
                        max_tokens=1000,
                        top_k=5,
                    )
                    if revision_context and logger:
                        logger.info(f"Retrieved revision context: {len(revision_context)} characters")
                except Exception as e:
                    if logger:
                        logger.warning(f"Failed to retrieve revision context: {e}")

            llm = get_llm_from_uri(config.chapter_revision_model)
            
            # Build revision prompt with RAG context
            if revision_context:
                enhanced_feedback = f"""Reference the following knowledge base content to improve the chapter:

{revision_context}

---
Original Feedback:
{feedback}"""
                prompt = prompts.CHAPTER_REVISION.format_messages(
                    _Chapter=current_chapter,
                    _Feedback=enhanced_feedback
                )
            else:
                prompt = prompts.CHAPTER_REVISION.format_messages(
                    _Chapter=current_chapter,
                    _Feedback=feedback
                )
            
            revised_chapter = llm.invoke(prompt).content

            if logger:
                logger.save_interaction(
                    f"Chapter_{state.get('current_chapter_index', 0) + 1}_Revision_{revision_count + 1}",
                    [p.dict() for p in prompt] + [{"content": revised_chapter}],
                )

        # Update the chapter in the chapters list
        chapters = state.get("chapters", [])
        current_index = state.get("current_chapter_index", 0)
        if chapters and current_index < len(chapters):
            chapters[current_index]["content"] = revised_chapter
            chapters[current_index]["current_chapter_text"] = revised_chapter
            chapters[current_index]["chapter_revision_count"] = revision_count + 1

        result = {
            **_preserve_state(state, exclude=["chapters", "current_chapter_text", "chapter_revision_count", "chapter_feedback"]),
            "chapters": chapters,
            "current_chapter_text": revised_chapter,
            "chapter_revision_count": revision_count + 1,
            "chapter_feedback": "",  # Clear feedback after revision
        }

        # Save checkpoint
        session_manager = state.get("session_manager")
        session_id = state.get("session_id")
        if session_manager and session_id and logger:
            session_manager.save_checkpoint(
                session_id,
                "revise_chapter",
                result,
                metadata={
                    "node_type": "chapter_revision",
                    "success": True,
                    "chapter_index": current_index,
                    "revision_count": revision_count + 1,
                },
            )
            logger.info(f"Checkpoint saved: chapter revision {revision_count + 1}")

        return result

    except Exception as e:
        if logger:
            logger.error(f"Error revising chapter: {e}")
        return {
            **_preserve_state(state),
            "errors": state.get("errors", []) + [str(e)],
        }


def should_revise_chapter(state: StoryState) -> str:
    """Determine if chapter needs more revisions based on min/max revisions and completion check"""
    config = state.get("config")
    logger = state.get("logger")
    revision_count = state.get("chapter_revision_count", 0)
    is_complete = state.get("chapter_is_complete", False)

    # Get revision limits from config
    min_revisions = getattr(config, "chapter_min_revisions", 1) if config else 1
    max_revisions = getattr(config, "chapter_max_revisions", 3) if config else 3

    if logger:
        logger.info(
            f"Revision check: count={revision_count}, min={min_revisions}, max={max_revisions}, is_complete={is_complete}"
        )

    # Always revise if below minimum
    if revision_count < min_revisions:
        if logger:
            logger.info(f"Below minimum revisions ({revision_count} < {min_revisions}), revising")
        return "revise"

    # Stop if at maximum
    if revision_count >= max_revisions:
        if logger:
            logger.info(f"Reached maximum revisions ({revision_count} >= {max_revisions}), moving on")
        return "increment"

    # Between min and max: revise if not complete
    if not is_complete:
        if logger:
            logger.info(f"Chapter not complete and below max revisions, revising")
        return "revise"

    if logger:
        logger.info(f"Chapter complete after {revision_count} revisions, moving on")
    return "increment"


def _preserve_state(state: StoryState, exclude: list = None) -> dict:
    """Helper to preserve all essential state fields"""
    exclude = exclude or []
    preserved = {
        "story_elements": state.get("story_elements", ""),
        "base_context": state.get("base_context", ""),
        "outline": state.get("outline", ""),
        "total_chapters": state.get("total_chapters", 1),
        "current_chapter_index": state.get("current_chapter_index", 0),
        "chapters": state.get("chapters", []),
        "current_chapter_text": state.get("current_chapter_text", ""),
        "chapter_revision_count": state.get("chapter_revision_count", 0),
        "chapter_feedback": state.get("chapter_feedback", ""),
        "chapter_is_complete": state.get("chapter_is_complete", False),
        "session_manager": state.get("session_manager"),
        "session_id": state.get("session_id"),
        "config": state.get("config"),
        "logger": state.get("logger"),
        "initial_prompt": state.get("initial_prompt"),
        "retriever": state.get("retriever"),
    }
    return {k: v for k, v in preserved.items() if k not in exclude}


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
    # Chapter revision loop nodes
    workflow.add_node("critique_chapter", critique_chapter_node)
    workflow.add_node("check_chapter_complete", check_chapter_complete_node)
    workflow.add_node("revise_chapter", revise_chapter_node)
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

    # Chapter revision loop:
    # generate_chapter → critique → check_complete → [revise → critique] OR increment
    workflow.add_edge(
        "generate_single_chapter_scene_by_scene", "critique_chapter"
    )
    workflow.add_edge("critique_chapter", "check_chapter_complete")

    # Conditional: should we revise or move to next chapter?
    workflow.add_conditional_edges(
        "check_chapter_complete",
        should_revise_chapter,
        {
            "revise": "revise_chapter",
            "increment": "increment_chapter_index",
        },
    )

    # After revision, go back to critique for another round
    workflow.add_edge("revise_chapter", "critique_chapter")

    # Add conditional edge for chapter generation loop
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
    # Chapter revision loop nodes
    workflow.add_node("critique_chapter", critique_chapter_node)
    workflow.add_node("check_chapter_complete", check_chapter_complete_node)
    workflow.add_node("revise_chapter", revise_chapter_node)
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

    # Chapter revision loop edges (needed for all chapter-related resume points)
    if resume_from_node in [
        "determine_chapter_count",
        "generate_single_chapter_scene_by_scene",
        "critique_chapter",
        "check_chapter_complete",
        "revise_chapter",
        "increment_chapter_index",
    ]:
        workflow.add_edge(
            "generate_single_chapter_scene_by_scene", "critique_chapter"
        )
        workflow.add_edge("critique_chapter", "check_chapter_complete")
        workflow.add_conditional_edges(
            "check_chapter_complete",
            should_revise_chapter,
            {
                "revise": "revise_chapter",
                "increment": "increment_chapter_index",
            },
        )
        workflow.add_edge("revise_chapter", "critique_chapter")
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
