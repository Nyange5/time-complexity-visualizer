import unittest
from queue_ds import Queue, NaiveQueue

class QueueContractMixin:
    """Both Queue and NaiveQueue must satisfy the same FIFO contract."""

    queue_class = None

    def test_new_queue_is_empty(self):
        q = self.queue_class()
        self.assertTrue(q.is_empty())
        self.assertEqual(len(q), 0)

    def test_enqueue_adds_item(self):
        q = self.queue_class()
        q.enqueue(1)
        self.assertFalse(q.is_empty())
        self.assertEqual(len(q), 1)

    def test_dequeue_returns_first_enqueued_item(self):
        q = self.queue_class()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), 3)

    def test_dequeue_removes_item(self):
        q = self.queue_class()
        q.enqueue(1)
        q.dequeue()
        self.assertTrue(q.is_empty())

    def test_dequeue_empty_raises(self):
        q = self.queue_class()
        with self.assertRaises(IndexError):
            q.dequeue()

    def test_peek_returns_first_item_without_removing(self):
        q = self.queue_class()
        q.enqueue(1)
        q.enqueue(2)
        self.assertEqual(q.peek(), 1)
        self.assertEqual(len(q), 2)

    def test_peek_empty_raises(self):
        q = self.queue_class()
        with self.assertRaises(IndexError):
            q.peek()

    def test_len_tracks_enqueues_and_dequeues(self):
        q = self.queue_class()
        for i in range(5):
            q.enqueue(i)
        self.assertEqual(len(q), 5)
        q.dequeue()
        q.dequeue()
        self.assertEqual(len(q), 3)

    def test_contains(self):
        q = self.queue_class()
        q.enqueue("a")
        q.enqueue("b")
        self.assertIn("a", q)
        self.assertNotIn("z", q)

    def test_fifo_order_with_mixed_operations(self):
        q = self.queue_class()
        q.enqueue(1)
        q.enqueue(2)
        self.assertEqual(q.dequeue(), 1)
        q.enqueue(3)
        q.enqueue(4)
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), 3)
        self.assertEqual(q.dequeue(), 4)
        self.assertTrue(q.is_empty())

    def test_stress_many_elements(self):
        q = self.queue_class()
        n = 5_000
        for i in range(n):
            q.enqueue(i)
        self.assertEqual(len(q), n)
        for i in range(n):
            self.assertEqual(q.dequeue(), i)
        self.assertTrue(q.is_empty())


class TestQueue(QueueContractMixin, unittest.TestCase):
    queue_class = Queue

    def test_repr_does_not_raise(self):
        q = Queue()
        q.enqueue(1)
        self.assertIn("Queue", repr(q))


class TestNaiveQueue(QueueContractMixin, unittest.TestCase):
    queue_class = NaiveQueue

    def test_repr_does_not_raise(self):
        q = NaiveQueue()
        q.enqueue(1)
        self.assertIn("NaiveQueue", repr(q))


class TestQueueAndNaiveQueueAgree(unittest.TestCase):
    def test_same_sequence_of_operations_gives_same_results(self):
        q, nq = Queue(), NaiveQueue()
        for i in range(200):
            q.enqueue(i)
            nq.enqueue(i)
        results_q, results_nq = [], []
        while not q.is_empty():
            results_q.append(q.dequeue())
            results_nq.append(nq.dequeue())
        self.assertEqual(results_q, results_nq)


if __name__ == "__main__":
    unittest.main()
