# WillWrite LLM Provider Specification

This document defines the URI-based format used to configure and select LLM providers and models within the `WillWrite` application. This system allows for flexible, dynamic selection of models from various sources through a single configuration string.

## 1. URI Format

The provider string is a URI with the following structure:

`provider_scheme://model_identifier@host?parameter1=value1&parameter2=value2`

### Components:

-   **`provider_scheme` (Required):** Identifies the LLM provider. Supported schemes are `ollama`, `google`, `openrouter`, and `myflowise`.
-   **`model_identifier` (Required):** The specific model to be used (e.g., `llama3.1`, `gemini-1.5-flash`, `google/gemini-pro`). The format depends on the provider.
-   **`host` (Optional):** The hostname and port for the provider's API endpoint (e.g., `localhost:11434`). Defaults are used if omitted.
-   **`parameters` (Optional):** A query string of key-value pairs that map to the model's generation parameters (e.g., `temperature`, `top_k`).

## 2. Provider-Specific Implementations

### 2.1. `ollama`

-   **Scheme:** `ollama://`
-   **Mapping:**
    -   `model_identifier`: Maps to the `model` parameter in the Ollama client.
    -   `host`: Maps to the `host` parameter. Defaults to `localhost:11434`.
    -   `parameters`: Maps directly to the `options` dictionary in the Ollama client (e.g., `temperature`, `num_ctx`).
-   **Example:** `ollama://llama3.1:8b-instruct-q8_0@localhost:11434?temperature=0.7&num_ctx=8192`

### 2.2. `google`

-   **Scheme:** `google://`
-   **Mapping:**
    -   `model_identifier`: Maps to the `model_name` parameter for Google's `GenerativeModel`. The model name is extracted from the hostname component of the URI.
    -   `host`: Not used (hostname contains model identifier).
    -   `parameters`: Maps to the `generation_config` dictionary.
-   **URI Parsing**: For Google models, the hostname component contains the model name (e.g., `google://gemini-2.5-flash` where `gemini-2.5-flash` is the hostname).
-   **Examples:** 
    - `google://gemini-1.5-pro-latest?temperature=0.8`
    - `google://gemini-2.5-flash?temperature=0.7` ✅ **NEW - Cost-Optimized Model**
    - `google://gemini-1.5-flash?max_output_tokens=8192`

### 2.2.1 Google Model Variants ✅ **NEW**

**Gemini 2.5 Flash** - Cost-effective model for extensive story generation:
- **Model ID**: `gemini-2.5-flash`
- **URI Format**: `google://gemini-2.5-flash`
- **Use Case**: Cost-optimized narrative generation with maintained quality
- **Benefits**: Enables extensive experimentation without budget constraints

**Gemini 1.5 Pro** - High-quality model for complex narrative tasks:
- **Model ID**: `gemini-1.5-pro-latest`  
- **URI Format**: `google://gemini-1.5-pro-latest`
- **Use Case**: Complex reasoning and high-quality content generation

### 2.3. `openrouter`

-   **Scheme:** `openrouter://`
-   **Mapping:**
    -   The full path including the `model_identifier` (e.g., `google/gemini-pro`) is used as the model name.
    -   `host`: Not used.
    -   `parameters`: Maps to the generation parameters of the OpenRouter client.
-   **Example:** `openrouter://google/gemini-pro-1.5-flash?temperature=0.9`

### 2.4. `myflowise`

-   **Scheme:** `myflowise://`
-   **Mapping:**
    -   `model_identifier`: This is the Flowise **Flow ID** (a UUID).
    -   `host`: The hostname and port of the Flowise instance (e.g., `localhost:3222`).
    -   `parameters`: Not typically used, as parameters are usually configured within the Flowise UI itself.
-   **Example:** `myflowise://f60dbba4-b5cb-48ba-b8ee-f434ff8ff7c3@localhost:3222`

## 3. Procedural Logic

The application must include a "Provider String Parser" utility that is called during initialization for each model configuration parameter. This parser will:
1.  Take the provider URI string as input.
2.  Deconstruct it into its components (scheme, model, host, parameters).
3.  Based on the scheme, instantiate the correct LLM client (e.g., `ChatOllama`).
4.  Configure the client with the parsed model, host, and parameters.
5.  Return the configured client object, ready for use.
