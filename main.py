from launch_options import launch_options, parse_time_signature
from chords import compose_chords_sequence
from notes import get_chords_notes, Note
from to_midi import save

TICKS_PER_BEAT = 96

args = launch_options()

time_sig_parts = args.time_sig.split('/')
time_sig = int(time_sig_parts[0]) / int(time_sig_parts[1])

result_chords: list[int] = compose_chords_sequence(args.chords, minor_chance=args.minor_chance, tonic_chance_init=args.tonic_chance, final_tonic=args.final_tonic)
print(result_chords)
keys: list[Note] = get_chords_notes(result_chords, args.octave, time_sig)

save(keys, args.tempo, args.output)

