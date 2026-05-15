import argparse


def args():
    parser = argparse.ArgumentParser(description='Generate MIDIolody')
    parser.add_argument('--chords', '-ch', type=int, default=16, help='Number of chords (default: 16)')
    parser.add_argument('--tempo', '-t', type=float, default=200.0, help='Tempo in BPM (default: 200.0)')
    parser.add_argument('--octave', '-oct', type=int, default=5, help='Octave number (default: 5)')
    parser.add_argument('--mode', '-m', type=str, default='minor', choices=['major', 'minor'], help='Music mode: major or minor (default: minor)')
    parser.add_argument('--tonic-chance', '-tc', type=float, default=0.2, help='Initial chance of tonic chord (default: 0.2)')
    parser.add_argument('--final-tonic', '-ft', action='store_true', help='Guarantees that the tonic is placed on the final beat (add if needed)')
    parser.add_argument('--meter', '-me', type=str, default='3/4', help='Time signature (default: 3/4)')
    parser.add_argument('--output', '-o', type=str, default='result', help='Output MIDI file (default: result)')

    return parser.parse_args()
