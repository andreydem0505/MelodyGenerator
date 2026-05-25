import argparse
import csv
import random
import sys
import wave
from pathlib import Path

import numpy as np

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

from analyser import NOTES
from batch_analyser import analyse_batch
from chords import compose_chords_sequence
from notes import get_chords_notes


FIELDNAMES = ["filename", "key", "mode", "time_signature"]
MISMATCH_FIELDNAMES = [
    "filename",
    "expected_key",
    "actual_key",
    "expected_mode",
    "actual_mode",
    "expected_time_signature",
    "actual_time_signature",
]

TICKS_PER_BEAT = 96
SAMPLE_RATE = 22050


def key_to_tonic(key: str, mode: str) -> int:
    tonic = NOTES.index(key) + 1
    return tonic if mode == "major" else -tonic


def midi_note_to_frequency(note: int) -> float:
    return 440.0 * (2 ** ((note - 69) / 12))


def render_notes_to_wav(notes, output_path: Path, tempo: float) -> None:
    seconds_per_tick = 60.0 / tempo / TICKS_PER_BEAT
    total_ticks = max(note.position + note.length for note in notes)
    total_samples = int((total_ticks * seconds_per_tick + 0.5) * SAMPLE_RATE)
    audio = np.zeros(total_samples, dtype=np.float32)

    for note in notes:
        start = int(note.position * seconds_per_tick * SAMPLE_RATE)
        length = max(1, int(note.length * seconds_per_tick * SAMPLE_RATE))
        end = min(start + length, total_samples)
        if start >= end:
            continue

        t = np.arange(end - start, dtype=np.float32) / SAMPLE_RATE
        tone = np.sin(2 * np.pi * midi_note_to_frequency(note.key) * t)

        fade_samples = min(int(0.01 * SAMPLE_RATE), len(tone) // 2)
        if fade_samples > 0:
            fade_in = np.linspace(0.0, 1.0, fade_samples, dtype=np.float32)
            fade_out = np.linspace(1.0, 0.0, fade_samples, dtype=np.float32)
            tone[:fade_samples] *= fade_in
            tone[-fade_samples:] *= fade_out

        audio[start:end] += tone * (note.velocity / 127.0) * 0.12

    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = audio / peak * 0.8

    pcm = (audio * 32767).astype(np.int16)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with wave.open(str(output_path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(pcm.tobytes())


def generate_expected_rows(count: int, seed: int) -> list[dict[str, str]]:
    rng = random.Random(seed)
    rows = []

    for index in range(1, count + 1):
        key = rng.choice(NOTES)
        mode = rng.choice(["major", "minor"])
        time_signature = rng.choice(["2/4", "3/4", "4/4"])
        rows.append({
            "filename": f"{index}.wav",
            "key": key,
            "mode": mode,
            "time_signature": time_signature,
        })

    return rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_by_filename(path: Path) -> dict[str, dict[str, str]]:
    with path.open(newline="") as file:
        return {
            row["filename"]: row
            for row in csv.DictReader(file)
        }


def generate_wavs(rows: list[dict[str, str]], output_dir: Path, tempo: float, chords_number: int) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for old_wav in output_dir.glob("*.wav"):
        old_wav.unlink()

    for index, row in enumerate(rows):
        random.seed(index)
        tonic = key_to_tonic(row["key"], row["mode"])
        mode = 1 if row["mode"] == "major" else -1

        chords = compose_chords_sequence(
            chords_number,
            mode=mode,
            tonic=tonic,
            final_tonic=True,
        )
        notes = get_chords_notes(chords, octave=5, meter=row["time_signature"])
        render_notes_to_wav(notes, output_dir / row["filename"], tempo)


def compare_results(expected_csv: Path, detected_csv: Path) -> list[dict[str, str]]:
    expected_rows = read_csv_by_filename(expected_csv)
    detected_rows = read_csv_by_filename(detected_csv)
    mismatches = []

    for filename, expected in expected_rows.items():
        actual = detected_rows.get(filename)
        if actual is None:
            mismatches.append({
                "filename": filename,
                "expected_key": expected["key"],
                "actual_key": "missing",
                "expected_mode": expected["mode"],
                "actual_mode": "missing",
                "expected_time_signature": expected["time_signature"],
                "actual_time_signature": "missing",
            })
            continue

        if (
            expected["key"] != actual["key"]
            or expected["mode"] != actual["mode"]
            or expected["time_signature"] != actual["time_signature"]
        ):
            mismatches.append({
                "filename": filename,
                "expected_key": expected["key"],
                "actual_key": actual["key"],
                "expected_mode": expected["mode"],
                "actual_mode": actual["mode"],
                "expected_time_signature": expected["time_signature"],
                "actual_time_signature": actual["time_signature"],
            })

    return mismatches


def run(args) -> None:
    expected_csv = Path(args.expected_csv)
    detected_csv = Path(args.detected_csv)
    mismatches_csv = Path(args.mismatches_csv)
    wav_dir = Path(args.wav_dir)

    expected_rows = generate_expected_rows(args.count, args.seed)
    write_csv(expected_csv, FIELDNAMES, expected_rows)

    generate_wavs(expected_rows, wav_dir, args.tempo, args.chords)
    analyse_batch(str(wav_dir), str(detected_csv), filenames=[row["filename"] for row in expected_rows])

    mismatches = compare_results(expected_csv, detected_csv)
    write_csv(mismatches_csv, MISMATCH_FIELDNAMES, mismatches)

    print()
    print(f"Generated: {len(expected_rows)}")
    print(f"Analysed: {len(read_csv_by_filename(detected_csv))}")
    print(f"Matched: {len(expected_rows) - len(mismatches)}")
    print(f"Mismatched: {len(mismatches)}")
    print(f"Expected CSV: {expected_csv}")
    print(f"Detected CSV: {detected_csv}")
    print(f"Mismatches CSV: {mismatches_csv}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate WAV files, analyse them, and compare detected metadata with expected CSV."
    )
    parser.add_argument("--count", type=int, default=5, help="Number of WAV files to generate.")
    parser.add_argument("--seed", type=int, default=133742069, help="Random seed for expected CSV generation.")
    parser.add_argument("--chords", type=int, default=16, help="Number of generated chords per file.")
    parser.add_argument("--tempo", type=float, default=200.0, help="Tempo in BPM.")
    parser.add_argument("--wav-dir", default="test/generated_wavs", help="Directory for generated WAV files.")
    parser.add_argument("--expected-csv", default="test/expected.csv", help="CSV with expected metadata.")
    parser.add_argument("--detected-csv", default="test/detected.csv", help="CSV with detected metadata.")
    parser.add_argument("--mismatches-csv", default="test/mismatches.csv", help="CSV with mismatched rows.")
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())
