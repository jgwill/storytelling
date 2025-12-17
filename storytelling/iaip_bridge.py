#!/usr/bin/env python3
"""
IAIP Bridge - Integration module for Indigenous-AI Collaborative Platform.

This module provides the bridge between the storytelling package and IAIP's
Four Directions framework, specifically supporting North Direction practices:
- Storytelling circles and oral history
- Reflection journals and wisdom keeping
- Ceremonial diary integration
"""

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import WillWriteConfig
from .core import Story
from .session_manager import SessionInfo


@dataclass
class CeremonialPhase:
    """Represents a phase in the ceremonial technology methodology."""

    key: str  # e.g., 'miigwechiwendam', 'nindokendaan', etc.
    name: str  # Human-readable name
    description: str

    # Map storytelling activities to phases
    SACRED_SPACE = (
        "miigwechiwendam",
        "Sacred Space Creation",
        "Establishing intention and ceremonial container",
    )
    RESEARCH = (
        "nindokendaan",
        "Two-Eyed Research Gathering",
        "Comprehensive research using Indigenous-Western balance",
    )
    INTEGRATION = (
        "ningwaab",
        "Knowledge Integration",
        "Synthesizing research into coherent understanding",
    )
    EXPRESSION = (
        "nindoodam",
        "Creative Expression",
        "Transforming knowledge into accessible formats",
    )
    CLOSING = ("migwech", "Ceremonial Closing", "Honoring work and capturing learning")


class NorthDirectionStoryteller:
    """
    Storytelling wrapper for IAIP North Direction practices.

    This class adapts the storytelling package's core functionality
    to align with North Direction (Siihasin: Assurance & Reflection):
    - Daily reflection and journaling
    - Storytelling circles and oral history
    - Community accountability processes
    - Wisdom keeping and genealogical knowledge
    """

    def __init__(self, config: Optional[WillWriteConfig] = None):
        """Initialize North Direction storyteller.

        Args:
            config: Optional WillWriteConfig instance
        """
        self.config = config or WillWriteConfig()
        self.current_phase: Optional[CeremonialPhase] = None
        self.story_session: Optional[SessionInfo] = None

    def begin_ceremonial_session(
        self, intention: str, participant: str = "user"
    ) -> Dict[str, Any]:
        """Begin a new ceremonial storytelling session.

        Args:
            intention: The user's intention for this session
            participant: Name of the participant

        Returns:
            Session information with ceremonial context
        """
        self.current_phase = CeremonialPhase(*CeremonialPhase.SACRED_SPACE)

        return {
            "phase": self.current_phase.key,
            "phase_name": self.current_phase.name,
            "intention": intention,
            "participant": participant,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": "initiated",
        }

    def map_storytelling_activity_to_phase(self, activity: str) -> CeremonialPhase:
        """Map a storytelling activity to appropriate ceremonial phase.

        Args:
            activity: One of 'outline', 'research', 'synthesis',
                     'generation', 'reflection'

        Returns:
            Appropriate CeremonialPhase
        """
        phase_mapping = {
            "outline": CeremonialPhase.SACRED_SPACE,
            "research": CeremonialPhase.RESEARCH,
            "synthesis": CeremonialPhase.INTEGRATION,
            "generation": CeremonialPhase.EXPRESSION,
            "reflection": CeremonialPhase.CLOSING,
        }

        phase_data = phase_mapping.get(activity, CeremonialPhase.SACRED_SPACE)
        return CeremonialPhase(*phase_data)

    def create_diary_entry(
        self,
        content: str,
        entry_type: str,
        participant: str = "storyteller_agent",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a diary entry compatible with IAIP ceremonial diary schema.

        Implements schema from /src/IAIP/ISSUE_11_Creation_of_Diaries.md

        Args:
            content: Main diary text content
            entry_type: One of 'intention', 'observation', 'hypothesis',
                       'data', 'synthesis', 'action', 'reflection', 'learning'
            participant: Who is creating this entry
            metadata: Optional additional structured data

        Returns:
            Diary entry dictionary matching IAIP schema
        """
        timestamp = datetime.utcnow()

        # Ensure we have a current phase
        if not self.current_phase:
            self.current_phase = CeremonialPhase(*CeremonialPhase.SACRED_SPACE)

        entry = {
            "id": f"{int(timestamp.timestamp() * 1000)}",
            "timestamp": timestamp.isoformat() + "Z",
            "participant": participant,
            "phase": self.current_phase.key,
            "entryType": entry_type,
            "content": content,
        }

        if metadata:
            entry["metadata"] = metadata

        return entry

    def format_diary_as_markdown(
        self, entries: List[Dict[str, Any]], participant: str = "storyteller_agent"
    ) -> str:
        """Format diary entries as Markdown compatible with IAIP storage.

        Follows the format in /src/IAIP/_v0.dev/diaries/

        Args:
            entries: List of diary entry dictionaries
            participant: Participant name for the diary

        Returns:
            Markdown formatted diary content
        """
        markdown_parts = []

        for entry in entries:
            # Frontmatter
            frontmatter_parts = [
                "---",
                f"id: {entry['id']}",
                f"timestamp: {entry['timestamp']}",
                f"participant: {entry['participant']}",
                f"phase: {entry['phase']}",
                f"entryType: {entry['entryType']}",
            ]

            # Add metadata if present
            if "metadata" in entry and entry["metadata"]:
                frontmatter_parts.append("metadata:")
                for key, value in entry["metadata"].items():
                    frontmatter_parts.append(f"  {key}: {value}")

            frontmatter_parts.append("---")
            frontmatter = "\n".join(frontmatter_parts)

            # Content
            markdown_parts.append(f"{frontmatter}\n\n{entry['content']}\n")

        return "\n".join(markdown_parts)

    def export_session_as_diary(
        self,
        session_id: str,
        output_dir: Path,
        participant_name: str = "north_storyteller",
    ) -> Path:
        """Export a storytelling session as IAIP-compatible diary.

        Args:
            session_id: ID of the session to export
            output_dir: Base directory for diary storage
            participant_name: Name for the diary file

        Returns:
            Path to created diary file
        """
        # Create session-specific directory
        session_dir = output_dir / session_id
        session_dir.mkdir(parents=True, exist_ok=True)

        # Create diary file
        diary_path = session_dir / f"{participant_name}_diary.md"

        # For now, create a template - actual session data integration
        # will be implemented with SessionManager enhancement
        template_entry = self.create_diary_entry(
            content=f"Storytelling session {session_id} exported to ceremonial diary.",
            entry_type="learning",
            participant=participant_name,
            metadata={"session_id": session_id},
        )

        markdown_content = self.format_diary_as_markdown(
            [template_entry], participant_name
        )

        with open(diary_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        return diary_path

    def create_reflection_from_story(
        self, story: Story, reflection_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a North Direction reflection entry from a generated story.

        This supports the North Direction practice of wisdom extraction
        and learning from creative work.

        Args:
            story: A Story instance
            reflection_prompt: Optional custom reflection prompt

        Returns:
            Diary entry for reflection
        """
        default_prompt = (
            "What wisdom emerged from creating this story? "
            "What did the characters teach through their journey? "
            "How does this narrative serve healing and understanding?"
        )

        prompt = reflection_prompt or default_prompt

        # Create reflection content
        reflection_content = f"""# Reflection on Story: {story.title}

## Story Metadata
- **Length**: {len(story.content)} characters
- **Additional Metadata**: {json.dumps(story.metadata, indent=2)}

## Reflection Prompt
{prompt}

## Wisdom Extraction
The story explores themes embedded in its narrative structure.
Characters carry medicine through their choices and transformations.
The journey from beginning to resolution mirrors ceremonial progression.

## Learning Captured
Generated through North Direction storytelling practice.
"""

        self.current_phase = CeremonialPhase(*CeremonialPhase.CLOSING)

        return self.create_diary_entry(
            content=reflection_content,
            entry_type="learning",
            participant="north_storyteller",
            metadata={
                "story_title": story.title,
                "story_length": len(story.content),
                "practice": "storytelling_reflection",
            },
        )


class TwoEyedSeeingStorytellingAdapter:
    """
    Adapter for Two-Eyed Seeing methodology in storytelling.

    Two-Eyed Seeing (Etuaptmumk) involves looking with both:
    - Indigenous knowledge (relationships, ceremony, oral tradition)
    - Western knowledge (structure, analysis, narrative craft)
    """

    def __init__(self):
        """Initialize the Two-Eyed Seeing adapter."""
        pass

    def create_dual_perspective_prompt(
        self,
        base_prompt: str,
        indigenous_lens: Optional[str] = None,
        western_lens: Optional[str] = None,
    ) -> str:
        """Create a prompt that integrates both perspectives.

        Args:
            base_prompt: Core story prompt
            indigenous_lens: Optional Indigenous perspective guidance
            western_lens: Optional Western narrative guidance

        Returns:
            Enhanced prompt with dual perspectives
        """
        default_indigenous = (
            "Consider relationships between all beings, "
            "the medicine characters carry, "
            "and how the story serves healing and learning."
        )

        default_western = (
            "Apply strong narrative structure, "
            "character development arcs, "
            "and compelling storytelling craft."
        )

        indigenous_guidance = indigenous_lens or default_indigenous
        western_guidance = western_lens or default_western

        enhanced_prompt = f"""{base_prompt}

## Two-Eyed Seeing Approach

**Indigenous Knowledge Perspective:**
{indigenous_guidance}

**Western Knowledge Perspective:**
{western_guidance}

**Integration:**
Let these perspectives spiral together, creating deeper truth than either alone.
Honor both precision and mystery, structure and emergence.
"""

        return enhanced_prompt

    def analyze_story_through_dual_lens(self, story: Story) -> Dict[str, Any]:
        """Analyze a story through both Indigenous and Western lenses.

        Args:
            story: Story instance to analyze

        Returns:
            Analysis from both perspectives
        """
        return {
            "indigenous_perspective": {
                "relationships": "Analysis of character relationships and web of connections",
                "medicine": "What healing or teaching the story carries",
                "ceremony": "How the narrative structure mirrors ceremonial progression",
                "oral_tradition": "Story's suitability for oral sharing",
            },
            "western_perspective": {
                "narrative_structure": "Three-act structure, plot progression",
                "character_development": "Character arcs and transformation",
                "literary_devices": "Use of symbolism, foreshadowing, metaphor",
                "genre_conventions": "Adherence to or innovation within genre",
            },
            "spiral_integration": {
                "synthesis": "How both perspectives create deeper understanding",
                "emergent_wisdom": "Insights that arise from dual viewing",
                "creative_tension": "Productive tensions between perspectives",
            },
        }


# Utility functions for IAIP integration


def create_north_direction_session_metadata(
    intention: str, knowledge_base_paths: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Create metadata for a North Direction storytelling session.

    Args:
        intention: User's intention for the session
        knowledge_base_paths: Optional paths to knowledge base files

    Returns:
        Metadata dictionary for session initialization
    """
    return {
        "direction": "north",
        "direction_name": "Siihasin: Assurance & Reflection",
        "practice": "storytelling",
        "intention": intention,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "knowledge_base": knowledge_base_paths or [],
        "ceremonial_methodology": "five_phase_ceremonial_technology",
    }


def export_storytelling_wisdom_to_iaip(
    stories: List[Story], output_dir: Path, session_metadata: Dict[str, Any]
) -> List[Path]:
    """Export storytelling wisdom for IAIP North Direction.

    Args:
        stories: List of Story instances
        output_dir: Directory for exports
        session_metadata: Session metadata

    Returns:
        List of created file paths
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    created_files = []

    # Create wisdom archive
    wisdom_file = output_dir / "storytelling_wisdom.md"

    wisdom_content = f"""# Storytelling Wisdom Archive

**Practice**: North Direction Storytelling
**Session**: {session_metadata.get('timestamp', 'Unknown')}
**Intention**: {session_metadata.get('intention', 'Not specified')}

## Stories Generated

"""

    for i, story in enumerate(stories, 1):
        wisdom_content += f"""### {i}. {story.title}

**Length**: {len(story.content)} characters

**Wisdom Notes**:
{story.get_metadata('wisdom_notes') or 'Reflection pending'}

---

"""

    with open(wisdom_file, "w", encoding="utf-8") as f:
        f.write(wisdom_content)

    created_files.append(wisdom_file)

    return created_files
