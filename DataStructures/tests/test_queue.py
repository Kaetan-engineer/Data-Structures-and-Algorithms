from DataStructures.Queue.Queue import PriorityQueue
from DataStructures.Heaps.heap import MinHeap, MaxHeap, Heap
import pytest


@pytest.mark.parametrize("heap_class, expected", [
    (MinHeap, (10, 10, 20)),
    (MaxHeap, (30, 30, 20))
])
def test_priority_queue_peek_insert_remove(heap_class: type[Heap[int]], expected: tuple[int, int, int]):
    min_queue = PriorityQueue(heap_class())

    min_queue.enqueue(30)
    min_queue.enqueue(20)
    min_queue.enqueue(10)

    assert min_queue.peek() == expected[0]
    assert min_queue.dequeue() == expected[1]
    assert min_queue.peek() == expected[2]


@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap])
def test_empty_priority_queue(heap_class: type[Heap[int]]):
    queue = PriorityQueue(heap_class())

    with pytest.raises(ValueError, match="Heap is empty"):
        queue.peek()

    with pytest.raises(ValueError, match="Heap is empty"):
        queue.dequeue()


@pytest.mark.parametrize("heap_class, expected", [
    (MinHeap, [10, 20, 30, 40]),
    (MaxHeap, [40, 30, 20, 10])
])
def test_iter_dunder(heap_class: type[Heap[int]], expected: list[int]):
    heap = PriorityQueue(heap_class())

    values = [20, 30, 10, 40]

    for v in values:
        heap.enqueue(v)

    temp_list = list(i for i in heap)

    assert temp_list == expected
    assert list(heap) == expected
    assert len(heap) == 4
    assert heap.peek() == expected[0]


@pytest.mark.parametrize("heap_class, values, expected", [
    (MinHeap, [], "PriorityQueue([])"),
    (MinHeap, [20, 5, 30, 10], "PriorityQueue([5, 10, 20, 30])"),
    (MaxHeap, [20, 5, 30, 10], "PriorityQueue([30, 20, 10, 5])"),
])
def test_priority_queue_repr(heap_class: type[Heap[int]], values: list[int], expected: str):
    queue = PriorityQueue(heap_class())

    for value in values:
        queue.enqueue(value)

    assert repr(queue) == expected


@pytest.mark.parametrize("heap_class1, values1, heap_class2, values2, expected", [
    (MinHeap, [], MinHeap, [], True),
    (MinHeap, [10, 20, 30], MinHeap, [30, 10, 20], True),
    (MinHeap, [10, 20, 30], MaxHeap, [10, 20, 30], False),
    (MinHeap, [10, 20, 30], MinHeap, [10, 20, 40], False),
])
def test_priority_queue_eq(heap_class1: type[Heap[int]], values1: list[int], heap_class2: type[Heap[int]], values2: list[int], expected: bool):
    queue1 = PriorityQueue(heap_class1())
    queue2 = PriorityQueue(heap_class2())

    for value in values1:
        queue1.enqueue(value)

    for value in values2:
        queue2.enqueue(value)

    assert (queue1 == queue2) is expected


def test_priority_queue_eq_with_non_priority_queue():
    queue = PriorityQueue(MinHeap())

    queue.enqueue(10)
    queue.enqueue(20)

    assert queue != [10, 20]


@pytest.mark.parametrize("heap_class, expected", [
    (MinHeap, [40, 30, 20, 10]),
    (MaxHeap, [10, 20, 30, 40]),
])
def test_reversed_dunder(heap_class: type[Heap[int]], expected: list[int],):
    queue = PriorityQueue(heap_class())

    values = [20, 30, 10, 40]

    for value in values:
        queue.enqueue(value)

    assert list(reversed(queue)) == expected

    assert len(queue) == 4
    assert queue.peek() == expected[-1]


@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap])
def test_priority_queue_clear(heap_class: type[Heap[int]]):
    queue = PriorityQueue(heap_class())

    for value in [20, 5, 30, 10]:
        queue.enqueue(value)

    assert len(queue) == 4
    assert queue

    queue.clear()

    assert len(queue) == 0
    assert not queue
    assert list(queue) == []


@pytest.mark.parametrize("heap_class, expected", [
    (MinHeap, [10, 20, 30, 40]),
    (MaxHeap, [40, 30, 20, 10]),
])
def test_priority_queue_getitem(heap_class: type[Heap[int]], expected: list[int]):
    queue = PriorityQueue(heap_class())

    for value in [20, 30, 10, 40]:
        queue.enqueue(value)

    assert queue[0] == expected[0]
    assert queue[1] == expected[1]
    assert queue[-1] == expected[-1]
    assert queue[1:3] == expected[1:3]


@pytest.mark.parametrize("heap_class, expected, new_expected", [
    (MinHeap, [10, 20, 30, 40], [10, 20, 30, 40, 50]),
    (MaxHeap, [40, 30, 20, 10], [50, 40, 30, 20, 10])
])
def test_priority_queue_copy(heap_class: type[Heap[int]], expected: list[int], new_expected: list[int]):
    heap = PriorityQueue(heap_class())
    copy1 = heap.copy()

    assert not copy1
    assert list(copy1) == []

    for i in [10, 20, 30, 40]:
        heap.enqueue(i)

    copy2 = heap.copy()

    assert list(copy2) == list(heap)
    assert list(heap) == expected

    copy2.enqueue(50)

    assert list(copy2) == new_expected
    assert list(heap) == expected


@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap])
def test_priority_queue_single_element(heap_class: type[Heap[int]]):
    queue = PriorityQueue(heap_class())

    queue.enqueue(42)

    assert len(queue) == 1
    assert queue.peek() == 42
    assert queue[0] == 42
    assert queue[-1] == 42
    assert list(queue) == [42]
    assert list(reversed(queue)) == [42]

    assert queue.dequeue() == 42
    assert not queue


@pytest.mark.parametrize("heap_class, expected", [
    (MinHeap, [10, 10, 20, 20, 30]),
    (MaxHeap, [30, 20, 20, 10, 10]),
])
def test_priority_queue_duplicates(heap_class: type[Heap[int]], expected: list[int]):
    queue = PriorityQueue(heap_class())

    for value in [20, 10, 20, 30, 10]:
        queue.enqueue(value)

    assert list(queue) == expected
    assert len(queue) == 5

    for value in expected:
        assert queue.dequeue() == value

    assert not queue


@pytest.mark.parametrize("heap_class, expected", [
    (MinHeap, [-10, -3, 0, 5, 20]),
    (MaxHeap, [20, 5, 0, -3, -10]),
])
def test_priority_queue_negative_values(heap_class: type[Heap[int]], expected: list[int]):
    queue = PriorityQueue(heap_class())

    for value in [0, -10, 20, -3, 5]:
        queue.enqueue(value)

    assert list(queue) == expected
    assert queue.peek() == expected[0]
    assert list(reversed(queue)) == expected[::-1]


@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap])
def test_priority_queue_empty_protocols(heap_class: type[Heap[int]]):
    queue = PriorityQueue(heap_class())

    assert len(queue) == 0
    assert not queue
    assert list(queue) == []
    assert list(reversed(queue)) == []
    assert repr(queue) == "PriorityQueue([])"

    with pytest.raises(IndexError):
        queue[0]


@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap])
def test_priority_queue_copy_is_independent(heap_class: type[Heap[int]]):
    queue = PriorityQueue(heap_class())

    for value in [10, 20, 30]:
        queue.enqueue(value)

    copy = queue.copy()

    copy.enqueue(40)

    assert list(queue) == [10, 20, 30] if heap_class is MinHeap else [30, 20, 10]
    assert len(queue) == 3
    assert len(copy) == 4


@pytest.mark.parametrize("heap_class, expected", [
    (MinHeap, [5, 10, 20]),
    (MaxHeap, [20, 10, 5]),
])
def test_priority_queue_clear_and_reuse(heap_class: type[Heap[int]], expected: list[int]):
    queue = PriorityQueue(heap_class())

    for value in [10, 20, 5]:
        queue.enqueue(value)

    queue.clear()

    assert not queue

    queue.enqueue(10)
    queue.enqueue(5)
    queue.enqueue(20)

    assert list(queue) == expected