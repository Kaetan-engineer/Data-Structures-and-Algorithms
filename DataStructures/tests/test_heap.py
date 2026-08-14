from DataStructures.Heaps.heap import Heap, MinHeap, MaxHeap
from typing import Callable, Iterable
import random
import pytest

def assert_valid_heap(heap: Heap[int]) -> None:
    for index in range(len(heap)):
        left = 2 * index + 1

        if left >= len(heap):
            continue

        right = 2 * index + 2

        if right >= len(heap):
            assert heap._comes_before(heap[index], heap[left]) or heap[index] == heap[left]
            continue

        assert heap._comes_before(heap[index], heap[left]) or heap[index] == heap[left]
        assert heap._comes_before(heap[index], heap[right]) or heap[index] == heap[right]


@pytest.mark.parametrize("heap_class, expected", [(MinHeap, 5), (MaxHeap, 35)])
def test_peek(heap_class: type[Heap[int]], expected: int):
    heap = heap_class()

    values = [20, 10, 30, 5, 15, 25, 35]

    for v in values:
        heap.insert(v)

    assert heap.peek() == expected


@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap])
def test_remove_empty_heap(heap_class: type[Heap[int]]):
    heap = heap_class()

    with pytest.raises(ValueError, match='Heap is empty'):
        heap.remove()


@pytest.mark.parametrize("heap_class, expected", [
    (MinHeap, (5, 10, 15, 20, 25, 30, 35)),
    (MaxHeap, (35, 30, 25, 20, 15, 10, 5))
])
def test_remove(heap_class: type[Heap[int]], expected: tuple[int, ...]):
    heap = heap_class()

    values = [20, 10, 30, 5, 15, 25, 35]

    for v in values:
        heap.insert(v)

    for value in expected:
        assert heap.remove() == value

    assert not bool(heap)


@pytest.mark.parametrize('heap_class', [MinHeap, MaxHeap])
def test_insert_duplicates(heap_class: type[Heap[int]]):
    heap = heap_class()
    values = [20, 20]

    for v in values:
        heap.insert(v)

    assert len(heap) == 2
    assert heap.peek() == 20

    for _ in range(len(heap)):
        assert heap.remove() == 20

    assert len(heap) == 0


@pytest.mark.parametrize('heap_class, remove_expected, peek_expected', [
        (MinHeap, (-20, -10, -5, 0, 5), -20),
        (MaxHeap, (5, 0, -5, -10, -20), 5)
    ])
def test_negative_numbers(heap_class: type[Heap[int]], remove_expected: tuple[int, ...], peek_expected: int):
    heap = heap_class()

    values = [-10, -5, -20, 0, 5]

    for v in values:
        heap.insert(v)

    assert len(heap) == 5
    assert heap.peek() == peek_expected

    for value in remove_expected:
        assert heap.remove() == value

    assert len(heap) == 0


@pytest.mark.parametrize("heap_class, expected", [
        (MinHeap, ('apple', 'banana', 'cherry', 'date')),
        (MaxHeap, ('date', 'cherry', 'banana', 'apple'))
    ])
def test_string_heap(heap_class: type[Heap[str]], expected: tuple[str, ...]):
    heap = heap_class()
    values = [
        "banana",
        "apple",
        "cherry",
        "date",
    ]

    for v in values:
        heap.insert(v)

    for value in expected:
        assert heap.remove() == value

    assert len(heap) == 0

@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap])
def test_heap_structure(heap_class: type[Heap[int]]):
    heap = heap_class()
    values = [5, 10, 20, 15, 30, 25, 35]

    for v in values:
        heap.insert(v)

    assert_valid_heap(heap)


@pytest.mark.parametrize("heap_class, operand", [
        (MinHeap, min),
        (MaxHeap, max)
    ])
def test_insert_remove_simulation(heap_class: type[Heap[int]], operand: Callable[[list[int]], int]):
    random.seed(42)

    heap = heap_class()
    reference = []

    for _ in range(100):
        choice = random.randint(0, 2)

        if choice == 0:
            value = random.randint(1, 100)

            heap.insert(value)
            reference.append(value)

        elif choice == 1:
            if heap:
                expected = operand(reference)
                assert heap.remove() == expected

                reference.remove(expected)
            else:
                with pytest.raises(ValueError, match='Heap is empty'):
                    heap.remove()

        else:
            replacement = random.randrange(1, 100)

            if not heap:
                with pytest.raises(ValueError, match='Heap is empty'):
                    heap.replace(replacement)
            else:
                expected = operand(reference)
                index = reference.index(expected)

                assert heap.replace(replacement) == expected
                reference[index] = replacement

        assert_valid_heap(heap)
        assert sorted(heap) == sorted(reference)


@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap])
def test_replace_empty_heap(heap_class: type[Heap[int]]):
    heap = heap_class()

    with pytest.raises(ValueError, match='Heap is empty'):
        heap.replace(20)


@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap])
def test_replace_single_value_heap(heap_class: type[Heap[int]]):
    heap = heap_class()
    heap.insert(20)

    assert heap.replace(50) == 20
    assert len(heap) == 1
    assert heap.peek() == 50


@pytest.mark.parametrize("heap_class, replacement, old_root,  new_root", [
    (MinHeap, 45, 10, 20),
    (MaxHeap, 10, 50, 40)
])
def test_replace_multiple_values_heap(heap_class: type[Heap[int]], replacement: int, old_root: int, new_root: int):
    heap = heap_class()

    values = [20, 10, 30, 50, 40]

    for v in values:
        heap.insert(v)

    assert heap.replace(replacement) == old_root
    assert heap.peek() == new_root
    assert_valid_heap(heap)


@pytest.mark.parametrize("heap_class, replacement, old_root", [(MinHeap, 15, 10), (MaxHeap, 25, 30)])
def test_no_movement_replace(heap_class: type[Heap[int]], replacement: int, old_root: int):
    heap = heap_class()

    values = [20, 10, 30]

    for v in values:
        heap.insert(v)

    assert heap.replace(replacement) == old_root
    assert heap.peek() == replacement
    assert_valid_heap(heap)


@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap])
def test_clear_method(heap_class: type[Heap[int]]):
    heap = heap_class()

    values = [40, 30, 10, 20]

    for v in values:
        heap.insert(v)

    heap.clear()

    assert len(heap) == 0
    assert not heap
    assert list(heap) == []

    heap.insert(25)

    assert heap.peek() == 25
    assert heap.remove() == 25


@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap])
def test_heapify_random_data(heap_class: type[Heap[int]]):
    random.seed(12)
    heap = heap_class()

    values = [random.randint(1, 100) for _ in range(20)]

    heap.heapify(values)

    assert_valid_heap(heap)
    assert sorted(heap) == sorted(values)


@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap])
def test_heapify_empty_iterable(heap_class: type[Heap[int]]):
    heap = heap_class()

    heap.heapify([])

    assert_valid_heap(heap)
    assert list(heap) == []
    assert len(heap) == 0


@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap])
def test_heapify_single_element(heap_class: type[Heap[int]]):
    heap = heap_class()

    heap.heapify([20])

    assert_valid_heap(heap)
    assert len(heap) == 1
    assert heap.peek() == 20
    assert heap.remove() == 20


@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap])
def test_heapify_duplicates(heap_class: type[Heap[int]]):
    heap = heap_class()

    heap.heapify([20, 20, 20])

    assert_valid_heap(heap)
    assert len(heap) == 3
    assert heap.peek() == 20
    assert heap.remove() == 20
    assert heap.remove() == 20
    assert heap.remove() == 20
    assert len(heap) == 0


@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap])
def test_heapify_replaces_existing_heap(heap_class: type[Heap[int]]):
    random.seed(10)
    heap = heap_class()

    for _ in range(10):
        heap.insert(random.randint(1, 20))

    values = [20, 40, 30, 50, 10]

    heap.heapify(values)

    assert_valid_heap(heap)
    assert len(heap) == 5
    assert sorted(heap) == sorted(values)


@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap])
def test_heapify_iter(heap_class: type[Heap[int]]):
    heap = heap_class()
    values = [20, 10, 30, 5, 15]

    heap.heapify(iter(values))

    assert_valid_heap(heap)
    assert sorted(heap) == sorted(values)


@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap])
def test_pushpop_empty_heap(heap_class: type[Heap[int]]):
    heap = heap_class()

    assert heap.push_pop(40) == 40
    assert not heap


@pytest.mark.parametrize("heap_class, heapify_values, value", [
    (MinHeap, [5, 20, 30, 40], 2),
    (MaxHeap, [25, 35, 40, 45], 50)
])
def test_pushpop_value_wins(heap_class: type[Heap[int]], heapify_values: list[int], value: int):
    heap = heap_class()

    heap.heapify(heapify_values)

    assert_valid_heap(heap)
    assert heap.push_pop(value) == value


@pytest.mark.parametrize("heap_class, heapify_values, push_pop_value, expected_return", [
    (MinHeap, {10, 20, 30, 40}, 15, 10),
    (MaxHeap, (40, 50, 60, 70), 55, 70)
])
def test_pushpop_root_wins(heap_class: type[Heap[int]], heapify_values: Iterable[int], push_pop_value: int, expected_return: int):
    heap = heap_class()

    heap.heapify(heapify_values)

    assert heap.push_pop(push_pop_value) == expected_return
    assert_valid_heap(heap)


@pytest.mark.parametrize("heap_class, heapify_values, push_pop_value, expected_return", [
    (MinHeap, [10, 20, 30], 10, 10),
    (MaxHeap, [40, 50, 60], 60, 60)
])
def test_pushpop_value_equals_root(heap_class: type[Heap[int]], heapify_values: Iterable[int], push_pop_value: int, expected_return: int):
    heap = heap_class()

    heap.heapify(heapify_values)

    assert heap.push_pop(push_pop_value) == expected_return
    assert_valid_heap(heap)


@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap])
def test_contains_dunder(heap_class: type[Heap[int]]):
    heap = heap_class()

    assert 20 not in heap

    values = [20, 20, 30]

    for v in values:
        heap.insert(v)

    assert 20 in heap
    assert 30 in heap
    assert 99 not in heap


@pytest.mark.parametrize("heap_class, expected", [
    (MinHeap, (10, 40, [30, 20, 40], [20, 40])),
    (MaxHeap, (40, 20, [30, 10, 20], [10, 20]))
])
def test_getitem_dunder(heap_class: type[Heap[int]], expected: tuple[int, int, list[int], list[int]]):
    heap = heap_class()

    values = [20, 30, 10, 40]

    for v in values:
        heap.insert(v)

    assert heap[0] == expected[0]
    assert heap[-1] == expected[1]
    assert heap[1:4] == expected[2]
    assert heap[2:] == expected[3]
    assert heap[:] == list(heap)

    with pytest.raises(IndexError):
        heap[100]


@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap])
def test_reversed_dunder(heap_class: type[Heap[int]]):
    heap = heap_class()

    assert list(reversed(heap)) == list(reversed(heap.heap))


@pytest.mark.parametrize("heap_class, expected", [
    (MinHeap, "MinHeap([])"),
    (MaxHeap, "MaxHeap([])")
])
def test_repr_empty_heap(heap_class: type[Heap[int]], expected: str):
    heap = heap_class()

    assert repr(heap) == expected


@pytest.mark.parametrize("heap_class, expected", [
        (MinHeap, "MinHeap([5, 10, 30, 20])"),
        (MaxHeap, "MaxHeap([30, 10, 20, 5])"),
    ])
def test_repr_populated(heap_class: type[Heap[int]], expected: str):
    heap = heap_class()
    heap.heapify([20, 5, 30, 10])

    assert repr(heap) == expected


@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap])
def test_eq_empty_heaps(heap_class: type[Heap[int]]):
    heap1 = heap_class()
    heap2 = heap_class()

    assert heap1 == heap2


@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap])
def test_eq_same_heaps(heap_class: type[Heap[int]]):
    heap1 = heap_class()
    heap2 = heap_class()

    values = [20, 10, 30, 5, 15]

    heap1.heapify(values)
    heap2.heapify(values)

    assert heap1 == heap2


@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap])
def test_eq_same_values_different_structure(heap_class: type[Heap[int]]):
    heap1 = heap_class()
    heap2 = heap_class()

    for value in [20, 10, 30, 5, 15]:
        heap1.insert(value)

    for value in [15, 5, 30, 10, 20]:
        heap2.insert(value)

    assert_valid_heap(heap1)
    assert_valid_heap(heap2)

    assert heap1 == heap2


@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap])
def test_eq_different_values(heap_class: type[Heap[int]]):
    heap1 = heap_class()
    heap2 = heap_class()

    heap1.heapify([10, 20, 30])
    heap2.heapify([10, 20, 40])

    assert heap1 != heap2


@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap])
def test_eq_different_values(heap_class: type[Heap[int]]):
    heap1 = heap_class()
    heap2 = heap_class()

    heap1.heapify([10, 20, 30])
    heap2.heapify([10, 20, 40])

    assert heap1 != heap2


def test_eq_min_heap_vs_max_heap():
    min_heap = MinHeap()
    max_heap = MaxHeap()

    values = [10, 20, 30]

    min_heap.heapify(values)
    max_heap.heapify(values)

    assert min_heap != max_heap


@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap])
def test_eq_duplicates(heap_class: type[Heap[int]]):
    heap1 = heap_class()
    heap2 = heap_class()

    heap1.heapify([10, 10, 20, 30])
    heap2.heapify([30, 10, 20, 10])

    assert heap1 == heap2


@pytest.mark.parametrize("heap_class", [MinHeap, MaxHeap])
def test_eq_different_duplicates(heap_class: type[Heap[int]]):
    heap1 = heap_class()
    heap2 = heap_class()

    heap1.heapify([10, 10, 20])
    heap2.heapify([10, 20, 20])

    assert heap1 != heap2


@pytest.mark.parametrize("other", [
    [10, 20, 30],
    (10, 20, 30),
    None,
    42,
    "heap",
])
def test_eq_other_objects(other: object):
    heap = MinHeap()
    heap.heapify([10, 20, 30])

    assert heap != other


@pytest.mark.parametrize("heap_class, expected_results", [
    (MinHeap, [[40, 30, 20, 10], 20, [20, 30]]),
    (MaxHeap, [[10, 30, 20, 40], 20, [20, 30]])
])
def test_all_builtin_operations(heap_class: type[Heap[int]], expected_results: tuple[list[int], int, list[int]]):
    heap = heap_class()

    heap.heapify([10, 20, 30, 40])

    assert sorted(list(heap)) == [10, 20, 30, 40]
    assert tuple(sorted(heap)) == (10, 20, 30, 40)
    assert list(reversed(heap)) == expected_results[0]
    assert 20 in heap
    assert heap[1] == expected_results[1]
    assert heap[1:3] == expected_results[2]
    assert len(heap) == 4
    assert bool(heap)
