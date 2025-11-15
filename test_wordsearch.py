import unittest
from word_search import WordSearch


class TestWordSearch(unittest.TestCase):

    def setUp(self):
        # 4×4 grid
        # a b c d
        # e f g h
        # i j k l
        # m n o p
        self.grid = "abcdefghijklmnop"
        self.ws = WordSearch(self.grid)

    # Horizontal tests
    def test_horizontal_full_row(self):
        self.assertTrue(self.ws.is_present("abcd"))
        self.assertTrue(self.ws.is_present("efgh"))
        self.assertTrue(self.ws.is_present("ijkl"))
        self.assertTrue(self.ws.is_present("mnop"))

    def test_horizontal_substrings(self):
        # substrings of length < 4 should NOT be valid words
        self.assertFalse(self.ws.is_present("abc"))
        self.assertFalse(self.ws.is_present("bcd"))

        # "bcde" would span from end of row1 into row2 → not contiguous in a row/column
        self.assertFalse(self.ws.is_present("bcde"))

    # Vertical tests
    def test_vertical_full_columns(self):
        self.assertTrue(self.ws.is_present("aeim"))
        self.assertTrue(self.ws.is_present("bfjn"))
        self.assertTrue(self.ws.is_present("cgko"))
        self.assertTrue(self.ws.is_present("dhlp"))

    # Negative tests
    def test_non_existent(self):
        self.assertFalse(self.ws.is_present("zzzz"))
        self.assertFalse(self.ws.is_present("mnopq"))  # too long
        self.assertFalse(self.ws.is_present("aceg"))   # diagonal


    # Boundary conditions
    def test_minimum_valid_length(self):
        # Only length >= 4 are marked as endpoints in Trie
        self.assertFalse(self.ws.is_present("abc"))
        self.assertTrue(self.ws.is_present("abcd"))

    def test_maximum_length_limit(self):
        # Whole flattened grid is not a single row/column string
        self.assertFalse(self.ws.is_present("abcdefghijklmnop"))
        self.assertFalse(self.ws.is_present("abcdefghijklmno"))


    # Grid validation
    def test_invalid_grid_raises(self):
        with self.assertRaises(ValueError):
            WordSearch("notaperfectsquare")

    # Overlapping substrings
    def test_overlapping_substrings(self):
        # "bc" and "bcd" exist as paths but arent words (length < 4)
        self.assertFalse(self.ws.is_present("bc"))
        self.assertFalse(self.ws.is_present("bcd"))
        # "abcd" should be a valid word
        self.assertTrue(self.ws.is_present("abcd"))

    # Case sensitivity
    def test_case_sensitivity(self):
        # Implementation is case sensitive and grid is lowercase
        self.assertFalse(self.ws.is_present("ABCD"))
        self.assertTrue(self.ws.is_present("abcd"))


if __name__ == "__main__":
    unittest.main()
