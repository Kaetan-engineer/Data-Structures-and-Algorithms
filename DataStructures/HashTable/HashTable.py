from typing import Generic, TypeVar, Hashable, Iterator
from collections.abc import Mapping
from dataclasses import dataclass


K = TypeVar('K', bound=Hashable)
V = TypeVar('V')


@dataclass
class Entry(Generic[K, V]):
    key: K
    value: V


class HashTable(Generic[K, V]):
    def __init__(self, capacity: int = 8) -> None:
        if capacity <= 0:
            raise ValueError('Capacity must be greater than 0')

        self._buckets: list[list[Entry]] = [
            [] for _ in range(capacity)
        ]
        self._size: int = 0
        self._capacity = capacity

    def __repr__(self) -> str:
        return f"HashTable({dict(self.items())})"

    def __len__(self) -> int:
        return self._size

    def __contains__(self, item: K) -> bool:
        return self.contains(item)

    def __getitem__(self, key: K) -> V:
        return self.get(key)

    def __setitem__(self, key: K, value: V) -> None:
        self.set(key, value)

    def __delitem__(self, key: K) -> None:
        self.remove(key)

    def __iter__(self) -> Iterator[K]:
        for bucket in self._buckets:
            for entry in bucket:
                yield entry.key

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HashTable):
            return False

        if len(self) != len(other):
            return False

        for key, value in self.items():
            if key not in other or other[key] != value:
                return False

        return True

    def _index(self, key: K) -> int:
        return hash(key) % self._capacity

    def _load_factor(self) -> float:
        return self._size / self._capacity

    def _resize(self) -> None:
        old_buckets = self._buckets

        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]

        for bucket in old_buckets:
            for entry in bucket:
                index = self._index(entry.key)
                self._buckets[index].append(entry)

    def items(self) -> Iterator[tuple[K, V]]:
        for bucket in self._buckets:
            for entry in bucket:
                yield entry.key, entry.value

    def _values(self) -> Iterator[V]:
        for bucket in self._buckets:
            for entry in bucket:
                yield entry.value

    def set(self, key: K, value: V) -> None:
        index = self._index(key)

        for entry in self._buckets[index]:
            if entry.key == key:
                entry.value = value
                return

        if (self._size + 1) / self._capacity > 0.75:
            self._resize()
            index = self._index(key)

        self._buckets[index].append(Entry(key, value))
        self._size += 1

    def get(self, key: K) -> V:
        index = self._index(key)

        for entry in self._buckets[index]:
            if entry.key == key:
                return entry.value

        raise KeyError(key)

    def contains(self, key: K) -> bool:
        index = self._index(key)

        for entry in self._buckets[index]:
            if entry.key == key:
                return True

        return False

    def remove(self, key: K) -> V:
        index = self._index(key)

        for entry in self._buckets[index]:
            if entry.key == key:
                value = entry.value
                self._buckets[index].remove(entry)
                self._size -= 1

                return value

        raise KeyError(key)

    def clear(self) -> None:
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0

    def copy(self) -> HashTable[K, V]:
        table_copy = HashTable(capacity=self._capacity)

        for key, value in self.items():
            table_copy[key] = value

        return table_copy

    def pop(self, key: K) -> V:
        return self.remove(key)

    def popitem(self) -> tuple[K, V]:
        for bucket in self._buckets:
            if bucket:
                entry = bucket.pop()
                self._size -= 1
                return entry.key, entry.value

        raise KeyError("HashTable is empty")

    def update(self, other: Mapping[K, V]) -> None:
        for key, value in other.items():
            self[key] = value


