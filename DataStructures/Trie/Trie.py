from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterator


@dataclass
class TrieNode:
    children: dict[str, TrieNode] = field(default_factory=dict)
    is_word: bool = False


class Trie:
    def __init__(self) -> None:
        self._root: TrieNode = TrieNode()
        self._size: int = 0

    def __repr__(self) -> str:
        return f"Trie({self.get_all_words()})"

    def __contains__(self, word: str) -> bool:
        return self.search(word)

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Iterator[str]:
        yield from self.get_all_words()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Trie):
            return False

        if len(self) != len(other):
            return False

        for word in self:
            if word not in other:
                return False

        return True

    def __bool__(self) -> bool:
        return self._size > 0

    def __or__(self, other: object) -> Trie:
        if not isinstance(other, Trie):
            raise TypeError(f"unsupported operand type(s) for |: 'Trie' and '{type(other).__name__}")

        result = self.copy()

        for word in other:
            result.insert(word)

        return result

    def __and__(self, other: object) -> Trie:
        if not isinstance(other, Trie):
            raise TypeError(f"unsupported operand type(s) for @: 'Trie' and '{type(other).__name__}")

        new_trie = Trie()

        if len(self) <= len(other):
            smaller = self
            larger = other
        else:
            smaller = other
            larger = self

        for word in smaller:
            if word in larger:
                new_trie.insert(word)

        return new_trie

    def __xor__(self, other: object) -> Trie:
        if not isinstance(other, Trie):
            raise TypeError(f"unsupported operand type(s) for ^: 'Trie' and '{type(other).__name__}'")

        return (self - other) | (other - self)

    def __sub__(self, other: object) -> Trie:
        if not isinstance(other, Trie):
            raise TypeError(f"'unsupported operand type(s) for -: 'Trie' and '{type(other).__name__}'")

        new_trie = Trie()

        for word in self:
            if word not in other:
                new_trie.insert(word)

        return new_trie

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Trie):
            raise TypeError(f"unsupported operand type(s) for <=: 'Trie' and '{type(other).__name__}'")

        if len(self) > len(other):
            return False

        for word in self:
            if word not in other:
                return False

        return True

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Trie):
            raise TypeError(f"unsupported operand type(s) for <: 'Trie' and '{type(other).__name__}'")

        return self <= other and self != other

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Trie):
            raise TypeError(f"unsupported operand type(s) for >=: 'Trie' and '{type(other).__name__}'")

        return other <= self

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Trie):
            raise TypeError(f"unsupported operand type(s) for >: 'Trie' and '{type(other).__name__}'")

        return self >= other and self != other

    def _find_node(self, prefix: str) -> TrieNode | None:
        current: TrieNode = self._root

        for char in prefix:
            if char not in current.children:
                return None

            current = current.children[char]

        return current

    def insert(self, word: str) -> None:
            current: TrieNode = self._root

            for char in word:
                if char not in current.children:
                    new_node: TrieNode = TrieNode()
                    current.children[char] = new_node

                current = current.children[char]
            if current.is_word:
                return

            current.is_word = True
            self._size += 1

    def search(self, word: str) -> bool:
        node = self._find_node(word)
        return node is not None and node.is_word

    def get_all_words(self) -> list[str]:
        return self.words_with_prefix('')

    def starts_with(self, prefix: str) -> bool:
        return self._find_node(prefix) is not None

    def delete(self, word: str) -> None:
        current: TrieNode = self._root
        path: list[tuple[TrieNode, str]] = []

        for char in word:
            if char not in current.children:
                raise KeyError(f'Word {word} not found in Trie')

            path.append((current, char))
            current = current.children[char]

        if not current.is_word:
            raise KeyError(f"Word {word} not found in Trie")

        current.is_word = False

        for parent, char in reversed(path):
            if current.is_word or current.children:
                break

            parent.children.pop(char)
            current = parent

        self._size -= 1

    def _collect_words(self, current: TrieNode, prefix: str) -> Iterator[str]:
        if current.is_word:
            yield prefix

        for char, node in current.children.items():
            yield from self._collect_words(node, prefix + char)

    def words_with_prefix(self, prefix: str) -> list[str]:
        node = self._find_node(prefix)

        if node is None:
            return []

        return list(self._collect_words(node, prefix))

    def clear(self) -> None:
        self._root = TrieNode()
        self._size = 0

    def copy(self) -> Trie:
        trie_copy = Trie()

        for word in self:
            trie_copy.insert(word)

        return trie_copy

    def _count_words(self, current: TrieNode) -> int:
        count = 1 if current.is_word else 0

        for child in current.children.values():
            count += self._count_words(child)

        return count

    def count_prefix(self, prefix: str) -> int:
        node = self._find_node(prefix)

        if node is None:
            return 0

        return self._count_words(node)

    def longest_prefix(self, word: str) -> str | None:
        current: TrieNode = self._root
        current_word: str = ''
        longest: str | None = None

        for char in word:
            if char not in current.children:
                break

            current = current.children[char]
            current_word += char

            if current.is_word:
                longest = current_word

        return longest

