from notes_math import add, sub


def test_add_wraps_notes_inside_one_octave():
    assert add(10, 5) == 3
    assert add(1, 12) == 1


def test_sub_wraps_notes_inside_one_octave():
    assert sub(1, 4) == 9
    assert sub(8, 3) == 5
