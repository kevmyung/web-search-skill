#!/usr/bin/env python3
"""
Wikipedia Search Skill - Search and retrieve Wikipedia articles
Provides CLI interface for Wikipedia search and article retrieval
"""

import argparse
import importlib.util
import json
import logging
import os
import subprocess
import sys
from pathlib import Path

# Auto-setup: create venv and install dependencies if needed
_SKILL_DIR = Path(__file__).resolve().parent.parent
_VENV_DIR = _SKILL_DIR / ".venv"
_REQUIRED = {"wikipediaapi": "wikipedia-api"}

if not sys.prefix.startswith(str(_VENV_DIR)):
    _env = {**os.environ, "PIP_DISABLE_PIP_VERSION_CHECK": "1"}
    if not _VENV_DIR.exists():
        subprocess.check_call([sys.executable, "-m", "venv", str(_VENV_DIR)])
    _pip = str(_VENV_DIR / "bin" / "pip")
    _missing = [pkg for mod, pkg in _REQUIRED.items()
                if subprocess.run([str(_VENV_DIR / "bin" / "python3"), "-c", f"import {mod}"],
                                  capture_output=True).returncode != 0]
    if _missing:
        subprocess.check_call([_pip, "install", "-q"] + _missing, env=_env)
    os.execv(str(_VENV_DIR / "bin" / "python3"), [str(_VENV_DIR / "bin" / "python3")] + sys.argv)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def wikipedia_search(query: str, language: str = "en") -> dict:
    """Search Wikipedia for articles matching the query."""
    try:
        import wikipediaapi

        wiki = wikipediaapi.Wikipedia(
            user_agent='WebSearchSkill/1.0',
            language=language
        )

        page = wiki.page(query)

        if not page.exists():
            return {
                "success": True,
                "status": "no_results",
                "query": query,
                "message": f"No Wikipedia articles found for: {query}",
                "results": []
            }

        summary = page.summary
        snippet = summary[:300] + "..." if len(summary) > 300 else summary

        # Also collect linked pages as related results
        related = []
        for title, link_page in list(page.links.items())[:5]:
            if link_page.exists():
                link_summary = link_page.summary
                related.append({
                    "title": link_page.title,
                    "snippet": link_summary[:150] + "..." if len(link_summary) > 150 else link_summary,
                    "url": link_page.fullurl
                })

        result = {
            "success": True,
            "status": "success",
            "query": query,
            "result": {
                "title": page.title,
                "snippet": snippet,
                "url": page.fullurl
            }
        }

        if related:
            result["related"] = related

        logger.info(f"Wikipedia search completed for '{query}'")
        return result

    except Exception as e:
        logger.error(f"Wikipedia search error: {e}")
        return {"success": False, "error": str(e), "query": query}


def wikipedia_get_article(title: str, summary_only: bool = False, max_length: int = 5000, language: str = "en") -> dict:
    """Retrieve content from a Wikipedia article by exact title."""
    try:
        import wikipediaapi

        wiki = wikipediaapi.Wikipedia(
            user_agent='WebSearchSkill/1.0',
            language=language
        )

        page = wiki.page(title)

        if not page.exists():
            return {
                "success": True,
                "status": "not_found",
                "title": title,
                "message": f"Wikipedia article not found: {title}",
                "suggestion": "Try using --query to search for the correct article title"
            }

        if summary_only:
            content = page.summary
            content_type = "summary"
        else:
            content = page.text[:max_length]
            content_type = "full_text"
            if len(page.text) > max_length:
                content += "\n\n[... Content truncated at {} characters]".format(max_length)

        categories = list(page.categories.keys())[:5]

        logger.info(f"Wikipedia article retrieved: '{title}' ({len(content)} chars)")

        return {
            "success": True,
            "status": "success",
            "title": page.title,
            "content_type": content_type,
            "content": content,
            "url": page.fullurl,
            "categories": categories,
            "character_count": len(content)
        }

    except Exception as e:
        logger.error(f"Wikipedia article error: {e}")
        return {"success": False, "error": str(e), "title": title}


def main():
    parser = argparse.ArgumentParser(
        description='Wikipedia Search Skill - Search and retrieve Wikipedia articles',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search Wikipedia
  %(prog)s --query "Quantum computing"

  # Get full article
  %(prog)s --title "Python (programming language)"

  # Get summary only
  %(prog)s --title "Machine learning" --summary-only

  # Search in another language
  %(prog)s --query "인공지능" --language ko
        """
    )

    parser.add_argument('--query', '-q', type=str, help='Search query string')
    parser.add_argument('--title', '-t', type=str, help='Exact article title to retrieve')
    parser.add_argument('--summary-only', '-s', action='store_true', help='Return only summary (with --title)')
    parser.add_argument('--max-length', '-l', type=int, default=5000, help='Max content length (default: 5000)')
    parser.add_argument('--language', type=str, default='en', help='Wikipedia language code (default: en)')

    args = parser.parse_args()

    if not args.query and not args.title:
        parser.error("Must specify either --query or --title")

    if args.query and args.title:
        parser.error("Cannot specify both --query and --title")

    if args.query:
        result = wikipedia_search(args.query, language=args.language)
    else:
        result = wikipedia_get_article(
            args.title,
            summary_only=args.summary_only,
            max_length=args.max_length,
            language=args.language
        )

    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("success") else 1)


if __name__ == '__main__':
    main()
