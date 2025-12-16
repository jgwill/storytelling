"""Tests for storytelling.cli module."""

from unittest.mock import patch

import pytest

from storytelling.cli import create_story, main


def test_main_no_args():
    """Test main function with no arguments shows help."""
    result = main([])
    assert result == 1


def test_main_version():
    """Test version argument."""
    with pytest.raises(SystemExit) as exc_info:
        main(["--version"])
    assert exc_info.value.code == 0


def test_main_help():
    """Test help argument."""
    with pytest.raises(SystemExit) as exc_info:
        main(["--help"])
    assert exc_info.value.code == 0


def test_create_story_basic():
    """Test basic story creation via CLI."""
    with patch("builtins.print") as mock_print:
        import argparse

        # Create a namespace object to simulate parsed arguments
        args = argparse.Namespace()
        args.title = "Test Story"
        args.content = "Test content"
        args.author = None
        args.genre = None

        create_story(args)

        # Check that print was called
        mock_print.assert_called()


def test_create_story_with_metadata():
    """Test story creation with metadata via CLI."""
    with patch("builtins.print") as mock_print:
        import argparse

        # Create a namespace object to simulate parsed arguments
        args = argparse.Namespace()
        args.title = "Test Story"
        args.content = "Test content"
        args.author = "Test Author"
        args.genre = "Fiction"

        create_story(args)

        # Check that print was called
        mock_print.assert_called()


def test_main_create_story():
    """Test main function with create command."""
    with patch("storytelling.cli.create_story") as mock_create:
        result = main(["create", "Test Title"])
        assert result == 0
        mock_create.assert_called_once()


def test_main_create_story_with_options():
    """Test main function with create command and options."""
    with patch("storytelling.cli.create_story") as mock_create:
        result = main(
            ["create", "Test Title", "--content", "Test content", "--author", "Author"]
        )
        assert result == 0
        mock_create.assert_called_once()
