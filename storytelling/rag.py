from typing import TYPE_CHECKING

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

if TYPE_CHECKING:
    from langchain_huggingface import HuggingFaceEmbeddings

# Check for unstructured package (required for document loading)
def _check_and_install_unstructured() -> bool:
    """Check if unstructured is installed, attempt to install if missing."""
    try:
        import unstructured  # noqa: F401
        return True
    except ImportError:
        try:
            import subprocess
            import sys
            
            print("Installing required 'unstructured' package...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-U", "unstructured"],
                capture_output=True,
                text=True,
                timeout=300,
            )
            
            if result.returncode == 0:
                print("✓ Successfully installed 'unstructured'")
                return True
            else:
                print(f"✗ Failed to install 'unstructured': {result.stderr}")
                return False
        except Exception as e:
            print(f"✗ Could not auto-install 'unstructured': {e}")
            return False

UNSTRUCTURED_AVAILABLE = _check_and_install_unstructured()

try:
    from langchain_huggingface import HuggingFaceEmbeddings

    HUGGINGFACE_AVAILABLE = True
except ImportError:
    try:
        # Fallback to community version if huggingface package not available
        from langchain_community.embeddings import HuggingFaceEmbeddings

        HUGGINGFACE_AVAILABLE = True
    except ImportError:
        HUGGINGFACE_AVAILABLE = False
        HuggingFaceEmbeddings = None

try:
    from langchain_ollama import OllamaEmbeddings
except ImportError:
    # Ollama embeddings not available
    OllamaEmbeddings = None


def get_embedding_model(
    model_name: str, ollama_base_url: str = "http://localhost:11434"
):
    """
    Get the appropriate embedding model instance based on the model name.

    Args:
        model_name: The name/identifier of the embedding model
        ollama_base_url: Base URL for Ollama API (default: http://localhost:11434)

    Returns:
        An embedding model instance
    """
    model_lower = model_name.lower()

    # Check for Ollama embedding models
    if (
        any(
            ollama_model in model_lower
            for ollama_model in ["mxbai-embed", "nomic-embed", ":latest"]
        )
        and OllamaEmbeddings
    ):
        return OllamaEmbeddings(model=model_name, base_url=ollama_base_url)

    # Check for OpenAI models
    elif (
        "openai" in model_lower
        or "ada" in model_lower
        or "text-embedding" in model_lower
    ):
        return OpenAIEmbeddings(model=model_name)

    # Check for HuggingFace models
    elif "sentence-transformers" in model_name or "all-MiniLM" in model_name:
        if not HUGGINGFACE_AVAILABLE:
            raise ImportError(
                f"HuggingFace embeddings not available for model '{model_name}'. "
                "Install with: pip install storytelling[local-ml]"
            )
        return HuggingFaceEmbeddings(model_name=model_name)

    # Check if it looks like an Ollama model but OllamaEmbeddings is not available
    elif any(
        ollama_indicator in model_lower
        for ollama_indicator in ["mxbai-embed", "nomic-embed", ":latest"]
    ):
        if not OllamaEmbeddings:
            raise ImportError(
                "Ollama embeddings not available. Please install langchain-ollama: pip install langchain-ollama"
            )

    else:
        # Default to Ollama if available, otherwise suggest options
        if OllamaEmbeddings:
            return OllamaEmbeddings(
                model="mxbai-embed-large:latest", base_url=ollama_base_url
            )
        elif HUGGINGFACE_AVAILABLE:
            return HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
        else:
            raise ImportError(
                "No embedding models available. Please install either:\n"
                "- Ollama with embedding models (already included)\n"
                "- Local ML models: pip install storytelling[local-ml]\n"
                "- Or use OpenAI embeddings with model name containing 'openai'"
            )


def initialize_knowledge_base(
    knowledge_base_path: str,
    embedding_model: str,
    ollama_base_url: str = "http://localhost:11434",
    default_top_k: int = 5,
) -> VectorStoreRetriever:
    """
    Initializes the knowledge base from a directory of Markdown files.

    Args:
        knowledge_base_path: The path to the directory containing the knowledge base files.
        embedding_model: The name of the embedding model to use.
        ollama_base_url: Base URL for Ollama API (default: http://localhost:11434)
        default_top_k: Default number of documents to retrieve (default: 5)

    Returns:
        A retriever object for the knowledge base.
    """
    if not UNSTRUCTURED_AVAILABLE:
        raise ImportError(
            "The 'unstructured' package is required for knowledge base functionality. "
            "Install it with: pip install -U unstructured\n"
            "Or install storytelling with RAG support: pip install 'storytelling[rag]'"
        )
    
    if not knowledge_base_path or not embedding_model:
        raise ValueError(
            "Both knowledge_base_path and embedding_model must be provided"
        )

    # Load documents
    try:
        loader = DirectoryLoader(
            knowledge_base_path,
            glob="**/*.md",
            show_progress=True,
            use_multithreading=True,
        )
        documents = loader.load()
    except Exception as e:
        raise ValueError(
            f"Error loading documents from {knowledge_base_path}: {e}"
        ) from e

    if not documents:
        raise ValueError(
            f"No documents found in {knowledge_base_path}. Ensure there are .md files in the directory."
        )

    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(documents)

    # Get embedding model instance
    embedding_instance = get_embedding_model(embedding_model, ollama_base_url)

    # Create vector store with configurable retriever
    vectorstore = FAISS.from_documents(documents=splits, embedding=embedding_instance)
    # Configure retriever with default search parameters (can be overridden at query time)
    return vectorstore.as_retriever(search_kwargs={"k": default_top_k})


def construct_chapter_queries(
    chapter_outline: str,
    chapter_number: int,
    previous_chapter_summary: str = None,
    story_elements=None,
) -> list:
    """
    Construct queries for chapter-specific knowledge retrieval.

    Args:
        chapter_outline: Current chapter's planned content
        chapter_number: Chapter index for context
        previous_chapter_summary: Summary of previous chapter for continuity
        story_elements: Characters, themes, setting from story elements

    Returns:
        List of contextually relevant queries for this chapter
    """
    queries = []

    # Primary query: chapter outline content
    if chapter_outline:
        queries.append(chapter_outline)

    # Character-specific queries from story elements
    if story_elements:
        if isinstance(story_elements, dict):
            if story_elements.get("characters"):
                char_list = story_elements["characters"]
                if isinstance(char_list, list):
                    for char in char_list[:3]:  # Limit to top 3 characters
                        queries.append(f"Character {char} in chapter {chapter_number}")
                else:
                    queries.append(f"Characters: {char_list}")

            # Setting/location queries
            if story_elements.get("setting"):
                queries.append(f"Setting details: {story_elements['setting']}")

            # Theme continuity queries
            if story_elements.get("theme"):
                queries.append(f"Thematic elements: {story_elements['theme']}")
        elif isinstance(story_elements, str) and len(story_elements) > 0:
            # Use story elements text as a query
            queries.append(story_elements[:500])

    # Continuity query from previous chapter
    if previous_chapter_summary:
        queries.append(f"Context following: {previous_chapter_summary[:300]}")

    return queries


def retrieve_chapter_context(
    retriever: VectorStoreRetriever,
    chapter_outline: str,
    chapter_number: int,
    previous_chapter_summary: str = None,
    story_elements=None,
    max_tokens: int = 1500,
    top_k: int = 8,
    similarity_threshold: float = 0.7,
) -> str:
    """
    Retrieve and format knowledge base context for chapter generation.

    Similar to retrieve_outline_context but tailored for chapter-level details.

    Args:
        retriever: Knowledge base retriever
        chapter_outline: Current chapter's outline
        chapter_number: Chapter index
        previous_chapter_summary: Summary of previous chapter
        story_elements: Story context (characters, themes, setting)
        max_tokens: Maximum tokens for the combined context
        top_k: Number of documents to retrieve per query
        similarity_threshold: Minimum similarity score (not currently used)

    Returns:
        Formatted context string with RAG content
    """
    queries = construct_chapter_queries(
        chapter_outline,
        chapter_number,
        previous_chapter_summary,
        story_elements,
    )

    if not queries:
        return ""

    # Retrieve documents for all queries
    all_docs = []
    seen_content = set()

    for query in queries:
        try:
            docs = retriever.invoke(query)
            docs = docs[:top_k]

            for doc in docs:
                content = doc.page_content.strip()
                if content and content not in seen_content:
                    seen_content.add(content)
                    all_docs.append({
                        "content": content,
                        "source": doc.metadata.get("source", "unknown"),
                        "query": query,
                    })
        except Exception as e:
            print(f"Error retrieving documents for query '{query[:50]}...': {e}")
            continue

    if not all_docs:
        return ""

    # Combine and truncate to max_tokens (rough estimate: 4 chars = 1 token)
    max_chars = max_tokens * 4
    formatted_chunks = []
    total_chars = 0

    for doc in all_docs[:12]:  # Limit to top 12 documents
        chunk = f"**Source:** {doc['source']}\n{doc['content']}"
        chunk_chars = len(chunk)

        if total_chars + chunk_chars > max_chars:
            remaining = max_chars - total_chars
            if remaining > 100:
                truncated = chunk[:remaining].rsplit(" ", 1)[0]
                formatted_chunks.append(truncated + "...")
            break

        formatted_chunks.append(chunk)
        total_chars += chunk_chars

    if formatted_chunks:
        context = "\n\n---\n\n".join(formatted_chunks)
        return f"""<RAG-CHAPTER-CONTEXT>
# Knowledge Base Context for Chapter {chapter_number}

{context}
</RAG-CHAPTER-CONTEXT>"""

    return ""


def construct_outline_queries(initial_prompt: str, story_elements=None) -> list:
    """
    Generate optimized queries for outline-stage knowledge retrieval.

    Args:
        initial_prompt: User's story prompt
        story_elements: Parsed story components (characters, setting, themes) as dict or string

    Returns:
        List of targeted queries for knowledge base
    """
    queries = []

    # Primary prompt-based query (most important)
    queries.append(initial_prompt)

    # Entity-specific queries if story elements are available
    if story_elements:
        # Handle story_elements as dict (structured)
        if isinstance(story_elements, dict):
            if story_elements.get("characters"):
                char_list = story_elements["characters"]
                if isinstance(char_list, list):
                    queries.append(f"Characters: {', '.join(char_list)}")
                else:
                    queries.append(f"Characters: {char_list}")

            if story_elements.get("setting"):
                queries.append(f"Setting and world: {story_elements['setting']}")

            if story_elements.get("theme"):
                queries.append(f"Themes and concepts: {story_elements['theme']}")
        
        # Handle story_elements as string (unstructured LLM output)
        elif isinstance(story_elements, str) and len(story_elements) > 0:
            # Use the entire story elements text as a query
            queries.append(story_elements)

    return queries


def retrieve_outline_context(
    retriever: VectorStoreRetriever,
    queries: list,
    max_tokens: int = 1000,
    top_k: int = 5,
    similarity_threshold: float = 0.7,
) -> str:
    """
    Retrieve and format relevant context for outline generation.

    Args:
        retriever: Knowledge base retriever
        queries: List of search queries
        max_tokens: Maximum tokens for the combined context
        top_k: Number of documents to retrieve per query
        similarity_threshold: Minimum similarity score

    Returns:
        Formatted context string
    """
    all_docs = []
    seen_content = set()

    # Retrieve documents for each query
    for query in queries:
        try:
            # Get top-k similar documents using search_kwargs
            # Note: invoke uses the retriever's default search_kwargs if not overridden
            docs = retriever.invoke(query)
            
            # Take only top_k documents from the results
            docs = docs[:top_k]

            # Filter by uniqueness and add
            for doc in docs:
                content = doc.page_content.strip()
                if content and content not in seen_content:
                    seen_content.add(content)
                    all_docs.append(
                        {
                            "content": content,
                            "source": doc.metadata.get("source", "unknown"),
                            "query": query,
                        }
                    )
        except Exception as e:
            print(f"Error retrieving documents for query '{query}': {e}")
            continue

    # Sort by relevance and truncate to token limit
    context_parts = []
    total_tokens = 0

    for doc in all_docs[:10]:  # Limit to top 10 documents
        # Rough token estimation (4 chars per token)
        estimated_tokens = len(doc["content"]) // 4

        if total_tokens + estimated_tokens > max_tokens:
            # Truncate the current document to fit
            remaining_tokens = max_tokens - total_tokens
            remaining_chars = remaining_tokens * 4
            truncated_content = doc["content"][:remaining_chars].rsplit(" ", 1)[
                0
            ]  # Break at word boundary
            context_parts.append(f"**Source:** {doc['source']}\n{truncated_content}")
            break

        context_parts.append(f"**Source:** {doc['source']}\n{doc['content']}")
        total_tokens += estimated_tokens

    if context_parts:
        return "# Knowledge Base Context\n\n" + "\n\n---\n\n".join(context_parts)
    else:
        return ""
