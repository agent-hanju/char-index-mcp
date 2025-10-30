"""
MCP Char-Index

Character-level string manipulation with precise index-based operations.
Essential for test generation, parsing, and text processing where exact
character positioning is critical.

Core capabilities:
- Find characters/substrings by position
- Split text at exact indices
- Extract ranges with index precision
- Modify text by position (insert/delete/replace)
- Pattern matching with position info

---
This code was created with Claude AI.
Repository: https://github.com/agent-hanju/char-index-mcp
"""

from mcp.server.fastmcp import FastMCP
import re
from typing import Annotated

mcp = FastMCP("char-index")


# ========================================
# 1. Character & Substring Finding (4)
# ========================================

@mcp.tool()
def find_nth_char(
    text: Annotated[str, "Text to search in"],
    char: Annotated[str, "Single character to find"],
    n: Annotated[int, "Which occurrence to find (1-based)"] = 1
) -> int:
    """Find index of nth occurrence of a character. Returns -1 if not found."""
    if len(char) != 1:
        raise ValueError("char must be a single character")
    if n < 1:
        raise ValueError("n must be >= 1")
    
    count = 0
    for i, c in enumerate(text):
        if c == char:
            count += 1
            if count == n:
                return i
    return -1


@mcp.tool()
def find_all_char_indices(
    text: Annotated[str, "Text to search in"],
    char: Annotated[str, "Single character to find"]
) -> list[int]:
    """Find all indices where a character appears. Returns empty list if not found."""
    if len(char) != 1:
        raise ValueError("char must be a single character")
    
    return [i for i, c in enumerate(text) if c == char]


@mcp.tool()
def find_nth_substring(
    text: Annotated[str, "Text to search in"],
    substring: Annotated[str, "Substring to find"],
    n: Annotated[int, "Which occurrence to find (1-based)"] = 1
) -> int:
    """Find starting index of nth occurrence of a substring. Returns -1 if not found."""
    if not substring:
        raise ValueError("substring cannot be empty")
    if n < 1:
        raise ValueError("n must be >= 1")
    
    count = 0
    start = 0
    
    while True:
        index = text.find(substring, start)
        if index == -1:
            return -1
        
        count += 1
        if count == n:
            return index
        
        start = index + 1


@mcp.tool()
def find_all_substring_indices(
    text: Annotated[str, "Text to search in"],
    substring: Annotated[str, "Substring to find"]
) -> list[int]:
    """Find all starting indices where a substring appears (includes overlaps)."""
    if not substring:
        raise ValueError("substring cannot be empty")
    
    indices = []
    start = 0
    
    while True:
        index = text.find(substring, start)
        if index == -1:
            break
        indices.append(index)
        start = index + 1
    
    return indices


# ========================================
# 2. Splitting (1)
# ========================================

@mcp.tool()
def split_at_indices(
    text: Annotated[str, "Text to split"],
    indices: Annotated[list[int], "Split positions (auto-sorted & deduplicated)"]
) -> list[str]:
    """Split text at exact index positions. Indices auto-sorted and deduplicated."""
    if not indices:
        return [text]
    
    # Sort and remove duplicates
    sorted_indices = sorted(set(indices))
    
    # Validate
    for idx in sorted_indices:
        if idx < 0 or idx > len(text):
            raise ValueError(f"Index {idx} out of bounds [0, {len(text)}]")
    
    result = []
    start = 0
    
    for idx in sorted_indices:
        result.append(text[start:idx])
        start = idx
    
    result.append(text[start:])
    
    return result


# ========================================
# 3. String Modification (3)
# ========================================

@mcp.tool()
def insert_at_index(
    text: Annotated[str, "Original text"],
    index: Annotated[int, "Position to insert at (negative = from end)"],
    insertion: Annotated[str, "Text to insert"]
) -> str:
    """Insert text at index position without replacing. Supports negative indices."""
    if index < 0:
        index = max(0, len(text) + index + 1)
    
    return text[:index] + insertion + text[index:]


@mcp.tool()
def delete_range(
    text: Annotated[str, "Original text"],
    start: Annotated[int, "Starting index (inclusive)"],
    end: Annotated[int, "Ending index (exclusive)"]
) -> str:
    """Delete characters in range [start, end)."""
    return text[:start] + text[end:]


@mcp.tool()
def replace_range(
    text: Annotated[str, "Original text"],
    start: Annotated[int, "Starting index (inclusive)"],
    end: Annotated[int, "Ending index (exclusive)"],
    replacement: Annotated[str, "Text to replace with"]
) -> str:
    """Replace characters in range [start, end) with new text."""
    return text[:start] + replacement + text[end:]


# ========================================
# 4. Utilities (3)
# ========================================

@mcp.tool()
def find_regex_matches(
    text: Annotated[str, "Text to search in"],
    pattern: Annotated[str, "Regular expression pattern"]
) -> list[dict]:
    """Find all regex matches with positions. Returns list of {start, end, match} dicts."""
    try:
        matches = []
        for match in re.finditer(pattern, text):
            matches.append({
                "start": match.start(),
                "end": match.end(),
                "match": match.group()
            })
        return matches
    except re.error as e:
        raise ValueError(f"Invalid regex pattern: {e}")


@mcp.tool()
def extract_between_markers(
    text: Annotated[str, "Text to search in"],
    start_marker: Annotated[str, "Opening marker"],
    end_marker: Annotated[str, "Closing marker"],
    occurrence: Annotated[int, "Which occurrence to extract (1-based)"] = 1
) -> dict:
    """Extract content between markers with positions. Returns dict with content and position info."""
    if not start_marker or not end_marker:
        raise ValueError("Markers cannot be empty")
    if occurrence < 1:
        raise ValueError("occurrence must be >= 1")
    
    count = 0
    search_start = 0
    
    while True:
        start_idx = text.find(start_marker, search_start)
        if start_idx == -1:
            return {
                "content": None,
                "content_start": None,
                "content_end": None,
                "full_start": None,
                "full_end": None
            }
        
        content_start = start_idx + len(start_marker)
        end_idx = text.find(end_marker, content_start)
        
        if end_idx == -1:
            return {
                "content": None,
                "content_start": None,
                "content_end": None,
                "full_start": None,
                "full_end": None
            }
        
        count += 1
        if count == occurrence:
            return {
                "content": text[content_start:end_idx],
                "content_start": content_start,
                "content_end": end_idx,
                "full_start": start_idx,
                "full_end": end_idx + len(end_marker)
            }
        
        search_start = content_start


@mcp.tool()
def count_chars(
    text: Annotated[str, "Text to analyze"]
) -> dict:
    """Count character statistics. Returns dict with total, without_spaces, letters, digits, spaces, special."""
    return {
        "total": len(text),
        "without_spaces": len(text.replace(" ", "")),
        "letters": sum(1 for c in text if c.isalpha()),
        "digits": sum(1 for c in text if c.isdigit()),
        "spaces": sum(1 for c in text if c.isspace()),
        "special": sum(1 for c in text if not c.isalnum() and not c.isspace())
    }


# ========================================
# 5. Batch Processing (1) - 핵심 통합
# ========================================

@mcp.tool()
def extract_substrings(
    text: Annotated[str, "Text to extract from"],
    ranges: Annotated[list[dict], "List of ranges with 'start' (required) and 'end' (optional). Negative indices supported"]
) -> list[dict]:
    """Extract substrings by index ranges. Supports negative indices and omitting end. Returns list of {start, end, substring, length} dicts."""
    results = []
    text_len = len(text)
    
    for r in ranges:
        start = r["start"]
        end = r.get("end", None)
        
        # Normalize negative indices
        if start < 0:
            start = max(0, text_len + start)
        if end is not None and end < 0:
            end = max(0, text_len + end)
        
        # Extract substring
        substring = text[start:end]
        actual_end = end if end is not None else text_len
        
        results.append({
            "start": start,
            "end": actual_end,
            "substring": substring,
            "length": len(substring)
        })
    
    return results


def main():
    """Entry point for the char-index-mcp CLI."""
    mcp.run()


if __name__ == "__main__":
    main()