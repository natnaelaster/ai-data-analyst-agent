"""Extra DynamicArray tests: negative indexes, shifting, clamping, spare slots, growth."""

import pytest

from data_agent.structures import DynamicArray


def make(*values):
    a = DynamicArray()
    for v in values:
        a.append(v)
    return a


def test_negative_index_read_and_write():
    a = make(10, 20, 30)
    assert a[-1] == 30
    assert a[-3] == 10
    a[-1] = 99
    assert list(a) == [10, 20, 99]
    with pytest.raises(IndexError):
        a[-4]
    with pytest.raises(IndexError):
        a[3]


def test_setitem_out_of_range():
    a = make(1, 2)
    with pytest.raises(IndexError):
        a[len(a)] = 5


def test_pop_from_the_middle_shifts_items_left():
    a = make("a", "b", "c", "d")
    assert a.pop(1) == "b"
    assert list(a) == ["a", "c", "d"]
    assert a.pop(-2) == "c"
    assert list(a) == ["a", "d"]


def test_insert_at_end_and_clamping_like_a_list():
    a = make(1, 2, 3)
    a.insert(len(a), 4)         # at the end, same as append
    a.insert(100, 5)            # past the end: goes to the end
    a.insert(-100, 0)           # before the start: goes to the front
    assert list(a) == [0, 1, 2, 3, 4, 5]


def test_spare_slots_never_leak_into_iteration():
    a = make(1, 2, 3)           # capacity is 4, so one spare slot
    assert list(a) == [1, 2, 3]
    a.pop()
    assert list(a) == [1, 2]
    b = make(None)              # a real stored None is different from a spare slot
    assert list(b) == [None]
    assert len(b) == 1


def test_capacity_doubles_when_full():
    a = DynamicArray()
    seen = []
    for i in range(5):
        a.append(i)
        seen.append(a.capacity)
    assert seen == [2, 2, 4, 4, 8]


def test_contains_and_repr():
    a = make(1, "x", None)
    assert 1 in a
    assert "x" in a
    assert None in a
    assert 99 not in a
    assert repr(make(1, "x")) == "DynamicArray([1, 'x'])"


def test_behaves_like_a_python_list():
    mine, reference = DynamicArray(), []
    for i in range(50):
        mine.append(i)
        reference.append(i)
        if i % 7 == 0:
            mine.insert(0, -i)
            reference.insert(0, -i)
        if i % 5 == 0:
            assert mine.pop() == reference.pop()
    assert list(mine) == reference
    assert len(mine) == len(reference)