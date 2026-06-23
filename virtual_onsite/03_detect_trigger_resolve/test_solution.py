import unittest
from solution import solution

class TestDetectTriggerResolve(unittest.TestCase):
    def test_sample_case_1(self):
        logs = [
            (1, 'm1', 500, 2),
            (2, 'm1', 500, 2),
            (5, 'm1', 500, 1),
            (6, 'm1', 500, 1)
        ]
        window_size = 3
        threshold = 4
        expected = [
            (2, 'm1', 500, 'TRIGGER'),
            (5, 'm1', 500, 'RESOLVE')
        ]
        self.assertEqual(solution(logs, window_size, threshold), expected)

    def test_sample_case_2(self):
        logs = [
            (1, 'A', 404, 2),
            (1, 'A', 404, 1),
            (2, 'B', 500, 3),
            (3, 'A', 404, 1),
            (4, 'B', 500, 1)
        ]
        window_size = 3
        threshold = 3
        expected = [
            (1, 'A', 404, 'TRIGGER'),
            (2, 'B', 500, 'TRIGGER')
        ]
        self.assertEqual(solution(logs, window_size, threshold), expected)

if __name__ == '__main__':
    unittest.main()
