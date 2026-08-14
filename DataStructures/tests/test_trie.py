from DataStructures.Trie.Trie import Trie
import pytest


def test_trie_existing_word(empty_trie):
    trie = empty_trie

    trie.insert('cat')
    assert trie.search('cat')


def test_trie_nonexistent_word(empty_trie):
    trie = empty_trie
    assert not trie.search('cat')

    trie.insert('cat')
    assert not trie.search('pie')


def test_trie_not_complete_word(empty_trie):
    trie = empty_trie

    trie.insert('apple')
    assert not trie.search('app')


def test_trie_empty_string(empty_trie):
    trie = empty_trie

    trie.insert('cat')
    assert not trie.search('')


def test_trie_existing_prefix(empty_trie):
    trie = empty_trie

    trie.insert('car')
    trie.insert('care')

    assert trie.search('car')
    assert trie.search('care')
    assert not trie.search('ca')


def test_trie_starts_with_existing_prefix(empty_trie):
    trie = empty_trie

    trie.insert('cat')
    assert trie.starts_with('ca')


def test_trie_starts_with_nonexisting_prefix(empty_trie):
    trie = empty_trie
    assert not trie.starts_with('ap')

    trie.insert('apple')
    assert not trie.starts_with('pr')


def test_trie_startswith_empty_prefix(empty_trie):
    trie = empty_trie

    trie.insert('care')
    assert trie.starts_with('')


def test_trie_delete_word(empty_trie):
    trie = empty_trie

    trie.insert("cat")

    trie.delete("cat")

    assert not trie.search("cat")
    assert not trie.starts_with("cat")


def test_trie_delete_word_with_shared_prefix(empty_trie):
    trie = empty_trie

    trie.insert("car")
    trie.insert("care")

    trie.delete("care")

    assert trie.search("car")
    assert not trie.search("care")
    assert trie.starts_with("car")


def test_trie_delete_prefix_of_another_word(empty_trie):
    trie = empty_trie

    trie.insert("car")
    trie.insert("care")

    trie.delete("car")

    assert not trie.search("car")
    assert trie.search("care")
    assert trie.starts_with("car")


def test_trie_delete_nonexistent_word(empty_trie):
    trie = Trie()

    trie.insert("cat")

    with pytest.raises(KeyError):
        trie.delete("dog")

    with pytest.raises(KeyError):
        trie.delete("ca")


def test_trie_contains(empty_trie):
    trie = empty_trie

    trie.insert("cat")
    trie.insert("care")

    assert "cat" in trie
    assert "care" in trie
    assert "ca" not in trie
    assert "dog" not in trie


def test_trie_len(empty_trie):
    trie = empty_trie

    assert len(trie) == 0

    trie.insert("car")
    assert len(trie) == 1

    trie.insert("car")
    assert len(trie) == 1

    trie.insert("care")
    assert len(trie) == 2

    trie.delete("care")
    assert len(trie) == 1

    trie.delete("car")
    assert len(trie) == 0


def test_trie_iter(empty_trie):
    trie = empty_trie

    assert list(trie) == []

    trie.insert('car')
    trie.insert('care')
    trie.insert('cat')

    assert list(trie) == ['car', 'care', 'cat']


def test_trie_repr(empty_trie):
    trie = empty_trie

    trie.insert('cat')
    trie.insert('care')
    trie.insert('bee')

    assert repr(trie) == "Trie(['cat', 'care', 'bee'])"


def test_trie_words_same_prefix(empty_trie):
    trie = empty_trie

    trie.insert('car')
    trie.insert('care')
    trie.insert('cape')
    trie.insert('candle')

    assert trie.words_with_prefix('ca') == ['car', 'care', 'cape', 'candle']


def test_trie_word_prefix(empty_trie):
    trie = empty_trie

    trie.insert('cat')
    trie.insert('catastrophe')

    assert trie.words_with_prefix('cat') == ['cat', 'catastrophe']


def test_trie_no_matches(empty_trie):
    trie = empty_trie

    trie.insert('apple')

    assert trie.words_with_prefix('ac') == []


def test_trie_all_words(empty_trie):
    trie = empty_trie

    trie.insert('car')
    trie.insert('care')
    trie.insert('cape')
    trie.insert('candle')

    assert trie.words_with_prefix('') == ['car', 'care', 'cape', 'candle']


def test_trie_clear(empty_trie):
    trie = empty_trie

    trie.insert("cat")
    trie.insert("care")
    trie.insert("dog")

    trie.clear()

    assert len(trie) == 0
    assert trie.get_all_words() == []
    assert "cat" not in trie
    assert not trie.starts_with("ca")


def test_trie_copy(empty_trie):
    trie = empty_trie

    trie.insert("cat")
    trie.insert("care")
    trie.insert("dog")

    copied = trie.copy()

    assert copied is not trie
    assert copied.get_all_words() == trie.get_all_words()
    assert len(copied) == len(trie)

    copied.insert("bee")
    copied.delete("cat")

    assert "bee" not in trie
    assert "cat" in trie
    assert "bee" in copied
    assert "cat" not in copied


def test_trie_count_prefix(empty_trie):
    trie = empty_trie

    trie.insert("car")
    trie.insert("care")
    trie.insert("cat")
    trie.insert("dog")

    assert trie.count_prefix("ca") == 3
    assert trie.count_prefix("car") == 2
    assert trie.count_prefix("dog") == 1


def test_trie_count_prefix_no_matches(empty_trie):
    trie = empty_trie

    trie.insert("apple")

    assert trie.count_prefix("xyz") == 0
    assert trie.count_prefix("apx") == 0


def test_trie_count_prefix_empty(empty_trie):
    trie = empty_trie

    trie.insert("car")
    trie.insert("care")
    trie.insert("cat")
    trie.insert("dog")

    assert trie.count_prefix("") == 4


def test_trie_count_prefix_non_word_prefix(empty_trie):
    trie = empty_trie

    trie.insert("care")
    trie.insert("car")
    trie.insert("cat")

    assert trie.count_prefix("ca") == 3
    assert trie.count_prefix("c") == 3


def test_trie_longest_prefix(empty_trie):
    trie = empty_trie

    trie.insert("car")
    trie.insert("care")
    trie.insert("cat")

    assert trie.longest_prefix("careful") == "care"
    assert trie.longest_prefix("catering") == "cat"
    assert trie.longest_prefix("car") == "car"


def test_trie_longest_prefix_no_match(empty_trie):
    trie = empty_trie

    trie.insert("cat")
    trie.insert("car")

    assert trie.longest_prefix("dog") is None


def test_trie_longest_prefix_partial_match(empty_trie):
    trie = empty_trie

    trie.insert("care")

    assert trie.longest_prefix("carpet") is None


def test_trie_eq(empty_trie):
    trie1 = empty_trie
    trie2 = Trie()

    # 1. Identical Tries
    trie1.insert("cat")
    trie1.insert("care")
    trie1.insert("dog")

    trie2.insert("cat")
    trie2.insert("care")
    trie2.insert("dog")

    assert trie1 == trie2

    # 2. Same words, different insertion order
    trie3 = Trie()

    trie3.insert("dog")
    trie3.insert("cat")
    trie3.insert("care")

    assert trie1 == trie3

    # 3. Different words
    trie4 = Trie()

    trie4.insert("cat")
    trie4.insert("care")
    trie4.insert("bird")

    assert trie1 != trie4

    # 4. Different sizes
    trie5 = Trie()

    trie5.insert("cat")
    trie5.insert("care")

    assert trie1 != trie5

    # 5. Non-Trie object
    assert trie1 != {"cat", "care", "dog"}


def test_trie_bool(empty_trie):
    trie = empty_trie

    assert not trie

    trie.insert("cat")

    assert trie

    trie.delete("cat")

    assert not trie


def test_trie_or(empty_trie):
    trie1 = empty_trie
    trie2 = Trie()

    trie1.insert("cat")
    trie1.insert("car")
    trie1.insert("dog")

    trie2.insert("cat")
    trie2.insert("care")
    trie2.insert("bird")

    result = trie1 | trie2

    expected = Trie()

    for word in ["cat", "car", "dog", "care", "bird"]:
        expected.insert(word)

    assert result == expected

    assert trie1.get_all_words() == ["cat", "car", "dog"]
    assert trie2.get_all_words() == ["cat", "care", "bird"]


def test_trie_or_invalid_type(empty_trie):
    trie = empty_trie

    trie.insert("cat")

    try:
        trie | {"dog"}
        assert False
    except TypeError:
        pass


def test_trie_or_invalid_type2(empty_trie):
    trie = empty_trie
    trie.insert("cat")

    with pytest.raises(TypeError):
        trie | {"dog"}


def test_trie_and(empty_trie):
    trie1 = empty_trie
    trie2 = Trie()

    trie1.insert("cat")
    trie1.insert("car")
    trie1.insert("dog")
    trie1.insert("care")

    trie2.insert("cat")
    trie2.insert("care")
    trie2.insert("bird")

    result = trie1 & trie2

    expected = Trie()
    expected.insert("cat")
    expected.insert("care")

    assert result == expected

    assert trie1.get_all_words() == ['cat', 'car', 'care', 'dog']
    assert trie2.get_all_words() == ["cat", "care", "bird"]


def test_trie_sub(empty_trie):
    trie1 = Trie()
    trie2 = Trie()

    trie1.insert('apple')
    trie1.insert('car')

    trie2.insert('car')
    trie2.insert('race')

    assert list(trie1 - trie2) == ['apple']
    assert trie1 - Trie() == trie1
    assert Trie() - trie2 == Trie()
    assert list(trie1 - trie1) == []


def test_trie_xor(empty_trie):
    trie1 = empty_trie
    trie2 = Trie()

    trie1.insert("cat")
    trie1.insert("car")
    trie1.insert("dog")

    trie2.insert("cat")
    trie2.insert("care")
    trie2.insert("bird")

    result = trie1 ^ trie2

    expected = Trie()

    for word in ["car", "dog", "care", "bird"]:
        expected.insert(word)

    assert result == expected


def test_trie_xor_no_overlap(empty_trie):
    trie1 = empty_trie
    trie2 = Trie()

    trie1.insert("cat")
    trie1.insert("dog")

    trie2.insert("bird")
    trie2.insert("fish")

    result = trie1 ^ trie2

    expected = Trie()

    for word in ["cat", "dog", "bird", "fish"]:
        expected.insert(word)

    assert result == expected


def test_trie_xor_empty(empty_trie):
    trie = empty_trie
    trie.insert("cat")
    trie.insert("dog")

    empty = Trie()

    assert trie ^ empty == trie
    assert empty ^ trie == trie


def test_trie_xor_same_trie(empty_trie):
    trie = empty_trie

    trie.insert("cat")
    trie.insert("dog")

    result = trie ^ trie

    assert not result


def test_trie_xor_shared_words(empty_trie):
    trie1 = empty_trie
    trie2 = Trie()

    trie1.insert("cat")
    trie1.insert("car")

    trie2.insert("car")
    trie2.insert("dog")

    result = trie1 ^ trie2

    expected = Trie()

    expected.insert("cat")
    expected.insert("dog")

    assert result == expected


def test_trie_xor_different_insertion_order(empty_trie):
    trie1 = empty_trie
    trie2 = Trie()

    trie1.insert("cat")
    trie1.insert("dog")
    trie1.insert("care")

    trie2.insert("care")
    trie2.insert("cat")
    trie2.insert("dog")

    result = trie1 ^ trie2

    assert not result


def test_trie_xor_invalid_type(empty_trie):
    trie = empty_trie
    trie.insert("cat")

    with pytest.raises(TypeError):
        trie ^ {"cat"}


def test_trie_xor_does_not_modify_operands(empty_trie):
    trie1 = empty_trie
    trie2 = Trie()

    trie1.insert("cat")
    trie1.insert("car")

    trie2.insert("car")
    trie2.insert("dog")

    original1 = trie1.copy()
    original2 = trie2.copy()

    _ = trie1 ^ trie2

    assert trie1 == original1
    assert trie2 == original2


def test_trie_le_subset(empty_trie):
    trie1 = empty_trie
    trie2 = Trie()

    trie1.insert("cat")
    trie1.insert("dog")

    trie2.insert("cat")
    trie2.insert("dog")
    trie2.insert("care")

    assert trie1 <= trie2


def test_trie_le_equal(empty_trie):
    trie1 = empty_trie
    trie2 = Trie()

    trie1.insert("cat")
    trie1.insert("dog")

    trie2.insert("dog")
    trie2.insert("cat")

    assert trie1 <= trie2
    assert trie2 <= trie1


def test_trie_le_not_subset(empty_trie):
    trie1 = empty_trie
    trie2 = Trie()

    trie1.insert("cat")
    trie1.insert("dog")

    trie2.insert("cat")
    trie2.insert("care")

    assert not trie1 <= trie2


def test_trie_le_larger_trie(empty_trie):
    trie1 = empty_trie
    trie2 = Trie()

    trie1.insert("cat")
    trie1.insert("dog")
    trie1.insert("care")

    trie2.insert("cat")
    trie2.insert("dog")

    assert not trie1 <= trie2


def test_trie_le_empty(empty_trie):
    trie = empty_trie
    trie.insert("cat")

    empty = Trie()

    assert empty <= trie
    assert empty <= empty
    assert not trie <= empty


def test_trie_le_invalid_type(empty_trie):
    trie = empty_trie
    trie.insert("cat")

    with pytest.raises(TypeError):
        trie <= {"cat"}


def test_lt_returns_true_for_proper_subset():
    trie_small = Trie()
    trie_small.insert('apple')

    trie_large = Trie()
    trie_large.insert('apple')
    trie_large.insert('banana')

    assert (trie_small < trie_large) is True


def test_lt_returns_false_when_equal():
    trie_a = Trie()
    trie_a.insert('apple')
    trie_a.insert('banana')

    trie_b = Trie()
    trie_b.insert('apple')
    trie_b.insert('banana')

    assert (trie_a < trie_b) is False


def test_lt_returns_false_when_larger():
    trie_large = Trie()
    trie_large.insert('apple')
    trie_large.insert('banana')

    trie_small = Trie()
    trie_small.insert('apple')

    assert (trie_large < trie_small) is False


def test_lt_returns_false_for_disjoint_tries():
    trie_a = Trie()
    trie_a.insert('apple')

    trie_b = Trie()
    trie_b.insert('banana')

    assert (trie_a < trie_b) is False


def test_lt_with_empty_tries():
    empty_trie = Trie()
    non_empty_trie = Trie()
    non_empty_trie.insert('apple')

    assert (empty_trie < non_empty_trie) is True
    assert (empty_trie < Trie()) is False


@pytest.mark.parametrize("invalid_operand", [
        "apple",
        123,
        ["apple"],
        {"apple": True},
        None,
        4.5,
    ])
def test_lt_raises_type_error_for_invalid_types(invalid_operand: str | int | float | list[str] | dict[str, bool] | None):
    trie = Trie()
    trie.insert('apple')

    with pytest.raises(TypeError):
        _ = trie < invalid_operand


def test_ge_returns_true_for_proper_superset():
    trie_large = Trie()
    trie_large.insert("apple")
    trie_large.insert("banana")

    trie_small = Trie()
    trie_small.insert("apple")

    assert trie_large >= trie_small


def test_ge_returns_true_when_equal():
    trie_a = Trie()
    trie_a.insert("apple")
    trie_a.insert("banana")

    trie_b = Trie()
    trie_b.insert("apple")
    trie_b.insert("banana")

    assert trie_a >= trie_b
    assert trie_b >= trie_a


def test_ge_returns_false_when_smaller():
    trie_small = Trie()
    trie_small.insert("apple")

    trie_large = Trie()
    trie_large.insert("apple")
    trie_large.insert("banana")

    assert not trie_small >= trie_large


def test_ge_returns_false_for_disjoint_tries():
    trie_a = Trie()
    trie_a.insert("apple")

    trie_b = Trie()
    trie_b.insert("banana")

    assert not trie_a >= trie_b


def test_ge_with_empty_tries():
    empty_trie = Trie()

    non_empty_trie = Trie()
    non_empty_trie.insert("apple")

    assert non_empty_trie >= empty_trie
    assert empty_trie >= empty_trie
    assert not empty_trie >= non_empty_trie


@pytest.mark.parametrize("invalid_operand", [
        "apple",
        123,
        4.5,
        ["apple"],
        {"apple": True},
        None,
    ])
def test_ge_raises_type_error_for_invalid_types(invalid_operand):
    trie = Trie()
    trie.insert("apple")

    with pytest.raises(TypeError):
        _ = trie >= invalid_operand


def test_gt_returns_true_for_proper_superset():
    trie_large = Trie()
    trie_large.insert("apple")
    trie_large.insert("banana")

    trie_small = Trie()
    trie_small.insert("apple")

    assert trie_large > trie_small


def test_gt_returns_false_when_equal():
    trie_a = Trie()
    trie_a.insert("apple")
    trie_a.insert("banana")

    trie_b = Trie()
    trie_b.insert("apple")
    trie_b.insert("banana")

    assert not trie_a > trie_b
    assert not trie_b > trie_a


def test_gt_returns_false_when_smaller():
    trie_small = Trie()
    trie_small.insert("apple")

    trie_large = Trie()
    trie_large.insert("apple")
    trie_large.insert("banana")

    assert not trie_small > trie_large


def test_gt_returns_false_for_disjoint_tries():
    trie_a = Trie()
    trie_a.insert("apple")

    trie_b = Trie()
    trie_b.insert("banana")

    assert not trie_a > trie_b


def test_gt_with_empty_tries():
    empty_trie = Trie()

    non_empty_trie = Trie()
    non_empty_trie.insert("apple")

    assert non_empty_trie > empty_trie
    assert not empty_trie > non_empty_trie
    assert not empty_trie > empty_trie


@pytest.mark.parametrize("invalid_operand", [
        "apple",
        123,
        4.5,
        ["apple"],
        {"apple": True},
        None,
    ])
def test_gt_raises_type_error_for_invalid_types(invalid_operand):
    trie = Trie()
    trie.insert("apple")

    with pytest.raises(TypeError):
        _ = trie > invalid_operand