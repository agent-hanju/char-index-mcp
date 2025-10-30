# Quick Start Guide

Get up and running with char-index-mcp server in 5 minutes!

> This project was created with Claude AI.

## Installation (5 minutes)

### 1. Install uv (if not already installed)
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone and setup
```bash
git clone https://github.com/agent-hanju/char-index-mcp.git
cd char-index-mcp
uv sync
```

### 3. Test it works
```bash
python -c "from server import find_nth_char; print(find_nth_char('hello', 'l', 2))"
# Should output: 3
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
```json
{
  "mcpServers": {
    "char-index": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/char-index-mcp",
        "run",
        "server.py"
      ]
    }
  }
}
```

**Important**: Replace `/ABSOLUTE/PATH/TO/` with your actual path!

Examples:
- macOS: `/Users/yourname/char-index-mcp`
- Windows: `C:\\Users\\yourname\\char-index-mcp`
- Linux: `/home/yourname/char-index-mcp`

### 4. Restart Claude Desktop

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
1. Check the path is absolute (not relative)
   - ❌ Wrong: `"./char-index-mcp"` or `"char-index-mcp"`
   - ✅ Right: `"/Users/yourname/char-index-mcp"` or `"C:\\Users\\yourname\\char-index-mcp"`
2. Check you restarted Claude Desktop completely (Quit and reopen)
3. Check the config file has valid JSON (no trailing commas, quotes matched)
4. Check the logs:
   - macOS: `~/Library/Logs/Claude/mcp*.log`
   - Windows: `%APPDATA%\Claude\logs\mcp*.log`

### "Module not found" or "ImportError"
```bash
cd /path/to/char-index-mcp
uv sync
```

This will reinstall all dependencies.

### "Permission denied" (Linux/macOS)
```bash
chmod +x server.py
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
npx @modelcontextprotocol/inspector uv --directory /path/to/char-index-mcp run server.py
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
# Add to Claude Code
claude mcp add char-index '{"command":"uv","args":["--directory","/absolute/path/char-index-mcp","run","server.py"]}'
```

### With Cursor
Add to `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "char-index": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/char-index-mcp", "run", "server.py"]
    }
  }
}
```

### With Custom MCP Clients
Use the standard MCP protocol to connect:
```python
from mcp import ClientSession

session = ClientSession()
await session.initialize()
result = await session.call_tool("find_nth_char", {
    "text": "hello",
    "char": "l",
    "n": 2
})
```

## Next Steps

- 📖 Read [README.md](README.md) for complete tool documentation
- 🧪 Check out the test files to see all features in action
- 🌟 Star the repo if you find it useful!
- 🐛 Report bugs or request features via GitHub Issues

## Useful Commands

```bash
# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=. --cov-report=term-missing

# Format code
uv run black .

# Lint code
uv run ruff check .

# Update dependencies
uv sync --upgrade
```

## Support

Found a bug? Have a feature request?
- 🐛 Open an issue: https://github.com/agent-hanju/char-index-mcp/issues
- 💬 Start a discussion: https://github.com/agent-hanju/char-index-mcp/discussions

---

**Pro Tip**: Once you're comfortable with the basics, try combining multiple tools to solve complex problems. For example, use `find_regex_matches()` to find patterns, then use `extract_substrings()` to extract them, and finally `replace_range()` to modify them!
