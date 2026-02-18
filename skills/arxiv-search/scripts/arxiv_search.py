#!/usr/bin/env python3
"""
ArXiv Search Skill - Search and retrieve scientific papers from ArXiv
Provides CLI interface for paper search and retrieval
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
_REQUIRED = {"arxiv": "arxiv"}

if not sys.prefix.startswith(str(_VENV_DIR)):
    if not _VENV_DIR.exists():
        subprocess.check_call([sys.executable, "-m", "venv", str(_VENV_DIR)])
    _pip = str(_VENV_DIR / "bin" / "pip")
    _missing = [pkg for mod, pkg in _REQUIRED.items()
                if subprocess.run([str(_VENV_DIR / "bin" / "python3"), "-c", f"import {mod}"],
                                  capture_output=True).returncode != 0]
    if _missing:
        subprocess.check_call([_pip, "install", "-q"] + _missing)
    os.execv(str(_VENV_DIR / "bin" / "python3"), [str(_VENV_DIR / "bin" / "python3")] + sys.argv)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def arxiv_search(query: str, max_results: int = 5) -> dict:
    """Search ArXiv for papers matching the query."""
    try:
        import arxiv

        max_results = min(max_results, 20)

        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )

        results = []
        for idx, paper in enumerate(client.results(search), 1):
            paper_id = paper.entry_id.split('/')[-1]
            results.append({
                "index": idx,
                "title": paper.title,
                "authors": ", ".join([a.name for a in paper.authors]),
                "published": paper.published.strftime("%Y-%m-%d"),
                "paper_id": paper_id,
                "abstract": paper.summary,
                "url": f"https://arxiv.org/abs/{paper_id}",
                "pdf_url": paper.pdf_url,
                "categories": paper.categories
            })

        logger.info(f"ArXiv search completed: {len(results)} results for '{query}'")

        return {
            "success": True,
            "query": query,
            "result_count": len(results),
            "results": results
        }

    except Exception as e:
        logger.error(f"ArXiv search error: {e}")
        return {"success": False, "error": str(e), "query": query}


def arxiv_get_paper(paper_ids: str, max_length: int = 5000) -> dict:
    """Get detailed paper content by ID(s)."""
    try:
        import arxiv

        id_list = [pid.strip().split("/")[-1] for pid in paper_ids.split(",")]

        client = arxiv.Client()
        search = arxiv.Search(id_list=id_list)

        papers = []
        for paper in client.results(search):
            paper_id = paper.entry_id.split('/')[-1]
            content = paper.summary
            if len(content) > max_length:
                content = content[:max_length] + "\n\n[... Content truncated]"

            papers.append({
                "paper_id": paper_id,
                "title": paper.title,
                "authors": ", ".join([a.name for a in paper.authors]),
                "published": paper.published.strftime("%Y-%m-%d"),
                "abstract": paper.summary,
                "pdf_url": paper.pdf_url,
                "categories": paper.categories,
                "url": f"https://arxiv.org/abs/{paper_id}"
            })

        # Report missing papers
        found_ids = {p["paper_id"] for p in papers}
        for pid in id_list:
            if pid not in found_ids:
                papers.append({"paper_id": pid, "error": f"Paper not found: {pid}"})

        logger.info(f"ArXiv paper retrieval: {len(papers)} paper(s)")

        return {
            "success": True,
            "papers_retrieved": len(papers),
            "papers": papers
        }

    except Exception as e:
        logger.error(f"ArXiv paper retrieval error: {e}")
        return {"success": False, "error": str(e), "paper_ids": paper_ids}


def main():
    parser = argparse.ArgumentParser(
        description='ArXiv Search Skill - Search and retrieve scientific papers',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search for papers
  %(prog)s --query "transformer attention mechanism"

  # Get specific paper by ID
  %(prog)s --paper-ids "2301.12345"

  # Get multiple papers
  %(prog)s --paper-ids "2301.12345,2302.67890"
        """
    )

    parser.add_argument('--query', '-q', type=str, help='Search query string')
    parser.add_argument('--paper-ids', '-p', type=str, help='Comma-separated paper IDs')
    parser.add_argument('--max-results', '-m', type=int, default=5, help='Max search results (default: 5, max: 20)')
    parser.add_argument('--max-length', '-l', type=int, default=5000, help='Max content length (default: 5000)')

    args = parser.parse_args()

    if not args.query and not args.paper_ids:
        parser.error("Must specify either --query or --paper-ids")

    if args.query and args.paper_ids:
        parser.error("Cannot specify both --query and --paper-ids")

    if args.query:
        result = arxiv_search(args.query, max_results=args.max_results)
    else:
        result = arxiv_get_paper(args.paper_ids, max_length=args.max_length)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("success") else 1)


if __name__ == '__main__':
    main()
