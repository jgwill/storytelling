"""
Role-Based Tooling Interface for Storytelling Package

This module provides role-specific interfaces that expose appropriate
tools for each participant in the narrative creation workflow.

Roles defined per storytelling-roles-tooling.rispec.md:
- ARCHITECT: Schema/structure design
- STRUCTURIST: Narrative structure (what story means)
- STORYTELLER: Prose crafting (how story is told)
- EDITOR: Quality refinement
- READER: Experience consumption
- COLLABORATOR: Human-AI mediation
- WITNESS: Ceremonial observation
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Callable, TYPE_CHECKING

logger = logging.getLogger(__name__)


# ============================================================================
# Role Definitions
# ============================================================================

class Role(str, Enum):
    """The seven roles in narrative creation."""
    ARCHITECT = "architect"      # Schema/structure design
    STRUCTURIST = "structurist"  # Narrative structure
    STORYTELLER = "storyteller"  # Prose crafting
    EDITOR = "editor"            # Quality refinement
    READER = "reader"            # Experience consumption
    COLLABORATOR = "collaborator"  # Human-AI mediation
    WITNESS = "witness"          # Ceremonial observation


class Universe(str, Enum):
    """Three-Universe mapping for roles."""
    ENGINEER = "engineer"
    CEREMONY = "ceremony"
    STORY_ENGINE = "story_engine"


# Role → Primary Universe mapping
ROLE_UNIVERSE_MAP: Dict[Role, Universe] = {
    Role.ARCHITECT: Universe.ENGINEER,
    Role.STRUCTURIST: Universe.STORY_ENGINE,
    Role.STORYTELLER: Universe.STORY_ENGINE,
    Role.EDITOR: Universe.ENGINEER,
    Role.READER: Universe.STORY_ENGINE,
    Role.COLLABORATOR: Universe.ENGINEER,
    Role.WITNESS: Universe.CEREMONY,
}


# ============================================================================
# Tool Registry
# ============================================================================

@dataclass
class Tool:
    """A tool available to roles."""
    tool_id: str
    name: str
    description: str
    roles: List[Role]
    universe: Universe
    handler: Optional[Callable] = None
    is_available: bool = True


class ToolRegistry:
    """Registry of all available tools mapped to roles."""
    
    def __init__(self):
        self._tools: Dict[str, Tool] = {}
        self._role_tools: Dict[Role, List[str]] = {role: [] for role in Role}
    
    def register(self, tool: Tool) -> None:
        """Register a tool."""
        self._tools[tool.tool_id] = tool
        for role in tool.roles:
            if tool.tool_id not in self._role_tools[role]:
                self._role_tools[role].append(tool.tool_id)
    
    def get_tools_for_role(self, role: Role) -> List[Tool]:
        """Get all tools available to a role."""
        return [self._tools[tid] for tid in self._role_tools.get(role, []) 
                if tid in self._tools and self._tools[tid].is_available]
    
    def get_tool(self, tool_id: str) -> Optional[Tool]:
        """Get a specific tool."""
        return self._tools.get(tool_id)
    
    def list_all(self) -> List[Tool]:
        """List all registered tools."""
        return list(self._tools.values())


# Global registry
_registry = ToolRegistry()


def register_tool(tool: Tool) -> None:
    """Register a tool in the global registry."""
    _registry.register(tool)


def get_tools_for_role(role: Role) -> List[Tool]:
    """Get tools for a specific role."""
    return _registry.get_tools_for_role(role)


# ============================================================================
# Role Interfaces
# ============================================================================

class RoleInterface(ABC):
    """Base interface for role-specific tooling."""
    
    def __init__(self, role: Role):
        self.role = role
        self.universe = ROLE_UNIVERSE_MAP[role]
        self._context: Dict[str, Any] = {}
    
    @property
    def tools(self) -> List[Tool]:
        """Get available tools for this role."""
        return get_tools_for_role(self.role)
    
    def set_context(self, key: str, value: Any) -> None:
        """Set context for tool operations."""
        self._context[key] = value
    
    @abstractmethod
    def primary_action(self, *args, **kwargs) -> Any:
        """The primary action this role performs."""
        pass
    
    @abstractmethod
    def key_question(self) -> str:
        """The key question this role answers."""
        pass


# ============================================================================
# Concrete Role Implementations
# ============================================================================

class ArchitectInterface(RoleInterface):
    """Interface for ARCHITECT role - Schema/structure design."""
    
    def __init__(self):
        super().__init__(Role.ARCHITECT)
    
    def key_question(self) -> str:
        return "What structure can represent any story we want to tell?"
    
    def primary_action(self, schema_definition: Dict[str, Any]) -> Dict[str, Any]:
        """Define or validate a schema."""
        return {"status": "schema_validated", "schema": schema_definition}
    
    def design_schema(self, requirements: List[str]) -> Dict[str, Any]:
        """Design a new schema based on requirements."""
        return {
            "version": "1.0",
            "requirements": requirements,
            "generated_at": datetime.utcnow().isoformat(),
        }
    
    def validate_migration(self, from_version: str, to_version: str) -> bool:
        """Validate schema migration is safe."""
        # Placeholder - would check for breaking changes
        return True


class StructuristInterface(RoleInterface):
    """Interface for STRUCTURIST role - Narrative structure design."""
    
    def __init__(self):
        super().__init__(Role.STRUCTURIST)
    
    def key_question(self) -> str:
        return "What happens, to whom, and why does it matter?"
    
    def primary_action(self, story_points: List[Dict]) -> Dict[str, Any]:
        """Define story structure."""
        return {"story_points": story_points, "beat_count": len(story_points)}
    
    def create_story_point(
        self,
        title: str,
        beats: List[str],
        theme: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new story point with beats."""
        return {
            "title": title,
            "beats": beats,
            "theme": theme,
            "created_at": datetime.utcnow().isoformat(),
        }
    
    def map_character_arc(
        self,
        character_id: str,
        start_state: str,
        end_state: str,
        key_moments: List[str],
    ) -> Dict[str, Any]:
        """Map a character's transformation arc."""
        return {
            "character_id": character_id,
            "start_state": start_state,
            "end_state": end_state,
            "key_moments": key_moments,
            "arc_type": "transformation",
        }


class StorytellerInterface(RoleInterface):
    """Interface for STORYTELLER role - Prose crafting."""
    
    def __init__(self, llm_provider: Any = None):
        super().__init__(Role.STORYTELLER)
        self.llm_provider = llm_provider
    
    def key_question(self) -> str:
        return "How do we make this feel alive on the page?"
    
    def primary_action(self, structure: Dict[str, Any]) -> str:
        """Transform structure into prose."""
        # Would use LLM to generate prose
        return f"[Prose generated from structure: {structure.get('title', 'Untitled')}]"
    
    def generate_prose(
        self,
        beat: Dict[str, Any],
        voice: Optional[str] = None,
        pacing: str = "moderate",
    ) -> str:
        """Generate prose for a specific beat."""
        return f"[Generated prose for beat with {pacing} pacing]"
    
    def craft_dialogue(
        self,
        character: str,
        emotion: str,
        context: str,
    ) -> str:
        """Generate character-appropriate dialogue."""
        return f'"{character} says something with {emotion} emotion"'


class EditorInterface(RoleInterface):
    """Interface for EDITOR role - Quality refinement."""
    
    def __init__(self, feedback_loop: Any = None):
        super().__init__(Role.EDITOR)
        self.feedback_loop = feedback_loop
    
    def key_question(self) -> str:
        return "Is this good enough? If not, what specifically needs improvement?"
    
    def primary_action(self, content: str) -> Dict[str, Any]:
        """Analyze content for quality gaps."""
        return {"quality_score": 0.75, "gaps": [], "suggestions": []}
    
    def identify_gaps(self, beat: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify quality gaps in a beat."""
        gaps = []
        # Would use AnalyticalFeedbackLoop
        return gaps
    
    def suggest_enrichments(
        self,
        beat: Dict[str, Any],
        gap_type: str,
    ) -> List[str]:
        """Suggest enrichments for identified gaps."""
        return [f"Suggested enrichment for {gap_type}"]
    
    def compare_versions(
        self,
        version_a: str,
        version_b: str,
    ) -> Dict[str, Any]:
        """Compare two versions of content."""
        return {"preferred": "a", "reason": "stronger emotional impact"}


class ReaderInterface(RoleInterface):
    """Interface for READER role - Experience consumption."""
    
    def __init__(self):
        super().__init__(Role.READER)
        self._annotations: List[Dict[str, Any]] = []
        self._highlights: List[Dict[str, Any]] = []
    
    def key_question(self) -> str:
        return "How does this make me feel? Do I want to keep reading?"
    
    def primary_action(self, story_content: str) -> Dict[str, Any]:
        """Read and respond to content."""
        return {"read": True, "engagement": "high"}
    
    def annotate(self, beat_id: str, note: str) -> None:
        """Add annotation to a beat."""
        self._annotations.append({
            "beat_id": beat_id,
            "note": note,
            "timestamp": datetime.utcnow().isoformat(),
        })
    
    def highlight(self, beat_id: str, text: str, emotion: str) -> None:
        """Highlight a passage with emotional tag."""
        self._highlights.append({
            "beat_id": beat_id,
            "text": text,
            "emotion": emotion,
        })
    
    def get_reading_progress(self, total_beats: int, current_beat: int) -> float:
        """Get reading progress as percentage."""
        return (current_beat / total_beats) * 100 if total_beats > 0 else 0


class CollaboratorInterface(RoleInterface):
    """Interface for COLLABORATOR role - Human-AI mediation."""
    
    def __init__(self, story_graph: Any = None):
        super().__init__(Role.COLLABORATOR)
        self.story_graph = story_graph
        self._prompt_cache: Dict[str, str] = {}
    
    def key_question(self) -> str:
        return "How do I get the AI to understand what I want?"
    
    def primary_action(self, human_intent: str) -> str:
        """Translate human intent to AI prompt."""
        return f"[Optimized prompt for: {human_intent}]"
    
    def translate_edit_to_prompt(
        self,
        edit: Dict[str, Any],
        context: Dict[str, Any],
    ) -> str:
        """Convert a human edit into regeneration guidance."""
        return f"Regenerate with edit: {edit}"
    
    def trigger_regeneration(
        self,
        beat_id: str,
        downstream: bool = True,
    ) -> Dict[str, Any]:
        """Trigger regeneration from a specific beat."""
        return {
            "triggered_at": beat_id,
            "downstream": downstream,
            "status": "queued",
        }
    
    def resolve_conflict(
        self,
        human_version: str,
        ai_version: str,
        preference: str = "human",
    ) -> str:
        """Resolve human-AI disagreement."""
        return human_version if preference == "human" else ai_version


class WitnessInterface(RoleInterface):
    """Interface for WITNESS role - Ceremonial observation."""
    
    def __init__(self):
        super().__init__(Role.WITNESS)
        self._observations: List[Dict[str, Any]] = []
        self._sacred_pauses: List[str] = []
    
    def key_question(self) -> str:
        return "Does this serve the deeper purpose we're creating for?"
    
    def primary_action(self, process_state: Dict[str, Any]) -> Dict[str, Any]:
        """Witness and validate the creative process."""
        return {"witnessed": True, "aligned": True}
    
    def invoke_sacred_pause(self, reason: str) -> None:
        """Invoke a sacred pause for reflection."""
        self._sacred_pauses.append(reason)
        logger.info(f"Sacred pause invoked: {reason}")
    
    def check_alignment(
        self,
        content: Dict[str, Any],
        values: List[str],
    ) -> Dict[str, Any]:
        """Check alignment with core values."""
        return {
            "aligned": True,
            "values_honored": values,
            "concerns": [],
        }
    
    def acknowledge_contribution(
        self,
        contributor: str,
        contribution: str,
    ) -> None:
        """K'é acknowledgment of contribution."""
        self._observations.append({
            "type": "gratitude",
            "contributor": contributor,
            "contribution": contribution,
            "timestamp": datetime.utcnow().isoformat(),
        })
    
    def assess_hozhó(self, story_state: Dict[str, Any]) -> float:
        """Assess Hózhó (beauty/harmony/balance) of current state."""
        # Would assess coherence and wholeness
        return 0.85


# ============================================================================
# Role Factory
# ============================================================================

def create_role_interface(
    role: Role,
    **kwargs,
) -> RoleInterface:
    """Factory to create role-specific interfaces."""
    
    interfaces = {
        Role.ARCHITECT: ArchitectInterface,
        Role.STRUCTURIST: StructuristInterface,
        Role.STORYTELLER: StorytellerInterface,
        Role.EDITOR: EditorInterface,
        Role.READER: ReaderInterface,
        Role.COLLABORATOR: CollaboratorInterface,
        Role.WITNESS: WitnessInterface,
    }
    
    interface_class = interfaces.get(role)
    if not interface_class:
        raise ValueError(f"Unknown role: {role}")
    
    return interface_class(**kwargs)


# ============================================================================
# Multi-Role Session
# ============================================================================

@dataclass
class RoleSession:
    """A session that can switch between roles."""
    
    session_id: str
    active_roles: List[Role] = field(default_factory=list)
    _interfaces: Dict[Role, RoleInterface] = field(default_factory=dict)
    
    def activate_role(self, role: Role, **kwargs) -> RoleInterface:
        """Activate a role for this session."""
        if role not in self._interfaces:
            self._interfaces[role] = create_role_interface(role, **kwargs)
        if role not in self.active_roles:
            self.active_roles.append(role)
        return self._interfaces[role]
    
    def get_interface(self, role: Role) -> Optional[RoleInterface]:
        """Get interface for an active role."""
        return self._interfaces.get(role)
    
    def switch_to(self, role: Role) -> RoleInterface:
        """Switch to a specific role."""
        if role not in self._interfaces:
            raise ValueError(f"Role {role} not activated in this session")
        return self._interfaces[role]
    
    def get_all_tools(self) -> List[Tool]:
        """Get all tools available across active roles."""
        tools = []
        seen = set()
        for role in self.active_roles:
            for tool in get_tools_for_role(role):
                if tool.tool_id not in seen:
                    tools.append(tool)
                    seen.add(tool.tool_id)
        return tools


# ============================================================================
# Register Default Tools
# ============================================================================

def _register_default_tools():
    """Register the default tools from the rispec."""
    
    # Architect tools
    register_tool(Tool(
        tool_id="schema_designer",
        name="Schema Designer",
        description="Define NCP JSON structures",
        roles=[Role.ARCHITECT],
        universe=Universe.ENGINEER,
    ))
    register_tool(Tool(
        tool_id="dependency_mapper",
        name="Dependency Mapper",
        description="Visualize beat→beat relationships",
        roles=[Role.ARCHITECT, Role.STRUCTURIST],
        universe=Universe.ENGINEER,
    ))
    
    # Structurist tools
    register_tool(Tool(
        tool_id="story_point_editor",
        name="Story Point Editor",
        description="Create/edit structural beats",
        roles=[Role.STRUCTURIST],
        universe=Universe.STORY_ENGINE,
    ))
    register_tool(Tool(
        tool_id="arc_planner",
        name="Arc Planner",
        description="Map character transformation",
        roles=[Role.STRUCTURIST],
        universe=Universe.STORY_ENGINE,
    ))
    register_tool(Tool(
        tool_id="theme_weaver",
        name="Theme Weaver",
        description="Track thematic throughlines",
        roles=[Role.STRUCTURIST, Role.EDITOR],
        universe=Universe.STORY_ENGINE,
    ))
    
    # Storyteller tools
    register_tool(Tool(
        tool_id="prose_generator",
        name="Prose Generator",
        description="Transform structure into narrative",
        roles=[Role.STORYTELLER],
        universe=Universe.STORY_ENGINE,
    ))
    register_tool(Tool(
        tool_id="voice_calibrator",
        name="Voice Calibrator",
        description="Maintain consistent narrative voice",
        roles=[Role.STORYTELLER],
        universe=Universe.STORY_ENGINE,
    ))
    register_tool(Tool(
        tool_id="dialogue_crafter",
        name="Dialogue Crafter",
        description="Generate character-appropriate speech",
        roles=[Role.STORYTELLER],
        universe=Universe.STORY_ENGINE,
    ))
    
    # Editor tools
    register_tool(Tool(
        tool_id="gap_identifier",
        name="Gap Identifier",
        description="Find quality weaknesses",
        roles=[Role.EDITOR],
        universe=Universe.ENGINEER,
    ))
    register_tool(Tool(
        tool_id="coherence_scorer",
        name="Coherence Scorer",
        description="Evaluate narrative consistency",
        roles=[Role.EDITOR],
        universe=Universe.ENGINEER,
    ))
    register_tool(Tool(
        tool_id="enrichment_router",
        name="Enrichment Router",
        description="Select appropriate fixes",
        roles=[Role.EDITOR, Role.COLLABORATOR],
        universe=Universe.ENGINEER,
    ))
    
    # Reader tools
    register_tool(Tool(
        tool_id="reading_mode",
        name="Reading Mode",
        description="Scroll through beats",
        roles=[Role.READER],
        universe=Universe.STORY_ENGINE,
    ))
    register_tool(Tool(
        tool_id="annotation_tool",
        name="Annotation Tool",
        description="Mark reactions/questions",
        roles=[Role.READER],
        universe=Universe.STORY_ENGINE,
    ))
    
    # Collaborator tools
    register_tool(Tool(
        tool_id="intent_translator",
        name="Intent Translator",
        description="Convert edits to generation guidance",
        roles=[Role.COLLABORATOR],
        universe=Universe.ENGINEER,
    ))
    register_tool(Tool(
        tool_id="regeneration_trigger",
        name="Regeneration Trigger",
        description="Initiate downstream updates",
        roles=[Role.COLLABORATOR],
        universe=Universe.ENGINEER,
    ))
    
    # Witness tools
    register_tool(Tool(
        tool_id="sacred_pause",
        name="Sacred Pause",
        description="Interrupt for reflection",
        roles=[Role.WITNESS],
        universe=Universe.CEREMONY,
    ))
    register_tool(Tool(
        tool_id="alignment_checker",
        name="Alignment Checker",
        description="Validate against core values",
        roles=[Role.WITNESS],
        universe=Universe.CEREMONY,
    ))
    register_tool(Tool(
        tool_id="hozhó_validator",
        name="Hózhó Validator",
        description="Confirm wholeness and beauty",
        roles=[Role.WITNESS],
        universe=Universe.CEREMONY,
    ))


# Initialize default tools
_register_default_tools()


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    # Enums
    "Role",
    "Universe",
    
    # Data classes
    "Tool",
    "RoleSession",
    
    # Registry
    "ToolRegistry",
    "register_tool",
    "get_tools_for_role",
    
    # Base class
    "RoleInterface",
    
    # Role interfaces
    "ArchitectInterface",
    "StructuristInterface",
    "StorytellerInterface",
    "EditorInterface",
    "ReaderInterface",
    "CollaboratorInterface",
    "WitnessInterface",
    
    # Factory
    "create_role_interface",
    
    # Constants
    "ROLE_UNIVERSE_MAP",
]
