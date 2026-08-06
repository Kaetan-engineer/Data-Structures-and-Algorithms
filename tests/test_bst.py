from BinarySearchTree.BST import BinarySearchTree
import pytest


def test_empty_tree(empty_tree):
    assert len(empty_tree) == 0


def test_insert_single_node(single_node_tree):
    assert list(single_node_tree) == [30]


def test_insert_multiple_values(populated_tree):
    assert list(populated_tree) == [20, 30, 40, 50, 70]


def test_search_existing_value(populated_tree):
    result = populated_tree.search(50)

    assert result is not None
    assert result.value == 50


def test_search_missing_value(populated_tree):
    assert populated_tree.search(60) is None


def test_contains(populated_tree):
    for v in [50, 30, 70, 20, 40]:
        assert v in populated_tree


def test_delete_single_node(single_node_tree):
    result = single_node_tree.delete(30)

    assert result
    assert 30 not in single_node_tree
    assert list(single_node_tree) == []
    assert len(single_node_tree) == 0


def test_delete_single_child(single_child_tree):
    result = single_child_tree.delete(30)

    assert result
    assert 30 not in single_child_tree
    assert list(single_child_tree) == [20]
    assert len(single_child_tree) == 1
    assert 20 in single_child_tree


def test_delete_multiple_children(populated_tree):
    result = populated_tree.delete(70)

    assert result
    assert 70 not in populated_tree
    assert list(populated_tree) == [20, 30, 40, 50]
    assert len(populated_tree) == 4
    assert 20 in populated_tree
    assert 40 in populated_tree
    assert 50 in populated_tree
    assert 30 in populated_tree


def test_delete_empty_tree(empty_tree):
    result = empty_tree.delete(30)

    assert not result
    assert 30 not in empty_tree
    assert len(empty_tree) == 0
    assert list(empty_tree) == []


def test_delete_missing_child(single_child_tree):
    result = single_child_tree.delete(50)

    assert not result
    assert 50 not in single_child_tree
    assert list(single_child_tree) == [20, 30]
    assert 20 in single_child_tree
    assert 30 in single_child_tree
    assert len(single_child_tree) == 2


def test_inorder(populated_tree):
    sorted_list = populated_tree.inorder()

    assert sorted_list == [20, 30, 40, 50, 70]


def test_preorder(populated_tree):
    result = populated_tree.preorder()

    assert result == [50, 30, 20, 40, 70]


def test_postorder(populated_tree):
    result = populated_tree.postorder()

    assert result == [20, 40, 30, 70, 50]


def test_levelorder(populated_tree):
    result = populated_tree.level_order()

    assert result == [50, 30, 70, 20, 40]


def test_empty_level_order(empty_tree):
    assert empty_tree.level_order() == []


def test_empty_tree_height(empty_tree):
    assert empty_tree.height == -1


def test_single_node_height(single_node_tree):
    assert single_node_tree.height == 0


def test_multiple_level_height(populated_tree):
    assert populated_tree.height == 2


def test_balanced_tree():
    tree = BinarySearchTree()

    tree.insert(30)
    tree.insert(20)
    tree.insert(50)

    assert tree.is_balanced()


def test_empty_balanced(empty_tree):
    assert empty_tree.is_balanced()


def test_unbalanced_tree():
    tree = BinarySearchTree()

    tree.insert(30)
    tree.insert(40)
    tree.insert(50)
    tree.insert(60)

    assert not tree.is_balanced()


def test_minimum_empty_tree(empty_tree):
    with pytest.raises(ValueError, match='Tree is empty'):
        empty_tree.min()


def test_minimum_single_node_tree(single_node_tree):
    assert single_node_tree.min() == 30


def test_minimum_multiple_node_tree(populated_tree):
    assert populated_tree.min() == 20


def test_maximum_empty_tree(empty_tree):
    with pytest.raises(ValueError, match='Tree is empty'):
        empty_tree.max()


def test_maximum_single_node_tree(single_node_tree):
    assert single_node_tree.max() == 30


def test_maximum_multiple_node_tree(populated_tree):
    assert populated_tree.max() == 70


def test_len_dunder():
    tree = BinarySearchTree()

    assert len(tree) == 0

    tree.insert(50)
    tree.insert(70)
    tree.insert(20)

    assert len(tree) == 3

    result = tree.delete(50)
    result2 = tree.delete(999)

    assert result
    assert not result2
    assert len(tree) == 2


def test_bool_dunder(empty_tree, single_node_tree):
    assert bool(empty_tree) is False

    assert bool(single_node_tree) is True


def test_iter_dunder(populated_tree):
    assert list(populated_tree) == [20, 30, 40, 50, 70]


def test_str_dunder(single_node_tree):
    assert str(single_node_tree) == 'BinarySearchTree([30])'


def test_repr_dunder(empty_tree, single_node_tree):
    assert repr(empty_tree) == 'None'

    assert repr(single_node_tree) == 'BinarySearchTree(root=30, size=1)'


def test_eq_same_dunder():
    t1 = BinarySearchTree()
    t2 = BinarySearchTree()

    assert t1 == t2

    t1.insert(20)
    t1.insert(30)

    t2.insert(30)
    t2.insert(20)

    assert t1 == t2

    t2.insert(40)

    assert t1 != t2


def test_reversed_dunder(populated_tree):
    assert list(reversed(populated_tree)) == [70, 50, 40, 30, 20]


def test_reversed_empty(empty_tree):
    assert list(reversed(empty_tree)) == []


def test_eq_wrong_type(empty_tree):
    assert empty_tree != [1, 2, 3]



