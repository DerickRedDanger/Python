"""
unittest Module - Unit Testing Framework

Introduction:
The 'unittest' module is a built-in Python library for testing small units of code, typically individual functions or classes, in isolation.

Installation:
The unittest module is part of the Python standard library, so no installation is required.

Basic Usage:
"""

import unittest

class TestSum(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6)

    def test_sum_tuple(self):
        self.assertEqual(sum((1, 2, 2)), 5)

if __name__ == '__main__':
    unittest.main()

"""
Advanced Usage:
"""

# 1. Using setUp and tearDown methods for reusable test fixtures
class TestMathOperations(unittest.TestCase):
    def setUp(self):
        self.numbers = [1, 2, 3, 4]

    def tearDown(self):
        self.numbers = []

    def test_sum(self):
        self.assertEqual(sum(self.numbers), 10)

if __name__ == '__main__':
    unittest.main()

"""
Real-World Example:
"""
# Test-driven development (TDD)
# Writing tests before implementing the function can help prevent bugs early in development.
