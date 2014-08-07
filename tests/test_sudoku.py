import unittest

from sudoku import Sudoku, SudokuError


class TestDLX(unittest.TestCase):

    def setUp(self):
        self.sudoku = Sudoku(validate=True, pretty=False)

    def read_line_by_line(self, filename, callback):
        lines = open(filename)
        for line in lines:
            self.assertEqual(len(line), 82)
            self.assertEqual(line[81], '\n')
            callback(line[:81])

    def assert_exception(self, line):
        self.assertRaises(SudokuError, self.sudoku.solve, line)

    def assert_valid(self, line):
        grids = self.sudoku.solve(line)
        self.assertEqual(len(grids), 1)

    def test_bad_solutions(self):
        filename = 'tests/data/collections/bad'
        self.read_line_by_line(filename, self.assert_exception)

    def test_valid_solutions(self):
        filename = 'tests/data/collections/hardest'
        self.read_line_by_line(filename, self.assert_valid)
