#!/usr/bin/env python
# Example functional test case from //coreinfra-org/app-base-python
import unittest
import re

from modules.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add_numbers(self):
        """Test that adding two numbers returns the correct sum"""
        result = self.calc.add(3, 5)
        self.assertEqual(result, 8, "3 + 5 should equal 8")

    def test_divide_by_zero(self):
        """Test that dividing by zero raises ValueError with correct message"""
        # Using context manager to check exception
        with self.assertRaises(ValueError) as context:
            self.calc.divide(10, 0)

        self.assertTrue(
            re.search(".*divide by zero.*", str(context.exception)),
            f"Exception message '{str(context.exception)}' should contain 'divide by zero'")


if __name__ == '__main__':
    unittest.main()
