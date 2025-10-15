# WillWrite Implementation Notes

This document provides recommended technical guidance for implementing the `WillWrite` application based on the specifications. While the core specs are technology-agnostic, these notes suggest libraries and patterns that align well with the application's architecture and intent.

## 1. Configuration Management

It is recommended to use a robust configuration library to manage the numerous parameters.

-   **Technology:** `pydantic` combined with Python's `argparse`.
-   **Pattern:**
    1.  Define a `WillWriteConfig` class using `pydantic.BaseModel` to get type validation, default values, and clear schema definition.
    2.  Use `argparse` to parse command-line arguments.
    3.  Instantiate the `WillWriteConfig` model from the parsed arguments to create a single, validated configuration object.
    4.  This pattern provides a clean separation of concerns and ensures that the application receives a valid configuration.

## 2. Data Schemas

The data schemas defined in `DataSchemas.md` should be enforced in the implementation.

-   **Technology:** `pydantic`.
-   **Pattern:**
    1.  Create a `pydantic.BaseModel` for each schema defined in `DataSchemas.md`.
    2.  When using an LLM framework like LangChain, integrate these Pydantic models with the output parser (`JsonOutputParser(pydantic_object=...)`) to automatically parse and validate the LLM's JSON output.
    3.  This ensures data consistency and catches errors early in the process.

## 3. LLM Interaction and Workflow Orchestration

The core of the application is a stateful, multi-step workflow. It is highly recommended to use a framework designed for this purpose.

-   **Technology:** `LangChain` and `LangGraph`.
-   **Pattern:**
    1.  **LLM Clients:** Implement a parser that conforms to `LLM_Provider_Specification.md`. This parser will read the URI string from the configuration and instantiate the appropriate LangChain client (`ChatOllama`, `ChatGoogleGenerativeAI`, etc.) with the correct parameters.
    2.  **State Management:** Use `LangGraph`'s `StatefulGraph` to manage the application's state (the `StoryState` object). This enables robust and scalable state persistence, including capabilities for checkpointing, session recovery, and even 'time-travel' to explore alternative narrative branches.
    3.  **Nodes and Edges:** Implement each step in the `ProceduralLogic.md` as a node in the LangGraph graph. The conditional logic (e.g., "if `-ExpandOutline` is true") should be implemented as conditional edges.
    4.  **Chains:** Use the LangChain Expression Language (LCEL) to construct chains for each LLM call (e.g., `prompt_template | model | output_parser`). This is a declarative and composable way to define the logic for each node.

## 4. Prompts

-   **Technology:** `LangChain`'s `ChatPromptTemplate`.
-   **Pattern:**
    1.  Store all prompts from `Prompts.md` in a dedicated module (e.g., `prompts.py`).
    2.  Define each prompt as a `ChatPromptTemplate` object. This allows for easy formatting and integration into LangChain chains.

By following these recommendations, an implementing agent can create a robust, maintainable, and scalable version of the `WillWrite` application that faithfully executes the creative intent laid out in the specifications.

## 6. Knowledge Base (RAG) - ✅ IMPLEMENTED

**Implementation Status**: Complete with full test coverage

-   **Technology:** `LangChain`'s document loaders, text splitters, embedding models, and vector stores.
-   **Implementation**: See `src/willwrite/rag.py` for complete implementation
-   **Pattern**:
    1.  **Document Loading:** Implemented using `langchain_community.document_loaders.DirectoryLoader` with recursive markdown file scanning.
    2.  **Vector Store:** FAISS in-memory vector store with configurable embedding models (OpenAI, HuggingFace).
    3.  **Retrieval Integration:** Context injection during scene generation in LangGraph workflow.
    4.  **Multi-Provider Support**: Automatic embedding model selection based on model identifier.
    5.  **Error Handling**: Comprehensive validation and graceful error recovery.

**Key Features**:
- Multi-provider embedding support (OpenAI, HuggingFace, with fallback)
- Recursive directory scanning for markdown knowledge files
- Text chunking with semantic boundary preservation (1000 chars, 200 overlap)
- Real-time context injection during story generation
- Performance optimization with in-memory vector search
- Comprehensive test suite with unit, integration, and performance tests

**Configuration**: 
- `--KnowledgeBasePath`: Directory containing markdown knowledge files
- `--EmbeddingModel`: Embedding model identifier (e.g., `text-embedding-ada-002`, `sentence-transformers/all-MiniLM-L6-v2`)

**See**: `specifications/RAG_Implementation_Specification.md` for complete technical documentation.

## 5. Logging and Traceability

-   **Technology:** Python's built-in `logging` module.
-   **Pattern:**
    1.  Create a custom `Logger` class that handles the setup of the session directory structure as defined in `Logging_And_Traceability_Specification.md`.
    2.  Use file handlers to direct logs to both the console (with color support, e.g., using the `termcolor` library) and the `Main.log` file.
    3.  Implement a dedicated method within the logger (e.g., `save_interaction`) that takes a message history and a descriptive name, and saves the `.json` and `.md` traceability files. This method should be called from a central point after each LLM call.
