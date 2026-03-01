/**
 * storytellingjs - Ceremonial Diary
 *
 * Parity with Python storytelling/ceremonial_diary.py
 * Diary export and management for IAIP integration.
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync } from 'fs';
import { join, dirname } from 'path';
import { v4 as uuidv4 } from 'uuid';

// =============================================================================
// Enums
// =============================================================================

export enum CeremonialPhase {
  MIIGWECHIWENDAM = 'miigwechiwendam', // Sacred Space Creation
  NINDOKENDAAN = 'nindokendaan',       // Two-Eyed Research Gathering
  NINGWAAB = 'ningwaab',               // Knowledge Integration
  NINDOODAM = 'nindoodam',             // Creative Expression
  MIGWECH = 'migwech',                 // Ceremonial Closing
}

export enum EntryType {
  INTENTION = 'intention',
  OBSERVATION = 'observation',
  HYPOTHESIS = 'hypothesis',
  DATA = 'data',
  SYNTHESIS = 'synthesis',
  ACTION = 'action',
  REFLECTION = 'reflection',
  LEARNING = 'learning',
}

// =============================================================================
// Diary Entry
// =============================================================================

export interface DiaryEntry {
  id: string;
  timestamp: string;
  participant: string;
  phase: CeremonialPhase;
  entryType: EntryType;
  content: string;
  metadata: Record<string, unknown>;
}

export function createDiaryEntry(
  participant: string,
  phase: CeremonialPhase,
  entryType: EntryType,
  content: string,
  metadata?: Record<string, unknown>,
): DiaryEntry {
  return {
    id: uuidv4(),
    timestamp: new Date().toISOString(),
    participant,
    phase,
    entryType,
    content,
    metadata: metadata ?? {},
  };
}

// =============================================================================
// Ceremonial Diary
// =============================================================================

export class CeremonialDiary {
  readonly diaryId: string;
  readonly title: string;
  private entries: DiaryEntry[] = [];
  private metadata: Record<string, unknown>;

  constructor(title: string, metadata?: Record<string, unknown>) {
    this.diaryId = uuidv4();
    this.title = title;
    this.metadata = metadata ?? {};
  }

  addEntry(entry: DiaryEntry): void {
    this.entries.push(entry);
  }

  getEntries(phase?: CeremonialPhase): DiaryEntry[] {
    if (phase) {
      return this.entries.filter((e) => e.phase === phase);
    }
    return [...this.entries];
  }

  getEntriesByParticipant(participant: string): DiaryEntry[] {
    return this.entries.filter((e) => e.participant === participant);
  }

  getEntriesByType(entryType: EntryType): DiaryEntry[] {
    return this.entries.filter((e) => e.entryType === entryType);
  }

  /**
   * Export diary as YAML-compatible object.
   */
  toYAML(): Record<string, unknown> {
    return {
      diary_id: this.diaryId,
      title: this.title,
      metadata: this.metadata,
      created_at: this.entries[0]?.timestamp ?? new Date().toISOString(),
      updated_at: this.entries[this.entries.length - 1]?.timestamp ?? new Date().toISOString(),
      entry_count: this.entries.length,
      phases: Object.values(CeremonialPhase).map((phase) => ({
        phase,
        entries: this.entries
          .filter((e) => e.phase === phase)
          .map((e) => ({
            id: e.id,
            timestamp: e.timestamp,
            participant: e.participant,
            type: e.entryType,
            content: e.content,
            ...(Object.keys(e.metadata).length > 0 ? { metadata: e.metadata } : {}),
          })),
      })),
    };
  }

  /**
   * Export diary as Markdown.
   */
  toMarkdown(): string {
    let md = `# ${this.title}\n\n`;
    md += `**Diary ID**: ${this.diaryId}\n`;
    md += `**Entries**: ${this.entries.length}\n\n`;

    for (const phase of Object.values(CeremonialPhase)) {
      const phaseEntries = this.entries.filter((e) => e.phase === phase);
      if (phaseEntries.length === 0) continue;

      md += `## ${phase}\n\n`;

      for (const entry of phaseEntries) {
        md += `### ${entry.entryType} — ${entry.participant}\n`;
        md += `*${entry.timestamp}*\n\n`;
        md += `${entry.content}\n\n`;
      }
    }

    return md;
  }

  /**
   * Save diary to JSON file.
   */
  save(filePath: string): void {
    const dir = dirname(filePath);
    if (!existsSync(dir)) {
      mkdirSync(dir, { recursive: true });
    }
    writeFileSync(filePath, JSON.stringify(this.toYAML(), null, 2));
  }

  /**
   * Load diary from JSON file.
   */
  static load(filePath: string): CeremonialDiary {
    const data = JSON.parse(readFileSync(filePath, 'utf-8'));
    const diary = new CeremonialDiary(data.title, data.metadata);

    for (const phaseGroup of data.phases ?? []) {
      for (const entry of phaseGroup.entries ?? []) {
        diary.addEntry({
          id: entry.id,
          timestamp: entry.timestamp,
          participant: entry.participant,
          phase: phaseGroup.phase as CeremonialPhase,
          entryType: entry.type as EntryType,
          content: entry.content,
          metadata: entry.metadata ?? {},
        });
      }
    }

    return diary;
  }
}

// =============================================================================
// Diary Manager
// =============================================================================

export class DiaryManager {
  readonly baseDir: string;

  constructor(baseDir: string = 'diaries') {
    this.baseDir = baseDir;
    if (!existsSync(baseDir)) {
      mkdirSync(baseDir, { recursive: true });
    }
  }

  createDiary(title: string, metadata?: Record<string, unknown>): CeremonialDiary {
    const diary = new CeremonialDiary(title, metadata);
    this.saveDiary(diary);
    return diary;
  }

  saveDiary(diary: CeremonialDiary): void {
    const filePath = join(this.baseDir, `${diary.diaryId}.json`);
    diary.save(filePath);
  }

  loadDiary(diaryId: string): CeremonialDiary {
    const filePath = join(this.baseDir, `${diaryId}.json`);
    return CeremonialDiary.load(filePath);
  }

  listDiaries(): string[] {
    if (!existsSync(this.baseDir)) return [];
    return readdirSync(this.baseDir)
      .filter((f) => f.endsWith('.json'))
      .map((f) => f.replace('.json', ''));
  }
}
