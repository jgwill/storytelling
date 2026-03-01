/**
 * storytellingjs - Prompt Templates
 *
 * Parity with Python storytelling/prompts.py
 * Template strings for each story generation stage.
 */

// =============================================================================
// Template Helper
// =============================================================================

/**
 * Simple template interpolation using {variable} syntax.
 * Mirrors ChatPromptTemplate.from_template behavior.
 */
export function formatTemplate(template: string, variables: Record<string, string>): string {
  let result = template;
  for (const [key, value] of Object.entries(variables)) {
    result = result.replaceAll(`{${key}}`, value);
  }
  return result;
}

// =============================================================================
// 1. Outline Generation Prompts
// =============================================================================

export const GET_IMPORTANT_BASE_PROMPT_INFO = `Please extract any important information from the user's prompt below:

<USER_PROMPT>
{_Prompt}
</USER_PROMPT>

Just write down any information that wouldn't be covered in an outline.
Please use the below template for formatting your response.
This would be things like instructions for chapter length, overall vision, instructions for formatting, etc.

<EXAMPLE>
# Important Additional Context
- Important point 1
- Important point 2
</EXAMPLE>

Do NOT write the outline itself, just some extra context. Keep your responses short.
Dont introduce nor conclude your answer, just output results.`;

export const STORY_ELEMENTS_PROMPT = `I'm working on writing a fictional story, and I'd like your help writing out the story elements.

Here's the prompt for my story.
<PROMPT>
{_OutlinePrompt}
</PROMPT>

Please make your response have the following format:

<RESPONSE_TEMPLATE>
# Story Title

## Genre
- **Category**: (e.g., romance, mystery, science fiction, fantasy, horror)

## Theme
- **Central Idea or Message**:

## Pacing
- **Speed**: (e.g., slow, fast)

## Style
- **Language Use**: (e.g., sentence structure, vocabulary, tone, figurative language)

## Plot
- **Exposition**:
- **Rising Action**:
- **Climax**:
- **Falling Action**:
- **Resolution**:

## Setting
- **Time**: (e.g., present day, future, past)
- **Location**: (e.g., city, countryside, space)
- **World-Building Details**:

## Characters
- **Protagonist**: (Name, description, motivations)
- **Antagonist**: (Name, description, motivations)
- **Supporting Characters**: (Names and roles)

## Conflict
- **Internal Conflict**: (Character vs. self)
- **External Conflict**: (Character vs. character, society, nature, technology)

## Perspective
- **Point of View**: (e.g., first person, third person, omniscient)
- **Narrative Voice**: (e.g., formal, casual, poetic)
</RESPONSE_TEMPLATE>

Please fill in the template above based on the story prompt.`;

export const INITIAL_OUTLINE_PROMPT = `I'm working on writing a fictional story. I need a detailed outline.

<STORY_ELEMENTS>
{_StoryElements}
</STORY_ELEMENTS>

<EXTRA_CONTEXT>
{_BaseContext}
</EXTRA_CONTEXT>

<KNOWLEDGE_CONTEXT>
{_RagContext}
</KNOWLEDGE_CONTEXT>

Please write a detailed chapter-by-chapter outline for this story. For each chapter, include:
1. Chapter title
2. Key events and plot points
3. Character development moments
4. Setting details
5. Emotional tone/arc

Write the outline in a clear, organized format.`;

export const CHAPTER_COUNT_PROMPT = `Based on the following outline, determine the optimal number of chapters:

<OUTLINE>
{_Outline}
</OUTLINE>

Respond with ONLY a JSON object in this format:
{{"TotalChapters": <number>}}`;

export const SCENE_OUTLINE_PROMPT = `Based on the following chapter outline, break it down into 3-4 detailed scenes:

<CHAPTER_OUTLINE>
{_ChapterOutline}
</CHAPTER_OUTLINE>

<STORY_CONTEXT>
{_StoryContext}
</STORY_CONTEXT>

For each scene, provide a detailed outline (2-3 sentences) describing:
- What happens in the scene
- Key character interactions
- Emotional beats

Respond with ONLY a JSON object: {{"scenes": ["scene 1 outline", "scene 2 outline", ...]}}`;

// =============================================================================
// 2. Chapter Generation Prompts
// =============================================================================

export const GENERATE_SCENE_PROMPT = `Write the following scene for a story chapter.

<STORY_ELEMENTS>
{_StoryElements}
</STORY_ELEMENTS>

<CHAPTER_OUTLINE>
{_ChapterOutline}
</CHAPTER_OUTLINE>

<PREVIOUS_CONTENT>
{_PreviousContent}
</PREVIOUS_CONTENT>

<KNOWLEDGE_CONTEXT>
{_RagContext}
</KNOWLEDGE_CONTEXT>

<SCENE_OUTLINE>
{_SceneOutline}
</SCENE_OUTLINE>

Write this scene as polished prose. Focus on:
- Vivid, sensory descriptions
- Natural dialogue
- Character voice consistency
- Emotional resonance

Write ONLY the scene content. Do not add scene titles or labels.`;

// =============================================================================
// 3. Critique and Revision Prompts
// =============================================================================

export const CRITIQUE_CHAPTER_PROMPT = `Provide a detailed critique of the following chapter:

<CHAPTER>
{_Chapter}
</CHAPTER>

<OUTLINE>
{_ChapterOutline}
</OUTLINE>

Evaluate:
1. Plot consistency with the outline
2. Character voice and development
3. Pacing and tension
4. Prose quality and style
5. Emotional impact

Provide specific, actionable suggestions for improvement.`;

export const CHECK_CHAPTER_COMPLETE_PROMPT = `Evaluate whether the following chapter meets quality standards:

<CHAPTER>
{_Chapter}
</CHAPTER>

<CRITIQUE>
{_Critique}
</CRITIQUE>

Consider: Does the chapter adequately address the critique points?
Respond with ONLY: {{"IsComplete": true}} or {{"IsComplete": false}}`;

export const REVISE_CHAPTER_PROMPT = `Revise the following chapter based on the critique:

<CHAPTER>
{_Chapter}
</CHAPTER>

<CRITIQUE>
{_Critique}
</CRITIQUE>

<OUTLINE>
{_ChapterOutline}
</OUTLINE>

Apply the suggested improvements while maintaining the chapter's voice and flow.
Output ONLY the revised chapter with no commentary.`;

// =============================================================================
// 4. Story Finalization Prompts
// =============================================================================

export const FINAL_STORY_PROMPT = `Compile and polish the final story from these chapters:

<STORY_ELEMENTS>
{_StoryElements}
</STORY_ELEMENTS>

<CHAPTERS>
{_Chapters}
</CHAPTERS>

Create a cohesive final version. Ensure:
- Smooth transitions between chapters
- Consistent character voices
- Resolved plot threads
- Satisfying narrative arc

Output the complete story.`;

export const STORY_INFO_PROMPT = `Based on the following story, provide metadata:

<STORY>
{_Story}
</STORY>

Respond with ONLY a JSON object:
{{
  "Title": "story title",
  "Summary": "brief summary",
  "Tags": "comma,separated,tags",
  "OverallRating": <1-10>
}}`;

// =============================================================================
// 5. Style Revision Prompts
// =============================================================================

export const REVISE_BUZZ_TERMS_PROMPT = `Revise the following chapter to remove overused terms and clichés:

<CHAPTER>
{_Chapter}
</CHAPTER>

## Terms to Avoid
{_AvoidTerms}

## Custom Phrases to Avoid
{_AvoidPhrases}

## Preferred Alternatives
{_Alternatives}

## Instructions
1. Identify any instances of the terms or phrases listed above
2. Replace them with more specific, vivid, or contextually appropriate alternatives
3. Maintain the original meaning, tone, and flow of the narrative
4. Do NOT add new content or change the plot
5. Preserve character voices and dialogue authenticity
6. If a term is used appropriately in context, it may remain

Output ONLY the revised chapter with no commentary.`;

export const DETECT_BUZZ_TERMS_PROMPT = `Analyze the following chapter and identify any overused, cliché, or "buzz" terms.

<CHAPTER>
{_Chapter}
</CHAPTER>

## Terms to Flag
{_AvoidTerms}

## Custom Phrases to Flag
{_AvoidPhrases}

## Output Format
Provide a JSON response:
{{
    "found_terms": ["list", "of", "found", "terms"],
    "found_phrases": ["list of found phrases"],
    "total_issues": <number>,
    "severity": "none" | "low" | "moderate" | "high",
    "suggestions": [
        {{"original": "term", "context": "...surrounding text...", "suggestion": "alternative"}}
    ]
}}

Only flag terms that are actually used in cliché or overused ways.`;

// =============================================================================
// 6. Translation Prompts
// =============================================================================

export const TRANSLATE_PROMPT = `Translate the following text to {_TargetLanguage}:

<TEXT>
{_Text}
</TEXT>

{_TranslateInstructions}

Maintain the original formatting, style, and tone.
Output ONLY the translated text.`;

// =============================================================================
// Prompt Registry
// =============================================================================

/** All available prompts indexed by name */
export const PROMPTS: Record<string, string> = {
  GET_IMPORTANT_BASE_PROMPT_INFO,
  STORY_ELEMENTS_PROMPT,
  INITIAL_OUTLINE_PROMPT,
  CHAPTER_COUNT_PROMPT,
  SCENE_OUTLINE_PROMPT,
  GENERATE_SCENE_PROMPT,
  CRITIQUE_CHAPTER_PROMPT,
  CHECK_CHAPTER_COMPLETE_PROMPT,
  REVISE_CHAPTER_PROMPT,
  FINAL_STORY_PROMPT,
  STORY_INFO_PROMPT,
  REVISE_BUZZ_TERMS_PROMPT,
  DETECT_BUZZ_TERMS_PROMPT,
  TRANSLATE_PROMPT,
};
