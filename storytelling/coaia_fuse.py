#!/usr/bin/env python3
"""
CoAiAPy Fuse integration for dataset and prompt retrieval.
Integrates with Langfuse for structured data access.
"""

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List


class CoAiaFuseIntegrator:
    """Integrates with CoAiAPy fuse commands for dataset and prompt retrieval."""

    def __init__(self) -> None:
        """Initialize the CoAiAPy Fuse integrator."""
        self.fuse_command = "coaia fuse"

    def check_availability(self) -> bool:
        """Check if CoAiAPy fuse is available in the system."""
        try:
            result = subprocess.run(
                f"{self.fuse_command} --help",
                shell=True,
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.returncode == 0
        except Exception:
            return False

    def get_dataset(
        self, dataset_name: str, output_format: str = "default"
    ) -> Dict[str, Any]:
        """Retrieve a dataset from Langfuse.

        Args:
            dataset_name: Name of the dataset to retrieve
            output_format: Format for output ("default", "openai", "gemini")

        Returns:
            Dictionary containing dataset content and metadata
        """
        print(f"📊 Retrieving dataset: {dataset_name}")

        try:
            # Build command based on format
            format_flag = ""
            if output_format == "openai":
                format_flag = " -oft"
            elif output_format == "gemini":
                format_flag = " -gft"

            command = f"{self.fuse_command} datasets get {dataset_name}{format_flag}"

            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=30
            )

            if result.returncode != 0:
                return {
                    "status": "error",
                    "error": result.stderr,
                    "dataset_name": dataset_name,
                    "content": "",
                }

            # Parse the content based on format
            content = result.stdout.strip()

            # Try to parse as JSON if it looks like JSON
            data_content = content
            if content.startswith("{") or content.startswith("["):
                try:
                    data_content = json.loads(content)
                except json.JSONDecodeError:
                    pass  # Keep as string

            return {
                "status": "success",
                "dataset_name": dataset_name,
                "format": output_format,
                "content": data_content,
                "raw_output": content,
                "content_length": len(content),
            }

        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "error": "Command timeout",
                "dataset_name": dataset_name,
                "content": "",
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "dataset_name": dataset_name,
                "content": "",
            }

    def get_prompt(
        self, prompt_name: str, content_only: bool = False, production: bool = False
    ) -> Dict[str, Any]:
        """Retrieve a prompt from Langfuse.

        Args:
            prompt_name: Name of the prompt to retrieve
            content_only: Return only content (-c flag)
            production: Use production version (--prod flag)

        Returns:
            Dictionary containing prompt content and metadata
        """
        print(f"📝 Retrieving prompt: {prompt_name}")

        try:
            # Build command with flags
            flags = ""
            if content_only:
                flags += " -c"
            if production:
                flags += " --prod"

            command = f"{self.fuse_command} prompts get {prompt_name}{flags}"

            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=30
            )

            if result.returncode != 0:
                return {
                    "status": "error",
                    "error": result.stderr,
                    "prompt_name": prompt_name,
                    "content": "",
                }

            content = result.stdout.strip()

            return {
                "status": "success",
                "prompt_name": prompt_name,
                "content": content,
                "content_only": content_only,
                "production": production,
                "content_length": len(content),
            }

        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "error": "Command timeout",
                "prompt_name": prompt_name,
                "content": "",
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "prompt_name": prompt_name,
                "content": "",
            }

    def list_datasets(self) -> Dict[str, Any]:
        """List all available datasets."""
        print("📋 Listing available datasets...")

        try:
            command = f"{self.fuse_command} datasets list"

            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=15
            )

            if result.returncode != 0:
                return {"status": "error", "error": result.stderr, "datasets": []}

            return {
                "status": "success",
                "raw_output": result.stdout.strip(),
                "datasets": (
                    result.stdout.strip().split("\n") if result.stdout.strip() else []
                ),
            }

        except Exception as e:
            return {"status": "error", "error": str(e), "datasets": []}

    def list_prompts(self) -> Dict[str, Any]:
        """List all available prompts."""
        print("📋 Listing available prompts...")

        try:
            command = f"{self.fuse_command} prompts list"

            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=15
            )

            if result.returncode != 0:
                return {"status": "error", "error": result.stderr, "prompts": []}

            return {
                "status": "success",
                "raw_output": result.stdout.strip(),
                "prompts": (
                    result.stdout.strip().split("\n") if result.stdout.strip() else []
                ),
            }

        except Exception as e:
            return {"status": "error", "error": str(e), "prompts": []}

    def process_dataset_for_rag(
        self, dataset_data: Dict[str, Any], output_dir: str
    ) -> List[str]:
        """Process dataset content and save as markdown files for RAG.

        Args:
            dataset_data: Dataset data from get_dataset()
            output_dir: Directory to save processed files

        Returns:
            List of created file paths
        """
        if dataset_data["status"] != "success":
            print(
                f"❌ Cannot process failed dataset: {dataset_data.get('error', 'Unknown error')}"
            )
            return []

        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        dataset_name = dataset_data["dataset_name"]
        content = dataset_data["content"]

        # Create markdown file with dataset content
        filename = f"dataset_{dataset_name}.md"
        file_path = output_path / filename

        # Format content for RAG
        if isinstance(content, dict) or isinstance(content, list):
            # JSON content - format nicely
            formatted_content = json.dumps(content, indent=2, ensure_ascii=False)
            markdown_content = f"""# Dataset: {dataset_name}

**Source:** CoAiAPy Fuse Dataset
**Format:** {dataset_data.get('format', 'default')}
**Length:** {dataset_data['content_length']} characters

## Content

```json
{formatted_content}
```
"""
        else:
            # Text content
            markdown_content = f"""# Dataset: {dataset_name}

**Source:** CoAiAPy Fuse Dataset
**Format:** {dataset_data.get('format', 'default')}
**Length:** {dataset_data['content_length']} characters

## Content

{content}
"""

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)

            print(f"✅ Created dataset file: {filename}")
            return [str(file_path)]

        except Exception as e:
            print(f"❌ Failed to create dataset file: {e}")
            return []

    def process_prompt_for_rag(
        self, prompt_data: Dict[str, Any], output_dir: str
    ) -> List[str]:
        """Process prompt content and save as markdown files for RAG.

        Args:
            prompt_data: Prompt data from get_prompt()
            output_dir: Directory to save processed files

        Returns:
            List of created file paths
        """
        if prompt_data["status"] != "success":
            print(
                f"❌ Cannot process failed prompt: {prompt_data.get('error', 'Unknown error')}"
            )
            return []

        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        prompt_name = prompt_data["prompt_name"]
        content = prompt_data["content"]

        # Create markdown file with prompt content
        filename = f"prompt_{prompt_name}.md"
        file_path = output_path / filename

        markdown_content = f"""# Prompt: {prompt_name}

**Source:** CoAiAPy Fuse Prompt
**Content Only:** {prompt_data.get('content_only', False)}
**Production:** {prompt_data.get('production', False)}
**Length:** {prompt_data['content_length']} characters

## Content

{content}
"""

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)

            print(f"✅ Created prompt file: {filename}")
            return [str(file_path)]

        except Exception as e:
            print(f"❌ Failed to create prompt file: {e}")
            return []


if __name__ == "__main__":
    # Test the integrator
    integrator = CoAiaFuseIntegrator()

    print("🧪 Testing CoAiAPy Fuse Integration")
    print("=" * 40)

    # Check availability
    if not integrator.check_availability():
        print("❌ CoAiAPy fuse not available")
        exit(1)

    print("✅ CoAiAPy fuse is available")

    # Test listing
    datasets = integrator.list_datasets()
    if datasets["status"] == "success":
        print(f"📊 Found {len(datasets['datasets'])} datasets")

    prompts = integrator.list_prompts()
    if prompts["status"] == "success":
        print(f"📝 Found {len(prompts['prompts'])} prompts")

    print("🎯 Test completed")
