# storytellingjs

🌸 TypeScript story generation library with CLI and MCP server.

Full parity with the Python `storytelling` package, designed for Node.js/TypeScript ecosystem.

## Installation

```bash
npm install storytellingjs
```

## CLI Usage

```bash
# Generate a story
storytellingjs --prompt story_prompt.txt --output my_story.md

# List sessions
storytellingjs --list-sessions

# Resume a session
storytellingjs --resume <session-id>

# Get session info
storytellingjs --session-info <session-id>
```

## Library Usage

```typescript
import { 
  StorySession, 
  SessionManager, 
  StorytellingConfig 
} from 'storytellingjs';

// Create session manager
const sessionManager = new SessionManager('./Logs');

// Create new session
const sessionId = await sessionManager.createSession({
  promptFile: 'story.txt',
  outputFile: 'output.md',
  config: {}
});

// List sessions
const sessions = await sessionManager.listSessions();
```

## MCP Server

```bash
# Start MCP server (stdio mode)
storytellingjs-mcp
```

Or programmatically:

```typescript
import { createStorytellingServer } from 'storytellingjs/mcp';

const server = createStorytellingServer();
await server.start();
```

### MCP Tools

- `generate_story` - Generate a complete story
- `list_sessions` - List all available sessions
- `get_session_info` - Get information about a session
- `resume_session` - Resume an interrupted session
- `describe_workflow` - Get workflow overview
- `get_workflow_stage_info` - Get stage details
- `validate_model_uri` - Validate model URI format
- `get_prompt_examples` - Get example prompts
- `suggest_model_combination` - Get model recommendations

## Model URI Format

```
google://gemini-2.5-flash
ollama://model-name@localhost:11434
openrouter://model-name
myflowise://flow-id
```

## Integration with mia-code/miatel

```typescript
// In miatel commands
import { SessionManager, Story } from 'storytellingjs';

const sessionManager = new SessionManager();
const session = await sessionManager.createSession({
  promptFile: 'prompt.txt',
  outputFile: 'story.md',
  config: { title: 'My Story' }
});
```

## RISE Framework

This package follows the RISE framework specifications. See `rispecs/` for detailed specifications.

## License

MIT
