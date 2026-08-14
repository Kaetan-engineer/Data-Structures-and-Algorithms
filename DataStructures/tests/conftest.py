from DataStructures.BinarySearchTree.BST import BinarySearchTree
from DataStructures.Trie.Trie import Trie
import pytest


@pytest.fixture
def empty_tree():
    return BinarySearchTree()


@pytest.fixture
def single_node_tree():
    tree = BinarySearchTree()

    tree.insert(30)

    return tree


@pytest.fixture
def single_child_tree():
    tree = BinarySearchTree()

    tree.insert(30)
    tree.insert(20)

    return tree


@pytest.fixture
def populated_tree():
    tree = BinarySearchTree()

    values = [50, 30, 70, 20, 40]

    for v in values:
        tree.insert(v)

    return tree


@pytest.mark.parametrize(
    'value, exists',
    [
        (20, True),
        (30, True),
        (40, True),
        (100, False)
    ]
)
def test_contains(populated_tree, value, exists):
    assert (value in populated_tree) is exists



@pytest.fixture
def empty_trie():
    return Trie()