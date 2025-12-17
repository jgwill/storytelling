"""
Session Management for WillWrite Storytelling System

This module provides session persistence and resume capabilities, allowing story generation
to be interrupted and continued from any checkpoint. Core architecture for continuation capability.
"""

import datetime
import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class SessionCheckpoint:
    """Represents a checkpoint in story generation"""

    checkpoint_id: str
    node_name: str
    timestamp: str
    state: Dict[str, Any]
    metadata: Dict[str, Any]


@dataclass
class SessionInfo:
    """Complete session information"""

    session_id: str
    created_at: str
    last_checkpoint: str
    status: str  # 'in_progress', 'completed', 'failed', 'interrupted'
    prompt_file: str
    output_file: str
    checkpoints: List[SessionCheckpoint]
    configuration: Dict[str, Any]


class SessionManager:
    """Manages story generation sessions with checkpoint and resume capabilities"""

    def __init__(self, base_logs_dir: str = "Logs") -> None:
        self.base_logs_dir = Path(base_logs_dir)
        self.base_logs_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(__name__)

    def create_session(
        self, prompt_file: str, output_file: str, config: Dict[str, Any]
    ) -> str:
        """Create a new generation session"""
        session_id = self._generate_session_id()
        session_dir = self.base_logs_dir / f"Generation_{session_id}"
        session_dir.mkdir(exist_ok=True)

        session_info = SessionInfo(
            session_id=session_id,
            created_at=datetime.datetime.now().isoformat(),
            last_checkpoint="session_start",
            status="in_progress",
            prompt_file=prompt_file,
            output_file=output_file,
            checkpoints=[],
            configuration=config,
        )

        self._save_session_info(session_info)
        self.logger.info(f"Created session {session_id}")
        return session_id

    def save_checkpoint(
        self,
        session_id: str,
        node_name: str,
        state: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Save a checkpoint during generation"""
        if metadata is None:
            metadata = {}

        checkpoint = SessionCheckpoint(
            checkpoint_id=f"{node_name}_{len(self.list_checkpoints(session_id))}",
            node_name=node_name,
            timestamp=datetime.datetime.now().isoformat(),
            state=self._sanitize_state_for_serialization(state),
            metadata=metadata,
        )

        # Save checkpoint file
        session_dir = self.base_logs_dir / f"Generation_{session_id}"
        checkpoint_file = session_dir / f"checkpoint_{checkpoint.checkpoint_id}.json"

        with open(checkpoint_file, "w") as f:
            json.dump(asdict(checkpoint), f, indent=2, default=str)

        # Update session info
        session_info = self.load_session_info(session_id)
        session_info.checkpoints.append(checkpoint)
        session_info.last_checkpoint = checkpoint.checkpoint_id
        self._save_session_info(session_info)

        self.logger.info(
            f"Saved checkpoint {checkpoint.checkpoint_id} for session {session_id}"
        )

    def load_session_state(
        self, session_id: str, checkpoint_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Load session state from latest or specific checkpoint"""
        session_info = self.load_session_info(session_id)

        if not session_info.checkpoints:
            raise ValueError(f"No checkpoints found for session {session_id}")

        if checkpoint_id:
            checkpoint = next(
                (
                    cp
                    for cp in session_info.checkpoints
                    if cp.checkpoint_id == checkpoint_id
                ),
                None,
            )
            if not checkpoint:
                raise ValueError(
                    f"Checkpoint {checkpoint_id} not found in session {session_id}"
                )
        else:
            # Get latest checkpoint
            checkpoint = session_info.checkpoints[-1]

        # Load checkpoint state
        session_dir = self.base_logs_dir / f"Generation_{session_id}"
        checkpoint_file = session_dir / f"checkpoint_{checkpoint.checkpoint_id}.json"

        if not checkpoint_file.exists():
            raise FileNotFoundError(f"Checkpoint file not found: {checkpoint_file}")

        with open(checkpoint_file) as f:
            checkpoint_data = json.load(f)

        return checkpoint_data["state"]  # type: Dict[str, Any]

    def list_sessions(self) -> List[SessionInfo]:
        """List all available sessions"""
        sessions = []
        for session_dir in self.base_logs_dir.glob("Generation_*"):
            if session_dir.is_dir():
                session_file = session_dir / "session_info.json"
                if session_file.exists():
                    try:
                        sessions.append(self._load_session_info_from_file(session_file))
                    except Exception as e:
                        self.logger.warning(
                            f"Could not load session from {session_dir}: {e}"
                        )

        return sorted(sessions, key=lambda s: s.created_at, reverse=True)

    def list_checkpoints(self, session_id: str) -> List[SessionCheckpoint]:
        """List checkpoints for a session"""
        session_info = self.load_session_info(session_id)
        return session_info.checkpoints

    def load_session_info(self, session_id: str) -> SessionInfo:
        """Load session information"""
        session_dir = self.base_logs_dir / f"Generation_{session_id}"
        session_file = session_dir / "session_info.json"

        if not session_file.exists():
            raise FileNotFoundError(f"Session {session_id} not found")

        return self._load_session_info_from_file(session_file)

    def update_session_status(
        self, session_id: str, status: str, metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Update session status"""
        session_info = self.load_session_info(session_id)
        session_info.status = status

        if metadata:
            # Update configuration or other metadata
            session_info.configuration.update(metadata.get("configuration", {}))

        self._save_session_info(session_info)
        self.logger.info(f"Updated session {session_id} status to {status}")

    def can_resume_from_node(self, session_id: str, node_name: str) -> bool:
        """Check if session can be resumed from a specific node"""
        try:
            checkpoints = self.list_checkpoints(session_id)
            return any(cp.node_name == node_name for cp in checkpoints)
        except Exception:
            return False

    def get_resume_entry_point(self, session_id: str) -> str:
        """Determine the best entry point for resuming generation"""
        checkpoints = self.list_checkpoints(session_id)

        if not checkpoints:
            return "generate_story_elements"

        # Determine next node based on last completed checkpoint
        last_checkpoint = checkpoints[-1]

        # Mapping of completed nodes to next nodes
        resume_mapping = {
            "generate_story_elements": "generate_initial_outline",
            "generate_initial_outline": "determine_chapter_count",
            "determine_chapter_count": "generate_single_chapter_scene_by_scene",
            "generate_single_chapter_scene_by_scene": "increment_chapter_index",
            "increment_chapter_index": "generate_single_chapter_scene_by_scene",  # or finalize based on chapter count
        }

        return resume_mapping.get(last_checkpoint.node_name, "generate_story_elements")

    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")

    def _save_session_info(self, session_info: SessionInfo) -> None:
        """Save session information to file"""
        session_dir = self.base_logs_dir / f"Generation_{session_info.session_id}"
        session_file = session_dir / "session_info.json"

        with open(session_file, "w") as f:
            json.dump(asdict(session_info), f, indent=2, default=str)

    def _load_session_info_from_file(self, session_file: Path) -> SessionInfo:
        """Load session info from JSON file"""
        with open(session_file) as f:
            data = json.load(f)

        # Convert checkpoint dictionaries back to SessionCheckpoint objects
        checkpoints = [SessionCheckpoint(**cp) for cp in data.get("checkpoints", [])]
        data["checkpoints"] = checkpoints

        return SessionInfo(**data)

    def _sanitize_state_for_serialization(
        self, state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Clean state for JSON serialization"""
        serializable_state = {}

        for key, value in state.items():
            # Skip non-serializable objects
            if key in ["logger", "config", "retriever"]:
                continue

            # Handle special cases
            if hasattr(value, "__dict__") and not isinstance(
                value, (str, int, float, bool, list, dict)
            ):
                # Skip complex objects that can't be serialized
                continue

            serializable_state[key] = value

        return serializable_state


def migrate_existing_session(logs_dir: str, session_id: str) -> SessionInfo:
    """Migrate an existing session directory to new session management format"""
    session_manager = SessionManager(logs_dir)
    session_dir = Path(logs_dir) / f"Generation_{session_id}"

    if not session_dir.exists():
        raise FileNotFoundError(f"Session directory not found: {session_dir}")

    # Try to extract information from existing files
    # Create basic session info from existing data
    session_info = SessionInfo(
        session_id=session_id,
        created_at=datetime.datetime.fromtimestamp(
            session_dir.stat().st_ctime
        ).isoformat(),
        last_checkpoint="determine_chapter_count",  # Based on Mia's session logs
        status="interrupted",
        prompt_file="mia_test_prompt.txt",  # Default, should be detected
        output_file=f"story_output_{session_id}",
        checkpoints=[],
        configuration={},
    )

    # Add checkpoints based on existing debug files
    debug_dir = session_dir / "LangchainDebug"
    if debug_dir.exists():
        if (debug_dir / "01_StoryElements.json").exists():
            checkpoint = SessionCheckpoint(
                checkpoint_id="story_elements_0",
                node_name="generate_story_elements",
                timestamp=datetime.datetime.fromtimestamp(
                    (debug_dir / "01_StoryElements.json").stat().st_ctime
                ).isoformat(),
                state={"completed": True},
                metadata={"source": "migrated"},
            )
            session_info.checkpoints.append(checkpoint)

        if (debug_dir / "02_InitialOutline.json").exists():
            checkpoint = SessionCheckpoint(
                checkpoint_id="initial_outline_0",
                node_name="generate_initial_outline",
                timestamp=datetime.datetime.fromtimestamp(
                    (debug_dir / "02_InitialOutline.json").stat().st_ctime
                ).isoformat(),
                state={"completed": True},
                metadata={"source": "migrated"},
            )
            session_info.checkpoints.append(checkpoint)

    # Save migrated session
    session_manager._save_session_info(session_info)
    return session_info
