# Optimized Word Search Solution

## Overview

This implementation solves word search problem using a Trie (prefix tree) data structure.

### The Problem
Given the massive scale (100M chars (10000x10000 grid), 1M queries),the naive approach wouldnt be efficient

Naive approach - (checking each word against each row/column):
- Time: O(queries × grid_size² × word_length)
- For the scale given in the example: 1M × 100M × 12 = 1.2 trillion operations

Trie approach :
- Construction: O(n²) where n = grid dimension
- Per-query: O(m) where m = word length
- Total: O(n² + queries × m)
- For our scale: 100M + (1M × 12) = 112M operations

## How It Works

### 1. Construction (`__init__`)

The Trie is built from all possible horizontal and vertical strings:

```python
# For a 4×4 grid:
# a b c d
# e f g h  
# i j k l
# m n o p

# Extract all rows (left to right):
# Row 0: "abcd"
# Row 1: "efgh"
# Row 2: "ijkl"
# Row 3: "mnop"

# Extract all columns (top to bottom):
# Col 0: "aeim"
# Col 1: "bfjn"
# Col 2: "cgko"
# Col 3: "dhlp"
```

For each row and column, we insert all substrings of length 4-20 into the Trie:
- "abcd" → inserts "abcd"
- "efgh" → inserts "efgh"
- "aeim" → inserts "aeim"

The Trie handles prefixes so if we have "test" and "testing", they share the prefix "test" and only change at "ing".

### 2. Querying (`is_present`)

Looking up a word is done like this:
1. Start at Trie root
2. Follow each character of the word through the tree
3. If path exists and reaches a valid point then the word is found
4. Otherwise it means the word is not present

This is O(m) where m is word length so it makes it independednt of the size of our grid


### Time Complexity

**Construction: O(n²)**
- Process n² grid cells
- Each row/column has n characters
- For each position, insert substrings (4-20 chars)
- Total: O(n² × substring_count) ≈ O(n²)

**Query: O(m)**
- m = word length (4-20 chars)
- Single traversal through Trie

**Total for problem: O(n² + Q×m)**
- n = 10,000 (grid dimension)
- Q = 1,000,000 (queries)
- m ≈ 12 (average word length)
- Calculation: 100M + 12M = 112M operations

### Space Complexity

**O(n² × k)** where k is average branching factor

- Worst case: Every substring is unique means the Trie will have to be bigger because it doesnt share many prefixes
- Typical case: Heavy prefix sharing reduces memory


## Multicore Optimization (Bonus Question)

While I haven't implemented it, here's how you could leverage multicore systems:

### 1. Parallel Trie Construction
To do this we could split rows and columns across worker processes, and each worker process builds a partial Trie, then merges them together


### 2. Parallel Query Batching
Another method would be to split querying with actual strings across multiple cores


**Expected speedup**: Almost a linear speedup with core count for queries maybe some ovreheads due to core communication when joining the trie back up.

### Challenges
- Trie merging may get complex as you have to overlap prefixes
- Python GIL doesnt allow for true parallelism so may need to use something like C++
- Memory duplication across processes


## Usage Example

```python
# Initialize with grid
grid = "abcdefghijklmnop"  # 4×4 grid
ws = WordSearch(grid)

# Query words
words_to_find = ["abcd", "efgh", "aeim", "test"]
for word in words_to_find:
    if ws.is_present(word):
        print(f"found {word}")

# Output:
# found abcd
# found efgh
# found aeim
```

## Testing

Run the test suite:
```bash
python3 word_search.py       # Basic functionality test
python3 test_wordsearch.py        # 9 Custom tests for valid, invalid and boundary data
```

## Trade-offs and Alternatives

### Hash Set
Hash set of all substrings would also give O(m) queries but:
- Similar construction time
- More memory would be used as it would store full strings, not shared prefixes
- No prefix based optimizations possible

### Suffix Array
Suffix arrays with binary search:
- Complex to implement correctly
- Still O(log n) query time vs O(m)
- Construction is similar O(n²log(n²))

