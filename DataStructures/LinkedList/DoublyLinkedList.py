from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass
class Node:
    value: Any
    next: Node | None = None
    previous: Node | None = None

class DoublyLinkedList:
    def __init__(self) -> None:
        self.head: Node | None = None # The first node of the list
        self.tail: Node | None = None # The last node of the list
        self.size: int = 0 # The number of nodes in the list

    def __str__(self) -> str:
        values = []
        current = self.head

        if current is None:
            return 'None'

        while current is not None:
            values.append(str(current.value))
            current = current.next

        values.append('None')
        return ' ↔ '.join(values)

    def __contains__(self, item: Any) -> bool:
        current = self.head

        while current is not None:
            if current.value == item:
                return True
            current = current.next

        return False

    def __len__(self) -> int:
        return self.size

    def _check_midpoint(self, index: int) -> bool:
        """
        Checks for the midpoint of the given index
        :param index:
        :return bool:
        """
        return index < self.size // 2

    def _check_index(self, index: int) -> None:
        """
        Checks if the given index is valid
        :param index:
        :return:
        """
        if index < 0 or index >= self.size:
            raise IndexError('Index is out of range')

    def display_reverse(self):
        current = self.tail

        while current:
            print(current.value, end=" ↔ ")
            current = current.previous

        print("None")

    def append(self, value: Any) -> None:
        """
        Adds a node with the given value at the end of the DLL
        :param value:
        :return:
        """
        new_node = Node(value)

        if self.head is None:
            self.head = new_node
            self.tail = new_node

        else:
            self.tail.next = new_node
            new_node.previous = self.tail
            self.tail = new_node

        self.size += 1

    def prepend(self, value: Any) -> None:
        """
        Adds a node with the given value at the start of the DLL
        :param value:
        :return:
        """
        new_node = Node(value)

        if self.head is None:
            self.head = new_node
            self.tail = new_node

        else:
            new_node.next = self.head
            self.head.previous = new_node
            self.head = new_node

        self.size += 1

    def get(self, index: int) -> Any:
        """
        Returns the value of the node at the given index
        :param index:
        :return:
        """
        self._check_index(index)

         # Case 1: The midpoint is greater than the index
        if self._check_midpoint(index):
            current = self.head
            counter = 0

            while counter < index:
                current = current.next
                counter += 1

            return current.value

        # Case 1: The index is greater than the midpoint
        else:
            current = self.tail
            counter = self.size - 1

            while counter > index:
                current = current.previous
                counter -= 1

            return current.value

    def remove(self, index: int) -> Any:
        """
        Removes the node from the list at the given index and return its value
        :param index:
        :return:
        """
        self._check_index(index)
        current: Node | None = self.head

        # Case 1: The DLL only had one node left
        if self.size == 1:
            removed_value = self.head.value
            self.head = None
            self.tail = None

        # Case 2: The index is at the start of the list
        elif index == 0:
            removed_value = self.head.value
            self.head = self.head.next
            self.head.previous = None

        # Case 3: The index is as the end of the list
        elif index == self.size - 1:
            removed_value = self.tail.value
            self.tail = self.tail.previous
            self.tail.next = None

        # Case 4: The index is between the start and the end of the list
        else:
            if self._check_midpoint(index):
                current = self.head
                counter = 0

                while counter < index:
                    current = current.next
                    counter += 1

            else:
                current = self.tail
                counter = self.size - 1

                while counter > index:
                    current = current.previous
                    counter -= 1

            removed_value = current.value
            current.previous.next = current.next
            current.next.previous = current.previous
            current.next = None
            current.previous = None

        self.size -= 1
        return removed_value

    def insert(self, index: int, value: Any) -> None:
        """
        Inserts a new node with the given value at the given index
        :param index:
        :param value:
        :return:
        """
        self._check_index(index)

        # Case 1: The index is at the start of the DLL
        if index == 0:
            self.prepend(value)
            return

        # Case 2: The index is at the end of the DLL
        elif index == self.size:
            self.append(value)
            return

        # Case 3: The index is in-between
        else:
            target_index = index - 1
            new_node = Node(value)

            if self._check_midpoint(target_index):
                current = self.head
                counter = 0

                while counter < target_index:
                    current = current.next
                    counter += 1

                new_node.next = current.next
                new_node.previous = current

                current.next.previous = new_node
                current.next = new_node
            else:
                current = self.tail
                counter = self.size - 1

                while counter > target_index:
                    current = current.previous
                    counter -= 1

                new_node.next = current.next
                new_node.previous = current

                current.next.previous = new_node
                current.next = new_node

        self.size += 1

    def reverse(self) -> None:
        """
        Reverses the order of the list
        :return:
        """
        current = self.head
        next_node = current.next

        while current is not None:
            next_node = current.next

            current.next = current.previous
            current.previous = next_node
            current = next_node

        self.head, self.tail = self.tail, self.head



DLL = DoublyLinkedList()

nodes: list[Node] = [Node(42),
                     Node(7),
                     Node(19),
                     Node(88),
                     Node(3),
                     Node(56),
                     Node(91),
                     Node(24),
                     Node(65),
                     Node(10),
                     Node(33),
                     Node(78),
                     Node(5),
                     Node(100),
                     Node(12)]

for node in nodes:
    DLL.append(node.value)

print(DLL)
DLL.reverse()
print(DLL)
