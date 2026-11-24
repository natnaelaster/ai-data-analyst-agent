import pytest
from data_agent.structures import DynamicArray

def test_append_10_items():
    a = DynamicArray()
    for i in range(10):
        a.append(i)

    assert len(a) == 10
    assert list(a) == list(range(10))
    assert a[-1] == 9

def test_insert_front_and_middle():
    a = DynamicArray()
    a.append(20)
    a.append(40)

    # Insert at the front
    a.insert(0, 10)
    assert list(a) == [10, 20, 40]

    # Insert in the middle
    a.insert(2, 30)
    assert list(a) == [10, 20, 30, 40]

def test_pop_end_front_and_empty():
    a = DynamicArray()
    for val in ["first", "middle", "last"]:
        a.append(val)

    # Pop from the end
    assert a.pop() == "last"
    assert list(a) == ["first", "middle"]

    # Pop from the front
    assert a.pop(0) == "first"
    assert list(a) == ["middle"]

    # Pop remaining item, then verify popping an empty array raises IndexError
    assert a.pop() == "middle"
    with pytest.raises(IndexError):
        a.pop()

def test_read_at_len_raises_index_error():
    a = DynamicArray()
    a.append(1)
    a.append(2)
    a.append(3)  # Triggers resize to capacity 4; index 3 is a spare None slot

    assert len(a) == 3
    assert a.capacity == 4

    with pytest.raises(IndexError):
        _ = a[len(a)]

def test_amortized_copies_1000_appends():
    a = DynamicArray()
    for i in range(1000):
        a.append(i)

    assert a.copies < 2 * 1000
