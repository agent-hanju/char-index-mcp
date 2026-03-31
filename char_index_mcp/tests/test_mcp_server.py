"""
Tests for char-index-mcp.

- char_ops correctness (unit tests)
- MCP server wrapper (integration tests)
- char_ops.py sync between skill and MCP copies
"""

from pathlib import Path

import pytest

from char_index_mcp.char_ops import (
    count_chars,
    delete_range,
    extract_between_markers,
    extract_substrings,
    find_all_char_indices,
    find_all_substring_indices,
    find_nth_char,
    find_nth_substring,
    insert_at_index,
    replace_range,
    split_at_indices,
)
from char_index_mcp.server import mcp


# ========================================
# char_ops unit tests
# ========================================


class TestFindingOperations:
    """Test finding & locating operations."""

    def test_find_nth_char(self):
        assert find_nth_char("hello world", "l", 1) == 2
        assert find_nth_char("hello world", "l", 2) == 3
        assert find_nth_char("hello world", "l", 3) == 9
        assert find_nth_char("hello world", "o", 1) == 4
        assert find_nth_char("hello world", "o", 2) == 7
        assert find_nth_char("hello world", "x", 1) == -1

    def test_find_nth_char_edge_cases(self):
        assert find_nth_char("", "a", 1) == -1
        assert find_nth_char("hello", "h", 1) == 0
        assert find_nth_char("hello", "o", 1) == 4

        with pytest.raises(ValueError):
            find_nth_char("hello", "l", 0)
        with pytest.raises(ValueError):
            find_nth_char("hello", "ll", 1)

    def test_find_all_char_indices(self):
        assert find_all_char_indices("hello world", "l") == [2, 3, 9]
        assert find_all_char_indices("hello world", "o") == [4, 7]
        assert find_all_char_indices("hello world", "x") == []

    def test_find_nth_substring(self):
        assert find_nth_substring("hello hello world", "hello", 1) == 0
        assert find_nth_substring("hello hello world", "hello", 2) == 6
        assert find_nth_substring("hello hello world", "world", 1) == 12
        assert find_nth_substring("hello hello world", "foo", 1) == -1

    def test_find_nth_substring_overlapping(self):
        assert find_nth_substring("aaa", "aa", 1) == 0
        assert find_nth_substring("aaa", "aa", 2) == 1

    def test_find_all_substring_indices(self):
        assert find_all_substring_indices("hello hello world", "hello") == [0, 6]
        assert find_all_substring_indices("hello hello world", "world") == [12]
        assert find_all_substring_indices("hello hello world", "foo") == []
        assert find_all_substring_indices("aaa", "aa") == [0, 1]


class TestSplittingOperations:
    """Test splitting & extraction operations."""

    def test_split_at_indices(self):
        assert split_at_indices("hello world", [2, 5, 8]) == ["he", "llo", " wo", "rld"]
        assert split_at_indices("hello world", [5]) == ["hello", " world"]
        assert split_at_indices("hello world", []) == ["hello world"]

    def test_split_at_indices_edge_cases(self):
        assert split_at_indices("", []) == [""]
        assert split_at_indices("hello", [0, 5]) == ["", "hello", ""]
        assert split_at_indices("hello", [2, 2, 2]) == ["he", "llo"]
        assert split_at_indices("hello", [4, 2]) == ["he", "ll", "o"]

    def test_extract_between_markers(self):
        result = extract_between_markers("start[content]end", "[", "]", 1)
        assert result["content"] == "content"
        assert result["content_start"] == 6
        assert result["content_end"] == 13
        assert result["full_start"] == 5
        assert result["full_end"] == 14

    def test_extract_between_markers_multiple(self):
        text = "<thinking>first</thinking> <thinking>second</thinking>"
        assert extract_between_markers(text, "<thinking>", "</thinking>", 1)["content"] == "first"
        assert extract_between_markers(text, "<thinking>", "</thinking>", 2)["content"] == "second"

    def test_extract_between_markers_not_found(self):
        result = extract_between_markers("no markers", "[", "]", 1)
        assert result["content"] is None
        assert result["content_start"] is None

    def test_extract_substrings(self):
        result = extract_substrings("hello world", [{"start": 0, "end": 5}])
        assert len(result) == 1
        assert result[0]["substring"] == "hello"
        assert result[0]["start"] == 0
        assert result[0]["end"] == 5
        assert result[0]["length"] == 5

    def test_extract_substrings_multiple(self):
        result = extract_substrings("hello world", [
            {"start": 0, "end": 5},
            {"start": 6, "end": 11},
        ])
        assert len(result) == 2
        assert result[0]["substring"] == "hello"
        assert result[1]["substring"] == "world"

    def test_extract_substrings_negative_indices(self):
        result = extract_substrings("hello world", [{"start": -5}])
        assert result[0]["substring"] == "world"

        result = extract_substrings("hello world", [{"start": -5, "end": -1}])
        assert result[0]["substring"] == "worl"


class TestModificationOperations:
    """Test modification operations."""

    def test_insert_at_index(self):
        assert insert_at_index("hello world", 5, ",") == "hello, world"
        assert insert_at_index("hello", 0, "PREFIX_") == "PREFIX_hello"
        assert insert_at_index("hello", 5, "_SUFFIX") == "hello_SUFFIX"

    def test_insert_at_index_negative(self):
        assert insert_at_index("hello", -1, "X") == "helloX"
        assert insert_at_index("hello", -6, "X") == "Xhello"

    def test_delete_range(self):
        assert delete_range("hello world", 5, 11) == "hello"
        assert delete_range("hello world", 0, 5) == " world"
        assert delete_range("hello world", 5, 6) == "helloworld"

    def test_delete_range_edge_cases(self):
        assert delete_range("hello", 2, 2) == "hello"
        assert delete_range("hello", 0, 5) == ""

    def test_replace_range(self):
        assert replace_range("hello world", 6, 11, "Python") == "hello Python"
        assert replace_range("hello world", 0, 5, "Hi") == "Hi world"
        assert replace_range("hello world", 5, 6, ", ") == "hello, world"

    def test_replace_range_different_lengths(self):
        assert replace_range("hello world", 0, 5, "Hi") == "Hi world"
        assert replace_range("hello world", 0, 5, "Greetings") == "Greetings world"
        assert replace_range("hello world", 0, 5, "HELLO") == "HELLO world"


class TestUtilityOperations:
    """Test utility operations."""

    def test_count_chars(self):
        result = count_chars("hello world")
        assert result["total"] == 11
        assert result["without_spaces"] == 10
        assert result["letters"] == 10
        assert result["digits"] == 0
        assert result["spaces"] == 1
        assert result["special"] == 0

    def test_count_chars_mixed(self):
        result = count_chars("hello world 123")
        assert result["total"] == 15
        assert result["letters"] == 10
        assert result["digits"] == 3
        assert result["spaces"] == 2

    def test_count_chars_special(self):
        result = count_chars("Hello World!")
        assert result["total"] == 12
        assert result["letters"] == 10
        assert result["special"] == 1

    def test_count_chars_empty(self):
        result = count_chars("")
        assert result["total"] == 0
        assert result["letters"] == 0
        assert result["digits"] == 0


class TestUnicodeSupport:
    """Test Unicode support across all operations."""

    def test_unicode_finding(self):
        text = "Hello \u4e16\u754c"
        assert find_nth_char(text, "\u4e16", 1) == 6
        assert find_all_char_indices(text, "\u4e16") == [6]

    def test_unicode_extraction(self):
        text = "Hello \u4e16\u754c"
        result = extract_substrings(text, [{"start": 6, "end": 8}])
        assert result[0]["substring"] == "\u4e16\u754c"

    def test_unicode_counting(self):
        text = "Hello \u4e16\u754c \U0001f30d"
        result = count_chars(text)
        assert result["total"] == 10
        assert result["letters"] == 7

    def test_emoji_support(self):
        text = "Hello \U0001f30d"
        assert find_nth_char(text, "\U0001f30d", 1) == 6
        assert count_chars(text)["total"] == 7


class TestErrorHandling:
    """Test error handling."""

    def test_invalid_char_length(self):
        with pytest.raises(ValueError, match="single character"):
            find_nth_char("hello", "ll", 1)
        with pytest.raises(ValueError, match="single character"):
            find_all_char_indices("hello", "ll")

    def test_empty_substring(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            find_nth_substring("hello", "", 1)
        with pytest.raises(ValueError, match="cannot be empty"):
            find_all_substring_indices("hello", "")

    def test_invalid_n(self):
        with pytest.raises(ValueError, match="must be >= 1"):
            find_nth_char("hello", "l", 0)
        with pytest.raises(ValueError, match="must be >= 1"):
            find_nth_substring("hello", "ll", 0)

    def test_empty_markers(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            extract_between_markers("test", "", "]", 1)
        with pytest.raises(ValueError, match="cannot be empty"):
            extract_between_markers("test", "[", "", 1)


# ========================================
# MCP server integration tests
# ========================================


class TestMCPServer:
    """Test MCP server initialization and tool registration."""

    def test_mcp_server_exists(self):
        assert mcp is not None
        assert mcp.name == "char-index"

    def test_tools_registered(self):
        assert hasattr(mcp, '_tool_manager')


# ========================================
# char_ops.py sync test
# ========================================


class TestCharOpsSync:
    """Ensure skill and MCP copies of char_ops.py stay identical."""

    def test_char_ops_files_are_identical(self):
        root = Path(__file__).parent.parent.parent
        skill_copy = root / "skills" / "char-index-skill" / "scripts" / "char_ops.py"
        mcp_copy = root / "char_index_mcp" / "char_ops.py"

        assert skill_copy.read_bytes() == mcp_copy.read_bytes(), (
            "skills/char-index-skill/scripts/char_ops.py and char_index_mcp/char_ops.py have diverged. "
            "Update both files to keep them in sync."
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
