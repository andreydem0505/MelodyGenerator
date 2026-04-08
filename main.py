import mido
from launch_options import launch_options
from chords import compose_chords_sequence
from notes import get_chords_notes, Note

TICKS_PER_BEAT = 96

args = launch_options()

time_sig_parts = args.time_sig.split('/')
time_sig = int(time_sig_parts[0]) / int(time_sig_parts[1])

result_chords: list[int] = compose_chords_sequence(args.chords, minor_chance=args.minor_chance, tonic_chance_init=args.tonic_chance, final_tonic=args.final_tonic)
print(result_chords)
keys: list[Note] = get_chords_notes(result_chords, args.octave, time_sig)


mid = mido.MidiFile(type=0, ticks_per_beat=TICKS_PER_BEAT)
track = mido.MidiTrack()
mid.tracks.append(track)

track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(args.tempo), time=0))

events = []
for note in keys:
    events.append((note.position, 'note_on', note.key, note.velocity))
    events.append((note.position + note.length, 'note_off', note.key, 0))

events.sort(key=lambda e: (e[0], e[1] == 'note_on'))

prev_time = 0
for abs_time, msg_type, key, velocity in events:
    track.append(mido.Message(msg_type, note=key, velocity=velocity, time=abs_time - prev_time))
    prev_time = abs_time

mid.save(args.output)
