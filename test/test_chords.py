import random

import pytest

from chords import compose_chords_sequence


MAJOR_TONIC_1_CHORDS = {1, 6, 8, -3, -10, -5}
MINOR_TONIC_1_CHORDS = {-1, 9, 4, 11, -6, -8}


def test_compose_chords_sequence_returns_requested_number_of_chords():
    random.seed(1)

    result = compose_chords_sequence(16, tonic=1)

    assert len(result) == 16


def test_compose_chords_sequence_supports_single_chord():
    random.seed(2)

    result = compose_chords_sequence(1, tonic=1)

    assert len(result) == 1


def test_compose_chords_sequence_ends_with_major_tonic_when_requested():
    random.seed(3)

    result = compose_chords_sequence(8, tonic=1, final_tonic=True)

    assert len(result) == 8
    assert result[-1] == 1


def test_compose_chords_sequence_ends_with_minor_tonic_when_requested():
    random.seed(4)

    result = compose_chords_sequence(8, tonic=-1, final_tonic=True)

    assert len(result) == 8
    assert result[-1] == -1


@pytest.mark.parametrize("chords_number", [0, -1])
def test_compose_chords_sequence_rejects_invalid_chords_number(chords_number):
    with pytest.raises(ValueError, match="chords_number"):
        compose_chords_sequence(chords_number, tonic=1)


@pytest.mark.parametrize("tonic", [0, 13, -13])
def test_compose_chords_sequence_rejects_invalid_tonic(tonic):
    with pytest.raises(ValueError, match="tonic"):
        compose_chords_sequence(4, tonic=tonic)


@pytest.mark.parametrize("tonic_chance_init", [-0.1, 1.1])
def test_compose_chords_sequence_rejects_invalid_tonic_chance(tonic_chance_init):
    with pytest.raises(ValueError, match="tonic_chance_init"):
        compose_chords_sequence(4, tonic=1, tonic_chance_init=tonic_chance_init)


def test_compose_chords_sequence_uses_only_allowed_chords_for_major_tonic():
    random.seed(5)

    result = compose_chords_sequence(100, tonic=1)

    assert set(result).issubset(MAJOR_TONIC_1_CHORDS)


def test_compose_chords_sequence_uses_only_allowed_chords_for_minor_tonic():
    random.seed(6)

    result = compose_chords_sequence(100, tonic=-1)

    assert set(result).issubset(MINOR_TONIC_1_CHORDS)


@pytest.mark.parametrize("mode", [1, -1, 0])
def test_compose_chords_sequence_supports_all_modes(mode):
    random.seed(7)

    result = compose_chords_sequence(20, mode=mode, tonic=1)

    assert len(result) == 20
    assert set(result).issubset(MAJOR_TONIC_1_CHORDS)


def test_compose_chords_sequence_is_reproducible_with_fixed_random_seed():
    random.seed(8)
    result_1 = compose_chords_sequence(16, tonic=1)

    random.seed(8)
    result_2 = compose_chords_sequence(16, tonic=1)

    assert result_1 == result_2


def test_compose_chords_sequence_with_random_tonic_returns_valid_chord_values():
    random.seed(9)

    result = compose_chords_sequence(32, tonic=None)

    assert len(result) == 32
    assert all(chord != 0 for chord in result)
    assert all(1 <= abs(chord) <= 12 for chord in result)
