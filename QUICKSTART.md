# Quick Start Guide

Get up and running with char-index-mcp server in 2 minutes!

> This project was created with Claude AI.

## Installation (30 seconds)

### Option 1: Using uvx (Recommended - No Installation!)

Just configure and it works! Skip directly to [Configure with Claude Desktop](#configure-with-claude-desktop).

### Option 2: Using pip

```bash
pip install char-index-mcp
```

### Test it works

```bash
# Test the CLI is available
char-index-mcp --help

# Or with uvx
uvx char-index-mcp --help
```

## Configure with Claude Desktop

### macOS
```bash
# Open config file
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### Windows
```bash
# Open config file
code %APPDATA%\Claude\claude_desktop_config.json
```

### Add this configuration:

**Option 1: Using uvx (Recommended)**
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

**Option 2: Using pip install**
```json
{
  "mcpServers": {
    "char-index": {
      "command": "char-index-mcp"
    }
  }
}
```

### Restart Claude Desktop

Look for the 🔨 hammer icon - that means the MCP tools are loaded!

## Test in Claude

Try asking:
- "Find the 3rd occurrence of 'e' in 'hello there everyone'"
- "Split 'hello-world-test' at positions 5 and 11"
- "Count characters in 'Hello World 123!'"
- "Extract substrings from 'hello world' at ranges 0-5 and 6-11"

## Common Use Cases

### 1. Test Code Generation
```
"Generate a test string that's exactly 100 characters"
→ Claude can use count_chars() to verify
```

### 2. Data Processing
```
"Extract email addresses from this text and tell me their positions"
→ Claude can use find_regex_matches()
```

### 3. String Surgery
```
"Replace characters 10-15 in this text with 'XXXXX'"
→ Claude can use replace_range()
```

### 4. Pattern Extraction
```
"Extract all content between <thinking> tags in this LLM response"
→ Claude can use extract_between_markers()
```

### 5. CSV/Fixed-Width Data Parsing
```
"Split this CSV line at the 3rd, 7th, and 12th comma"
→ Claude can use find_nth_char() + split_at_indices()
```

### 6. Position-Based Text Analysis
```
"Find all numbers in this text and tell me their exact positions"
→ Claude can use find_regex_matches(text, r"\d+")
```

## Tool Reference

### Finding (4 tools)
- `find_nth_char(text, char, n)` - Find nth character
- `find_all_char_indices(text, char)` - Find all character positions
- `find_nth_substring(text, substring, n)` - Find nth substring
- `find_all_substring_indices(text, substring)` - Find all substring positions

### Splitting (1 tool)
- `split_at_indices(text, indices)` - Split at multiple positions

### Modification (3 tools)
- `insert_at_index(text, index, insertion)` - Insert text
- `delete_range(text, start, end)` - Delete range
- `replace_range(text, start, end, replacement)` - Replace range

### Utilities (3 tools)
- `find_regex_matches(text, pattern)` - Regex with positions
- `extract_between_markers(text, start_marker, end_marker, occurrence)` - Extract between markers
- `count_chars(text)` - Character statistics

### Batch (1 tool)
- `extract_substrings(text, ranges)` - Extract multiple ranges

## Troubleshooting

### "Server not loaded" or "No hammer icon"
1. Check you restarted Claude Desktop completely (Quit and reopen)
2. Check the config file has valid JSON (no trailing commas, quotes matched)
3. If using uvx, make sure it's installed: `pip install uvx` or `pipx install uv`
4. Check the logs:
   - macOS: `~/Library/Logs/Claude/mcp*.log`
   - Windows: `%APPDATA%\Claude\logs\mcp*.log`

### "Module not found" or "ImportError"
```bash
# Reinstall the package
pip install --force-reinstall char-index-mcp

# Or with uvx, clear the cache
uvx --refresh char-index-mcp --help
```

### Config file doesn't exist
Create it manually:

**macOS**:
```bash
mkdir -p ~/Library/Application\ Support/Claude
touch ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows** (PowerShell):
```powershell
New-Item -Path "$env:APPDATA\Claude\claude_desktop_config.json" -ItemType File -Force
```

### Testing outside Claude Desktop

You can test the server directly using the MCP inspector:

```bash
# With uvx
npx @modelcontextprotocol/inspector uvx char-index-mcp

# With pip install
npx @modelcontextprotocol/inspector char-index-mcp
```

This will open a web interface where you can test all the tools.

## Quick Examples

### Example 1: Extract email domain
```
User: "From email 'user@example.com', extract just the domain"

Claude: Let me use extract_between_markers to get the domain:
- extract_between_markers("user@example.com", "@", "")
Result: "example.com"
```

### Example 2: Generate exact-length string
```
User: "Generate a random string that's exactly 50 characters"

Claude: Here's a string:
"abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMN"

Let me verify: count_chars(...)
Result: {"total": 50, ...}
Confirmed: exactly 50 characters!
```

### Example 3: Split fixed-width data
```
User: "This is fixed-width data: 'John      Smith     42'
Split at positions 10 and 20"

Claude: split_at_indices("John      Smith     42", [10, 20])
Result: ["John      ", "Smith     ", "42"]
```

### Example 4: Find all code blocks
```
User: "Extract all code blocks from this markdown text"

Claude: Using find_regex_matches(text, r"```.*?```")
Result: [
  {"start": 10, "end": 45, "match": "```python\ncode\n```"},
  {"start": 60, "end": 85, "match": "```bash\nls\n```"}
]
```

## Performance Tips

1. **Batch operations**: Use `extract_substrings()` instead of multiple calls
   - ❌ Slow: Call 10 times for 10 ranges
   - ✅ Fast: One call with 10 ranges in array

2. **Use specific tools**: Don't use regex when simple find works
   - ❌ Slow: `find_regex_matches(text, "hello")`
   - ✅ Fast: `find_all_substring_indices(text, "hello")`

3. **Pre-calculate positions**: Store positions if you need them multiple times

## Advanced Usage

### Chaining Operations

Find and replace the 2nd occurrence:
```
1. find_nth_substring(text, "target", 2) → get position
2. replace_range(text, position, position + len("target"), "new")
```

### Negative Indices

```python
# Get last character
extract_substrings("hello", [{"start": -1}])
# Result: [{"substring": "o", ...}]

# Get last 3 characters
extract_substrings("hello", [{"start": -3}])
# Result: [{"substring": "llo", ...}]
```

### Complex Patterns

```python
# Find all URLs in text
find_regex_matches(text, r"https?://[^\s]+")

# Find all email addresses
find_regex_matches(text, r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")

# Find all words with exactly 5 letters
find_regex_matches(text, r"\b\w{5}\b")
```

## Integration with Other Tools

### With Claude Code
```bash
# Using uvx (recommended)
claude mcp add char-index '{"command":"uvx","args":["char-index-mcp"]}'

# Using pip install
claude mcp add char-index '{"command":"char-index-mcp"}'
```

### With Cursor
Add to `~/.cursor/mcp.json`:

**Using uvx (Recommended)**
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

**Using pip install**
```json
{
  "mcpServers": {
    "char-index": {
      "command": "char-index-mcp"
    }
  }
}
```

## Next Steps

- 📖 Read [README.md](README.md) for complete tool documentation
- 🧪 Check out the test files to see all features in action
- 🌟 Star the repo if you find it useful!
- 🐛 Report bugs or request features via GitHub Issues

## Development Commands

For contributors and developers:

```bash
# Clone and install in dev mode
git clone https://github.com/agent-hanju/char-index-mcp.git
cd char-index-mcp
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=char_index_mcp --cov-report=term-missing

# Format code
black .

# Lint code
ruff check .
```

## Support

Found a bug? Have a feature request?
- 🐛 Open an issue: https://github.com/agent-hanju/char-index-mcp/issues
- 💬 Start a discussion: https://github.com/agent-hanju/char-index-mcp/discussions

---

**Pro Tip**: Once you're comfortable with the basics, try combining multiple tools to solve complex problems. For example, use `find_regex_matches()` to find patterns, then use `extract_substrings()` to extract them, and finally `replace_range()` to modify them!
