import unittest

from dlx import DLX

from numpy import array


class TestDLX(unittest.TestCase):

    def validate(self, correct, solutions, s):
        result = []
        for k in s:
            result.append(k.ID + 1)
        self.assertEqual(solutions, 1)
        self.assertEqual(correct, sorted(result))

    def test_problem_1(self):

        def callback(solutions, s):
            self.validate([1], solutions, s)

        problem = array([[1]])

        dlx = DLX.from_matrix(problem, callback)
        dlx.run(True)

    def test_problem_2(self):

        def callback(solutions, s):
            self.validate([1, 4, 5], solutions, s)

        problem = array([[0, 0, 1, 0, 1, 1, 0],
                         [1, 0, 0, 1, 0, 0, 1],
                         [0, 1, 1, 0, 0, 1, 0],
                         [1, 0, 0, 1, 0, 0, 0],
                         [0, 1, 0, 0, 0, 0, 1],
                         [0, 0, 0, 1, 1, 0, 1]])

        dlx = DLX.from_matrix(problem, callback)
        dlx.run(True)

    def test_problem_3(self):

        def callback(solutions, s):
            self.validate([2, 4, 6], solutions, s)

        problem = array([[1, 0, 0, 1, 0, 0, 1],
                         [1, 0, 0, 1, 0, 0, 0],
                         [0, 0, 0, 1, 0, 0, 1],
                         [0, 0, 1, 0, 1, 1, 0],
                         [0, 1, 1, 0, 0, 1, 1],
                         [0, 1, 0, 0, 0, 0, 1]])

        dlx = DLX.from_matrix(problem, callback)
        dlx.run(True)

    def test_no_solution(self):

        def callback(solutions, s):
            self.assertTrue(False)

        problem = array([[]])
        dlx = DLX.from_matrix(problem, callback)
        dlx.run(True)

        problem = array([[0]])
        dlx = DLX.from_matrix(problem, callback)
        dlx.run(True)

        problem = array([[0, 0],
                         [0, 0]])
        dlx = DLX.from_matrix(problem, callback)
        dlx.run(True)

        problem = array([[0, 1]])
        dlx = DLX.from_matrix(problem, callback)
        dlx.run(True)

        problem = array([[1, 0, 0],
                         [0, 0, 0],
                         [0, 0, 1]])
        dlx = DLX.from_matrix(problem, callback)
        dlx.run(True)
