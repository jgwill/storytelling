/**
 * storytellingjs - Role-Based Tooling Interface
 *
 * Parity with Python storytelling/role_tooling.py
 * Seven roles in narrative creation with tool registry.
 */

// =============================================================================
// Role Definitions
// =============================================================================

export enum Role {
  ARCHITECT = 'architect',
  STRUCTURIST = 'structurist',
  STORYTELLER = 'storyteller',
  EDITOR = 'editor',
  READER = 'reader',
  COLLABORATOR = 'collaborator',
  WITNESS = 'witness',
}

export enum RoleUniverse {
  ENGINEER = 'engineer',
  CEREMONY = 'ceremony',
  STORY_ENGINE = 'story_engine',
}

/** Role → Primary Universe mapping */
export const ROLE_UNIVERSE_MAP: Record<Role, RoleUniverse> = {
  [Role.ARCHITECT]: RoleUniverse.ENGINEER,
  [Role.STRUCTURIST]: RoleUniverse.STORY_ENGINE,
  [Role.STORYTELLER]: RoleUniverse.STORY_ENGINE,
  [Role.EDITOR]: RoleUniverse.ENGINEER,
  [Role.READER]: RoleUniverse.STORY_ENGINE,
  [Role.COLLABORATOR]: RoleUniverse.ENGINEER,
  [Role.WITNESS]: RoleUniverse.CEREMONY,
};

// =============================================================================
// Tool Registry
// =============================================================================

export interface RoleTool {
  toolId: string;
  name: string;
  description: string;
  roles: Role[];
  universe: RoleUniverse;
  handler?: (...args: unknown[]) => Promise<unknown>;
  isAvailable: boolean;
}

export class ToolRegistry {
  private tools: Map<string, RoleTool> = new Map();

  register(tool: RoleTool): void {
    this.tools.set(tool.toolId, tool);
  }

  getToolsForRole(role: Role): RoleTool[] {
    return Array.from(this.tools.values()).filter(
      (t) => t.isAvailable && t.roles.includes(role),
    );
  }

  getToolsForUniverse(universe: RoleUniverse): RoleTool[] {
    return Array.from(this.tools.values()).filter(
      (t) => t.isAvailable && t.universe === universe,
    );
  }

  getTool(toolId: string): RoleTool | undefined {
    return this.tools.get(toolId);
  }

  getAllTools(): RoleTool[] {
    return Array.from(this.tools.values());
  }
}

// =============================================================================
// Role Interface (abstract base)
// =============================================================================

export interface RoleContext {
  sessionId?: string;
  currentPhase: string;
  availableTools: RoleTool[];
}

export abstract class RoleInterface {
  readonly role: Role;
  readonly universe: RoleUniverse;
  protected registry: ToolRegistry;

  constructor(role: Role, registry: ToolRegistry) {
    this.role = role;
    this.universe = ROLE_UNIVERSE_MAP[role];
    this.registry = registry;
  }

  getAvailableTools(): RoleTool[] {
    return this.registry.getToolsForRole(this.role);
  }

  abstract primaryAction(context: RoleContext): Promise<unknown>;
}

// =============================================================================
// Concrete Role Implementations
// =============================================================================

export class Architect extends RoleInterface {
  constructor(registry: ToolRegistry) {
    super(Role.ARCHITECT, registry);
  }

  async primaryAction(context: RoleContext): Promise<unknown> {
    return { role: 'architect', action: 'schema_design', phase: context.currentPhase };
  }
}

export class Structurist extends RoleInterface {
  constructor(registry: ToolRegistry) {
    super(Role.STRUCTURIST, registry);
  }

  async primaryAction(context: RoleContext): Promise<unknown> {
    return { role: 'structurist', action: 'narrative_structure', phase: context.currentPhase };
  }
}

export class Storyteller extends RoleInterface {
  constructor(registry: ToolRegistry) {
    super(Role.STORYTELLER, registry);
  }

  async primaryAction(context: RoleContext): Promise<unknown> {
    return { role: 'storyteller', action: 'prose_crafting', phase: context.currentPhase };
  }
}

export class Editor extends RoleInterface {
  constructor(registry: ToolRegistry) {
    super(Role.EDITOR, registry);
  }

  async primaryAction(context: RoleContext): Promise<unknown> {
    return { role: 'editor', action: 'quality_refinement', phase: context.currentPhase };
  }
}

export class Reader extends RoleInterface {
  constructor(registry: ToolRegistry) {
    super(Role.READER, registry);
  }

  async primaryAction(context: RoleContext): Promise<unknown> {
    return { role: 'reader', action: 'experience_consumption', phase: context.currentPhase };
  }
}

export class Collaborator extends RoleInterface {
  constructor(registry: ToolRegistry) {
    super(Role.COLLABORATOR, registry);
  }

  async primaryAction(context: RoleContext): Promise<unknown> {
    return { role: 'collaborator', action: 'human_ai_mediation', phase: context.currentPhase };
  }
}

export class Witness extends RoleInterface {
  constructor(registry: ToolRegistry) {
    super(Role.WITNESS, registry);
  }

  async primaryAction(context: RoleContext): Promise<unknown> {
    return { role: 'witness', action: 'ceremonial_observation', phase: context.currentPhase };
  }
}

// =============================================================================
// Default Tool Definitions
// =============================================================================

export function createDefaultRegistry(): ToolRegistry {
  const registry = new ToolRegistry();

  // Architect tools
  registry.register({
    toolId: 'define_schema',
    name: 'Define Schema',
    description: 'Define or modify the story schema and structure',
    roles: [Role.ARCHITECT, Role.COLLABORATOR],
    universe: RoleUniverse.ENGINEER,
    isAvailable: true,
  });

  // Structurist tools
  registry.register({
    toolId: 'analyze_structure',
    name: 'Analyze Structure',
    description: 'Analyze narrative structure and identify gaps',
    roles: [Role.STRUCTURIST, Role.EDITOR],
    universe: RoleUniverse.STORY_ENGINE,
    isAvailable: true,
  });

  registry.register({
    toolId: 'map_themes',
    name: 'Map Themes',
    description: 'Map and track thematic threads across the narrative',
    roles: [Role.STRUCTURIST],
    universe: RoleUniverse.STORY_ENGINE,
    isAvailable: true,
  });

  // Storyteller tools
  registry.register({
    toolId: 'generate_beat',
    name: 'Generate Beat',
    description: 'Generate a story beat with emotional and structural awareness',
    roles: [Role.STORYTELLER, Role.COLLABORATOR],
    universe: RoleUniverse.STORY_ENGINE,
    isAvailable: true,
  });

  registry.register({
    toolId: 'craft_dialogue',
    name: 'Craft Dialogue',
    description: 'Generate or refine character dialogue',
    roles: [Role.STORYTELLER],
    universe: RoleUniverse.STORY_ENGINE,
    isAvailable: true,
  });

  // Editor tools
  registry.register({
    toolId: 'critique_beat',
    name: 'Critique Beat',
    description: 'Provide quality critique of a story beat',
    roles: [Role.EDITOR],
    universe: RoleUniverse.ENGINEER,
    isAvailable: true,
  });

  registry.register({
    toolId: 'revise_prose',
    name: 'Revise Prose',
    description: 'Apply style and quality revisions to prose',
    roles: [Role.EDITOR, Role.STORYTELLER],
    universe: RoleUniverse.ENGINEER,
    isAvailable: true,
  });

  // Reader tools
  registry.register({
    toolId: 'experience_story',
    name: 'Experience Story',
    description: 'Consume and assess story from reader perspective',
    roles: [Role.READER],
    universe: RoleUniverse.STORY_ENGINE,
    isAvailable: true,
  });

  // Witness tools
  registry.register({
    toolId: 'observe_ceremony',
    name: 'Observe Ceremony',
    description: 'Witness and record ceremonial process',
    roles: [Role.WITNESS],
    universe: RoleUniverse.CEREMONY,
    isAvailable: true,
  });

  registry.register({
    toolId: 'record_diary',
    name: 'Record Diary',
    description: 'Create ceremonial diary entry',
    roles: [Role.WITNESS, Role.COLLABORATOR],
    universe: RoleUniverse.CEREMONY,
    isAvailable: true,
  });

  return registry;
}
