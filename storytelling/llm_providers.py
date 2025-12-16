from urllib.parse import parse_qs, urlparse

from langchain_core.language_models.chat_models import BaseChatModel

# Core providers (always available)
from langchain_ollama import ChatOllama

from .openrouter_patch import PatchedOpenRouterLLM

# Optional providers with graceful degradation
try:
    from langchain_google_genai import ChatGoogleGenerativeAI

    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False
    ChatGoogleGenerativeAI = None


def get_llm_from_uri(uri: str) -> BaseChatModel:
    """
    Parses a provider URI string and returns a configured LangChain chat model instance.
    Also handles direct model names for Google Gemini models.

    Args:
        uri: The provider URI string (e.g., "ollama://llama3.1@localhost:11434?temperature=0.7")
             or direct model name (e.g., "gemini-2.5-flash").

    Returns:
        An instance of a LangChain chat model.
    """
    # Remove direct model name handling - always use URI schemes

    # Handle URI-based models
    parsed_uri = urlparse(uri)
    scheme = parsed_uri.scheme

    # For Google URIs like google://gemini-2.5-flash, the model name is in hostname
    if scheme == "google":
        model_identifier = parsed_uri.hostname or parsed_uri.path.strip("/")
    else:
        model_identifier = parsed_uri.username or parsed_uri.path.strip("/")

    host = parsed_uri.hostname
    port = parsed_uri.port
    params = {k: v[0] for k, v in parse_qs(parsed_uri.query).items()}

    if scheme == "ollama":
        base_url = (
            f"http://{host}:{port}" if host and port else "http://localhost:11434"
        )
        if "temperature" in params:
            params["temperature"] = float(params["temperature"])
        if "num_ctx" in params:
            params["num_ctx"] = int(params["num_ctx"])

        return ChatOllama(
            model=model_identifier,
            base_url=base_url,
            timeout=60,  # Reduced from 300 to 60 seconds
            verbose=True,
            **params,
        )

    elif scheme == "google":
        if not GOOGLE_AVAILABLE:
            raise ImportError(
                "Google Generative AI not available. "
                "Install with: pip install storytelling[google]"
            )

        # Handle temperature parameter separately for Google
        google_params = {}
        if "temperature" in params:
            google_params["temperature"] = float(params["temperature"])

        return ChatGoogleGenerativeAI(model=model_identifier, **google_params)

    elif scheme == "openrouter":
        if "temperature" in params:
            params["temperature"] = float(params["temperature"])

        return PatchedOpenRouterLLM(model_name=model_identifier, **params)

    elif scheme == "myflowise":
        raise NotImplementedError(
            "The 'myflowise' provider scheme is not yet implemented."
        )

    else:
        raise ValueError(f"Unsupported LLM provider scheme: {scheme}")


if __name__ == "__main__":
    # Example usage
    try:
        ollama_uri = "ollama://llama3.1:8b-instruct-q8_0@localhost:11434?temperature=0.7&num_ctx=8192"
        ollama_llm = get_llm_from_uri(ollama_uri)
        print(f"Successfully loaded Ollama model: {ollama_llm.model}")
    except Exception as e:
        print(f"An error occurred: {e}")
