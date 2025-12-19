"""Command line interface for storytelling package."""

import argparse
import os
import sys
import time
from typing import List, Optional

from . import __version__
from .config import load_config
from .logger import Logger
from .session_manager import SessionManager, migrate_existing_session

# Import core only if available (for compatibility)
try:
    from .core import Story

    SIMPLE_MODE = False
except ImportError:
    SIMPLE_MODE = True
    Story = None

# Advanced components (optional)
try:
    from .graph import (
        create_graph,
        create_resume_graph,
        load_state_from_session,
    )
    from .rag import initialize_knowledge_base

    ADVANCED_MODE = True
except ImportError:
    ADVANCED_MODE = False


def parse_session_arguments():
    """Parse session management arguments only"""
    parser = argparse.ArgumentParser(
        description="Storytelling - AI Story Generation System", add_help=False
    )

    # Session management commands
    parser.add_argument("--resume", type=str, help="Resume from session ID")
    parser.add_argument(
        "--resume-from-node", type=str, help="Resume from specific node"
    )
    parser.add_argument(
        "--list-sessions", action="store_true", help="List available sessions"
    )
    parser.add_argument(
        "--session-info", type=str, help="Show information about a session"
    )
    parser.add_argument(
        "--migrate-session", type=str, help="Migrate existing session to new format"
    )

    # Parse only known session args, ignore the rest
    args, remaining = parser.parse_known_args()
    return args, remaining


def list_sessions(session_manager: SessionManager):
    """List all available sessions"""
    sessions = session_manager.list_sessions()

    if not sessions:
        print("No sessions found.")
        return

    print(f"Found {len(sessions)} sessions:")
    print("-" * 80)
    for session in sessions:
        status_icon = {
            "completed": "✅",
            "in_progress": "🔄",
            "failed": "❌",
            "interrupted": "⏸️",
        }.get(session.status, "❓")
        print(f"{status_icon} {session.session_id}")
        print(f"   Created: {session.created_at}")
        print(f"   Status: {session.status}")
        print(f"   Prompt: {session.prompt_file}")
        print(f"   Checkpoints: {len(session.checkpoints)}")
        if session.checkpoints:
            print(f"   Last checkpoint: {session.checkpoints[-1].node_name}")
        print()


def show_session_info(session_manager: SessionManager, session_id: str):
    """Show detailed information about a session"""
    try:
        session_info = session_manager.load_session_info(session_id)
        checkpoints = session_manager.list_checkpoints(session_id)

        print(f"Session: {session_id}")
        print("-" * 50)
        print(f"Created: {session_info.created_at}")
        print(f"Status: {session_info.status}")
        print(f"Prompt: {session_info.prompt_file}")
        print(f"Output: {session_info.output_file}")
        print(f"Last checkpoint: {session_info.last_checkpoint}")
        print()
        print(f"Checkpoints ({len(checkpoints)}):")
        for i, cp in enumerate(checkpoints):
            print(f"  {i+1}. {cp.node_name} ({cp.timestamp})")

        if checkpoints:
            resume_entry = session_manager.get_resume_entry_point(session_id)
            print(f"\nSuggested resume point: {resume_entry}")

    except Exception as e:
        print(f"Error loading session info: {e}")


def create_story(args: argparse.Namespace) -> None:
    """Create a new story using simple mode."""
    if not SIMPLE_MODE or not Story:
        print("Simple story creation not available. Please use advanced mode.")
        return

    story = Story(args.title, args.content or "")
    if args.author:
        story.set_metadata("author", args.author)
    if args.genre:
        story.set_metadata("genre", args.genre)

    print(f"Created story: {story}")
    if story.content:
        print(f"Content preview: {story.content[:100]}...")


def main(argv: Optional[List[str]] = None) -> int:
    """Main CLI entry point with advanced story generation support."""
    if not ADVANCED_MODE:
        return simple_main(argv)

    start_time = time.time()

    # Parse session management arguments first
    session_args, remaining_args = parse_session_arguments()

    # Initialize session manager
    session_manager = SessionManager()

    # Handle session management commands
    if session_args.list_sessions:
        list_sessions(session_manager)
        return 0

    if session_args.session_info:
        show_session_info(session_manager, session_args.session_info)
        return 0

    if session_args.migrate_session:
        try:
            session_info = migrate_existing_session(
                "Logs", session_args.migrate_session
            )
            print(f"Successfully migrated session {session_args.migrate_session}")
            print(f"Session status: {session_info.status}")
            print(f"Checkpoints: {len(session_info.checkpoints)}")
        except Exception as e:
            print(f"Error migrating session: {e}")
            return 1
        return 0

    # Handle resume operations
    if session_args.resume or session_args.resume_from_node:
        if not session_args.resume:
            print("Error: --resume-from-node requires --resume SESSION_ID")
            return 1

        try:
            # Load session info and state
            session_info = session_manager.load_session_info(session_args.resume)

            # Parse the remaining config arguments with the original argv
            config = load_config()

            print(f"Resuming session {session_args.resume}...")
            print(f"Original prompt: {session_info.prompt_file}")
            print(f"Session status: {session_info.status}")

            # Determine resume entry point
            if session_args.resume_from_node:
                resume_node = session_args.resume_from_node
            else:
                resume_node = session_manager.get_resume_entry_point(
                    session_args.resume
                )

            print(f"Resuming from node: {resume_node}")

            # Load session state
            try:
                # Initialize logger for resume
                logger = Logger(config)
                loaded_state = load_state_from_session(
                    session_manager, session_args.resume, config, logger
                )
                print(f"Loaded state from session with {len(loaded_state)} keys")
            except Exception as e:
                print(f"Warning: Could not load full session state: {e}")
                loaded_state = {}

            # Update session status
            session_manager.update_session_status(session_args.resume, "in_progress")

            # Create resume graph
            graph = create_resume_graph(
                session_manager, session_args.resume, resume_node
            )

            # Initialize state for resume
            initial_state = loaded_state if loaded_state else {}
            initial_state["session_id"] = session_args.resume

            # Run the graph
            final_state = graph.invoke(initial_state)

            # Write the final story to output file if completed
            if final_state.get("status") == "completed" or (
                session_info.status == "completed"
            ):
                if (
                    "final_story_markdown" in final_state
                    and final_state["final_story_markdown"]
                ):
                    try:
                        output_path = session_info.output_file
                        with open(output_path, "w", encoding="utf-8") as f:
                            f.write(final_state["final_story_markdown"])
                        print(f"Story written to: {output_path}")
                    except Exception as e:
                        print(f"Error writing output file: {e}")
                        return 1

            print("\nSession resumed successfully!")
            print(
                "Final status: Session completed"
                if final_state.get("status") == "completed"
                else "Session in progress"
            )

        except Exception as e:
            print(f"Error resuming session: {e}")
            session_manager.update_session_status(session_args.resume, "failed")
            return 1

        return 0

    # Standard generation workflow
    try:
        config = load_config()
    except SystemExit:
        return 1

    # Validate required arguments
    if not config.prompt_file:
        print("Error: --prompt is required for story generation")
        return 1

    if not os.path.exists(config.prompt_file):
        print(f"Error: Prompt file '{config.prompt_file}' not found")
        return 1

    # Initialize logger
    logger = Logger(config)
    logger.info("Starting story generation...")

    # Create new session
    session_id = session_manager.create_session(
        prompt_file=config.prompt_file,
        output_file=config.output_file or f"story_output_{int(time.time())}",
        config=config.model_dump(),
    )

    logger.info(f"Created session: {session_id}")

    # Initialize RAG if knowledge base is provided
    retriever = None
    if config.knowledge_base_path and config.embedding_model:
        try:
            retriever = initialize_knowledge_base(
                config.knowledge_base_path,
                config.embedding_model,
                config.ollama_base_url,
                config.outline_rag_top_k,  # Pass the configured top_k value
            )
            logger.info(f"Initialized knowledge base from {config.knowledge_base_path}")
        except ImportError as e:
            logger.error(f"Missing dependency for knowledge base: {e}")
            return 1
        except Exception as e:
            logger.warning(f"Could not initialize knowledge base: {e}")

    try:
        # Create and run the workflow graph
        graph = create_graph(config, session_id, session_manager, retriever)

        # Load prompt
        with open(config.prompt_file, encoding="utf-8") as f:
            initial_prompt = f.read().strip()

        # Initialize state
        initial_state = {
            "initial_prompt": initial_prompt,
            "session_id": session_id,
            "config": config,
            "logger": logger,
            "session_manager": session_manager,
            "retriever": retriever,
        }

        # Run the graph with increased recursion limit for longer stories
        final_state = graph.invoke(initial_state, {"recursion_limit": 50})

        # Write the final story to output file
        if (
            "final_story_markdown" in final_state
            and final_state["final_story_markdown"]
        ):
            try:
                output_path = config.output_file
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(final_state["final_story_markdown"])
                logger.info(f"Story written to: {output_path}")
            except Exception as e:
                logger.error(f"Failed to write output file: {e}")
                return 1
        else:
            logger.error("No final story generated (final_story_markdown not in state)")
            return 1

        # Update session status
        session_manager.update_session_status(session_id, "completed")

        logger.info("Story generation completed successfully!")
        logger.info(f"Session: {session_id}")

        execution_time = time.time() - start_time
        logger.info(f"Total execution time: {execution_time:.2f} seconds")

    except KeyboardInterrupt:
        logger.warning("Story generation interrupted by user")
        session_manager.update_session_status(session_id, "interrupted")
        return 130  # SIGINT exit code

    except Exception as e:
        logger.error(f"Story generation failed: {e}")
        session_manager.update_session_status(session_id, "failed")
        return 1

    return 0


def simple_main(argv: Optional[List[str]] = None) -> int:
    """Simple CLI for basic functionality when advanced features unavailable."""
    parser = argparse.ArgumentParser(
        description="Storytelling - A Python package for storytelling applications"
    )
    parser.add_argument(
        "--version", action="version", version=f"storytelling {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create story command (simple mode)
    if SIMPLE_MODE and Story:
        create_parser = subparsers.add_parser("create", help="Create a new story")
        create_parser.add_argument("title", help="Story title")
        create_parser.add_argument("--content", help="Story content")
        create_parser.add_argument("--author", help="Story author")
        create_parser.add_argument("--genre", help="Story genre")

    args = parser.parse_args(argv)

    if args.command == "create" and SIMPLE_MODE:
        create_story(args)
    else:
        print("Advanced storytelling features not available.")
        print("Install with: pip install storytelling[all]")
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
