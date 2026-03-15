import pyflp
from chords import compose_chords_sequence
from notes import get_chords_notes, Note


CHORDS_NUMBER = 8

TEMPO = 200.0

# base octave
OCTAVE_NUMBER = 5

result_chords: list[int] = compose_chords_sequence(CHORDS_NUMBER)
print(result_chords)
keys: list[Note] = get_chords_notes(result_chords, OCTAVE_NUMBER)


project = pyflp.parse("base.flp")
project.tempo = TEMPO
counter = 0
for note in project.patterns.current.notes:
    if counter < len(keys):
        key = keys[counter]
        note.key = key.key
        note.length = key.length
        note.position = key.position
        note.velocity = key.velocity
        counter += 1
    else:
        note.position = 0
        note.velocity = 0
        note.key = 0

pyflp.save(project, "result.flp")
