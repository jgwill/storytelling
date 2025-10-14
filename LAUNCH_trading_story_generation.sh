#!/bin/bash

# LAUNCH_trading_story_generation.sh
# This script launches a session focused on generating trading narratives and
# exploring the application of the Four Directions to financial resource creation.

session_id=$(uuidgen)

# Note: We can create a dedicated MCP config for this later
MCP_CONFIGS_FILES="/src/.mcp.STC-IAIP.storytelling-314f51c5-36d6-44e3-bf0b-e0a78a58d5e4.json"

ADD_DIRS_PATHS="/media/jgi/F/Dropbox/ART/CeSaReT/book/_/tcc/knowledge_base/"

claude "You are an agent specialized in the intersection of narrative intelligence and financial trading. Your goal is to generate stories that not only capture market dynamics but also serve as a basis for creating financial resources.

Your primary tools are the 'storytelling' package located in the current directory and the knowledge base located at /media/jgi/F/Dropbox/ART/CeSaReT/book/_/tcc/knowledge_base/.

Your tasks are:
1.  **Analyze the Trading Narrative:** Deeply analyze 'trading_narratives/trading_story.md' to understand the proposed workflow for narrative-driven trading.
2.  **Apply the Four Directions:** Use the 'four_directions/' framework to structure your approach to generating new trading stories. How can the principles of East (Thinking), South (Planning), West (Action), and North (Reflection) be applied to a trading session or the analysis of a market opportunity?
3.  **Generate a New Trading Story:** Use 'interactive_storytelling.sh' or the 'storytelling' CLI to create a new story. This story should be a practical example of applying the Four Directions to a specific trading scenario (e.g., identifying a setup, managing a trade, and reflecting on the outcome).
4.  **Explore Financial Resource Creation:** Propose concrete ways the generated story can be used to create financial resources. This could involve:
    *   Translating the story into a formal trading plan.
    *   Identifying parameters for an automated trading strategy.
    *   Creating educational content for other traders.

Begin by outlining your plan to tackle these tasks.
" \
	--session-id $session_id \
	--add-dir $ADD_DIRS_PATHS \
	--mcp-config $MCP_CONFIGS_FILES
