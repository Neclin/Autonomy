from unittest import TestCase
from buildings.belt import Belt


class TestBelt(TestCase):
    def test_gen_points(self):
        self.assertEqual(Belt.genPoints((0,1), (0, 1), ()))
