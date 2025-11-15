"""
Word Search Solution using a Trie Data Structure

This implementation is designed for large-scale word searching:

My key optimizations:
1. Trie construction during object initialization
2. All rows and columns are indexed in the Trie
3. Each query is O(m) where m is word length, not grid size
4. Memory trade-off: O(n²) space for O(m) query time

Time Complexity:
- Construction: O(n²) where n is grid dimension
- Query: O(m) where m is word length (between 4 and 20)
- Total: O(n² * m) as m is constant O(n^2)

"""

class TrieNode:
    """Node in the Trie structure for efficient string matching."""
    __slots__ = ['children', 'is_end']
    
    def __init__(self):
        self.children = {}
        self.is_end = False


class WordSearch:
    """
    Optimized word search using Trie for O(m) query time.
    
    The grid is preprocessed to build a Trie containing all possible
    horizontal and vertical strings. String matching is then constant
    relative tosize of the grid.
    """
    
    def __init__(self, grid: str):
        self.grid = grid
        self.size = int(len(grid) ** 0.5)
        
        # Need to make sure its a perfect square grid
        if self.size * self.size != len(grid):
            raise ValueError("Grid must be a perfect square")
        
        # Build Trie containing all rows and columns
        self.trie_root = TrieNode()
        self._build_trie()
    
    def _build_trie(self):
        """
        Build Trie from all horizontal rows and vertical columns.
        
        Time complexity: O(n²) where n is grid dimension
        Space complexity: O(n² * alphabet_size) worst case, 
                         but on average will be less due to shared prefixes
        """
        # horizontal rows
        for row_idx in range(self.size):
            start = row_idx * self.size
            end = start + self.size
            row_string = self.grid[start:end]
            self._insert_string(row_string)
        
        # vertical columns 
        for col_idx in range(self.size):
            column_string = self.grid[col_idx::self.size]
            self._insert_string(column_string)
    
    def _insert_string(self, s: str):
        """
        Add a string and all its substrings into the Trie.
        For a string of length n, this means you have to insert n(n+1)/2 substrings,
        but many of these string will share prefixes in the Trie.
        
        Arguements:
            s: String to insert (row or column from grid)
        """
        length = len(s)
        
        # Add substrings of length 4-20 
        for start_idx in range(length):
            node = self.trie_root
            for end_idx in range(start_idx, min(start_idx + 20, length)):
                char = s[end_idx]
                
                if char not in node.children:
                    node.children[char] = TrieNode()
                
                node = node.children[char]
                
                # Mark as valid word endpoint if length >= 4
                if end_idx - start_idx >= 3:
                    node.is_end = True
    
    def is_present(self, word: str) -> bool:
        """
        Check if word exists in the grid either horizontally or vertically
        
        Time complexity: O(m) where m is word length
        
        Arguments:
            word: Word to search for
            
        Returns:
            True if word is present, False otherwise
        """
        node = self.trie_root
        
        # Traverse the Trie
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end


# Example usage
if __name__ == "__main__":
    test_grid = "abcdefghijklmnop"  # 4x4 grid (16 chars)
    # Grid layout:
    # a b c d
    # e f g h
    # i j k l
    # m n o p
    
    ws = WordSearch(test_grid)
    
    # Some small tests (Horizontal)
    print(f"'abcd' present: {ws.is_present('abcd')}")  # True
    print(f"'efgh' present: {ws.is_present('efgh')}")  # True
    print(f"'bcde' present: {ws.is_present('bcde')}")  # False
    
    # Vertical words
    print(f"'aeim' present: {ws.is_present('aeim')}")  # True
    print(f"'bfjn' present: {ws.is_present('bfjn')}")  # True
    
    # Non existent
    print(f"'zzzz' present: {ws.is_present('zzzz')}")  # False
