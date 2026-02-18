# Web Search Skill

A Claude Code skill for searching the web using DuckDuckGo and fetching content from URLs. No API key required. Dependencies are auto-installed on first run.

## Features

- **Web Search** — Search via DuckDuckGo (privacy-friendly, no API key)
- **URL Content Fetching** — Extract clean text from any web page
- **Search + Auto-Fetch** — Search and automatically fetch content from top results

## Installation

### Claude Code (recommended)

```bash
# Clone and copy to your skills directory
git clone https://github.com/kevmyung/web-search-skill.git /tmp/web-search-skill
cp -r /tmp/web-search-skill/skills/web-search ~/.claude/skills/
rm -rf /tmp/web-search-skill
```

Or for a specific project only:

```bash
git clone https://github.com/kevmyung/web-search-skill.git /tmp/web-search-skill
cp -r /tmp/web-search-skill/skills/web-search <your-project>/.claude/skills/
rm -rf /tmp/web-search-skill
```

That's it. Claude Code will auto-discover the skill and install Python dependencies on first use.

### Strands Agent

Copy `skills/web-search` into your agent's `skills/` folder:

```bash
cp -r skills/web-search /path/to/your/agent/skills/
```

## Usage

Once installed, Claude Code will automatically invoke this skill when you ask it to search the web.

You can also use it directly from the command line:

```bash
cd ~/.claude/skills/web-search

# Search the web
python3 scripts/web_search.py --query "Python async programming"

# Fetch content from a URL
python3 scripts/web_search.py --fetch-url "https://example.com/article"

# Search and auto-fetch top 3 results
python3 scripts/web_search.py --query "AWS Lambda best practices" --fetch-content --top-n 3
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--query`, `-q` | Search query string | (required) |
| `--max-results`, `-m` | Max search results (max: 10) | 5 |
| `--fetch-url`, `-u` | URL to fetch content from | |
| `--fetch-content`, `-f` | Auto-fetch content from top search results | false |
| `--top-n`, `-n` | Number of top results to fetch | 3 |
| `--include-html` | Include raw HTML in response | false |
| `--max-length`, `-l` | Max character length for fetched content | 50000 |

## Requirements

- Python 3.8+
- Dependencies (`ddgs`, `httpx`, `beautifulsoup4`) are **auto-installed** on first run

## License

MIT
