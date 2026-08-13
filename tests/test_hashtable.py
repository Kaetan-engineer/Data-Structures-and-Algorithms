import pytest
from HashTable.HashTable import HashTable


@pytest.mark.parametrize("capacity", [0, -1, -5, -100])
def test_hash_table_invalid_capacity(capacity: int):
    with pytest.raises(ValueError):
        HashTable(capacity)


def test_hash_table_empty_len():
    table = HashTable()

    assert len(table) == 0
    assert len(table._buckets) == 8


def test_hash_table_set():
    table = HashTable()

    table.set('name', 'Kaetan')
    assert len(table) == 1

    table.set('name', 'John')
    assert len(table) == 1


def test_hash_table_get():
    table = HashTable()

    table.set('city', 'Texas')
    assert table.get('city') == 'Texas'

    table.set("nothing", None)
    assert table.get("nothing") is None

    with pytest.raises(KeyError) as exc_info:
        table.get('age')

    assert exc_info.value.args[0] == 'age'


def test_hashs_table_contains():
    table = HashTable()

    table.set("city", " New York")
    table.set("name", None)

    assert "city" in table
    assert "name" in table
    assert "age" not in table


def test_hash_table_remove():
    table = HashTable()

    table.set('name', 'Kaetan')
    table.set('age', None)

    assert table.remove('name') == 'Kaetan'
    assert 'name' not in table
    assert len(table) == 1

    with pytest.raises(KeyError):
        table.remove('gender')

    assert table.remove('age') is None
    assert len(table) == 0
    assert "age" not in table


def test_hash_table_resize():
    table = HashTable(capacity=4)

    table.set("a", 1)
    table.set("b", 2)
    table.set("c", 3)

    old_size = len(table)

    table.set('d', 4)

    assert table._capacity == 8
    assert len(table) == old_size + 1

    assert table.get("a") == 1
    assert table.get("b") == 2
    assert table.get("c") == 3
    assert table.get('d') == 4


def test_hash_table_getitem():
    table = HashTable()

    table.set("name", "Kaetan")

    assert table["name"] == "Kaetan"

    with pytest.raises(KeyError):
        table["age"]


def test_hash_table_setitem():
    table = HashTable()

    table["name"] = "Kaetan"

    assert table["name"] == "Kaetan"
    assert len(table) == 1

    table["name"] = "John"

    assert table["name"] == "John"
    assert len(table) == 1


def test_hash_table_delitem():
    table = HashTable()

    table["name"] = "Kaetan"
    table["age"] = 15

    del table["name"]

    assert "name" not in table
    assert len(table) == 1

    with pytest.raises(KeyError):
        table["name"]

    with pytest.raises(KeyError):
        del table["gender"]


def test_hash_table_iter():
    table = HashTable()

    table["name"] = "Kaetan"
    table["age"] = 15
    table["city"] = "Montreal"
    table["nothing"] = None

    keys = list(table)

    assert set(keys) == {"name", "age", "city", "nothing"}
    assert len(keys) == 4


def test_hash_table_items():
    table = HashTable()

    table["name"] = "Kaetan"
    table["age"] = 15
    table["city"] = "Montreal"
    table["nothing"] = None

    items = list(table.items())

    assert set(items) == {
        ("name", "Kaetan"),
        ("age", 15),
        ("city", "Montreal"),
        ("nothing", None),
    }

    assert len(items) == 4


def test_hash_table_values():
    table = HashTable()

    table["name"] = "Kaetan"
    table["age"] = 15
    table["city"] = "Montreal"
    table["nothing"] = None

    values = list(table._values())

    assert set(values) == {"Kaetan", 15, "Montreal", None}
    assert len(values) == 4


def test_hash_table_clear():
    table = HashTable(capacity=4)

    table["name"] = "Kaetan"
    table["age"] = 15
    table["city"] = "Montreal"

    # Force a resize.
    table["country"] = "Canada"

    capacity = table._capacity

    table.clear()

    assert len(table) == 0
    assert table._capacity == capacity
    assert list(table) == []
    assert list(table.items()) == []
    assert list(table._values()) == []

    # The table should still work after being cleared.
    table["name"] = "John"

    assert len(table) == 1
    assert table["name"] == "John"


def test_hash_table_copy():
    table = HashTable(capacity=4)

    table["name"] = "Kaetan"
    table["age"] = 15
    table["city"] = "Montreal"

    table_copy = table.copy()

    assert list(table_copy.items()) == list(table.items())
    assert table_copy._capacity == table._capacity

    table_copy["name"] = "John"
    table_copy["country"] = "Canada"

    assert table["name"] == "Kaetan"
    assert "country" not in table


@pytest.mark.parametrize("first, second, expected", [
    (
        {},
        {},
        True,
    ),
    (
        {"a": 1, "b": 2},
        {"a": 1, "b": 2},
        True,
    ),
    (
        {"a": 1, "b": 2},
        {"a": 1, "b": 3},
        False,
    ),
    (
        {"a": 1, "b": 2},
        {"a": 1, "c": 2},
        False,
    ),
    (
        {"a": 1},
        {"a": 1, "b": 2},
        False,
    ),
])
def test_hash_table_eq(first: dict[str, int], second: dict[str, int], expected: bool):
    first_table = HashTable()
    second_table = HashTable()

    for key, value in first.items():
        first_table[key] = value

    for key, value in second.items():
        second_table[key] = value

    assert (first_table == second_table) is expected


def test_hash_table_eq_non_hash_table():
    table = HashTable()
    table["a"] = 1

    assert table != {"a": 1}
    assert table is not None
    assert table != 42


def test_hash_table_pop():
    table = HashTable()

    table["name"] = "Kaetan"
    table["age"] = None

    assert table.pop("name") == "Kaetan"
    assert "name" not in table
    assert len(table) == 1

    assert table.pop("age") is None
    assert len(table) == 0

    with pytest.raises(KeyError):
        table.pop("missing")


def test_hash_table_popitem():
    table: HashTable[str, str | int] = HashTable[str, str | int]()

    expected: dict[str, str | int] = {
        "name": "Kaetan",
        "age": 15,
        "city": "Montreal",
    }

    for key, value in expected.items():
        table[key] = value

    original_size = len(table)

    key, value = table.popitem()

    assert expected[key] == value
    assert key not in table
    assert len(table) == original_size - 1

    while table:
        table.popitem()

    assert len(table) == 0

    with pytest.raises(KeyError):
        table.popitem()


def test_hash_table_update():
    table: HashTable[str, str | int] = HashTable[str, int | str]()

    table["name"] = "Kaetan"
    table["age"] = 15

    table.update({
        "name": "John",
        "city": "Montreal",
    })

    assert table["name"] == "John"
    assert table["age"] == 15
    assert table["city"] == "Montreal"
    assert len(table) == 3


def test_hash_table_multiple_resizes():
    table: HashTable[str, int] = HashTable[str, int](capacity=2)

    entries = {
        "a": 1,
        "b": 2,
        "c": 3,
        "d": 4,
        "e": 5,
        "f": 6,
        "g": 7,
    }

    for key, value in entries.items():
        table[key] = value

    assert table._capacity >= 8
    assert len(table) == len(entries)

    for key, value in entries.items():
        assert table[key] == value


def test_hash_table_iteration_after_resize():
    table: HashTable[str, int] = HashTable[str, int](capacity=2)

    expected = {
        "a": 1,
        "b": 2,
        "c": 3,
        "d": 4,
        "e": 5,
    }

    for key, value in expected.items():
        table[key] = value

    assert set(table) == set(expected)
    assert len(list(table)) == len(expected)
    assert set(table.items()) == set(expected.items())
    assert set(table._values()) == set(expected.values())