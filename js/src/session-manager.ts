/**
 * storytellingjs - Session Manager
 * 
 * Parity with Python storytelling/session_manager.py
 * Provides session persistence and resume capabilities.
 */

import { v4 as uuidv4 } from 'uuid';
import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync, statSync } from 'fs';
import { join, dirname } from 'path';
import type { 
  SessionInfo, 
  SessionCheckpoint, 
  SessionStatus, 
  WorkflowNode 
} from './types.js';

/**
 * Manages story generation sessions with checkpoint and resume capabilities.
 */
export class SessionManager {
  readonly baseLogsDir: string;

  constructor(baseLogsDir: string = 'Logs') {
    this.baseLogsDir = baseLogsDir;
    this.ensureDir(baseLogsDir);
  }

  /**
   * Create a new generation session.
   */
  createSession(options: {
    promptFile: string;
    outputFile: string;
    config: Record<string, unknown>;
  }): string {
    const sessionId = this.generateSessionId();
    const sessionDir = join(this.baseLogsDir, `Generation_${sessionId}`);
    this.ensureDir(sessionDir);

    const sessionInfo: SessionInfo = {
      sessionId,
      createdAt: new Date().toISOString(),
      lastCheckpoint: 'session_start',
      status: 'in_progress',
      promptFile: options.promptFile,
      outputFile: options.outputFile,
      checkpoints: [],
      configuration: options.config,
    };

    this.saveSessionInfo(sessionInfo);
    return sessionId;
  }

  /**
   * Save a checkpoint during generation.
   */
  saveCheckpoint(
    sessionId: string,
    nodeName: WorkflowNode,
    state: Record<string, unknown>,
    metadata: Record<string, unknown> = {}
  ): void {
    const sessionInfo = this.loadSessionInfo(sessionId);
    const checkpointId = `${nodeName}_${sessionInfo.checkpoints.length}`;

    const checkpoint: SessionCheckpoint = {
      checkpointId,
      nodeName,
      timestamp: new Date().toISOString(),
      state: this.sanitizeState(state),
      metadata,
    };

    // Save checkpoint file
    const sessionDir = join(this.baseLogsDir, `Generation_${sessionId}`);
    const checkpointFile = join(sessionDir, `checkpoint_${checkpointId}.json`);
    writeFileSync(checkpointFile, JSON.stringify(checkpoint, null, 2));

    // Update session info
    sessionInfo.checkpoints.push(checkpoint);
    sessionInfo.lastCheckpoint = checkpointId;
    this.saveSessionInfo(sessionInfo);
  }

  /**
   * Load session state from latest or specific checkpoint.
   */
  loadSessionState(
    sessionId: string,
    checkpointId?: string
  ): Record<string, unknown> {
    const sessionInfo = this.loadSessionInfo(sessionId);

    if (sessionInfo.checkpoints.length === 0) {
      throw new Error(`No checkpoints found for session ${sessionId}`);
    }

    let checkpoint: SessionCheckpoint | undefined;
    if (checkpointId) {
      checkpoint = sessionInfo.checkpoints.find(
        cp => cp.checkpointId === checkpointId
      );
      if (!checkpoint) {
        throw new Error(
          `Checkpoint ${checkpointId} not found in session ${sessionId}`
        );
      }
    } else {
      checkpoint = sessionInfo.checkpoints[sessionInfo.checkpoints.length - 1];
    }

    // Load checkpoint state from file
    const sessionDir = join(this.baseLogsDir, `Generation_${sessionId}`);
    const checkpointFile = join(sessionDir, `checkpoint_${checkpoint.checkpointId}.json`);

    if (!existsSync(checkpointFile)) {
      throw new Error(`Checkpoint file not found: ${checkpointFile}`);
    }

    const checkpointData = JSON.parse(readFileSync(checkpointFile, 'utf-8'));
    return checkpointData.state;
  }

  /**
   * List all available sessions.
   */
  listSessions(): SessionInfo[] {
    const sessions: SessionInfo[] = [];
    
    if (!existsSync(this.baseLogsDir)) {
      return sessions;
    }

    const entries = readdirSync(this.baseLogsDir);
    for (const entry of entries) {
      if (entry.startsWith('Generation_')) {
        const sessionDir = join(this.baseLogsDir, entry);
        const sessionFile = join(sessionDir, 'session_info.json');
        
        if (existsSync(sessionFile)) {
          try {
            const info = this.loadSessionInfoFromFile(sessionFile);
            sessions.push(info);
          } catch (e) {
            // Skip invalid sessions
          }
        }
      }
    }

    // Sort by creation date, newest first
    return sessions.sort((a, b) => 
      new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    );
  }

  /**
   * List checkpoints for a session.
   */
  listCheckpoints(sessionId: string): SessionCheckpoint[] {
    const sessionInfo = this.loadSessionInfo(sessionId);
    return sessionInfo.checkpoints;
  }

  /**
   * Load session information.
   */
  loadSessionInfo(sessionId: string): SessionInfo {
    const sessionDir = join(this.baseLogsDir, `Generation_${sessionId}`);
    const sessionFile = join(sessionDir, 'session_info.json');

    if (!existsSync(sessionFile)) {
      throw new Error(`Session ${sessionId} not found`);
    }

    return this.loadSessionInfoFromFile(sessionFile);
  }

  /**
   * Update session status.
   */
  updateSessionStatus(
    sessionId: string,
    status: SessionStatus,
    metadata?: Record<string, unknown>
  ): void {
    const sessionInfo = this.loadSessionInfo(sessionId);
    sessionInfo.status = status;

    if (metadata?.configuration) {
      Object.assign(sessionInfo.configuration, metadata.configuration);
    }

    this.saveSessionInfo(sessionInfo);
  }

  /**
   * Check if session can be resumed from a specific node.
   */
  canResumeFromNode(sessionId: string, nodeName: WorkflowNode): boolean {
    try {
      const checkpoints = this.listCheckpoints(sessionId);
      return checkpoints.some(cp => cp.nodeName === nodeName);
    } catch {
      return false;
    }
  }

  /**
   * Determine the best entry point for resuming generation.
   */
  getResumeEntryPoint(sessionId: string): WorkflowNode {
    const checkpoints = this.listCheckpoints(sessionId);

    if (checkpoints.length === 0) {
      return 'generate_story_elements';
    }

    const lastCheckpoint = checkpoints[checkpoints.length - 1];

    // Special case for chapter iteration
    if (lastCheckpoint.nodeName === 'increment_chapter_index') {
      const state = lastCheckpoint.state as {
        current_chapter_index?: number;
        total_chapters?: number;
      };
      const currentIndex = state.current_chapter_index ?? 0;
      const totalChapters = state.total_chapters ?? 1;

      if (currentIndex >= totalChapters) {
        return 'generate_final_story';
      }
      return 'generate_single_chapter_scene_by_scene';
    }

    // Node progression mapping
    const resumeMapping: Record<WorkflowNode, WorkflowNode> = {
      'generate_story_elements': 'generate_initial_outline',
      'generate_initial_outline': 'determine_chapter_count',
      'determine_chapter_count': 'generate_single_chapter_scene_by_scene',
      'generate_single_chapter_scene_by_scene': 'critique_chapter',
      'critique_chapter': 'check_chapter_complete',
      'check_chapter_complete': 'revise_chapter',
      'revise_chapter': 'critique_chapter',
      'increment_chapter_index': 'generate_single_chapter_scene_by_scene',
      'generate_final_story': 'generate_final_story',
    };

    return resumeMapping[lastCheckpoint.nodeName] ?? 'generate_story_elements';
  }

  // Private helpers

  private generateSessionId(): string {
    const now = new Date();
    return now.toISOString()
      .replace(/[:.]/g, '-')
      .replace('T', '_')
      .replace('Z', '');
  }

  private saveSessionInfo(sessionInfo: SessionInfo): void {
    const sessionDir = join(this.baseLogsDir, `Generation_${sessionInfo.sessionId}`);
    const sessionFile = join(sessionDir, 'session_info.json');
    this.ensureDir(sessionDir);
    writeFileSync(sessionFile, JSON.stringify(sessionInfo, null, 2));
  }

  private loadSessionInfoFromFile(sessionFile: string): SessionInfo {
    const data = JSON.parse(readFileSync(sessionFile, 'utf-8'));
    return data as SessionInfo;
  }

  private sanitizeState(state: Record<string, unknown>): Record<string, unknown> {
    const serializable: Record<string, unknown> = {};
    const skipKeys = ['logger', 'config', 'retriever'];

    for (const [key, value] of Object.entries(state)) {
      if (skipKeys.includes(key)) continue;
      
      // Skip non-serializable objects
      if (typeof value === 'function') continue;
      if (typeof value === 'object' && value !== null) {
        // Try to serialize, skip if fails
        try {
          JSON.stringify(value);
          serializable[key] = value;
        } catch {
          continue;
        }
      } else {
        serializable[key] = value;
      }
    }

    return serializable;
  }

  private ensureDir(dir: string): void {
    if (!existsSync(dir)) {
      mkdirSync(dir, { recursive: true });
    }
  }
}

/**
 * Migrate an existing session directory to new format.
 */
export function migrateExistingSession(
  logsDir: string,
  sessionId: string
): SessionInfo {
  const sessionManager = new SessionManager(logsDir);
  const sessionDir = join(logsDir, `Generation_${sessionId}`);

  if (!existsSync(sessionDir)) {
    throw new Error(`Session directory not found: ${sessionDir}`);
  }

  const stat = statSync(sessionDir);
  const sessionInfo: SessionInfo = {
    sessionId,
    createdAt: stat.birthtime.toISOString(),
    lastCheckpoint: 'determine_chapter_count',
    status: 'interrupted',
    promptFile: 'prompt.txt',
    outputFile: `story_output_${sessionId}`,
    checkpoints: [],
    configuration: {},
  };

  // Check for existing debug files and create checkpoints
  const debugDir = join(sessionDir, 'LangchainDebug');
  if (existsSync(debugDir)) {
    const storyElementsFile = join(debugDir, '01_StoryElements.json');
    if (existsSync(storyElementsFile)) {
      const stat = statSync(storyElementsFile);
      sessionInfo.checkpoints.push({
        checkpointId: 'story_elements_0',
        nodeName: 'generate_story_elements',
        timestamp: stat.mtime.toISOString(),
        state: { completed: true },
        metadata: { source: 'migrated' },
      });
    }

    const outlineFile = join(debugDir, '02_InitialOutline.json');
    if (existsSync(outlineFile)) {
      const stat = statSync(outlineFile);
      sessionInfo.checkpoints.push({
        checkpointId: 'initial_outline_0',
        nodeName: 'generate_initial_outline',
        timestamp: stat.mtime.toISOString(),
        state: { completed: true },
        metadata: { source: 'migrated' },
      });
    }
  }

  // Save migrated session
  const sessionFile = join(sessionDir, 'session_info.json');
  writeFileSync(sessionFile, JSON.stringify(sessionInfo, null, 2));

  return sessionInfo;
}
