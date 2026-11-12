import unittest

from palindrome import is_palindrome


class IsPalindromeTest(unittest.TestCase):
    def test_strings_true(self):
        for s in ["racecar", "Level", "A man, a plan, a canal: Panama"]:
            self.assertIs(is_palindrome(s), True)

    def test_strings_false(self):
        self.assertIs(is_palindrome("hello"), False)

    def test_empty_and_symbols(self):
        self.assertIs(is_palindrome(""), True)
        self.assertIs(is_palindrome("!?  "), True)

    def test_ints_true(self):
        for n in [121, 7, 0]:
            self.assertIs(is_palindrome(n), True)

    def test_ints_false(self):
        for n in [123, 10]:
            self.assertIs(is_palindrome(n), False)

    def test_negative_int(self):
        self.assertIs(is_palindrome(-121), False)

    def test_bad_types(self):
        for v in [12.21, None, [1, 2, 1], True, False]:
            with self.assertRaises(TypeError) as ctx:
                is_palindrome(v)
            self.assertTrue(str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
