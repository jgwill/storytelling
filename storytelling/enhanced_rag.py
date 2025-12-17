#!/usr/bin/env python3
"""
Enhanced RAG system with multi-source content integration.
Combines web content, CoAiAPy datasets/prompts, and local files.
"""

import json
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

from .coaia_fuse import CoAiaFuseIntegrator
from .rag import initialize_knowledge_base
from .web_fetcher import WebContentFetcher, fetch_urls_from_scratchpad


class EnhancedRAGSystem:
    """Enhanced RAG system with multiple content sources."""

    def __init__(self, base_knowledge_dir: str = "enhanced_knowledge_base"):
        """Initialize the enhanced RAG system.

        Args:
            base_knowledge_dir: Base directory for all knowledge content
        """
        self.base_dir = Path(base_knowledge_dir)
        self.web_dir = self.base_dir / "web_content"
        self.coaia_dir = self.base_dir / "coaia_content"
        self.local_dir = self.base_dir / "local_content"

        # Create directories
        for dir_path in [self.base_dir, self.web_dir, self.coaia_dir, self.local_dir]:
            dir_path.mkdir(exist_ok=True)

        # Initialize components
        self.web_fetcher = WebContentFetcher(cache_dir=str(self.base_dir / "web_cache"))
        self.coaia_integrator = CoAiaFuseIntegrator()

        # Track sources
        self.sources_manifest = {
            "web_urls": [],
            "coaia_datasets": [],
            "coaia_prompts": [],
            "local_files": [],
            "created_at": None,
            "last_updated": None,
        }

    def add_web_sources(
        self, urls: Optional[List[str]] = None, scratchpad_file: Optional[str] = None
    ) -> int:
        """Add web content sources to the knowledge base.

        Args:
            urls: List of URLs to fetch (optional)
            scratchpad_file: Path to scratchpad file to extract URLs from (optional)

        Returns:
            Number of successfully processed URLs
        """
        print("🌐 Adding web sources to enhanced RAG...")

        # Get URLs from scratchpad if provided
        if scratchpad_file and not urls:
            urls = fetch_urls_from_scratchpad(scratchpad_file)

        if not urls:
            print("⚠️  No URLs provided")
            return 0

        # Fetch content
        results = self.web_fetcher.fetch_multiple_urls(urls, delay=1.5)

        # Process for RAG
        rag_files = self.web_fetcher.process_for_rag(results, str(self.web_dir))

        # Update manifest
        successful_urls = [r["url"] for r in results if r["status"] == "success"]
        self.sources_manifest["web_urls"].extend(successful_urls)

        print(f"✅ Added {len(rag_files)} web content files to RAG")
        return len(rag_files)

    def add_coaia_sources(
        self,
        dataset_names: Optional[List[str]] = None,
        prompt_names: Optional[List[str]] = None,
    ) -> int:
        """Add CoAiAPy dataset and prompt sources to the knowledge base.

        Args:
            dataset_names: List of dataset names to retrieve (optional)
            prompt_names: List of prompt names to retrieve (optional)

        Returns:
            Number of successfully processed items
        """
        print("🔗 Adding CoAiAPy sources to enhanced RAG...")

        created_files = 0

        # Process datasets
        if dataset_names:
            for dataset_name in dataset_names:
                dataset_data = self.coaia_integrator.get_dataset(dataset_name)
                if dataset_data["status"] == "success":
                    rag_files = self.coaia_integrator.process_dataset_for_rag(
                        dataset_data, str(self.coaia_dir)
                    )
                    created_files += len(rag_files)
                    self.sources_manifest["coaia_datasets"].append(dataset_name)
                else:
                    print(f"❌ Failed to retrieve dataset: {dataset_name}")

        # Process prompts
        if prompt_names:
            for prompt_name in prompt_names:
                prompt_data = self.coaia_integrator.get_prompt(
                    prompt_name, content_only=True
                )
                if prompt_data["status"] == "success":
                    rag_files = self.coaia_integrator.process_prompt_for_rag(
                        prompt_data, str(self.coaia_dir)
                    )
                    created_files += len(rag_files)
                    self.sources_manifest["coaia_prompts"].append(prompt_name)
                else:
                    print(f"❌ Failed to retrieve prompt: {prompt_name}")

        print(f"✅ Added {created_files} CoAiAPy content files to RAG")
        return created_files

    def add_local_sources(self, source_dirs: List[str]) -> int:
        """Add local file sources to the knowledge base.

        Args:
            source_dirs: List of local directories to copy content from

        Returns:
            Number of successfully copied files
        """
        print("📁 Adding local sources to enhanced RAG...")

        copied_files = 0

        for source_dir in source_dirs:
            source_path = Path(source_dir)

            if not source_path.exists():
                print(f"⚠️  Source directory not found: {source_dir}")
                continue

            # Copy markdown files
            for md_file in source_path.glob("**/*.md"):
                try:
                    # Create relative path structure
                    rel_path = md_file.relative_to(source_path)
                    dest_path = self.local_dir / rel_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)

                    shutil.copy2(md_file, dest_path)
                    copied_files += 1
                    self.sources_manifest["local_files"].append(str(md_file))

                except Exception as e:
                    print(f"❌ Failed to copy {md_file}: {e}")

        print(f"✅ Added {copied_files} local content files to RAG")
        return copied_files

    def build_unified_knowledge_base(
        self,
        embedding_model: str = "mxbai-embed-large:latest",
        ollama_base_url: str = "http://localhost:11434",
    ):
        """Build unified knowledge base from all sources.

        Args:
            embedding_model: Embedding model to use
            ollama_base_url: Ollama base URL

        Returns:
            Initialized retriever or None if failed
        """
        print("🧠 Building unified knowledge base from all sources...")

        # Update manifest timestamps
        import time

        timestamp = time.time()
        if not self.sources_manifest["created_at"]:
            self.sources_manifest["created_at"] = timestamp
        self.sources_manifest["last_updated"] = timestamp

        # Save manifest
        manifest_file = self.base_dir / "sources_manifest.json"
        try:
            with open(manifest_file, "w", encoding="utf-8") as f:
                json.dump(self.sources_manifest, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Failed to save manifest: {e}")

        # Initialize knowledge base with unified directory
        try:
            retriever = initialize_knowledge_base(
                str(self.base_dir), embedding_model, ollama_base_url
            )

            if retriever:
                print("✅ Unified knowledge base built successfully")
                return retriever
            else:
                print("❌ Failed to build knowledge base")
                return None

        except Exception as e:
            print(f"❌ Error building knowledge base: {e}")
            return None

    def get_source_summary(self) -> Dict[str, Any]:
        """Get summary of all knowledge base sources.

        Returns:
            Dictionary with source statistics
        """
        # Count files in each directory
        web_count = len(list(self.web_dir.glob("*.md")))
        coaia_count = len(list(self.coaia_dir.glob("*.md")))
        local_count = len(list(self.local_dir.glob("**/*.md")))

        total_files = web_count + coaia_count + local_count

        return {
            "total_files": total_files,
            "web_files": web_count,
            "coaia_files": coaia_count,
            "local_files": local_count,
            "web_urls": len(self.sources_manifest["web_urls"]),
            "coaia_datasets": len(self.sources_manifest["coaia_datasets"]),
            "coaia_prompts": len(self.sources_manifest["coaia_prompts"]),
            "local_sources": len(self.sources_manifest["local_files"]),
            "base_directory": str(self.base_dir),
        }


def create_enhanced_knowledge_base(
    scratchpad_file: str = "STORY_250907_RAG_and_More.md",
    existing_knowledge_dirs: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Create enhanced knowledge base with all sources from scratchpad.

    Args:
        scratchpad_file: Path to scratchpad file with URLs
        existing_knowledge_dirs: List of existing knowledge directories to include

    Returns:
        Dictionary with retriever and source summary
    """
    print("🚀 Creating Enhanced Multi-Source Knowledge Base")
    print("=" * 55)

    # Initialize enhanced RAG system
    rag_system = EnhancedRAGSystem("enhanced_knowledge_base")

    # Add web sources from scratchpad
    rag_system.add_web_sources(scratchpad_file=scratchpad_file)

    # Add CoAiAPy sources from scratchpad
    rag_system.add_coaia_sources(
        dataset_names=["Story250907DS"],
        prompt_names=["Story250907KeyCitationsDiscussionPrompt"],
    )

    # Add existing local knowledge bases if provided
    if existing_knowledge_dirs:
        rag_system.add_local_sources(existing_knowledge_dirs)

    # Build unified knowledge base
    retriever = rag_system.build_unified_knowledge_base()

    # Get summary
    summary = rag_system.get_source_summary()

    print("\n📊 Enhanced Knowledge Base Summary:")
    print(f"  Total files: {summary['total_files']}")
    print(
        f"  Web content: {summary['web_files']} files from {summary['web_urls']} URLs"
    )
    print(
        f"  CoAiAPy content: {summary['coaia_files']} files ({summary['coaia_datasets']} datasets, {summary['coaia_prompts']} prompts)"
    )
    print(
        f"  Local content: {summary['local_files']} files from {summary['local_sources']} sources"
    )
    print(f"  Base directory: {summary['base_directory']}")

    return {"retriever": retriever, "summary": summary, "rag_system": rag_system}


if __name__ == "__main__":
    # Test the enhanced RAG system
    result = create_enhanced_knowledge_base(
        existing_knowledge_dirs=["test_knowledge_base", "test_knowledge_base_mia"]
    )

    if result["retriever"]:
        print("\n✅ Enhanced RAG system ready for story generation!")
    else:
        print("\n❌ Failed to create enhanced RAG system")

    print("\n🎯 Test completed")
