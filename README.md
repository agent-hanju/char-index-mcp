# char-index-mcp

A Model Context Protocol (MCP) server providing **character-level index-based string manipulation**. Perfect for test code generation where precise character positioning matters.

[![smithery badge](https://smithery.ai/badge/char-index-mcp)](https://smithery.ai/server/char-index-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/pypi/v/char-index-mcp)](https://pypi.org/project/char-index-mcp/)
[![Python](https://img.shields.io/pypi/pyversions/char-index-mcp)](https://pypi.org/project/char-index-mcp/)

> This project was created with Claude AI.

## 🎯 Why This Exists

LLMs generate text token-by-token and struggle with exact character counting. When generating test code with specific length requirements or validating string positions, you need precise index-based tools. This MCP server solves that problem.

## ✨ Features (12 Tools)

### 🔍 Character & Substring Finding (4 tools)
- `find_nth_char` - Find nth occurrence of a character
- `find_all_char_indices` - Find all indices of a character
- `find_nth_substring` - Find nth occurrence of a substring
- `find_all_substring_indices` - Find all occurrences of a substring

### ✂️ Splitting (1 tool)
- `split_at_indices` - Split string at multiple positions

### ✏️ String Modification (3 tools)
- `insert_at_index` - Insert text at specific position
- `delete_range` - Delete characters in range
- `replace_range` - Replace range with new text

### 🛠️ Utilities (3 tools)
- `find_regex_matches` - Find regex pattern matches with positions
- `extract_between_markers` - Extract text between two markers
- `count_chars` - Character statistics (total, letters, digits, etc.)

### 📦 Batch Processing (1 tool)
- `extract_substrings` - Extract one or more substrings (unified tool)

## 🚀 Installation

### Option 1: Using uvx (Recommended)

No installation required! Just configure and run:

```bash
# Test it works
uvx char-index-mcp --help
```

### Option 2: From PyPI

```bash
pip install char-index-mcp
```

### Option 3: From Source

```bash
git clone https://github.com/agent-hanju/char-index-mcp.git
cd char-index-mcp
pip install -e .
```

## 🔧 Configuration

### Claude Desktop

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

#### Using uvx (Recommended)

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

#### Using pip install

```json
{
  "mcpServers": {
    "char-index": {
      "command": "char-index-mcp"
    }
  }
}
```

### Claude Code

```bash
# Using uvx (recommended)
claude mcp add char-index '{"command":"uvx","args":["char-index-mcp"]}'

# Using pip install
claude mcp add char-index '{"command":"char-index-mcp"}'
```

### Cursor

Add to `~/.cursor/mcp.json`:

#### Using uvx (Recommended)

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

#### Using pip install

```json
{
  "mcpServers": {
    "char-index": {
      "command": "char-index-mcp"
    }
  }
}
```

## 📖 Usage Examples

### Finding Characters
```python
# Find 3rd occurrence of 'l'
find_nth_char("hello world", "l", 3)  # Returns: 9

# Find all occurrences of 'l'
find_all_char_indices("hello world", "l")  # Returns: [2, 3, 9]
```

### Working with Substrings
```python
# Find 2nd "hello"
find_nth_substring("hello hello world", "hello", 2)  # Returns: 6

# Find all occurrences
find_all_substring_indices("hello hello world", "hello")  # Returns: [0, 6]
```

### String Manipulation
```python
# Insert comma after "hello"
insert_at_index("hello world", 5, ",")  # Returns: "hello, world"

# Delete " world"
delete_range("hello world", 5, 11)  # Returns: "hello"

# Replace "world" with "Python"
replace_range("hello world", 6, 11, "Python")  # Returns: "hello Python"
```

### Splitting & Extracting
```python
# Split at multiple positions
split_at_indices("hello world", [2, 5, 8])  # Returns: ["he", "llo", " wo", "rld"]

# Extract single character
extract_substrings("hello", [{"start": 1, "end": 2}])
# Returns: [{"start": 1, "end": 2, "substring": "e", "length": 1}]

# Batch extraction
extract_substrings("hello world", [
    {"start": 0, "end": 5},
    {"start": 6, "end": 11}
])
# Returns: [
#   {"start": 0, "end": 5, "substring": "hello", "length": 5},
#   {"start": 6, "end": 11, "substring": "world", "length": 5}
# ]
```

### Pattern Matching
```python
# Find all numbers with their positions
find_regex_matches("test123abc456", r"\d+")
# Returns: [
#   {"start": 4, "end": 7, "match": "123"},
#   {"start": 10, "end": 13, "match": "456"}
# ]
```

### Extracting Text
```python
# Extract content between markers
extract_between_markers("start[content]end", "[", "]", 1)
# Returns: {
#   "content": "content",
#   "content_start": 6,
#   "content_end": 13,
#   "full_start": 5,
#   "full_end": 14
# }
```

## 🧪 Development

```bash
# Clone the repository
git clone https://github.com/agent-hanju/char-index-mcp.git
cd char-index-mcp

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=char_index_mcp --cov-report=term-missing
```

## 🎯 Use Cases

1. **Test Code Generation**: Generate strings with exact character counts
2. **Data Processing**: Split/extract data at precise positions
3. **Text Formatting**: Insert/delete/replace at specific indices
4. **Pattern Analysis**: Find and extract pattern matches with positions
5. **LLM Response Parsing**: Extract content between XML tags by position

## 📝 Example: Test Code Generation

```python
# Ask Claude: "Generate a test string that's exactly 100 characters long"
# Claude can use count_chars() to verify the exact length

# Ask: "Find where the 5th comma is in this CSV line"
# Claude can use find_nth_char(csv_line, ",", 5)

# Ask: "Split this string at characters 10, 25, and 50"
# Claude can use split_at_indices(text, [10, 25, 50])

# Ask: "Extract the text between the 2nd <thinking> and </thinking> tags"
# Claude can use extract_between_markers(text, "<thinking>", "</thinking>", 2)
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🔗 Related Projects

- [mcp-character-counter](https://github.com/webreactiva-devs/mcp-character-counter) - Character counting & analysis
- [mcp-wordcounter](https://github.com/qpd-v/mcp-wordcounter) - Word & character counting for files
- [text-master-mcp](https://github.com/very99/text-master-mcp) - Comprehensive text processing toolkit

## 📮 Contact

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Note**: This is the first MCP server specifically designed for index-based string manipulation. All other text MCP servers focus on counting, case conversion, or encoding - not precise character positioning.
