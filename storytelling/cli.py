"""Command line interface for storytelling package."""

import argparse
import sys
from typing import List, Optional

from . import __version__
from .core import Story


def create_story(args: argparse.Namespace) -> None:
    """Create a new story."""
    story = Story(args.title, args.content or "")
    if args.author:
        story.set_metadata("author", args.author)
    if args.genre:
        story.set_metadata("genre", args.genre)
    
    print(f"Created story: {story}")
    if story.content:
        print(f"Content preview: {story.content[:100]}...")


def main(argv: Optional[List[str]] = None) -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Storytelling - A Python package for storytelling applications"
    )
    parser.add_argument(
        "--version", action="version", version=f"storytelling {__version__}"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create story command
    create_parser = subparsers.add_parser("create", help="Create a new story")
    create_parser.add_argument("title", help="Story title")
    create_parser.add_argument("--content", help="Story content")
    create_parser.add_argument("--author", help="Story author")
    create_parser.add_argument("--genre", help="Story genre")
    
    args = parser.parse_args(argv)
    
    if args.command == "create":
        create_story(args)
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())