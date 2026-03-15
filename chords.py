from random import choice, randint
from notes_math import add, sub

def compose_chords_sequence(chords_number: int) -> list[int]:
    tonic = randint(1, 12)
    print(tonic)
    possible_chords = [tonic, sub(tonic, 7), sub(tonic, 5), -sub(tonic, 3), -add(tonic, 2), -add(tonic, 4)]
    return [choice(possible_chords) for _ in range(chords_number)]
