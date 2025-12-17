#!/usr/bin/env python3
"""
Ceremonial Diary - Diary export and management for IAIP integration.

This module provides comprehensive diary management functionality aligned
with IAIP's ceremonial diary structure (Issue #11) and the Five-Phase
Ceremonial Technology Methodology.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml


class CeremonialPhaseEnum(str, Enum):
    """Ceremonial phase enumeration."""

    MIIGWECHIWENDAM = "miigwechiwendam"  # Sacred Space Creation
    NINDOKENDAAN = "nindokendaan"  # Two-Eyed Research Gathering
    NINGWAAB = "ningwaab"  # Knowledge Integration
    NINDOODAM = "nindoodam"  # Creative Expression
    MIGWECH = "migwech"  # Ceremonial Closing


class EntryTypeEnum(str, Enum):
    """Diary entry type enumeration."""

    INTENTION = "intention"
    OBSERVATION = "observation"
    HYPOTHESIS = "hypothesis"
    DATA = "data"
    SYNTHESIS = "synthesis"
    ACTION = "action"
    REFLECTION = "reflection"
    LEARNING = "learning"


@dataclass
class DiaryEntry:
    """
    Represents a ceremonial diary entry.

    Implements the schema from /src/IAIP/ISSUE_11_Creation_of_Diaries.md
    """

    id: str
    timestamp: str  # ISO 8601 format
    participant: str  # 'user', 'mia', 'miette', 'echo_weaver', 'system', custom
    phase: CeremonialPhaseEnum
    entryType: EntryTypeEnum
    content: str  # Main diary text, supports Markdown
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create_new(
        cls,
        content: str,
        participant: str,
        phase: CeremonialPhaseEnum,
        entry_type: EntryTypeEnum,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "DiaryEntry":
        """Create a new diary entry with auto-generated ID and timestamp.

        Args:
            content: Entry content
            participant: Who is creating the entry
            phase: Ceremonial phase
            entry_type: Type of entry
            metadata: Optional additional metadata

        Returns:
            New DiaryEntry instance
        """
        timestamp = datetime.utcnow()

        return cls(
            id=f"{int(timestamp.timestamp() * 1000)}",
            timestamp=timestamp.isoformat() + "Z",
            participant=participant,
            phase=phase,
            entryType=entry_type,
            content=content,
            metadata=metadata or {},
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert entry to dictionary format."""
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "participant": self.participant,
            "phase": self.phase.value,
            "entryType": self.entryType.value,
            "content": self.content,
            "metadata": self.metadata,
        }

    def to_markdown(self) -> str:
        """Convert entry to Markdown format with YAML frontmatter."""
        frontmatter_dict = {
            "id": self.id,
            "timestamp": self.timestamp,
            "participant": self.participant,
            "phase": self.phase.value,
            "entryType": self.entryType.value,
        }

        if self.metadata:
            frontmatter_dict["metadata"] = self.metadata

        frontmatter = yaml.dump(frontmatter_dict, default_flow_style=False)

        return f"---\n{frontmatter}---\n\n{self.content}\n"

    @classmethod
    def from_markdown(cls, markdown_text: str) -> "DiaryEntry":
        """Parse a diary entry from Markdown format.

        Args:
            markdown_text: Markdown text with YAML frontmatter

        Returns:
            DiaryEntry instance
        """
        # Split frontmatter and content
        parts = markdown_text.split("---\n", 2)
        if len(parts) < 3:
            raise ValueError("Invalid diary entry format - missing frontmatter")

        frontmatter_text = parts[1]
        content = parts[2].strip()

        # Parse frontmatter
        frontmatter = yaml.safe_load(frontmatter_text)

        return cls(
            id=frontmatter["id"],
            timestamp=frontmatter["timestamp"],
            participant=frontmatter["participant"],
            phase=CeremonialPhaseEnum(frontmatter["phase"]),
            entryType=EntryTypeEnum(frontmatter["entryType"]),
            content=content,
            metadata=frontmatter.get("metadata", {}),
        )


@dataclass
class CeremonialDiary:
    """
    Manages a collection of diary entries for a session.

    Provides functionality for:
    - Creating and managing entries
    - Exporting to IAIP-compatible formats
    - Filtering and querying entries
    - Session progression tracking
    """

    session_id: str
    participant_name: str
    entries: List[DiaryEntry] = field(default_factory=list)
    session_metadata: Dict[str, Any] = field(default_factory=dict)

    def add_entry(
        self,
        content: str,
        entry_type: EntryTypeEnum,
        phase: CeremonialPhaseEnum,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> DiaryEntry:
        """Add a new entry to the diary.

        Args:
            content: Entry content
            entry_type: Type of entry
            phase: Ceremonial phase
            metadata: Optional metadata

        Returns:
            Created DiaryEntry
        """
        entry = DiaryEntry.create_new(
            content=content,
            participant=self.participant_name,
            phase=phase,
            entry_type=entry_type,
            metadata=metadata,
        )

        self.entries.append(entry)
        return entry

    def get_entries_by_phase(self, phase: CeremonialPhaseEnum) -> List[DiaryEntry]:
        """Get all entries for a specific phase.

        Args:
            phase: Ceremonial phase to filter by

        Returns:
            List of entries in that phase
        """
        return [entry for entry in self.entries if entry.phase == phase]

    def get_entries_by_type(self, entry_type: EntryTypeEnum) -> List[DiaryEntry]:
        """Get all entries of a specific type.

        Args:
            entry_type: Entry type to filter by

        Returns:
            List of entries of that type
        """
        return [entry for entry in self.entries if entry.entryType == entry_type]

    def export_to_markdown_file(self, output_path: Path) -> Path:
        """Export diary to a single Markdown file.

        Format matches /src/IAIP/_v0.dev/diaries/ structure.

        Args:
            output_path: Path for the output file

        Returns:
            Path to created file
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Combine all entries
        markdown_content = f"""# Ceremonial Diary: {self.participant_name}

**Session ID**: {self.session_id}
**Participant**: {self.participant_name}
**Entries**: {len(self.entries)}

## Session Metadata
{json.dumps(self.session_metadata, indent=2)}

---

## Diary Entries

"""

        for entry in self.entries:
            markdown_content += entry.to_markdown() + "\n---\n\n"

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        return output_path

    def export_to_iaip_directory(
        self, base_dir: Path, separate_files: bool = False
    ) -> List[Path]:
        """Export diary to IAIP _v0.dev/diaries/ structure.

        Args:
            base_dir: Base directory for diaries (e.g., _v0.dev/diaries/)
            separate_files: If True, create separate file per phase

        Returns:
            List of created file paths
        """
        session_dir = base_dir / self.session_id
        session_dir.mkdir(parents=True, exist_ok=True)

        created_files = []

        if separate_files:
            # Create separate file for each phase
            for phase in CeremonialPhaseEnum:
                phase_entries = self.get_entries_by_phase(phase)
                if not phase_entries:
                    continue

                phase_file = session_dir / f"{self.participant_name}_{phase.value}.md"

                markdown_content = f"""# {phase.value.title()} Phase Entries

**Participant**: {self.participant_name}
**Session**: {self.session_id}
**Entries in Phase**: {len(phase_entries)}

---

"""
                for entry in phase_entries:
                    markdown_content += entry.to_markdown() + "\n---\n\n"

                with open(phase_file, "w", encoding="utf-8") as f:
                    f.write(markdown_content)

                created_files.append(phase_file)
        else:
            # Single diary file
            diary_file = session_dir / f"{self.participant_name}_diary.md"
            created_files.append(self.export_to_markdown_file(diary_file))

        # Also create session metadata file
        metadata_file = session_dir / "session_metadata.json"
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "session_id": self.session_id,
                    "participant": self.participant_name,
                    "entry_count": len(self.entries),
                    "phases_covered": [
                        p.value for p in {e.phase for e in self.entries}
                    ],
                    "session_metadata": self.session_metadata,
                },
                f,
                indent=2,
            )

        created_files.append(metadata_file)

        return created_files

    def get_phase_progression(self) -> List[Tuple[CeremonialPhaseEnum, int]]:
        """Get progression through ceremonial phases.

        Returns:
            List of (phase, entry_count) tuples in order
        """
        phase_counts = {}
        for phase in CeremonialPhaseEnum:
            phase_counts[phase] = len(self.get_entries_by_phase(phase))

        return list(phase_counts.items())

    def get_session_summary(self) -> Dict[str, Any]:
        """Generate a summary of the diary session.

        Returns:
            Summary dictionary with statistics and insights
        """
        phase_progression = self.get_phase_progression()

        entry_types = {}
        for entry_type in EntryTypeEnum:
            entry_types[entry_type.value] = len(self.get_entries_by_type(entry_type))

        return {
            "session_id": self.session_id,
            "participant": self.participant_name,
            "total_entries": len(self.entries),
            "phase_progression": [
                {"phase": phase.value, "entries": count}
                for phase, count in phase_progression
            ],
            "entry_type_distribution": entry_types,
            "first_entry": self.entries[0].timestamp if self.entries else None,
            "last_entry": self.entries[-1].timestamp if self.entries else None,
            "session_metadata": self.session_metadata,
        }


class DiaryManager:
    """
    Manager for multiple ceremonial diaries across sessions.

    Provides high-level operations for:
    - Creating and managing diaries
    - Cross-session analysis
    - IAIP integration workflows
    """

    def __init__(self, base_diary_dir: Path):
        """Initialize diary manager.

        Args:
            base_diary_dir: Base directory for all diaries
        """
        self.base_dir = base_diary_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.active_diaries: Dict[str, CeremonialDiary] = {}

    def create_diary(
        self,
        session_id: str,
        participant_name: str,
        session_metadata: Optional[Dict[str, Any]] = None,
    ) -> CeremonialDiary:
        """Create a new ceremonial diary.

        Args:
            session_id: Unique session identifier
            participant_name: Name of the participant
            session_metadata: Optional session metadata

        Returns:
            New CeremonialDiary instance
        """
        diary = CeremonialDiary(
            session_id=session_id,
            participant_name=participant_name,
            session_metadata=session_metadata or {},
        )

        self.active_diaries[session_id] = diary
        return diary

    def get_diary(self, session_id: str) -> Optional[CeremonialDiary]:
        """Retrieve an active diary by session ID.

        Args:
            session_id: Session identifier

        Returns:
            CeremonialDiary if found, None otherwise
        """
        return self.active_diaries.get(session_id)

    def save_diary(
        self, session_id: str, separate_by_phase: bool = False
    ) -> List[Path]:
        """Save a diary to the base directory.

        Args:
            session_id: Session identifier
            separate_by_phase: Create separate files per phase

        Returns:
            List of created file paths
        """
        diary = self.get_diary(session_id)
        if not diary:
            raise ValueError(f"No diary found for session: {session_id}")

        return diary.export_to_iaip_directory(
            self.base_dir, separate_files=separate_by_phase
        )

    def load_diary_from_directory(self, session_id: str) -> Optional[CeremonialDiary]:
        """Load a diary from the base directory.

        Args:
            session_id: Session identifier

        Returns:
            Loaded CeremonialDiary or None if not found
        """
        session_dir = self.base_dir / session_id
        if not session_dir.exists():
            return None

        # Look for diary files
        diary_files = list(session_dir.glob("*_diary.md"))
        if not diary_files:
            return None

        # Load the first diary file found
        diary_file = diary_files[0]
        participant_name = diary_file.stem.replace("_diary", "")

        # Parse entries from file
        with open(diary_file, encoding="utf-8") as f:
            content = f.read()

        # Simple parsing - split by entry markers
        entry_texts = content.split("\n---\n\n")
        entries = []

        for entry_text in entry_texts:
            if entry_text.strip() and entry_text.startswith("---\n"):
                try:
                    entry = DiaryEntry.from_markdown(entry_text)
                    entries.append(entry)
                except Exception:
                    continue  # Skip malformed entries

        # Load metadata if available
        metadata_file = session_dir / "session_metadata.json"
        session_metadata = {}
        if metadata_file.exists():
            with open(metadata_file, encoding="utf-8") as f:
                session_metadata = json.load(f).get("session_metadata", {})

        diary = CeremonialDiary(
            session_id=session_id,
            participant_name=participant_name,
            entries=entries,
            session_metadata=session_metadata,
        )

        self.active_diaries[session_id] = diary
        return diary

    def list_sessions(self) -> List[str]:
        """List all session IDs with saved diaries.

        Returns:
            List of session IDs
        """
        return [d.name for d in self.base_dir.iterdir() if d.is_dir()]

    def get_all_session_summaries(self) -> List[Dict[str, Any]]:
        """Get summaries for all sessions.

        Returns:
            List of session summary dictionaries
        """
        summaries = []

        for session_id in self.list_sessions():
            diary = self.load_diary_from_directory(session_id)
            if diary:
                summaries.append(diary.get_session_summary())

        return summaries
