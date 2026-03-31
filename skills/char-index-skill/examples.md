# Character-Level String Manipulation Examples

This document provides practical examples for common use cases.

## Example 1: Test Code Generation - Exact Length String

**Problem**: Generate a test string exactly 50 characters long

```bash
#!/bin/bash
# Generate candidate string
TEXT="The quick brown fox jumps over the lazy dog and continues running"

# Check length
STATS=$(python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py count --text "$TEXT")
echo $STATS
# {"total": 67, "without_spaces": 56, "letters": 51, ...}

# Extract exactly 50 characters
RESULT=$(python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py extract --text "$TEXT" --start 0 --end 50)
echo $RESULT
# {"substring": "The quick brown fox jumps over the lazy dog and ", "length": 50}
```

## Example 2: CSV Parsing at Fixed Positions

**Problem**: Parse fixed-width CSV with columns at positions 10, 20, 30

```bash
#!/bin/bash
DATA="John      Smith     42        Engineer  "

# Split at exact column boundaries
RESULT=$(python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py split-at \
  --text "$DATA" \
  --indices "10,20,30")

echo $RESULT | jq -r '.parts[]'
# John
# Smith
# 42
# Engineer

# Extract and trim specific fields
FIRST_NAME=$(echo $RESULT | jq -r '.parts[0]' | xargs)
LAST_NAME=$(echo $RESULT | jq -r '.parts[1]' | xargs)
AGE=$(echo $RESULT | jq -r '.parts[2]' | xargs)
TITLE=$(echo $RESULT | jq -r '.parts[3]' | xargs)

echo "Name: $FIRST_NAME $LAST_NAME, Age: $AGE, Title: $TITLE"
# Name: John Smith, Age: 42, Title: Engineer
```

## Example 3: Extract LLM Thinking Blocks

**Problem**: Extract the 2nd `<thinking>` block from LLM output

```bash
#!/bin/bash
TEXT="Response: <thinking>first thoughts</thinking> Some text here. <thinking>second thoughts</thinking> More text."

# Extract 2nd thinking block
RESULT=$(python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py extract-between \
  --text "$TEXT" \
  --start-marker "<thinking>" \
  --end-marker "</thinking>" \
  --occurrence 2)

echo $RESULT | jq -r '.content'
# second thoughts

# Get position info
echo $RESULT | jq -r '.content_start, .content_end'
# 76
# 91
```

## Example 4: Find and Replace Nth Occurrence

**Problem**: Replace the 3rd occurrence of "foo" with "REPLACED"

```bash
#!/bin/bash
TEXT="foo bar foo baz foo qux"

# Find position of 3rd "foo"
INDEX=$(python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py find-nth-substring \
  --text "$TEXT" \
  --substring "foo" \
  --n 3 | jq -r '.index')

echo "Found at index: $INDEX"
# 16

# Replace it
RESULT=$(python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py replace \
  --text "$TEXT" \
  --start $INDEX \
  --end $((INDEX + 3)) \
  --replacement "REPLACED")

echo $RESULT | jq -r '.result'
# foo bar foo baz REPLACED qux
```

## Example 5: Batch String Extraction

**Problem**: Extract multiple words at once from a sentence

```bash
#!/bin/bash
TEXT="The quick brown fox jumps over the lazy dog"

# Define ranges for words to extract: "The", "quick", "brown"
RANGES='[
  {"start": 0, "end": 3},
  {"start": 4, "end": 9},
  {"start": 10, "end": 15}
]'

RESULT=$(python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py extract-batch \
  --text "$TEXT" \
  --ranges "$RANGES")

echo $RESULT | jq -r '.results[] | .substring'
# The
# quick
# brown
```

## Example 6: Validate String Length in Tests

**Problem**: Verify that generated strings meet exact length requirements

```bash
#!/bin/bash
# Function to generate and validate test string
generate_test_string() {
  local required_length=$1
  local candidate="Lorem ipsum dolor sit amet consectetur adipiscing elit"

  # Extract exact length
  local extracted=$(python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py extract \
    --text "$candidate" \
    --start 0 \
    --end $required_length | jq -r '.substring')

  # Validate
  local stats=$(python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py count --text "$extracted")
  local actual=$(echo $stats | jq -r '.total')

  if [ "$actual" -eq "$required_length" ]; then
    echo "✓ Valid: '$extracted' (length: $actual)"
  else
    echo "✗ Invalid: expected $required_length, got $actual"
  fi
}

generate_test_string 20
# ✓ Valid: 'Lorem ipsum dolor si' (length: 20)
```

## Example 7: Insert Formatting Characters

**Problem**: Add commas to a number string every 3 digits

```bash
#!/bin/bash
TEXT="1000000"

# Insert comma at position 1 (from right = position 4 from left in "1000000")
RESULT1=$(python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py insert \
  --text "$TEXT" \
  --index 1 \
  --insertion ",")

# Continue inserting
RESULT2=$(python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py insert \
  --text "$(echo $RESULT1 | jq -r '.result')" \
  --index 5 \
  --insertion ",")

echo $RESULT2 | jq -r '.result'
# 1,000,000
```

## Example 8: Parse Log Timestamps

**Problem**: Extract timestamp from fixed-format log lines

```bash
#!/bin/bash
LOG="2024-01-15 14:30:45 INFO User logged in successfully"

# Extract date (positions 0-10)
DATE=$(python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py extract \
  --text "$LOG" \
  --start 0 \
  --end 10 | jq -r '.substring')

# Extract time (positions 11-19)
TIME=$(python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py extract \
  --text "$LOG" \
  --start 11 \
  --end 19 | jq -r '.substring')

# Extract level (positions 20-24)
LEVEL=$(python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py extract \
  --text "$LOG" \
  --start 20 \
  --end 24 | jq -r '.substring')

echo "Date: $DATE, Time: $TIME, Level: $LEVEL"
# Date: 2024-01-15, Time: 14:30:45, Level: INFO
```

## Example 9: Clean Up Extra Whitespace

**Problem**: Remove a range of whitespace characters

```bash
#!/bin/bash
TEXT="Hello     World"

# Find where multiple spaces start
FIRST_SPACE=$(python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py find-nth-char \
  --text "$TEXT" \
  --char " " \
  --n 1 | jq -r '.index')

# Find where they end (next non-space)
LAST_SPACE=$(python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py find-nth-char \
  --text "$TEXT" \
  --char "W" \
  --n 1 | jq -r '.index')

# Replace multiple spaces with single space
RESULT=$(python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py replace \
  --text "$TEXT" \
  --start $FIRST_SPACE \
  --end $LAST_SPACE \
  --replacement " ")

echo $RESULT | jq -r '.result'
# Hello World
```

## Example 10: Extract All Occurrences and Process

**Problem**: Find all positions of a character and process them

```bash
#!/bin/bash
TEXT="a-b-c-d-e"

# Find all hyphens
INDICES=$(python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py find-all-chars \
  --text "$TEXT" \
  --char "-")

echo "Found hyphens at:"
echo $INDICES | jq -r '.indices[]'
# 1
# 3
# 5
# 7

# Split at all hyphen positions
PARTS=$(python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py split-at \
  --text "$TEXT" \
  --indices "$(echo $INDICES | jq -r '.indices | join(",")')")

echo "Parts:"
echo $PARTS | jq -r '.parts[]'
# a
# -b
# -c
# -d
# -e
```

## Tips for Complex Operations

### Tip 1: Chain Operations with Variables

```bash
# Store intermediate results
INDEX=$(python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py find-nth-char --text "$TEXT" --char "x" --n 1 | jq -r '.index')
SUBSTRING=$(python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py extract --text "$TEXT" --start 0 --end $INDEX | jq -r '.substring')
FINAL=$(python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py insert --text "$SUBSTRING" --index 0 --insertion "PREFIX_" | jq -r '.result')
```

### Tip 2: Use jq for JSON Processing

```bash
# Extract specific fields
python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py count --text "hello" | jq -r '.total'

# Process arrays
python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py find-all-chars --text "hello" --char "l" | jq -r '.indices | length'
```

### Tip 3: Combine with Standard Unix Tools

```bash
# Read from file
TEXT=$(cat data.txt)
python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py count --text "$TEXT"

# Pipe to other commands
python ${CLAUDE_SKILL_DIR}/scripts/char_ops.py split-at --text "$TEXT" --indices "10,20" | jq -r '.parts[]' | while read part; do
  echo "Processing: $part"
done
```
