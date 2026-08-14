from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass
class Node:
    value: Any
    next: Node | None = None


class LinkedList:
    def __init__(self) -> None:
        self.head: Node | None = None
        self.tail: Node | None = None
        self.size: int = 0

    def __len__(self) -> int:
        return self.size

    def __bool__(self) -> bool:
        return 0 < self.size

    def __contains__(self, item: Any) -> bool:
        current = self.head

        while current is not None:
            if current.value == item:
                return True

            current = current.next

        return False

    def __str__(self) -> str:
        values = []
        current = self.head

        if current is None:
            return 'None'

        while current is not None:
            values.append(str(current.value))
            current = current.next

        values.append('None')
        return ' -> '.join(values)

    def __getitem__(self, index: int) -> Any:
        return self.get(index)

    def __iter__(self):
        current = self.head

        while current is not None:
            yield current.value
            current = current.next

    def _check_index(self, index: int) -> None:
        if index < 0 or index >= self.size:
            raise IndexError('Index out of range')

    def _previous(self, index: int) -> Node | None:
        self._check_index(index)

        counter = 0
        current = self.head

        while counter < index:
            current = current.next
            counter += 1

        return current

    def append(self, value: Any) -> None:
        new_node = Node(value)

        if self.head is None:
            self.head = new_node
            self.tail = new_node

        else:
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1

    def prepend(self, value: Any) -> None:
        new_head = Node(value)

        if self.head is None:
            self.head = new_head
            self.tail = new_head

        else:
            new_head.next = self.head
            self.head = new_head

        self.size += 1

    def get(self, index: int) -> Any:
        self._check_index(index)

        counter = 0
        current = self.head

        while counter < index:
            current = current.next
            counter += 1

        return current.value

    def remove(self, index: int) -> Any:
        self._check_index(index)

        current = self.head
        previous = None
        counter = 0

        if index == 0:
            removed_value = current.value
            self.head = self.head.next

            if self.size == 1:
                self.tail = None

            self.size -= 1
            return removed_value
        elif index == self.size - 1:
            removed_value = self.tail.value
            self.tail = self._previous(self.size-2)
            self.tail.next = None
            self.size -= 1
            return removed_value
        else:
            while counter < index:
                previous = current
                current = current.next
                counter += 1

            previous.next = current.next
            removed_value = current.value
            current.next = None
            self.size -= 1
            return removed_value

    def reverse(self) -> None:
        self.tail = self.head
        
        current = self.head
        previous = self._previous(0)

        while current is not None:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node

        self.head = previous


def main():
    LL = LinkedList()

    LL.prepend(5.5)
    LL.append(10)
    LL.append('Hello')
    LL.append(True)
    removed = LL.remove(0)

    for i in LL:
        print(type(i))

if __name__ == "__main__":
    main()