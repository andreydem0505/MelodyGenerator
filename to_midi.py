import mido
from notes import Note


def save(keys: list[Note], tempo: float, output: str):
    mid = mido.MidiFile(type=0, ticks_per_beat=96)
    track = mido.MidiTrack()
    mid.tracks.append(track)

    track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(tempo), time=0))

    events = []
    for note in keys:
        events.append((note.position, 'note_on', note.key, note.velocity))
        events.append((note.position + note.length, 'note_off', note.key, 0))

    events.sort(key=lambda e: (e[0], e[1] == 'note_on'))

    prev_time = 0
    for abs_time, msg_type, key, velocity in events:
        track.append(mido.Message(msg_type, note=key, velocity=velocity, time=abs_time - prev_time))
        prev_time = abs_time

    mid.save(output)
