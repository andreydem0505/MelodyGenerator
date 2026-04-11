from fractions import Fraction
import random


class Note:
    def __init__(self, position, length, velocity, key):
        self.position = int(position)
        self.length = int(length)
        self.velocity = velocity
        self.key = key

CELL_LENGTH = 384

def get_chords_notes(chords: list[int],
                     octave: int,
                     meter: str) -> list[Note]:
    
    beat_length = float(Fraction(meter))

    result = []
    position = 0

    for i in range(len(chords)):
        cur_beat_length = beat_length

        chord = chords[i]
        if chord < 0:
            chord = abs(chord)
            keys = [chord, chord + 3, chord + 7]
        else:
            keys = [chord, chord + 4, chord + 7]

        bass_keys = get_bass_keys(keys)
        result.extend([Note(position, CELL_LENGTH * beat_length, 100, octave * 12 + key - 1) for key in bass_keys])

        while cur_beat_length > 0:
            modified = keys_modified(keys)
            chord_length = choose_length_in_beat(cur_beat_length, 1, 4, 2, 0)
            cur_beat_length -= chord_length
            void_length = choose_length_in_beat(cur_beat_length, 1, 4, 2, 7)
            cur_beat_length -= void_length

            result.extend([Note(position, CELL_LENGTH * chord_length, 100, octave * 12 + key - 1) for key in modified])
            position += CELL_LENGTH * (chord_length + void_length)

    return result

def get_bass_keys(keys: list[int]):
    return list(map(lambda x: x - 12, random.sample(keys, 2)))

def keys_modified(keys: list[int]):
    return [key + 12 if random.random() < 0.3 else key for key in keys]

def choose_length_in_beat(max_length: float,
                          one_eight_weight: int,
                          one_forth_weight: int,
                          one_second_weight: int,
                          zero_weight: int) -> float:
    if max_length < 1/8:
        return 0.0
    if max_length < 1/4:
        zero_weight = max(zero_weight - one_forth_weight, 0)
        one_forth_weight = 0
    if max_length < 1/2:
        zero_weight = max(zero_weight - one_second_weight, 0)
        one_second_weight = 0
    return random.choices([1/8, 1/4, 1/2, 0.0],
            weights=[one_eight_weight, one_forth_weight, one_second_weight, zero_weight],
            k=1)[0]

