class Note:
    def __init__(self, position, length, velocity, key):
        self.position = position
        self.length = length
        self.velocity = velocity
        self.key = key

CHORD_LENGTH = 384

def get_chords_notes(chords: list[int], octave: int) -> list[Note]:
    result = []
    for i in range(len(chords)):
        chord = chords[i]
        if chord < 0:
            chord = abs(chord)
            keys = [chord, chord + 3, chord + 7]
        else:
            keys = [chord, chord + 4, chord + 7]
        result.extend([Note(CHORD_LENGTH * i, CHORD_LENGTH, 100, octave * 12 + key - 1) for key in keys])
    return result
