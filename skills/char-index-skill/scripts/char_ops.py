#!/usr/bin/env python3
"""
Character-level string manipulation utilities for Claude Skills.

This script provides 12 operations for precise index-based string manipulation:
- Finding characters/substrings (4 ops)
- Splitting & extraction (4 ops)
- Modification (3 ops)
- Utilities (1 op)

All operations return JSON output for easy parsing.
"""

import argparse
import json
import sys
from typing import Any

# ========================================
# 1. Finding & Locating (4 operations)
# ========================================

def find_nth_char(text: str, char: str, n: int = 1) -> int:
    """Find index of nth occurrence of a character (1-based). Returns -1 if not found."""
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


def find_all_char_indices(text: str, char: str) -> list[int]:
    """Find all indices where a character appears. Returns empty list if not found."""
    if len(char) != 1:
        raise ValueError("char must be a single character")

    return [i for i, c in enumerate(text) if c == char]


def find_nth_substring(text: str, substring: str, n: int = 1) -> int:
    """Find starting index of nth occurrence of a substring (1-based). Returns -1 if not found."""
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


def find_all_substring_indices(text: str, substring: str) -> list[int]:
    """Find all starting indices where a substring appears (includes overlaps)."""
    if not substring:
        raise ValueError("substring cannot be empty")

    indices: list[int] = []
    start = 0

    while True:
        index = text.find(substring, start)
        if index == -1:
            break
        indices.append(index)
        start = index + 1

    return indices


# ========================================
# 2. Splitting & Extraction (4 operations)
# ========================================

def split_at_indices(text: str, indices: list[int]) -> list[str]:
    """Split text at exact index positions. Indices auto-sorted and deduplicated."""
    if not indices:
        return [text]

    # Sort and remove duplicates
    sorted_indices = sorted(set(indices))

    # Validate
    for idx in sorted_indices:
        if idx < 0 or idx > len(text):
            raise ValueError(f"Index {idx} out of bounds [0, {len(text)}]")

    result: list[str] = []
    start = 0

    for idx in sorted_indices:
        result.append(text[start:idx])
        start = idx

    result.append(text[start:])

    return result


def extract_substring(text: str, start: int, end: int | None = None) -> dict[str, Any]:
    """Extract substring by start and end positions. Supports negative indices."""
    text_len = len(text)

    # Handle negative indices
    if start < 0:
        start = max(0, text_len + start)
    if end is not None and end < 0:
        end = max(0, text_len + end)

    # Extract
    substring = text[start:end]
    actual_end = end if end is not None else text_len

    return {
        "start": start,
        "end": actual_end,
        "substring": substring,
        "length": len(substring)
    }


def extract_between_markers(
    text: str,
    start_marker: str,
    end_marker: str,
    occurrence: int = 1
) -> dict[str, Any | None]:
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


def extract_substrings(text: str, ranges: list[dict[str, int]]) -> list[dict[str, Any]]:
    """Extract multiple substrings by index ranges. Supports negative indices."""
    results: list[dict[str, Any]] = []
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


# ========================================
# 3. Modification (3 operations)
# ========================================

def insert_at_index(text: str, index: int, insertion: str) -> str:
    """Insert text at index position without replacing. Supports negative indices."""
    if index < 0:
        index = max(0, len(text) + index + 1)

    return text[:index] + insertion + text[index:]


def delete_range(text: str, start: int, end: int) -> str:
    """Delete characters in range [start, end)."""
    return text[:start] + text[end:]


def replace_range(text: str, start: int, end: int, replacement: str) -> str:
    """Replace characters in range [start, end) with new text."""
    return text[:start] + replacement + text[end:]


# ========================================
# 4. Utilities (1 operation)
# ========================================

def count_chars(text: str) -> dict[str, int]:
    """Count character statistics. Returns dict with detailed counts."""
    return {
        "total": len(text),
        "without_spaces": len(text.replace(" ", "")),
        "letters": sum(1 for c in text if c.isalpha()),
        "digits": sum(1 for c in text if c.isdigit()),
        "spaces": sum(1 for c in text if c.isspace()),
        "special": sum(1 for c in text if not c.isalnum() and not c.isspace())
    }


# ========================================
# CLI Interface
# ========================================

def main() -> None:
    """Main CLI entry point with subcommands for each operation."""
    parser = argparse.ArgumentParser(
        description="Character-level string manipulation utilities",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Operation to perform")

    # === Finding & Locating ===

    # find-nth-char
    p = subparsers.add_parser("find-nth-char", help="Find nth occurrence of a character")
    p.add_argument("--text", required=True, help="Text to search in")
    p.add_argument("--char", required=True, help="Single character to find")
    p.add_argument("--n", type=int, default=1, help="Which occurrence to find (1-based)")

    # find-all-chars
    p = subparsers.add_parser("find-all-chars", help="Find all indices of a character")
    p.add_argument("--text", required=True, help="Text to search in")
    p.add_argument("--char", required=True, help="Single character to find")

    # find-nth-substring
    p = subparsers.add_parser("find-nth-substring", help="Find nth occurrence of a substring")
    p.add_argument("--text", required=True, help="Text to search in")
    p.add_argument("--substring", required=True, help="Substring to find")
    p.add_argument("--n", type=int, default=1, help="Which occurrence to find (1-based)")

    # find-all-substrings
    p = subparsers.add_parser("find-all-substrings", help="Find all indices of a substring")
    p.add_argument("--text", required=True, help="Text to search in")
    p.add_argument("--substring", required=True, help="Substring to find")

    # === Splitting & Extraction ===

    # split-at
    p = subparsers.add_parser("split-at", help="Split text at exact index positions")
    p.add_argument("--text", required=True, help="Text to split")
    p.add_argument("--indices", required=True, help="Comma-separated list of indices")

    # extract
    p = subparsers.add_parser("extract", help="Extract substring by range")
    p.add_argument("--text", required=True, help="Text to extract from")
    p.add_argument("--start", type=int, required=True, help="Starting index (inclusive)")
    p.add_argument("--end", type=int, help="Ending index (exclusive, optional)")

    # extract-between
    p = subparsers.add_parser("extract-between", help="Extract content between markers")
    p.add_argument("--text", required=True, help="Text to search in")
    p.add_argument("--start-marker", required=True, help="Opening marker")
    p.add_argument("--end-marker", required=True, help="Closing marker")
    p.add_argument("--occurrence", type=int, default=1, help="Which occurrence to extract (1-based)")

    # extract-batch
    p = subparsers.add_parser("extract-batch", help="Extract multiple substrings (batch)")
    p.add_argument("--text", required=True, help="Text to extract from")
    p.add_argument("--ranges", required=True, help="JSON array of ranges with start/end")

    # === Modification ===

    # insert
    p = subparsers.add_parser("insert", help="Insert text at index")
    p.add_argument("--text", required=True, help="Original text")
    p.add_argument("--index", type=int, required=True, help="Position to insert at")
    p.add_argument("--insertion", required=True, help="Text to insert")

    # delete
    p = subparsers.add_parser("delete", help="Delete range of characters")
    p.add_argument("--text", required=True, help="Original text")
    p.add_argument("--start", type=int, required=True, help="Starting index (inclusive)")
    p.add_argument("--end", type=int, required=True, help="Ending index (exclusive)")

    # replace
    p = subparsers.add_parser("replace", help="Replace range with new text")
    p.add_argument("--text", required=True, help="Original text")
    p.add_argument("--start", type=int, required=True, help="Starting index (inclusive)")
    p.add_argument("--end", type=int, required=True, help="Ending index (exclusive)")
    p.add_argument("--replacement", required=True, help="Text to replace with")

    # === Utilities ===

    # count
    p = subparsers.add_parser("count", help="Count character statistics")
    p.add_argument("--text", required=True, help="Text to analyze")

    # Parse arguments
    args = parser.parse_args()

    # Execute command
    try:
        result: Any = None

        if args.command == "find-nth-char":
            index = find_nth_char(args.text, args.char, args.n)
            result = {"index": index}

        elif args.command == "find-all-chars":
            indices = find_all_char_indices(args.text, args.char)
            result = {"indices": indices}

        elif args.command == "find-nth-substring":
            index = find_nth_substring(args.text, args.substring, args.n)
            result = {"index": index}

        elif args.command == "find-all-substrings":
            indices = find_all_substring_indices(args.text, args.substring)
            result = {"indices": indices}

        elif args.command == "split-at":
            indices = [int(x.strip()) for x in args.indices.split(",")]
            parts = split_at_indices(args.text, indices)
            result = {"parts": parts}

        elif args.command == "extract":
            result = extract_substring(args.text, args.start, args.end)

        elif args.command == "extract-between":
            result = extract_between_markers(
                args.text,
                args.start_marker,
                args.end_marker,
                args.occurrence
            )

        elif args.command == "extract-batch":
            ranges = json.loads(args.ranges)
            results = extract_substrings(args.text, ranges)
            result = {"results": results}

        elif args.command == "insert":
            text = insert_at_index(args.text, args.index, args.insertion)
            result = {"result": text}

        elif args.command == "delete":
            text = delete_range(args.text, args.start, args.end)
            result = {"result": text}

        elif args.command == "replace":
            text = replace_range(args.text, args.start, args.end, args.replacement)
            result = {"result": text}

        elif args.command == "count":
            result = count_chars(args.text)

        # Output JSON
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    except Exception as e:
        error = {"error": str(e), "type": type(e).__name__}
        print(json.dumps(error, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
