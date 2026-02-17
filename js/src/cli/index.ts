#!/usr/bin/env node
/**
 * storytellingjs CLI
 * 
 * Command-line interface for story generation.
 * Parity with Python storytelling CLI.
 */

import { Command } from 'commander';
import chalk from 'chalk';
import { existsSync, readFileSync } from 'fs';
import { 
  SessionManager, 
  createConfig, 
  VERSION,
  getModelUriExamples,
  suggestModelCombination,
} from '../index.js';

const program = new Command();

program
  .name('storytellingjs')
  .description('🌸 storytellingjs — AI Story Generation System')
  .version(VERSION);

// Generate story command (default)
program
  .option('-p, --prompt <file>', 'Path to prompt file')
  .option('-o, --output <file>', 'Output file path')
  .option('--initial-outline-model <uri>', 'Model for initial outline')
  .option('--chapter-outline-model <uri>', 'Model for chapter outline')
  .option('--chapter-s1-model <uri>', 'Model for scene 1')
  .option('--chapter-s2-model <uri>', 'Model for scene 2')
  .option('--chapter-s3-model <uri>', 'Model for scene 3')
  .option('--chapter-s4-model <uri>', 'Model for scene 4')
  .option('--chapter-revision-model <uri>', 'Model for chapter revision')
  .option('--revision-model <uri>', 'Model for final revision')
  .option('--knowledge-base-path <path>', 'Path to knowledge base')
  .option('--embedding-model <uri>', 'Embedding model for RAG')
  .option('--chapter-max-revisions <n>', 'Max revisions per chapter', '3')
  .option('--expand-outline', 'Expand outline', true)
  .option('--no-expand-outline', 'Do not expand outline')
  .option('--debug', 'Enable debug mode')
  .option('--mock-mode', 'Use mock responses for testing');

// Session management options
program
  .option('--list-sessions', 'List available sessions')
  .option('--session-info <id>', 'Show information about a session')
  .option('--resume <id>', 'Resume from session ID')
  .option('--resume-from-node <node>', 'Resume from specific node')
  .option('--migrate-session <id>', 'Migrate existing session to new format');

// Main action
program.action(async (options) => {
  const sessionManager = new SessionManager();

  // Handle --list-sessions
  if (options.listSessions) {
    const sessions = sessionManager.listSessions();
    
    if (sessions.length === 0) {
      console.log('No sessions found.');
      return;
    }

    console.log(chalk.bold(`Found ${sessions.length} sessions:`));
    console.log('-'.repeat(80));
    
    for (const session of sessions) {
      const statusIcon = {
        'completed': '✅',
        'in_progress': '🔄',
        'failed': '❌',
        'interrupted': '⏸️',
      }[session.status] ?? '❓';

      console.log(`${statusIcon} ${chalk.cyan(session.sessionId)}`);
      console.log(`   Created: ${session.createdAt}`);
      console.log(`   Status: ${session.status}`);
      console.log(`   Prompt: ${session.promptFile}`);
      console.log(`   Checkpoints: ${session.checkpoints.length}`);
      if (session.checkpoints.length > 0) {
        const lastCp = session.checkpoints[session.checkpoints.length - 1];
        console.log(`   Last checkpoint: ${lastCp.nodeName}`);
      }
      console.log();
    }
    return;
  }

  // Handle --session-info
  if (options.sessionInfo) {
    try {
      const session = sessionManager.loadSessionInfo(options.sessionInfo);
      const checkpoints = sessionManager.listCheckpoints(options.sessionInfo);

      console.log(chalk.bold(`Session: ${session.sessionId}`));
      console.log('-'.repeat(50));
      console.log(`Created: ${session.createdAt}`);
      console.log(`Status: ${session.status}`);
      console.log(`Prompt: ${session.promptFile}`);
      console.log(`Output: ${session.outputFile}`);
      console.log(`Last checkpoint: ${session.lastCheckpoint}`);
      console.log();
      console.log(chalk.bold(`Checkpoints (${checkpoints.length}):`));
      
      checkpoints.forEach((cp, i) => {
        console.log(`  ${i + 1}. ${cp.nodeName} (${cp.timestamp})`);
      });

      if (checkpoints.length > 0) {
        const resumePoint = sessionManager.getResumeEntryPoint(options.sessionInfo);
        console.log(`\nSuggested resume point: ${chalk.green(resumePoint)}`);
      }
    } catch (e) {
      console.error(chalk.red(`Error loading session info: ${(e as Error).message}`));
      process.exit(1);
    }
    return;
  }

  // Handle --migrate-session
  if (options.migrateSession) {
    try {
      const { migrateExistingSession } = await import('../session-manager.js');
      const sessionInfo = migrateExistingSession('Logs', options.migrateSession);
      console.log(chalk.green(`✓ Successfully migrated session ${options.migrateSession}`));
      console.log(`  Status: ${sessionInfo.status}`);
      console.log(`  Checkpoints: ${sessionInfo.checkpoints.length}`);
    } catch (e) {
      console.error(chalk.red(`Error migrating session: ${(e as Error).message}`));
      process.exit(1);
    }
    return;
  }

  // Handle --resume
  if (options.resume) {
    try {
      const session = sessionManager.loadSessionInfo(options.resume);
      const config = createConfig(options);

      console.log(chalk.bold(`Resuming session ${options.resume}...`));
      console.log(`Original prompt: ${session.promptFile}`);
      console.log(`Session status: ${session.status}`);

      const resumeNode = options.resumeFromNode ?? 
        sessionManager.getResumeEntryPoint(options.resume);
      
      console.log(`Resuming from node: ${chalk.green(resumeNode)}`);

      // Update session status
      sessionManager.updateSessionStatus(options.resume, 'in_progress');

      // TODO: Implement actual graph execution
      console.log(chalk.yellow('\n⚠ Graph execution not yet implemented in JS version.'));
      console.log('Use Python storytelling package for full generation.');
      
    } catch (e) {
      console.error(chalk.red(`Error resuming session: ${(e as Error).message}`));
      process.exit(1);
    }
    return;
  }

  // Handle story generation (requires --prompt)
  if (!options.prompt) {
    console.log(chalk.bold('🌸 storytellingjs - AI Story Generation System\n'));
    console.log('Usage: storytellingjs [OPTIONS] --prompt <file>\n');
    console.log('Session Management:');
    console.log('  --list-sessions           List available sessions');
    console.log('  --session-info <id>       Show information about a session');
    console.log('  --resume <id>             Resume from session ID');
    console.log('  --resume-from-node <node> Resume from specific node');
    console.log('\nFor full options, run: storytellingjs --help');
    console.log('\n' + getModelUriExamples());
    return;
  }

  // Validate prompt file exists
  if (!existsSync(options.prompt)) {
    console.error(chalk.red(`Error: Prompt file '${options.prompt}' not found`));
    process.exit(1);
  }

  const config = createConfig({
    promptFile: options.prompt,
    outputFile: options.output ?? `story_output_${Date.now()}`,
    initialOutlineModel: options.initialOutlineModel,
    chapterOutlineModel: options.chapterOutlineModel,
    chapterS1Model: options.chapterS1Model,
    chapterS2Model: options.chapterS2Model,
    chapterS3Model: options.chapterS3Model,
    chapterS4Model: options.chapterS4Model,
    chapterRevisionModel: options.chapterRevisionModel,
    revisionModel: options.revisionModel,
    knowledgeBasePath: options.knowledgeBasePath,
    embeddingModel: options.embeddingModel,
    chapterMaxRevisions: parseInt(options.chapterMaxRevisions, 10),
    expandOutline: options.expandOutline,
    debug: options.debug ?? false,
    mockMode: options.mockMode ?? false,
  });

  // Create new session
  const sessionId = sessionManager.createSession({
    promptFile: config.promptFile!,
    outputFile: config.outputFile!,
    config: config as unknown as Record<string, unknown>,
  });

  console.log(chalk.bold('🌸 storytellingjs - Starting Story Generation\n'));
  console.log(`Session: ${chalk.cyan(sessionId)}`);
  console.log(`Prompt: ${config.promptFile}`);
  console.log(`Output: ${config.outputFile}`);
  console.log();

  // TODO: Implement actual graph execution
  console.log(chalk.yellow('⚠ Full graph execution not yet implemented in JS version.'));
  console.log('Use Python storytelling package for complete generation.');
  console.log('\nSession created. You can resume later with:');
  console.log(chalk.dim(`  storytellingjs --resume ${sessionId}`));
});

// Workflow info command
program
  .command('workflow')
  .description('Describe the story generation workflow')
  .option('--stage <name>', 'Get info about a specific stage')
  .action((options) => {
    if (options.stage) {
      const stageInfo = getStageInfo(options.stage);
      console.log(stageInfo);
    } else {
      console.log(getWorkflowDescription());
    }
  });

// Model recommendation command
program
  .command('recommend')
  .description('Get model recommendations for story types')
  .option('-t, --type <type>', 'Story type (general, fantasy, scifi, mystery, romance)', 'general')
  .option('-s, --speed', 'Prioritize speed over quality')
  .action((options) => {
    const result = suggestModelCombination(options.type, options.speed);
    console.log(chalk.bold(`\nRecommended Model Configuration for ${options.type.charAt(0).toUpperCase() + options.type.slice(1)} Story\n`));
    console.log(result.recommendation);
    console.log('\nAll Recommendations:');
    console.log(`  Balanced: ${result.details.balanced}`);
    console.log(`  Quality: ${result.details.quality}`);
    console.log(`  Local: ${result.details.local}`);
  });

// Examples command
program
  .command('examples')
  .description('Show usage examples')
  .action(() => {
    console.log(chalk.bold('\n🌸 storytellingjs Examples\n'));
    
    console.log(chalk.dim('# Generate a story'));
    console.log('  storytellingjs --prompt story_prompt.txt --output my_story.md\n');
    
    console.log(chalk.dim('# List sessions'));
    console.log('  storytellingjs --list-sessions\n');
    
    console.log(chalk.dim('# Resume a session'));
    console.log('  storytellingjs --resume <session-id>\n');
    
    console.log(chalk.dim('# Get workflow info'));
    console.log('  storytellingjs workflow\n');
    
    console.log(chalk.dim('# Get model recommendations'));
    console.log('  storytellingjs recommend --type fantasy\n');
    
    console.log(chalk.dim('# With specific models'));
    console.log('  storytellingjs --prompt story.txt \\');
    console.log('    --initial-outline-model google://gemini-pro \\');
    console.log('    --chapter-s1-model google://gemini-2.5-flash\n');
  });

program.parseAsync(process.argv);

// Helper functions

function getWorkflowDescription(): string {
  return `
${chalk.bold('Storytelling Workflow')}

The storytelling system generates narratives through 6 major stages:

${chalk.bold('1. Story Elements Extraction')}
   - Analyzes the user's prompt
   - Identifies genre, theme, pacing, and style preferences

${chalk.bold('2. Initial Outline Generation')}
   - Creates comprehensive story outline with:
     - Story title and premise
     - Main characters with details
     - Plot structure

${chalk.bold('3. Chapter Planning')}
   - Breaks down outline into individual chapters
   - Creates detailed chapter outline with 4-scene structure

${chalk.bold('4. Scene Generation')}
   - Generates 4 scenes per chapter:
     - Scene 1: Establish/Introduce
     - Scene 2: Develop/Complicate
     - Scene 3: Intensify/Escalate
     - Scene 4: Resolve/Transition

${chalk.bold('5. Chapter Revision')} (Up to 3 passes)
   - Internal consistency
   - Character coherence
   - Pacing and flow

${chalk.bold('6. Final Story Revision')}
   - Global consistency checks
   - Thematic coherence
   - Final prose polish

Use ${chalk.cyan('storytellingjs workflow --stage <name>')} for stage details.
`.trim();
}

function getStageInfo(stageName: string): string {
  const stages: Record<string, string> = {
    story_elements: `
${chalk.bold('Story Elements Stage')}

Extracts and structures information from the user's story prompt.

${chalk.dim('Input:')} Raw user prompt
${chalk.dim('Output:')} Structured story elements (genre, theme, pacing, style)

${chalk.bold('Why This Matters:')}
- Sets the tone for all subsequent generation
- Ensures the story remains true to user's vision

${chalk.dim('Typical Duration:')} 1-2 minutes
`,
    initial_outline: `
${chalk.bold('Initial Outline Generation')}

Creates the foundational story structure.

${chalk.dim('Input:')} Story elements, user prompt, optional knowledge base context
${chalk.dim('Output:')} Complete story outline including title, premise, characters, plot points

${chalk.bold('Key Components:')}
- Story title and tagline
- Protagonist and antagonist profiles
- Plot structure breakdown
- Chapter-level summaries

${chalk.dim('Typical Duration:')} 2-5 minutes
`,
    scene_generation: `
${chalk.bold('Scene Generation')}

Generates polished prose for individual scenes.

${chalk.dim('Input:')} Chapter outline, scene specifications
${chalk.dim('Output:')} 4 complete scenes per chapter (500-1000 words each)

${chalk.bold('Scene Types:')}
- Scene 1: Establish/Introduce scene elements
- Scene 2: Develop conflict or complication
- Scene 3: Intensify drama or tension
- Scene 4: Resolve or transition forward

${chalk.dim('Typical Duration:')} 3-5 minutes per chapter
`,
  };

  const key = stageName.toLowerCase().replace(/-/g, '_');
  return stages[key] ?? chalk.yellow(`Stage '${stageName}' not found. Try: story_elements, initial_outline, scene_generation`);
}
