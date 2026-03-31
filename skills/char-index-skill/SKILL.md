---
name: char-index-skill
description: "Character-level string manipulation: find nth char/substring, split at indices, extract ranges, modify at positions. For test generation, parsing, position-critical tasks."
allowed-tools: Bash, Read, Grep
argument-hint: "<command> [options]"
---

# Char-Index String Manipulation

Precise index-based string operations. Use when you need exact character positioning for test generation, parsing, or LLM response extraction.

## 📦 Operations (11 tools)

All via `python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py <command> [options]`. Returns JSON.

### Finding (4)
- `find-nth-char`: Find nth occurrence of char → `{"index": N}`
- `find-all-chars`: All positions of char → `{"indices": [...]}`
- `find-nth-substring`: Find nth occurrence of substring → `{"index": N}`
- `find-all-substrings`: All positions of substring → `{"indices": [...]}`

### Splitting & Extraction (3)
- `split-at`: Split at indices → `{"parts": [...]}`
- `extract`: Substring by range → `{"substring": "...", "length": N}`
- `extract-between`: Content between markers → `{"content": "...", "content_start": N, ...}`
- `extract-batch`: Multiple ranges → `{"results": [{...}, ...]}`

### Modification (3)
- `insert`: Insert at index → `{"result": "..."}`
- `delete`: Delete range [start, end) → `{"result": "..."}`
- `replace`: Replace range with text → `{"result": "..."}`

### Utilities (1)
- `count`: Character statistics → `{"total": N, "letters": N, "digits": N, ...}`

## 🚀 Quick Reference

| Task | Command |
|------|---------|
| Find 3rd 'l' | `find-nth-char --text "hello world" --char "l" --n 3` |
| All 'l' positions | `find-all-chars --text "hello world" --char "l"` |
| Split at 2,5,8 | `split-at --text "hello world" --indices "2,5,8"` |
| Extract chars 0-5 | `extract --text "hello world" --start 0 --end 5` |
| Between markers | `extract-between --text "a[b]c" --start-marker "[" --end-marker "]"` |
| Insert comma | `insert --text "hello world" --index 5 --insertion ","` |
| Delete range | `delete --text "hello world" --start 5 --end 11` |
| Replace range | `replace --text "hello world" --start 6 --end 11 --replacement "Python"` |
| Count chars | `count --text "hello world"` |

## 💡 Usage Patterns

**Basic:**
```bash
python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py find-nth-char \
  --text "hello world" --char "l" --n 3
# {"index": 9}
```

**Chain with jq:**
```bash
INDEX=$(python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py find-nth-char \
  --text "$TEXT" --char "x" --n 1 | jq -r '.index')
```

**Batch operations:**
```bash
python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py extract-batch \
  --text "hello world" \
  --ranges '[{"start":0,"end":5},{"start":6,"end":11}]'
```

## ⚡ Key Points

- **0-indexed**: All positions start from 0
- **1-based occurrence**: `find-nth-*` uses `--n 1` for first occurrence
- **Negative indices**: `-1` = last char, `-5` = 5th from end
- **Returns -1**: When char/substring not found
- **Range format**: `[start, end)` - start inclusive, end exclusive
- **Unicode safe**: Each Unicode character = 1 position
- **Overlaps included**: `find-all-*` finds overlapping matches

## 📖 More Info

- Practical examples: [examples.md](examples.md)
- Command help: `python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py --help`
