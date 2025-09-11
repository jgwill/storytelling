"""Tests for storytelling.core module."""

from storytelling.core import Story


def test_story_creation():
    """Test basic story creation."""
    story = Story("Test Title", "Test content")
    assert story.title == "Test Title"
    assert story.content == "Test content"
    assert story.metadata == {}


def test_story_creation_no_content():
    """Test story creation without content."""
    story = Story("Test Title")
    assert story.title == "Test Title"
    assert story.content == ""
    assert story.metadata == {}


def test_story_add_content():
    """Test adding content to story."""
    story = Story("Test Title")
    story.add_content("First paragraph")
    assert story.content == "First paragraph"

    story.add_content("Second paragraph")
    assert story.content == "First paragraph\n\nSecond paragraph"


def test_story_add_content_to_existing():
    """Test adding content to story with existing content."""
    story = Story("Test Title", "Initial content")
    story.add_content("Additional content")
    assert story.content == "Initial content\n\nAdditional content"


def test_story_metadata():
    """Test story metadata functionality."""
    story = Story("Test Title")
    story.set_metadata("author", "Test Author")
    story.set_metadata("genre", "Fiction")

    assert story.get_metadata("author") == "Test Author"
    assert story.get_metadata("genre") == "Fiction"
    assert story.get_metadata("nonexistent") is None


def test_story_metadata_update():
    """Test updating existing metadata."""
    story = Story("Test Title")
    story.set_metadata("author", "First Author")
    story.set_metadata("author", "Updated Author")

    assert story.get_metadata("author") == "Updated Author"


def test_story_string_representation():
    """Test story string representations."""
    story = Story("Test Title", "Some content")
    assert str(story) == "Story: Test Title"
    assert repr(story) == "Story(title='Test Title', content_length=12)"


def test_story_empty_content_length():
    """Test string representation with empty content."""
    story = Story("Test Title")
    assert repr(story) == "Story(title='Test Title', content_length=0)"
