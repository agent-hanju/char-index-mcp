# char-index-skill

**Character-level index-based string manipulation** as a Claude Code Skill (plugin).

LLMs generate text token-by-token and struggle with exact character counting. This skill provides precise index-based tools for test code generation, string parsing, and position-critical tasks.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation

### As a Claude Code Plugin (Recommended)

```bash
# Install the plugin
claude plugin install char-index-skill
```

Or clone and use directly:

```bash
git clone https://github.com/agent-hanju/char-index-skill.git
```

The skill is in `skills/char-index-skill/` and will be automatically available in Claude Code.

### Usage

Claude will automatically invoke the skill when you need character-level string operations. You can also call it explicitly with `/char-index-skill`.

All operations are available via:

```bash
python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py <command> [options]
```

See [SKILL.md](skills/char-index-skill/SKILL.md) for the full command reference.

## Features (11 Operations)

### Finding (4)
- `find-nth-char` - Find nth occurrence of a character
- `find-all-chars` - Find all indices of a character
- `find-nth-substring` - Find nth occurrence of a substring
- `find-all-substrings` - Find all occurrences of a substring

### Splitting & Extraction (4)
- `split-at` - Split string at multiple positions
- `extract` - Extract substring by range
- `extract-between` - Extract text between two markers
- `extract-batch` - Extract multiple substrings by index ranges

### Modification (3)
- `insert` - Insert text at specific position
- `delete` - Delete characters in range
- `replace` - Replace range with new text

### Utilities (1)
- `count` - Character statistics (total, letters, digits, etc.)

## Quick Examples

```bash
# Find 3rd 'l'
python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py find-nth-char \
  --text "hello world" --char "l" --n 3
# {"index": 9}

# Split at positions
python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py split-at \
  --text "hello world" --indices "2,5,8"
# {"parts": ["he", "llo", " wo", "rld"]}

# Extract between markers
python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py extract-between \
  --text "<tag>content</tag>" --start-marker "<tag>" --end-marker "</tag>"
# {"content": "content", ...}

# Count characters
python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py count --text "Hello World!"
# {"total": 12, "letters": 10, "digits": 0, "spaces": 1, "special": 1}
```

See [examples.md](skills/char-index-skill/examples.md) for more practical examples.

## Key Points

- **0-indexed**: All positions start from 0
- **1-based occurrence**: `find-nth-*` uses `--n 1` for first occurrence
- **Negative indices**: `-1` = last char, `-5` = 5th from end
- **Range format**: `[start, end)` - start inclusive, end exclusive
- **Unicode safe**: Each Unicode character = 1 position
- **JSON output**: All operations return JSON for easy parsing

## Use Cases

1. **Test Code Generation** - Generate strings with exact character counts
2. **Data Processing** - Split/extract data at precise positions
3. **Text Formatting** - Insert/delete/replace at specific indices
4. **LLM Response Parsing** - Extract content between XML tags by position

## Project Structure

```
char-index-skill/
├── .claude-plugin/plugin.json     # Plugin manifest
├── skills/
│   └── char-index-skill/
│       ├── SKILL.md               # Skill definition
│       ├── examples.md            # Usage examples
│       └── scripts/char_ops.py    # Implementation (11 operations)
├── char_index_mcp/                # MCP server (legacy)
│   ├── server.py
│   ├── char_ops.py                # Synced copy
│   └── tests/
├── pyproject.toml                 # MCP package config
├── README.md
└── LICENSE
```

## Development

```bash
git clone https://github.com/agent-hanju/char-index-skill.git
cd char-index-skill

python -m venv .venv
.venv/Scripts/activate  # or source .venv/bin/activate

pip install -e .
pytest char_index_mcp/tests/ -v
ruff check .
mypy char_index_mcp/
```

## MCP Server (Legacy)

The `char-index-mcp` package provides the same 11 operations as an MCP server for integration with Claude Desktop, Cursor, and other MCP clients. This is maintained for backward compatibility but the Claude Code Skill is the recommended approach.

```bash
# Install
pip install char-index-mcp

# Or run directly
uvx char-index-mcp
```

Configuration for Claude Desktop (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "char-index": {
      "command": "uvx",
      "args": ["char-index-mcp"]
    }
  }
}
```

[![PyPI](https://img.shields.io/pypi/v/char-index-mcp)](https://pypi.org/project/char-index-mcp/)
[![Python](https://img.shields.io/pypi/pyversions/char-index-mcp)](https://pypi.org/project/char-index-mcp/)

## License

MIT License - see LICENSE file for details
