from typing import Any, Iterator, overload
from DataStructures.LinkedList.Linked_list import LinkedList
from DataStructures.Heaps.heap import Heap
from typing import Generic, TypeVar

T = TypeVar("T")


class Queue:
    def __init__(self) -> None:
        self.data = LinkedList()

    def __len__(self) -> int:
        return len(self.data)

    def __str__(self) -> str:
        return 'Front -> ' + ' -> '.join([str(i) for i in self.data]) + ' <- Rear'

    def __iter__(self):
        yield from self.data.__iter__()

    def enqueue(self, value: Any) -> None:
        self.data.append(value)

    def dequeue(self) -> Any:
        return self.data.remove(0)

    def peek(self) -> Any:
        return self.data[0]

    @property
    def is_empty(self) -> bool:
        return len(self.data) == 0


class PriorityQueue(Generic[T]):
    def __init__(self, heap: Heap[T]) -> None:
        self._heap: Heap[T] = heap

    def __repr__(self) -> str:
        return f"{type(self).__name__}({list(self)})"

    def __len__(self) -> int:
        return len(self._heap)

    def __bool__(self) -> bool:
        return bool(self._heap)

    def __contains__(self, item: T) -> bool:
        return item in self._heap

    def __iter__(self) -> Iterator[T]:
        temp_heap = type(self._heap)()
        temp_heap.heapify(self._heap)

        while temp_heap:
            yield temp_heap.remove()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PriorityQueue):
            return False

        if type(self._heap) is not type(other._heap):
            return False

        return list(self) == list(other)

    def __reversed__(self) -> Iterator[T]:
        return reversed(list(self))

    @overload
    def __getitem__(self, index: int) -> T:
        ...

    @overload
    def __getitem__(self, index: slice) -> list[T]:
        ...

    def __getitem__(self, index: int | slice) -> T | list[T]:
        if isinstance(index, slice):
            return list(self)[index]

        return list(self)[index]

    def enqueue(self, value: T) -> None:
        self._heap.insert(value)

    def dequeue(self) -> T:
        return self._heap.remove()

    def peek(self) -> T:
        return self._heap.peek()

    def clear(self) -> None:
        self._heap.clear()

    def copy(self) -> PriorityQueue[T]:
        new_heap = type(self._heap)()
        new_heap.heapify(self._heap)

        return PriorityQueue(new_heap)

