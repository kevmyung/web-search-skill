# Web Search Skills

A collection of Claude Code skills for searching the web, Wikipedia, and ArXiv. No API keys required. Dependencies are auto-installed on first run.

## Skills

| Skill | Description | Source |
|-------|-------------|--------|
| **web-search** | DuckDuckGo web search + URL content fetching | DuckDuckGo |
| **wikipedia-search** | Wikipedia article search and retrieval | Wikipedia API |
| **arxiv-search** | Scientific paper search and retrieval | ArXiv API |

## Installation

### Claude Code

Install individual skills or all at once:

```bash
git clone https://github.com/kevmyung/web-search-skill.git /tmp/web-search-skill

# Install all skills
cp -r /tmp/web-search-skill/skills/* ~/.claude/skills/

# Or install individually
cp -r /tmp/web-search-skill/skills/web-search ~/.claude/skills/
cp -r /tmp/web-search-skill/skills/wikipedia-search ~/.claude/skills/
cp -r /tmp/web-search-skill/skills/arxiv-search ~/.claude/skills/

rm -rf /tmp/web-search-skill
```

For a specific project only, replace `~/.claude/skills/` with `<your-project>/.claude/skills/`.

Claude Code will auto-discover the skills and install Python dependencies on first use.

### Strands Agent

Copy skills into your agent's `skills/` folder:

```bash
cp -r skills/* /path/to/your/agent/skills/
```

## Usage

Once installed, Claude Code will automatically invoke relevant skills based on your questions. You can also run them directly from the command line.

### Web Search

```bash
cd ~/.claude/skills/web-search
python3 scripts/web_search.py --query "Python async programming"
python3 scripts/web_search.py --fetch-url "https://example.com/article"
python3 scripts/web_search.py --query "AWS Lambda" --fetch-content --top-n 3
```

### Wikipedia Search

```bash
cd ~/.claude/skills/wikipedia-search
python3 scripts/wikipedia_search.py --query "Quantum computing"
python3 scripts/wikipedia_search.py --title "Python (programming language)"
python3 scripts/wikipedia_search.py --title "Machine learning" --summary-only
python3 scripts/wikipedia_search.py --query "인공지능" --language ko
```

### ArXiv Search

```bash
cd ~/.claude/skills/arxiv-search
python3 scripts/arxiv_search.py --query "transformer attention mechanism"
python3 scripts/arxiv_search.py --paper-ids "2301.12345"
python3 scripts/arxiv_search.py --paper-ids "2301.12345,2302.67890"
```

## Requirements

- Python 3.8+
- All dependencies are **auto-installed** on first run per skill

## License

MIT
