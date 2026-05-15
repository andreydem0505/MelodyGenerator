import random

from typing import List

from notes_math import add, sub

def compose_chords_sequence(chords_number: int,
                            mode: str = 'minor',
                            tonic: int = random.randint(1, 12),
                            tonic_chance_init: float = 0.17,
                            final_tonic: bool = False) -> List[int]:
    if mode not in ['minor', 'major']:
        raise ValueError("mode must be 'minor' or 'major'")
    if not 1 <= tonic <= 12:
        raise ValueError("tonic must be in range [1, 12]")
    if chords_number < 1:
        raise ValueError("chords_number must be >= 1")
    if not 0.0 <= tonic_chance_init <= 1.0:
        raise ValueError("tonic_chance_init must be in range [0.0, 1.0]")

    possible_chords = [sub(tonic, 7), sub(tonic, 5), -sub(tonic, 3), -add(tonic, 2), -add(tonic, 4)]
    if tonic_chance_init < 1/len(possible_chords): tonic_chance_init = 1/len(possible_chords) - 0.01
    result_sequence = []
    tonic_chance = tonic_chance_init
    chance_step = (1 - tonic_chance_init) / chords_number

    for _ in range (chords_number if not final_tonic else chords_number - 1):
        if random.random() <= tonic_chance:
            result_sequence.append(tonic)
            tonic_chance = tonic_chance_init
        else:
            if mode == 'minor':
                if random.random() < 0.75:
                    next_chord = random.choice(possible_chords[-3:])
                else:
                    next_chord = random.choice(possible_chords[:2])
            else:
                if random.random() < 0.25:
                    next_chord = random.choice(possible_chords[-3:])
                else:
                    next_chord = random.choice(possible_chords[:2])
            result_sequence.append(next_chord)
            tonic_chance += min(1.0 - tonic_chance, chance_step)
    if final_tonic: result_sequence.append(tonic)
    print(f'tonic: {tonic}, mode: {mode}')
    return result_sequence
