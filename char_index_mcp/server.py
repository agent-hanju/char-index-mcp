"""
MCP Char-Index Server

Character-level string manipulation with precise index-based operations.
This MCP server wraps the implementation in char_index_mcp/char_ops.py.
"""

from typing import Annotated, Any

from mcp.server.fastmcp import FastMCP

from .char_ops import (
    count_chars as _count_chars,
    delete_range as _delete_range,
    extract_between_markers as _extract_between_markers,
    extract_substrings as _extract_substrings,
    find_all_char_indices as _find_all_char_indices,
    find_all_substring_indices as _find_all_substring_indices,
    find_nth_char as _find_nth_char,
    find_nth_substring as _find_nth_substring,
    insert_at_index as _insert_at_index,
    replace_range as _replace_range,
    split_at_indices as _split_at_indices,
)

mcp = FastMCP("char-index")


# ========================================
# MCP Tool Wrappers
# These wrap the Skills implementations with FastMCP decorators
# ========================================

@mcp.tool()
def find_nth_char(
    text: Annotated[str, "Text to search in"],
    char: Annotated[str, "Single character to find"],
    n: Annotated[int, "Which occurrence to find (1-based)"] = 1
) -> int:
    """Find index of nth occurrence of a character. Returns -1 if not found."""
    return _find_nth_char(text, char, n)


@mcp.tool()
def find_all_char_indices(
    text: Annotated[str, "Text to search in"],
    char: Annotated[str, "Single character to find"]
) -> list[int]:
    """Find all indices where a character appears. Returns empty list if not found."""
    return _find_all_char_indices(text, char)


@mcp.tool()
def find_nth_substring(
    text: Annotated[str, "Text to search in"],
    substring: Annotated[str, "Substring to find"],
    n: Annotated[int, "Which occurrence to find (1-based)"] = 1
) -> int:
    """Find starting index of nth occurrence of a substring. Returns -1 if not found."""
    return _find_nth_substring(text, substring, n)


@mcp.tool()
def find_all_substring_indices(
    text: Annotated[str, "Text to search in"],
    substring: Annotated[str, "Substring to find"]
) -> list[int]:
    """Find all starting indices where a substring appears (includes overlaps)."""
    return _find_all_substring_indices(text, substring)


@mcp.tool()
def split_at_indices(
    text: Annotated[str, "Text to split"],
    indices: Annotated[list[int], "Split positions (auto-sorted & deduplicated)"]
) -> list[str]:
    """Split text at exact index positions. Indices auto-sorted and deduplicated."""
    return _split_at_indices(text, indices)


@mcp.tool()
def insert_at_index(
    text: Annotated[str, "Original text"],
    index: Annotated[int, "Position to insert at (negative = from end)"],
    insertion: Annotated[str, "Text to insert"]
) -> str:
    """Insert text at index position without replacing. Supports negative indices."""
    return _insert_at_index(text, index, insertion)


@mcp.tool()
def delete_range(
    text: Annotated[str, "Original text"],
    start: Annotated[int, "Starting index (inclusive)"],
    end: Annotated[int, "Ending index (exclusive)"]
) -> str:
    """Delete characters in range [start, end)."""
    return _delete_range(text, start, end)


@mcp.tool()
def replace_range(
    text: Annotated[str, "Original text"],
    start: Annotated[int, "Starting index (inclusive)"],
    end: Annotated[int, "Ending index (exclusive)"],
    replacement: Annotated[str, "Text to replace with"]
) -> str:
    """Replace characters in range [start, end) with new text."""
    return _replace_range(text, start, end, replacement)


@mcp.tool()
def extract_between_markers(
    text: Annotated[str, "Text to search in"],
    start_marker: Annotated[str, "Opening marker"],
    end_marker: Annotated[str, "Closing marker"],
    occurrence: Annotated[int, "Which occurrence to extract (1-based)"] = 1
) -> dict[str, Any | None]:
    """Extract content between markers with positions. Returns dict with content and position info."""
    return _extract_between_markers(text, start_marker, end_marker, occurrence)


@mcp.tool()
def count_chars(
    text: Annotated[str, "Text to analyze"]
) -> dict[str, int]:
    """Count character statistics. Returns dict with total, without_spaces, letters, digits, spaces, special."""
    return _count_chars(text)


@mcp.tool()
def extract_substrings(
    text: Annotated[str, "Text to extract from"],
    ranges: Annotated[
        list[dict[str, Any]],
        "List of ranges with 'start' (required) and 'end' (optional). Negative indices supported",
    ],
) -> list[dict[str, Any]]:
    """Extract substrings by index ranges. Supports negative indices and omitting end."""
    return _extract_substrings(text, ranges)


def main() -> None:
    """Entry point for the char-index-mcp CLI."""
    mcp.run()


if __name__ == "__main__":
    main()
