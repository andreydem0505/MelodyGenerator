from args import args
from chords import compose_chords_sequence
from notes import get_chords_notes, Note
from to_midi import save

args = args()

result_chords: list[int] = compose_chords_sequence(args.chords, minor_chance=args.minor_chance, tonic_chance_init=args.tonic_chance, final_tonic=args.final_tonic)
print(result_chords)
keys: list[Note] = get_chords_notes(result_chords, args.octave, args.meter)

save(keys, args.tempo, args.output)
