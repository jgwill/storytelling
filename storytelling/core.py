"""Core storytelling functionality."""

from typing import Dict, Optional


class Story:
    """A basic story class for storytelling applications."""

    def __init__(self, title: str, content: str = ""):
        """Initialize a new story.

        Args:
            title: The title of the story
            content: The content of the story
        """
        self.title = title
        self.content = content
        self.metadata: Dict[str, str] = {}

    def add_content(self, content: str) -> None:
        """Add content to the story.

        Args:
            content: Content to add to the story
        """
        if self.content:
            self.content += f"\n\n{content}"
        else:
            self.content = content

    def set_metadata(self, key: str, value: str) -> None:
        """Set metadata for the story.

        Args:
            key: Metadata key
            value: Metadata value
        """
        self.metadata[key] = value

    def get_metadata(self, key: str) -> Optional[str]:
        """Get metadata value by key.

        Args:
            key: Metadata key

        Returns:
            Metadata value or None if key doesn't exist
        """
        return self.metadata.get(key)

    def __str__(self) -> str:
        """String representation of the story."""
        return f"Story: {self.title}"

    def __repr__(self) -> str:
        """Detailed string representation of the story."""
        return f"Story(title='{self.title}', content_length={len(self.content)})"
