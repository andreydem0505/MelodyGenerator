import random
from notes_math import add, sub

def compose_chords_sequence(chords_number: int,
                            mode: str = 'major', #если не major и minor, то без настроения
                            tonic: int = random.randint(1, 12),
                            tonic_chance_init: float = 0.17,
                            final_tonic: bool = False) -> list[int]:
    # if mode not in ['minor', 'major']:
    #     raise ValueError("mode must be 'minor' or 'major'")
    if not 1 <= abs(tonic) <= 12:
        raise ValueError("tonic must be in range ±[1, 12]")
    if chords_number < 1:
        raise ValueError("chords_number must be >= 1")
    if not 0.0 <= tonic_chance_init <= 1.0:
        raise ValueError("tonic_chance_init must be in range [0.0, 1.0]")

    tonic_sign = int(abs(tonic)/tonic)
    tonic = abs(tonic)

    if tonic_sign > 0:
        major_chords = [add(tonic, 5), add(tonic, 7)]
        minor_chords = [-add(tonic, 2), -add(tonic, 9), -add(tonic, 4)]
    else:
        major_chords = [sub(tonic, 4), sub(tonic, 9), sub(tonic, 2)]
        minor_chords = [-sub(tonic, 7), -sub(tonic, 5)]
    print('[ POSSIBLE_CHORDS ]: ', tonic_sign * tonic, major_chords, minor_chords)

    
    if tonic_chance_init < 1/len(minor_chords + major_chords): 
        tonic_chance_init = 1/len(minor_chords + major_chords) - 0.01
    result_sequence = []
    tonic_chance = tonic_chance_init
    chance_step = (1 - tonic_chance_init) / chords_number

    for _ in range(chords_number if not final_tonic else chords_number - 1):
        if random.random() <= tonic_chance:
            result_sequence.append(tonic_sign*tonic)
            tonic_chance = tonic_chance_init
        else:
            if mode == 'minor':
                if random.random() < 0.75:
                    next_chord = random.choice(minor_chords)
                else:
                    next_chord = random.choice(major_chords)
            elif mode == 'major':
                if random.random() < 0.25:
                    next_chord = random.choice(minor_chords)
                else:
                    next_chord = random.choice(major_chords)
            else:
                next_chord = random.choice(major_chords + minor_chords)
            result_sequence.append(next_chord)
            tonic_chance += min(1.0 - tonic_chance, chance_step)
    if final_tonic: result_sequence.append(tonic_sign*tonic)
    return result_sequence
