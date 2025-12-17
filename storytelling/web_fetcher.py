#!/usr/bin/env python3
"""
Web content fetching module for RAG knowledge base enhancement.
Handles URL content retrieval and processing for story generation.
"""

import hashlib
import json
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import requests


class WebContentFetcher:
    """Fetches and processes web content for RAG integration."""

    def __init__(self, cache_dir: Optional[str] = None):
        """Initialize the web content fetcher.

        Args:
            cache_dir: Directory for caching fetched content (optional)
        """
        self.cache_dir = Path(cache_dir) if cache_dir else None
        if self.cache_dir:
            self.cache_dir.mkdir(exist_ok=True)

        # Simple headers to avoid bot detection
        self.headers = {
            "User-Agent": "Mozilla/5.0 (compatible; StoryGenerator/1.0)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }

    def fetch_url(self, url: str, timeout: int = 10) -> Dict[str, Any]:
        """Fetch content from a single URL.

        Args:
            url: URL to fetch
            timeout: Request timeout in seconds

        Returns:
            Dictionary containing url, content, title, and metadata
        """
        # Check cache first
        if self.cache_dir:
            cache_key = hashlib.md5(url.encode()).hexdigest()
            cache_file = self.cache_dir / f"{cache_key}.json"

            if cache_file.exists():
                try:
                    with open(cache_file, encoding="utf-8") as f:
                        cached_data = json.load(f)
                    print(f"📋 Using cached content for {url}")
                    return cached_data
                except Exception as e:
                    print(f"⚠️  Cache read error for {url}: {e}")

        print(f"🌐 Fetching: {url}")

        try:
            response = requests.get(url, headers=self.headers, timeout=timeout)
            response.raise_for_status()

            # Extract basic content - simple text extraction
            content = response.text

            # Basic title extraction
            title_match = re.search(
                r"<title[^>]*>([^<]+)</title>", content, re.IGNORECASE
            )
            title = title_match.group(1).strip() if title_match else "Untitled"

            # Simple text cleanup - remove HTML tags and extract readable content
            # This is basic - for production, use proper HTML parsing
            text_content = re.sub(r"<[^>]+>", "", content)
            text_content = re.sub(r"\s+", " ", text_content).strip()

            # Limit content size (avoid huge pages)
            if len(text_content) > 10000:
                text_content = text_content[:10000] + "... [truncated]"

            result = {
                "url": url,
                "title": title,
                "content": text_content,
                "status": "success",
                "timestamp": time.time(),
                "content_length": len(text_content),
            }

            # Cache the result
            if self.cache_dir:
                try:
                    with open(cache_file, "w", encoding="utf-8") as f:
                        json.dump(result, f, indent=2, ensure_ascii=False)
                except Exception as e:
                    print(f"⚠️  Cache write error for {url}: {e}")

            print(f"✅ Fetched {len(text_content)} characters from {url}")
            return result

        except requests.exceptions.RequestException as e:
            error_result = {
                "url": url,
                "title": "Error",
                "content": "",
                "status": "error",
                "error": str(e),
                "timestamp": time.time(),
                "content_length": 0,
            }
            print(f"❌ Failed to fetch {url}: {e}")
            return error_result

    def fetch_multiple_urls(
        self, urls: List[str], delay: float = 1.0
    ) -> List[Dict[str, Any]]:
        """Fetch content from multiple URLs with rate limiting.

        Args:
            urls: List of URLs to fetch
            delay: Delay between requests in seconds

        Returns:
            List of content dictionaries
        """
        results = []

        print(f"🚀 Fetching {len(urls)} URLs...")

        for i, url in enumerate(urls):
            if i > 0:  # Don't delay before first request
                time.sleep(delay)

            result = self.fetch_url(url)
            results.append(result)

            # Progress indicator
            if len(urls) > 1:
                print(f"📊 Progress: {i + 1}/{len(urls)} URLs fetched")

        successful = len([r for r in results if r["status"] == "success"])
        print(f"🎯 Completed: {successful}/{len(urls)} URLs successfully fetched")

        return results

    def process_for_rag(
        self, fetched_content: List[Dict[str, Any]], output_dir: str
    ) -> List[str]:
        """Process fetched content and save as markdown files for RAG ingestion.

        Args:
            fetched_content: List of fetched content dictionaries
            output_dir: Directory to save processed markdown files

        Returns:
            List of created file paths
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        created_files = []

        print("📝 Processing content for RAG ingestion...")

        for i, content_data in enumerate(fetched_content):
            if content_data["status"] != "success":
                print(f"⚠️  Skipping failed URL: {content_data['url']}")
                continue

            # Create safe filename from URL
            parsed_url = urlparse(content_data["url"])
            safe_name = re.sub(
                r"[^\w\-_.]", "_", f"{parsed_url.netloc}_{parsed_url.path}"
            )
            safe_name = safe_name.strip("_")[:50]  # Limit filename length

            filename = f"web_content_{i:03d}_{safe_name}.md"
            file_path = output_path / filename

            # Create markdown content with metadata
            markdown_content = f"""# {content_data['title']}

**Source:** {content_data['url']}
**Fetched:** {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(content_data['timestamp']))}
**Length:** {content_data['content_length']} characters

---

{content_data['content']}
"""

            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(markdown_content)

                created_files.append(str(file_path))
                print(f"✅ Created: {filename}")

            except Exception as e:
                print(f"❌ Failed to create {filename}: {e}")

        print(f"🎯 Processed {len(created_files)} files for RAG")
        return created_files


def fetch_urls_from_scratchpad(scratchpad_file: str) -> List[str]:
    """Extract URLs from scratchpad markdown file.

    Args:
        scratchpad_file: Path to scratchpad file

    Returns:
        List of extracted URLs
    """
    try:
        with open(scratchpad_file, encoding="utf-8") as f:
            content = f.read()

        # Extract URLs - look for http/https URLs
        urls = re.findall(r'https?://[^\s<>"\'\[\]()]+', content)

        # Clean up URLs (remove trailing punctuation)
        cleaned_urls = []
        for url in urls:
            url = re.sub(r"[,.)]+$", "", url)  # Remove trailing punctuation
            cleaned_urls.append(url)

        # Remove duplicates while preserving order
        unique_urls = list(dict.fromkeys(cleaned_urls))

        print(f"📋 Found {len(unique_urls)} unique URLs in scratchpad")
        return unique_urls

    except Exception as e:
        print(f"❌ Error reading scratchpad: {e}")
        return []


if __name__ == "__main__":
    # Test the web fetcher
    fetcher = WebContentFetcher(cache_dir="web_cache")

    # Test with a simple URL
    test_urls = ["https://httpbin.org/html"]  # Simple test endpoint

    results = fetcher.fetch_multiple_urls(test_urls)
    processed_files = fetcher.process_for_rag(results, "test_web_rag")

    print(f"✅ Test completed. Created {len(processed_files)} files.")
