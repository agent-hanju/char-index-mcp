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
from typing import Optional

mcp = FastMCP("char-index")


# ========================================
# 1. Character & Substring Finding (4)
# ========================================

@mcp.tool()
def find_nth_char(text: str, char: str, n: int = 1) -> int:
    """
    Find the index of the nth occurrence of a character.
    
    Use this when you need to locate a specific character occurrence,
    like finding the 3rd comma in a CSV line or the 2nd quote in a string.
    
    Args:
        text: Text to search in
        char: Single character to find
        n: Which occurrence to find (1-based, default: 1)
    
    Returns:
        Zero-based index of the character, or -1 if not found
    
    Examples:
        find_nth_char("hello world", "l", 1) -> 2
        find_nth_char("hello world", "l", 3) -> 9
        find_nth_char("hello", "x", 1) -> -1
    """
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
def find_all_char_indices(text: str, char: str) -> list[int]:
    """
    Find all indices where a character appears.
    
    Use this to get all positions of a character at once, useful for
    analyzing patterns or finding multiple delimiters.
    
    Args:
        text: Text to search in
        char: Single character to find
    
    Returns:
        List of zero-based indices (empty list if not found)
    
    Examples:
        find_all_char_indices("hello world", "l") -> [2, 3, 9]
        find_all_char_indices("test", "x") -> []
    """
    if len(char) != 1:
        raise ValueError("char must be a single character")
    
    return [i for i, c in enumerate(text) if c == char]


@mcp.tool()
def find_nth_substring(text: str, substring: str, n: int = 1) -> int:
    """
    Find the starting index of the nth occurrence of a substring.
    
    Use this when searching for repeated patterns like finding the 2nd
    occurrence of a word or the 3rd XML tag.
    
    Args:
        text: Text to search in
        substring: Substring to find
        n: Which occurrence to find (1-based, default: 1)
    
    Returns:
        Zero-based starting index, or -1 if not found
    
    Examples:
        find_nth_substring("hello hello world", "hello", 1) -> 0
        find_nth_substring("hello hello world", "hello", 2) -> 6
        find_nth_substring("test", "xyz", 1) -> -1
    """
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
def find_all_substring_indices(text: str, substring: str) -> list[int]:
    """
    Find all starting indices where a substring appears.
    
    Use this to locate all occurrences of a pattern at once, including
    overlapping matches.
    
    Args:
        text: Text to search in
        substring: Substring to find
    
    Returns:
        List of zero-based starting indices (empty list if not found)
    
    Examples:
        find_all_substring_indices("hello hello world", "hello") -> [0, 6]
        find_all_substring_indices("aaa", "aa") -> [0, 1]  # overlapping
    """
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
def split_at_indices(text: str, indices: list[int]) -> list[str]:
    """
    Split text at specific index positions.
    
    Use this when you need to divide text at exact positions, not by
    delimiters. Perfect for fixed-width parsing or position-based splitting.
    
    Args:
        text: Text to split
        indices: List of split positions (automatically sorted & deduplicated)
    
    Returns:
        List of substrings (n indices = n+1 parts)
    
    Examples:
        split_at_indices("hello world", [5]) -> ["hello", " world"]
        split_at_indices("abcdef", [2, 4]) -> ["ab", "cd", "ef"]
        split_at_indices("test", [1, 3, 1]) -> ["t", "es", "t"]  # auto-sorted
    """
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
def insert_at_index(text: str, index: int, insertion: str) -> str:
    """
    Insert text at a specific index position.
    
    Use this to inject content at precise positions without replacing
    existing text. Supports negative indices.
    
    Args:
        text: Original text
        index: Position to insert at (negative = from end)
        insertion: Text to insert
    
    Returns:
        Modified text
    
    Examples:
        insert_at_index("hello world", 5, ",") -> "hello, world"
        insert_at_index("test", 0, "pre") -> "pretest"
        insert_at_index("test", -1, "!") -> "test!"  # before last char
    """
    if index < 0:
        index = max(0, len(text) + index + 1)
    
    return text[:index] + insertion + text[index:]


@mcp.tool()
def delete_range(text: str, start: int, end: int) -> str:
    """
    Delete characters in the specified range [start, end).
    
    Use this to remove exact portions of text by position, like removing
    a detected pattern or cleaning up specific ranges.
    
    Args:
        text: Original text
        start: Starting index (inclusive)
        end: Ending index (exclusive)
    
    Returns:
        Text with specified range removed
    
    Examples:
        delete_range("hello world", 5, 11) -> "hello"
        delete_range("test123", 4, 7) -> "test"
    """
    return text[:start] + text[end:]


@mcp.tool()
def replace_range(text: str, start: int, end: int, replacement: str) -> str:
    """
    Replace characters in a range [start, end) with new text.
    
    Use this to swap out exact portions, like replacing detected patterns
    or updating specific text regions by position.
    
    Args:
        text: Original text
        start: Starting index (inclusive)
        end: Ending index (exclusive)
        replacement: Text to replace with
    
    Returns:
        Modified text
    
    Examples:
        replace_range("hello world", 6, 11, "Python") -> "hello Python"
        replace_range("test", 0, 4, "best") -> "best"
    """
    return text[:start] + replacement + text[end:]


# ========================================
# 4. Utilities (3)
# ========================================

@mcp.tool()
def find_regex_matches(text: str, pattern: str) -> list[dict]:
    """
    Find all regex pattern matches with their exact positions.
    
    Use this for complex pattern matching where you need both the matched
    text and its location, like finding all numbers, emails, or tags.
    
    Args:
        text: Text to search in
        pattern: Regular expression pattern
    
    Returns:
        List of matches: [{"start": int, "end": int, "match": str}, ...]
        Empty list if no matches found
    
    Examples:
        find_regex_matches("test123abc456", r"\\d+")
        -> [
            {"start": 4, "end": 7, "match": "123"},
            {"start": 10, "end": 13, "match": "456"}
        ]
        
        find_regex_matches("hello@test.com", r"\\S+@\\S+")
        -> [{"start": 0, "end": 14, "match": "hello@test.com"}]
    """
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
    text: str, 
    start_marker: str, 
    end_marker: str, 
    occurrence: int = 1
) -> dict:
    """
    Extract content between two marker strings with position info.
    
    Use this to extract content wrapped by tags, brackets, or delimiters,
    getting both the content and where it's located.
    
    Args:
        text: Text to search in
        start_marker: Opening marker
        end_marker: Closing marker
        occurrence: Which occurrence to extract (1-based, default: 1)
    
    Returns:
        {
            "content": str or None,       # extracted content
            "content_start": int or None, # start of content (after start_marker)
            "content_end": int or None,   # end of content (before end_marker)
            "full_start": int or None,    # start of start_marker
            "full_end": int or None       # end of end_marker
        }
    
    Examples:
        extract_between_markers("test[content]end", "[", "]", 1)
        -> {
            "content": "content",
            "content_start": 5,
            "content_end": 12,
            "full_start": 4,
            "full_end": 13
        }
        
        extract_between_markers("<p>Hello</p>", "<p>", "</p>", 1)
        -> {
            "content": "Hello",
            "content_start": 3,
            "content_end": 8,
            "full_start": 0,
            "full_end": 12
        }
    """
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
def count_chars(text: str) -> dict:
    """
    Count detailed character statistics.
    
    Use this when you need to verify exact string lengths, character
    composition, or validate text constraints.
    
    Args:
        text: Text to analyze
    
    Returns:
        {
            "total": int,           # total characters
            "without_spaces": int,  # excluding all whitespace
            "letters": int,         # alphabetic characters
            "digits": int,          # numeric characters
            "spaces": int,          # space characters
            "special": int          # non-alphanumeric, non-space
        }
    
    Examples:
        count_chars("Hello World!")
        -> {
            "total": 12,
            "without_spaces": 11,
            "letters": 10,
            "digits": 0,
            "spaces": 1,
            "special": 1
        }
    """
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
def extract_substrings(text: str, ranges: list[dict]) -> list[dict]:
    """
    Extract one or more substrings by exact index ranges.
    
    This is the unified tool for all extraction needs - from getting a single
    character to batch-extracting multiple ranges. Supports negative indices.
    
    Use cases:
    - Single character extraction: [{"start": 5, "end": 6}]
    - Single range: [{"start": 0, "end": 5}]
    - Multiple ranges: [{"start": 0, "end": 5}, {"start": 6, "end": 11}]
    - From index to end: [{"start": 6}] (omit "end")
    
    Args:
        text: Text to extract from
        ranges: List of ranges, each with "start" (required) and "end" (optional)
                Negative indices count from end: -1 = last char
    
    Returns:
        List of extractions: [
            {
                "start": int,        # normalized start index
                "end": int,          # normalized end index
                "substring": str,    # extracted text
                "length": int        # length of substring
            },
            ...
        ]
    
    Examples:
        # Single character (replaces get_char_at)
        extract_substrings("hello", [{"start": 1, "end": 2}])
        -> [{"start": 1, "end": 2, "substring": "e", "length": 1}]
        
        # Single range (replaces slice_by_index)
        extract_substrings("hello world", [{"start": 0, "end": 5}])
        -> [{"start": 0, "end": 5, "substring": "hello", "length": 5}]
        
        # Batch extraction
        extract_substrings("hello world", [
            {"start": 0, "end": 5},
            {"start": 6, "end": 11}
        ])
        -> [
            {"start": 0, "end": 5, "substring": "hello", "length": 5},
            {"start": 6, "end": 11, "substring": "world", "length": 5}
        ]
        
        # Negative indices
        extract_substrings("hello", [{"start": -3, "end": -1}])
        -> [{"start": 2, "end": 4, "substring": "ll", "length": 2}]
        
        # From index to end
        extract_substrings("hello world", [{"start": 6}])
        -> [{"start": 6, "end": 11, "substring": "world", "length": 5}]
    """
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


if __name__ == "__main__":
    mcp.run()