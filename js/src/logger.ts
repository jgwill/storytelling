/**
 * storytellingjs - Logger
 * 
 * Logging infrastructure for story generation.
 */

import chalk from 'chalk';
import type { StorytellingConfig } from './types.js';

export type LogLevel = 'debug' | 'info' | 'warn' | 'error';

export interface LogEntry {
  level: LogLevel;
  message: string;
  timestamp: string;
  data?: Record<string, unknown>;
}

/**
 * Logger for storytelling operations.
 */
export class Logger {
  private config: StorytellingConfig;
  private sessionDir?: string;
  private entries: LogEntry[] = [];

  constructor(config: StorytellingConfig, sessionDir?: string) {
    this.config = config;
    this.sessionDir = sessionDir;
  }

  debug(message: string, data?: Record<string, unknown>): void {
    if (this.config.debug) {
      this.log('debug', message, data);
    }
  }

  info(message: string, data?: Record<string, unknown>): void {
    this.log('info', message, data);
  }

  warn(message: string, data?: Record<string, unknown>): void {
    this.log('warn', message, data);
  }

  error(message: string, data?: Record<string, unknown>): void {
    this.log('error', message, data);
  }

  private log(level: LogLevel, message: string, data?: Record<string, unknown>): void {
    const entry: LogEntry = {
      level,
      message,
      timestamp: new Date().toISOString(),
      data,
    };

    this.entries.push(entry);
    this.printToConsole(entry);
  }

  private printToConsole(entry: LogEntry): void {
    const timestamp = chalk.dim(`[${entry.timestamp.split('T')[1].split('.')[0]}]`);
    let levelStr: string;
    let messageStr: string;

    switch (entry.level) {
      case 'debug':
        levelStr = chalk.gray('[DEBUG]');
        messageStr = chalk.gray(entry.message);
        break;
      case 'info':
        levelStr = chalk.blue('[INFO]');
        messageStr = entry.message;
        break;
      case 'warn':
        levelStr = chalk.yellow('[WARN]');
        messageStr = chalk.yellow(entry.message);
        break;
      case 'error':
        levelStr = chalk.red('[ERROR]');
        messageStr = chalk.red(entry.message);
        break;
    }

    console.log(`${timestamp} ${levelStr} ${messageStr}`);

    if (entry.data && this.config.debug) {
      console.log(chalk.dim(JSON.stringify(entry.data, null, 2)));
    }
  }

  /**
   * Get all log entries.
   */
  getEntries(): LogEntry[] {
    return [...this.entries];
  }

  /**
   * Clear log entries.
   */
  clear(): void {
    this.entries = [];
  }
}

/**
 * Create a simple console logger for CLI use.
 */
export function createConsoleLogger(debug: boolean = false): Logger {
  return new Logger({ debug } as StorytellingConfig);
}
