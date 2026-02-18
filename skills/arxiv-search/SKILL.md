---
name: arxiv-search
description: "Find academic papers, preprints, and scientific research on ArXiv. Use when the user asks about state-of-the-art methods, recent research, or needs citations for technical claims."
allowed-tools: Bash(python3 *)
---

# ArXiv Search Skill

Determine the skill directory from where this SKILL.md was loaded. Use that path for all commands below (replace `$SKILL_DIR`).

## Usage

```bash
# Search for papers
cd $SKILL_DIR && python3 scripts/arxiv_search.py --query "transformer attention mechanism"

# Get specific paper by ID
cd $SKILL_DIR && python3 scripts/arxiv_search.py --paper-ids "2301.12345"

# Get multiple papers
cd $SKILL_DIR && python3 scripts/arxiv_search.py --paper-ids "2301.12345,2302.67890"

# Search with more results
cd $SKILL_DIR && python3 scripts/arxiv_search.py --query "LLM reasoning" --max-results 10
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--query`, `-q` | Search query string | |
| `--paper-ids`, `-p` | Comma-separated paper IDs | |
| `--max-results`, `-m` | Max search results (max: 20) | 5 |
| `--max-length`, `-l` | Max content length | 5000 |

## Notes

- Use specific academic keywords for best results (e.g., "transformer attention mechanism" not "AI")
- Paper IDs follow the format: `2301.12345`
- Use `--query` first to find papers, then `--paper-ids` for details
- Dependencies (`arxiv`) are auto-installed on first run
- All output is JSON; check `"success": true/false` for status
