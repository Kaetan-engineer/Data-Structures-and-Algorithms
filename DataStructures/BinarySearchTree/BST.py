from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Generator
from collections.abc import Iterator
from DataStructures.Queue.Queue import Queue


@dataclass
class Node:
    value: Any
    left: Node | None = None
    right: Node| None = None


class BinarySearchTree:
    def __init__(self) -> None:
        self.root: Node | None = None
        self._size = 0

    def __str__(self) -> str:
        return f'BinarySearchTree({self.inorder()})'

    def __repr__(self) -> str:
        if self.root is None:
            return 'None'
        return f'BinarySearchTree(root={self.root.value}, size={self._size})'

    def __iter__(self) -> Iterator[Any]:
        yield from self._inorder_genererator(self.root)

    def __reversed__(self) -> Iterator[Any]:
        return self._reversed_generator(self.root)

    def __len__(self) -> int:
        return self._size

    def __contains__(self, item: Any) -> bool:
        return self.search(item) is not None

    def __eq__(self, other: BinarySearchTree) -> bool:
        if not isinstance(other, BinarySearchTree):
            return NotImplemented

        return self.inorder() == other.inorder()

    def __bool__(self) -> bool:
        return self.root is not None

    def _inorder_genererator(self, node: Node | None) -> Generator[Any, None, None]:
        if node is None:
            return

        yield from self._inorder_genererator(node.left)
        yield node.value
        yield from self._inorder_genererator(node.right)

    def _reversed_generator(self, node: Node | None) -> Generator[Any, None, None]:
        if node is None:
            return

        yield from self._reversed_generator(node.right)

        yield node.value

        yield from self._reversed_generator(node.left)

    def _insert(self, node: Node | None, value: Any) -> Node:
        if node is None:
            return Node(value)

        if value <= node.value:
            node.left = self._insert(node.left, value)

        else:
            node.right = self._insert(node.right, value)

        return node

    def insert(self, value: Any) -> None:
        if self.root is None:
            self.root = Node(value)
        else:
            self.root = self._insert(self.root, value)

        self._size += 1

    def _search(self, node: Node | None, value: Any) -> Node | None:
        if node is None:
            return None

        if node.value == value:
            return node

        if value < node.value:
            return self._search(node.left, value)
        else:
            return self._search(node.right, value)

    def search(self, value: Any) -> Node | None:
        return_value = self._search(self.root, value)
        return return_value if return_value is not None else None

    def _delete(self, node: Node | None, value: Any) -> tuple[Node | None, bool]:
        if node is None:
            return None, False

        if value < node.value:
            node.left, deleted = self._delete(node.left, value)
            return node, deleted
        elif value > node.value:
            node.right, deleted = self._delete(node.right, value)
            return node, deleted
        else:
            # Deletion scenario
            if node.left is None:
                return node.right, True

            elif node.right is None:
                return node.left, True

            succesor = node.right

            while succesor.left is not None:
                succesor = succesor.left

            node.value = succesor.value
            node.right, _ = self._delete(node.right, succesor.value)

        return node, True

    def delete(self, value: Any) -> bool:
        self.root, deleted = self._delete(self.root, value)

        if deleted:
            self._size -= 1

        return deleted

    def _inorder(self, node: Node | None, values: list[Any]) -> None:
        if node is None:
            return

        self._inorder(node.left, values)
        values.append(node.value)
        self._inorder(node.right, values)

    def inorder(self) -> list[Any]:
        values = []
        self._inorder(self.root, values)
        return values

    def _preorder(self, node: Node | None, values: list[Any]) -> None:
        if node is None:
            return

        values.append(node.value)
        self._preorder(node.left, values)
        self._preorder(node.right, values)

    def preorder(self) -> list[Any]:
        values = []
        self._preorder(self.root, values)
        return values

    def _postorder(self, node: Node | None, values: list[Any]) -> None:
        if node is None:
            return

        self._postorder(node.left, values)
        self._postorder(node.right, values)
        values.append(node.value)

    def postorder(self) -> list[Any]:
        values = []
        self._postorder(self.root, values)
        return values

    def level_order(self) -> list[Any]:
        if self.root is None:
            return []
        values = []
        queue = Queue()
        queue.enqueue(self.root)

        while not queue.is_empty:
            node = queue.dequeue()

            values.append(node.value)

            if node.left is not None:
                queue.enqueue(node.left)

            if node.right is not None:
                queue.enqueue(node.right)

        return values

    def _check_balance(self, node: Node | None) -> tuple[bool, int]:
        if node is None:
            return True, -1

        left_balanced, left_height = self._check_balance(node.left)
        right_balanced, right_height = self._check_balance(node.right)

        balanced = left_balanced and right_balanced and abs(left_height - right_height) <= 1
        height = max(left_height, right_height) + 1

        return balanced, height

    def is_balanced(self) -> bool:
        if self.root is None:
            return True

        balanced, _ = self._check_balance(self.root)
        return balanced

    @property
    def height(self) -> int:
        if self.root is None:
            return -1

        _, height = self._check_balance(self.root)
        return height

    def min(self) -> Any:
        if self.root is None:
            raise ValueError('Tree is empty, so no minimum was found')

        current = self.root

        while current.left is not None:
            current = current.left

        return current.value

    def max(self) -> Any:
        if self.root is None:
            raise ValueError('Tree is empty, so no minimum was found')

        current = self.root

        while current.right is not None:
            current = current.right

        return current.value

