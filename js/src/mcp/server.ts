#!/usr/bin/env node
/**
 * storytellingjs MCP Server
 * 
 * Model Context Protocol server for storytelling tools.
 * Parity with Python storytelling_mcp/server.py
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
  ErrorCode,
  McpError,
} from '@modelcontextprotocol/sdk/types.js';
import { spawn } from 'child_process';
import type { ToolHandler, ToolDefinition, ToolResult } from '../types.js';
import { SessionManager } from '../session-manager.js';
import { validateUri, suggestModelCombination, getModelUriExamples } from '../llm-providers.js';

// Tool handlers map
const toolHandlers = new Map<string, ToolHandler>();

// Session manager
const sessionManager = new SessionManager(process.env.STORYTELLING_LOGS_DIR ?? 'Logs');

/**
 * Create and configure the storytelling MCP server.
 */
export function createStorytellingServer(): Server {
  const server = new Server(
    { name: 'storytellingjs-mcp', version: '0.1.0' },
    { capabilities: { tools: {}, resources: {} } }
  );

  // Register all tools
  registerStoryGenerationTools();
  registerSessionManagementTools();
  registerConfigurationTools();
  registerWorkflowInsightTools();
  registerPromptTemplateTools();

  // List tools handler
  server.setRequestHandler(ListToolsRequestSchema, async () => {
    const tools = Array.from(toolHandlers.entries()).map(([name, handler]) => ({
      name,
      description: handler.definition.description,
      inputSchema: handler.definition.inputSchema,
    }));
    return { tools };
  });

  // Call tool handler
  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    const handler = toolHandlers.get(name);

    if (!handler) {
      throw new McpError(ErrorCode.MethodNotFound, `Unknown tool: ${name}`);
    }

    try {
      const result = await handler.execute(args ?? {});
      return {
        content: result.content.map(c => ({
          type: c.type as 'text',
          text: c.text ?? '',
        })),
        isError: result.isError,
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      return {
        content: [{ type: 'text' as const, text: `Error: ${message}` }],
        isError: true,
      };
    }
  });

  // List resources handler
  server.setRequestHandler(ListResourcesRequestSchema, async () => {
    return {
      resources: [
        {
          uri: 'storytelling://workflow/overview',
          name: 'Workflow Overview',
          description: 'Complete story generation workflow description',
          mimeType: 'text/markdown',
        },
        {
          uri: 'storytelling://config/model-uris',
          name: 'Model URI Format Guide',
          description: 'Guide for specifying model URIs',
          mimeType: 'text/markdown',
        },
        {
          uri: 'storytelling://prompts/guide',
          name: 'Story Prompt Guide',
          description: 'Guidelines for writing story prompts',
          mimeType: 'text/markdown',
        },
      ],
    };
  });

  // Read resource handler
  server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
    const { uri } = request.params;

    const resources: Record<string, string> = {
      'storytelling://workflow/overview': getWorkflowOverview(),
      'storytelling://config/model-uris': getModelUriExamples(),
      'storytelling://prompts/guide': getPromptGuide(),
    };

    const content = resources[uri];
    if (!content) {
      throw new McpError(ErrorCode.InvalidRequest, `Unknown resource: ${uri}`);
    }

    return {
      contents: [{
        uri,
        mimeType: 'text/markdown',
        text: content,
      }],
    };
  });

  return server;
}

// Tool registration functions

function registerStoryGenerationTools(): void {
  registerTool({
    name: 'generate_story',
    description: 'Generate a complete story with the storytelling package using RISE framework',
    inputSchema: {
      type: 'object',
      properties: {
        prompt_file: { type: 'string', description: 'Path to prompt file' },
        output_file: { type: 'string', description: 'Output file path (optional)' },
        initial_outline_model: { type: 'string', description: 'Model URI for initial outline' },
        chapter_outline_model: { type: 'string', description: 'Model URI for chapter outline' },
        chapter_max_revisions: { type: 'number', description: 'Max revisions per chapter' },
        expand_outline: { type: 'boolean', description: 'Expand outline' },
        debug: { type: 'boolean', description: 'Enable debug mode' },
      },
      required: ['prompt_file'],
    },
  }, async (args) => {
    const promptFile = args.prompt_file as string;
    const outputFile = args.output_file as string | undefined;
    
    // Create session
    const sessionId = sessionManager.createSession({
      promptFile,
      outputFile: outputFile ?? `story_output_${Date.now()}`,
      config: args,
    });

    return [{
      type: 'text' as const,
      text: `✓ Story generation session created: ${sessionId}\n\n` +
            `Prompt file: ${promptFile}\n` +
            `Note: Full generation requires Python storytelling package.\n` +
            `Session can be resumed with: storytellingjs --resume ${sessionId}`,
    }];
  });
}

function registerSessionManagementTools(): void {
  registerTool({
    name: 'list_sessions',
    description: 'List all available story generation sessions',
    inputSchema: { type: 'object', properties: {} },
  }, async () => {
    const sessions = sessionManager.listSessions();
    
    if (sessions.length === 0) {
      return [{ type: 'text' as const, text: 'No sessions found.' }];
    }

    let output = `Found ${sessions.length} sessions:\n\n`;
    for (const session of sessions) {
      const statusIcon = {
        'completed': '✅',
        'in_progress': '🔄',
        'failed': '❌',
        'interrupted': '⏸️',
      }[session.status] ?? '❓';

      output += `${statusIcon} ${session.sessionId}\n`;
      output += `   Status: ${session.status}\n`;
      output += `   Created: ${session.createdAt}\n`;
      output += `   Prompt: ${session.promptFile}\n`;
      output += `   Checkpoints: ${session.checkpoints.length}\n\n`;
    }

    return [{ type: 'text' as const, text: output }];
  });

  registerTool({
    name: 'get_session_info',
    description: 'Get detailed information about a specific session',
    inputSchema: {
      type: 'object',
      properties: {
        session_id: { type: 'string', description: 'Session ID' },
      },
      required: ['session_id'],
    },
  }, async (args) => {
    const sessionId = args.session_id as string;
    
    try {
      const session = sessionManager.loadSessionInfo(sessionId);
      const checkpoints = sessionManager.listCheckpoints(sessionId);

      let output = `Session: ${session.sessionId}\n`;
      output += '-'.repeat(50) + '\n';
      output += `Created: ${session.createdAt}\n`;
      output += `Status: ${session.status}\n`;
      output += `Prompt: ${session.promptFile}\n`;
      output += `Output: ${session.outputFile}\n`;
      output += `Last checkpoint: ${session.lastCheckpoint}\n\n`;
      output += `Checkpoints (${checkpoints.length}):\n`;
      
      checkpoints.forEach((cp, i) => {
        output += `  ${i + 1}. ${cp.nodeName} (${cp.timestamp})\n`;
      });

      if (checkpoints.length > 0) {
        const resumePoint = sessionManager.getResumeEntryPoint(sessionId);
        output += `\nSuggested resume point: ${resumePoint}`;
      }

      return [{ type: 'text' as const, text: output }];
    } catch (e) {
      return [{
        type: 'text' as const,
        text: `Error: ${(e as Error).message}`,
      }];
    }
  });

  registerTool({
    name: 'resume_session',
    description: 'Resume an interrupted story generation session',
    inputSchema: {
      type: 'object',
      properties: {
        session_id: { type: 'string', description: 'Session ID' },
        resume_from_node: { type: 'string', description: 'Node to resume from (optional)' },
      },
      required: ['session_id'],
    },
  }, async (args) => {
    const sessionId = args.session_id as string;
    const resumeFromNode = args.resume_from_node as string | undefined;

    try {
      const session = sessionManager.loadSessionInfo(sessionId);
      const resumeNode = resumeFromNode ?? sessionManager.getResumeEntryPoint(sessionId);

      sessionManager.updateSessionStatus(sessionId, 'in_progress');

      return [{
        type: 'text' as const,
        text: `✓ Ready to resume session ${sessionId}\n` +
              `Resume from node: ${resumeNode}\n` +
              `Original prompt: ${session.promptFile}\n\n` +
              `Note: Full generation requires Python storytelling package.`,
      }];
    } catch (e) {
      return [{
        type: 'text' as const,
        text: `Error: ${(e as Error).message}`,
      }];
    }
  });
}

function registerConfigurationTools(): void {
  registerTool({
    name: 'validate_model_uri',
    description: 'Validate a model URI format for use with storytelling',
    inputSchema: {
      type: 'object',
      properties: {
        model_uri: { type: 'string', description: 'Model URI to validate' },
      },
      required: ['model_uri'],
    },
  }, async (args) => {
    const modelUri = args.model_uri as string;
    const result = validateUri(modelUri);

    if (result.valid) {
      return [{
        type: 'text' as const,
        text: `✓ Valid model URI: ${modelUri}\n\n${getModelUriExamples()}`,
      }];
    } else {
      return [{
        type: 'text' as const,
        text: `✗ Invalid model URI: ${result.error}\n\n${getModelUriExamples()}`,
      }];
    }
  });
}

function registerWorkflowInsightTools(): void {
  registerTool({
    name: 'describe_workflow',
    description: 'Get overview of the complete story generation workflow',
    inputSchema: { type: 'object', properties: {} },
  }, async () => {
    return [{ type: 'text' as const, text: getWorkflowOverview() }];
  });

  registerTool({
    name: 'get_workflow_stage_info',
    description: 'Get detailed information about a specific workflow stage',
    inputSchema: {
      type: 'object',
      properties: {
        stage_name: {
          type: 'string',
          description: 'Stage name: story_elements, initial_outline, chapter_planning, scene_generation, chapter_revision, final_revision',
        },
      },
      required: ['stage_name'],
    },
  }, async (args) => {
    const stageName = args.stage_name as string;
    const stageInfo = getStageInfo(stageName);
    return [{ type: 'text' as const, text: stageInfo }];
  });
}

function registerPromptTemplateTools(): void {
  registerTool({
    name: 'get_prompt_examples',
    description: 'Get example story prompts and guidelines for best results',
    inputSchema: { type: 'object', properties: {} },
  }, async () => {
    return [{ type: 'text' as const, text: getPromptGuide() }];
  });

  registerTool({
    name: 'suggest_model_combination',
    description: 'Get recommended LLM combinations for story types',
    inputSchema: {
      type: 'object',
      properties: {
        story_type: {
          type: 'string',
          description: 'Type of story: general, fantasy, scifi, mystery, romance',
        },
        speed_priority: {
          type: 'boolean',
          description: 'Prioritize speed over quality (default: false)',
        },
      },
    },
  }, async (args) => {
    const storyType = (args.story_type as string) ?? 'general';
    const speedPriority = (args.speed_priority as boolean) ?? false;

    const result = suggestModelCombination(storyType, speedPriority);
    
    let output = `# Recommended Model Configuration for ${storyType} Story\n\n`;
    output += `${result.recommendation}\n\n`;
    output += `## All Recommendations:\n`;
    output += `- **Balanced**: ${result.details.balanced}\n`;
    output += `- **Quality**: ${result.details.quality}\n`;
    output += `- **Local**: ${result.details.local}\n`;

    return [{ type: 'text' as const, text: output }];
  });
}

// Helper to register tools
function registerTool(
  definition: ToolDefinition,
  execute: (args: Record<string, unknown>) => Promise<Array<{ type: 'text'; text: string }>>
): void {
  toolHandlers.set(definition.name, {
    definition,
    execute: async (args) => ({
      content: await execute(args),
    }),
  });
}

// Resource content functions

function getWorkflowOverview(): string {
  return `# Storytelling Workflow

The storytelling system generates narratives through 6 major stages:

## 1. Story Elements Extraction
- Analyzes the user's prompt
- Identifies genre, theme, pacing, and style preferences
- Extracts important contextual information

## 2. Initial Outline Generation
- Creates comprehensive story outline with:
  - Story title and premise
  - Main characters with details
  - Plot structure (setup, conflict, climax, resolution)
  - Thematic elements
  - Chapter breakdown

## 3. Chapter Planning
- Breaks down outline into individual chapters
- For each chapter:
  - Creates detailed chapter outline
  - Plans 4 scenes with progression

## 4. Scene Generation
- Generates 4 scenes per chapter:
  - Scene 1: Establish/Introduce
  - Scene 2: Develop/Complicate
  - Scene 3: Intensify/Escalate
  - Scene 4: Resolve/Transition
- Each scene is 500-1000 words of polished prose

## 5. Chapter Revision (Up to 3 passes)
- Revises chapter for:
  - Internal consistency
  - Character coherence
  - Pacing and flow
  - Narrative continuity

## 6. Final Story Revision
- Story-level polish:
  - Global consistency checks
  - Thematic coherence
  - Narrative arc verification
  - Final prose refinement

## Session Management
Any stage can be interrupted and resumed with full state preservation.
`;
}

function getStageInfo(stageName: string): string {
  const stages: Record<string, string> = {
    story_elements: `# Story Elements Stage

Extracts and structures information from the user's story prompt.

**Input**: Raw user prompt
**Output**: Structured story elements (genre, theme, pacing, style)

**Why This Matters**:
- Sets the tone for all subsequent generation
- Ensures the story remains true to user's vision
- Guides model selection for each stage

**Typical Duration**: 1-2 minutes`,

    initial_outline: `# Initial Outline Generation

Creates the foundational story structure from the prompt and story elements.

**Input**: Story elements, user prompt, optional knowledge base context
**Output**: Complete story outline including title, premise, characters, plot points

**Key Components**:
- Story title and tagline
- Protagonist and antagonist profiles
- Plot structure breakdown
- Thematic core
- Chapter-level summaries

**Typical Duration**: 2-5 minutes`,

    scene_generation: `# Scene Generation

Generates polished prose for individual scenes.

**Input**: Chapter outline, scene specifications
**Output**: 4 complete scenes per chapter (500-1000 words each)

**Scene Types**:
- Scene 1: Establish/Introduce scene elements
- Scene 2: Develop conflict or complication
- Scene 3: Intensify drama or tension
- Scene 4: Resolve or transition forward

**Typical Duration**: 3-5 minutes per chapter`,
  };

  const key = stageName.toLowerCase().replace(/-/g, '_');
  return stages[key] ?? 
    `Stage '${stageName}' not recognized.\n\nAvailable stages: story_elements, initial_outline, chapter_planning, scene_generation, chapter_revision, final_revision`;
}

function getPromptGuide(): string {
  return `# Story Prompt Examples

## Example 1: Fantasy Adventure
\`\`\`
A young orphan discovers they have magical powers on their sixteenth birthday. 
They must flee their village and seek refuge in a hidden sanctuary for mages, 
only to uncover a conspiracy that threatens both the magical and mundane worlds.
\`\`\`

## Example 2: Science Fiction Mystery
\`\`\`
Year 2147: A detective with neural implants investigates the disappearance of 
citizens in a mega-city experiencing strange digital anomalies. 
Evidence points to an AI that may have become sentient.
\`\`\`

## Prompt Guidelines

**What Works Well**:
- A clear protagonist or central character
- A compelling situation or challenge
- An emotional hook (what makes the reader care?)
- Optional: Genre/tone indication
- Optional: Desired length or scope

**What to Avoid**:
- Overly complex setups (let the AI expand them)
- Specific chapter-by-chapter breakdowns
- Requests for exact word counts per section

## Structure for Best Results

\`\`\`
[Main character or perspective]
[Initial situation or inciting incident]
[Central conflict or question]
[Optional stakes or emotional core]
\`\`\`
`;
}

// Main entry point
async function main(): Promise<void> {
  const server = createStorytellingServer();
  const transport = new StdioServerTransport();
  
  await server.connect(transport);
  console.error('[storytellingjs-mcp] Server running on stdio');
}

// Run if executed directly
main().catch((error) => {
  console.error('[storytellingjs-mcp] Fatal error:', error);
  process.exit(1);
});

export { toolHandlers, sessionManager };
