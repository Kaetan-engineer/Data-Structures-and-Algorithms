from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from typing import Generic, TypeVar, overload


T = TypeVar("T")


class Heap(ABC, Generic[T]):
    def __init__(self, iterable: Iterable[T] | None = None):
        self._heap: list[T] = []

        if iterable is not None:
            self.heapify(iterable)

    def __contains__(self, value: object) -> bool:
        return value in self._heap

    def __len__(self) -> int:
        return len(self._heap)

    def __bool__(self) -> bool:
        return bool(self._heap)

    def __iter__(self) -> Iterator[T]:
        return iter(self._heap)

    def __reversed__(self) -> Iterator[T]:
        return reversed(self._heap)

    @overload
    def __getitem__(self, index: int) -> T:
        ...

    @overload
    def __getitem__(self, index: slice) -> list[T]:
        ...

    def __getitem__(self, index: int | slice) -> T | list[T]:
        if isinstance(index, slice):
            return self._heap[index]

        return self._heap[index]

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self._heap!r})"

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return False

        other_heap = other

        return sorted(self._heap) == sorted(other_heap.heap)

    @abstractmethod
    def _comes_before(self, first: T, second: T) -> bool:
        """Return True if first has higher priority than second."""
        pass

    def _heapify_up(self, index: int) -> None:
        while index > 0:
            parent = (index - 1) // 2

            if not self._comes_before(self._heap[index], self._heap[parent]):
                break

            self._heap[index], self._heap[parent] = (
                self._heap[parent],
                self._heap[index],
            )

            index = parent

    def _heapify_down(self, index: int) -> None:
        size = len(self._heap)

        while True:
            left = 2 * index + 1
            right = 2 * index + 2
            best = index

            if (
                left < size
                and self._comes_before(self._heap[left], self._heap[best])
            ):
                best = left

            if (
                right < size
                and self._comes_before(self._heap[right], self._heap[best])
            ):
                best = right

            if best == index:
                break

            self._heap[index], self._heap[best] = (
                self._heap[best],
                self._heap[index],
            )

            index = best

    @property
    def heap(self) -> list[T]:
        return self._heap

    def insert(self, value: T) -> None:
        self._heap.append(value)
        self._heapify_up(len(self._heap) - 1)

    def remove(self) -> T:
        if not self._heap:
            raise ValueError("Heap is empty")

        if len(self._heap) == 1:
            return self._heap.pop()

        root = self._heap[0]
        self._heap[0] = self._heap.pop()
        self._heapify_down(0)

        return root

    def peek(self) -> T:
        if not self._heap:
            raise ValueError("Heap is empty")

        return self._heap[0]

    def replace(self, value: T) -> T:
        if not self._heap:
            raise ValueError("Heap is empty")

        old_root = self._heap[0]
        self._heap[0] = value

        if len(self._heap) > 1:
            self._heapify_down(0)

        return old_root

    def push_pop(self, value: T) -> T:
        if not self._heap:
            return value

        if self._comes_before(value, self._heap[0]):
            return value

        old_root = self._heap[0]
        self._heap[0] = value
        self._heapify_down(0)

        return old_root

    def heapify(self, iterable: Iterable[T]) -> None:
        self._heap = list(iterable)

        last_parent = len(self._heap) // 2 - 1

        for i in range(last_parent, -1, -1):
            self._heapify_down(i)

    def clear(self) -> None:
        self._heap = []



class MinHeap(Heap[T]):
    def _comes_before(self, first: T, second: T) -> bool:
        return first < second


class MaxHeap(Heap[T]):
    def _comes_before(self, first: T, second: T) -> bool:
        return first > second