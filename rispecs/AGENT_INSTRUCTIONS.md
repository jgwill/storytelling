# Agent Build Instructions for WillWrite

**Status**: ✅ IMPLEMENTED

**Objective:** Your primary goal is to build a fully functional Python application that implements the `WillWrite` specification. You must use **only the documents within this `rispecs/` directory** as your source of truth. Do not reference the original source code that was used to generate these specs.

> Creative Orientation Operating Rules: Before writing or updating any spec or agent output, follow `rispecs/Creative_Orientation_Operating_Guide.md`. Include a Structural Tension block, keep Observations neutral (including Risks & Issues), place advancement classification in a separate Structural Assessment, and add Advancing Moves when useful. Use create-language; avoid problem-elimination phrasing.

## Step 1: Understand the Vision and the Blueprint

Before writing any code, you must first understand the entire specification suite. Read the following documents in order to grasp the project's intent and structure:

1.  **`RISE_Spec.md`**: This is the most important document. It explains the *creative purpose* of the application. Understand the **Core Creative Intent** and the **Creative Advancement Scenarios** before proceeding. This is your guide to the "why."
2.  **`ApplicationLogic.md`**: This provides a high-level, sequential overview of the application's workflow.
3.  **`ProceduralLogic.md`**: This document contains the detailed, step-by-step "pseudo-code" for the application's main control flow and sub-procedures. This is your primary guide to the "how."

## Step 2: Review the Technical Details

Once you understand the workflow, familiarize yourself with the specific technical contracts and requirements:

1.  **`Configuration.md`**: Understand all the command-line arguments that the final application must accept.
2.  **`LLM_Provider_Specification.md`**: Study the URI-based format for configuring LLM providers. Your application must parse these strings correctly.
3.  **`DataSchemas.md`**: Review the exact JSON structures that are expected as outputs from various LLM calls.
4.  **`Prompts.md`**: This file contains the exact text of every prompt you will need. Do not invent your own.
5.  **`Logging_And_Traceability_Specification.md`**: Understand the requirements for creating session-based log directories and saving detailed traceability files for every LLM call.

## Step 3: Follow the Implementation Plan

Use the **`ImplementationNotes.md`** as your guide for technology and architecture choices. The following is a recommended build order:

1.  **Project Setup:**
    *   Create a Python project with a `storytelling/` structure.
    *   Create a `requirements.txt` file and add the libraries mentioned in `ImplementationNotes.md` (Pydantic, LangChain, LangGraph, etc.).

2.  **Core Components:**
    *   Implement the configuration loader (`config.py`) using Pydantic and argparse, as specified.
    *   Implement the data models (`data_models.py`) using Pydantic, as specified in `DataSchemas.md`.
    *   Create a `prompts.py` module to store all prompts from `Prompts.md` as constants.
    *   Implement the LLM Provider parser utility (`llm_providers.py`) that can read the URI format and initialize the correct LangChain LLM clients.

3.  **Workflow Orchestration (LangGraph):**
    *   Define the `StoryState` TypedDict that will be used to manage the graph's state.
    *   Create a separate function for each node in the graph as described in `RISE_Spec.md` and `ProceduralLogic.md`. Each function will handle a specific step of the process (e.g., `generate_outline`, `generate_chapter`).
    *   Use the LangChain Expression Language (LCEL) within each node to chain together prompts, models, and output parsers.
    *   Assemble the state machine (the graph) using LangGraph, connecting the nodes with conditional edges based on the application state and configuration.

4.  **Main Application (`main.py`):**
    *   Create the main entry point for the application.
    *   This script should:
        *   Load the configuration.
        *   Initialize the LangGraph application.
        *   Read the initial user prompt from the file.
        *   Invoke the graph with the initial state.
        *   Handle the final output, saving the story and metadata files as specified.

## Final Validation

The final application must be executable from the command line and accept all the arguments defined in `Configuration.md`. A successful run should produce the log structure and output files described in the specifications.
