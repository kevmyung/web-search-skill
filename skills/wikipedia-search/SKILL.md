---
name: wikipedia-search
description: "Look up factual knowledge, definitions, historical context, or background information on people, places, concepts, and events from Wikipedia."
allowed-tools: Bash(python3 *)
---

# Wikipedia Search Skill

Determine the skill directory from where this SKILL.md was loaded. Use that path for all commands below (replace `$SKILL_DIR`).

## Usage

```bash
# Search Wikipedia
cd $SKILL_DIR && python3 scripts/wikipedia_search.py --query "Quantum computing"

# Get full article by exact title
cd $SKILL_DIR && python3 scripts/wikipedia_search.py --title "Python (programming language)"

# Get summary only
cd $SKILL_DIR && python3 scripts/wikipedia_search.py --title "Machine learning" --summary-only

# Search in another language
cd $SKILL_DIR && python3 scripts/wikipedia_search.py --query "인공지능" --language ko
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--query`, `-q` | Search query string | |
| `--title`, `-t` | Exact article title to retrieve | |
| `--summary-only`, `-s` | Return only summary (with --title) | false |
| `--max-length`, `-l` | Max content length | 5000 |
| `--language` | Wikipedia language code | en |

## Notes

- Use `--query` first to find the correct article title, then `--title` for full content
- Article titles are case-sensitive — use the exact title from search results
- Dependencies (`wikipedia-api`) are auto-installed on first run
- All output is JSON; check `"success": true/false` for status
