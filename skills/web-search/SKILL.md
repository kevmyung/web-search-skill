---
name: web-search
description: "Search the web for up-to-date information, recent news, current events, or any topic that may require knowledge beyond the training cutoff. Also fetches full content from URLs when deeper reading is needed."
allowed-tools: Bash(python3 *)
---

# Web Search Skill

Determine the skill directory from where this SKILL.md was loaded. Use that path for all commands below (replace `$SKILL_DIR`).

## Usage

```bash
# Search the web
cd $SKILL_DIR && python scripts/web_search.py --query "your search query"

# Fetch content from a URL
cd $SKILL_DIR && python scripts/web_search.py --fetch-url "https://example.com"

# Search and auto-fetch top results
cd $SKILL_DIR && python scripts/web_search.py --query "your query" --fetch-content --top-n 3
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--query`, `-q` | Search query string | (required) |
| `--max-results`, `-m` | Max search results (max: 10) | 5 |
| `--fetch-url`, `-u` | URL to fetch content from | |
| `--fetch-content`, `-f` | Auto-fetch content from top search results | false |
| `--top-n`, `-n` | Number of top results to fetch | 3 |
| `--include-html` | Include raw HTML in response | false |
| `--max-length`, `-l` | Max character length for fetched content | 50000 |

## Notes

- Dependencies (`ddgs`, `httpx`, `beautifulsoup4`) are auto-installed on first run
- Uses DuckDuckGo for privacy-friendly search (no API key required)
- All output is JSON; check `"success": true/false` for status
- 30-second timeout for URL fetching
