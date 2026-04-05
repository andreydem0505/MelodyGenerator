import mido
from chords import compose_chords_sequence
from notes import get_chords_notes, Note


CHORDS_NUMBER = 8

TEMPO = 200.0

OCTAVE_NUMBER = 5

TICKS_PER_BEAT = 96

result_chords: list[int] = compose_chords_sequence(1, CHORDS_NUMBER, minor_chance=0.6, tonic_chance_init=0.0)
print(result_chords)
keys: list[Note] = get_chords_notes(result_chords, OCTAVE_NUMBER)


mid = mido.MidiFile(type=0, ticks_per_beat=TICKS_PER_BEAT)
track = mido.MidiTrack()
mid.tracks.append(track)

track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(TEMPO), time=0))

events = []
for note in keys:
    events.append((note.position, 'note_on', note.key, note.velocity))
    events.append((note.position + note.length, 'note_off', note.key, 0))

events.sort(key=lambda e: (e[0], e[1] == 'note_on'))

prev_time = 0
for abs_time, msg_type, key, velocity in events:
    track.append(mido.Message(msg_type, note=key, velocity=velocity, time=abs_time - prev_time))
    prev_time = abs_time

mid.save("result.mid")
