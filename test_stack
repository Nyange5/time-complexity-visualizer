import unittest
from stack import Stack


class TestStack(unittest.TestCase):
    def test_new_stack_is_empty(self):
        s = Stack()
        self.assertTrue(s.is_empty())
        self.assertEqual(len(s), 0)

    def test_push_adds_item(self):
        s = Stack()
        s.push(1)
        self.assertFalse(s.is_empty())
        self.assertEqual(len(s), 1)

    def test_pop_returns_last_pushed_item(self):
        s = Stack()
        s.push(1)
        s.push(2)
        s.push(3)
        self.assertEqual(s.pop(), 3)
        self.assertEqual(s.pop(), 2)
        self.assertEqual(s.pop(), 1)

    def test_pop_removes_item(self):
        s = Stack()
        s.push(1)
        s.pop()
        self.assertTrue(s.is_empty())

    def test_pop_empty_raises(self):
        s = Stack()
        with self.assertRaises(IndexError):
            s.pop()

    def test_peek_returns_last_item_without_removing(self):
        s = Stack()
        s.push(1)
        s.push(2)
        self.assertEqual(s.peek(), 2)
        self.assertEqual(len(s), 2)

    def test_peek_empty_raises(self):
        s = Stack()
        with self.assertRaises(IndexError):
            s.peek()

    def test_len_tracks_pushes_and_pops(self):
        s = Stack()
        for i in range(5):
            s.push(i)
        self.assertEqual(len(s), 5)
        s.pop()
        s.pop()
        self.assertEqual(len(s), 3)

    def test_contains(self):
        s = Stack()
        s.push("a")
        s.push("b")
        self.assertIn("a", s)
        self.assertNotIn("z", s)

    def test_lifo_order_with_mixed_operations(self):
        s = Stack()
        s.push(1)
        s.push(2)
        self.assertEqual(s.pop(), 2)
        s.push(3)
        s.push(4)
        self.assertEqual(s.pop(), 4)
        self.assertEqual(s.pop(), 3)
        self.assertEqual(s.pop(), 1)
        self.assertTrue(s.is_empty())

    def test_stress_many_elements(self):
        s = Stack()
        n = 10_000
        for i in range(n):
            s.push(i)
        self.assertEqual(len(s), n)
        for i in reversed(range(n)):
            self.assertEqual(s.pop(), i)
        self.assertTrue(s.is_empty())

    def test_repr_does_not_raise(self):
        s = Stack()
        s.push(1)
        self.assertIn("Stack", repr(s))


if __name__ == "__main__":
    unittest.main()
