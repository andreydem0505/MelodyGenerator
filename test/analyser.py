import numpy as np
import librosa
import collections
import collections.abc

from collections import Counter

collections.MutableSequence = collections.abc.MutableSequence

from madmom.features.downbeats import (
    RNNDownBeatProcessor,
    DBNDownBeatTrackingProcessor
)

# ==========================================
# KEY PROFILES
# ==========================================

MAJOR_PROFILE = np.array([
    6.35, 2.23, 3.48, 2.33,
    4.38, 4.09, 2.52, 5.19,
    2.39, 3.66, 2.29, 2.88
])

MINOR_PROFILE = np.array([
    6.33, 2.68, 3.52, 5.38,
    2.60, 3.53, 2.54, 4.75,
    3.98, 2.69, 3.34, 3.17
])

NOTES = [
    "C", "C#", "D", "D#", "E", "F",
    "F#", "G", "G#", "A", "A#", "B"
]


# ==========================================
# KEY DETECTION
# ==========================================

def detect_key(audio_path):

    # mono audio
    y, sr = librosa.load(
        audio_path,
        sr=22050,
        mono=True
    )

    # harmonic separation
    # improves tonal analysis for piano
    y_harmonic, _ = librosa.effects.hpss(y)

    # chroma extraction
    chroma = librosa.feature.chroma_cqt(
        y=y_harmonic,
        sr=sr
    )

    # normalize frames
    chroma /= np.maximum(
        chroma.sum(axis=0, keepdims=True),
        1e-6
    )

    # average chroma
    chroma_mean = np.mean(chroma, axis=1)

    best_score = -np.inf
    best_key = None
    best_mode = None

    for i in range(12):

        major_profile = np.roll(MAJOR_PROFILE, i)
        minor_profile = np.roll(MINOR_PROFILE, i)

        major_score = np.corrcoef(
            chroma_mean,
            major_profile
        )[0, 1]

        minor_score = np.corrcoef(
            chroma_mean,
            minor_profile
        )[0, 1]

        if major_score > best_score:
            best_score = major_score
            best_key = NOTES[i]
            best_mode = "major"

        if minor_score > best_score:
            best_score = minor_score
            best_key = NOTES[i]
            best_mode = "minor"

    # ==========================================
    # TIME SIGNATURE DETECTION
    # ==========================================

    act = RNNDownBeatProcessor()(audio_path)

    proc = DBNDownBeatTrackingProcessor(
        beats_per_bar=[2, 3, 4],
        fps=96
    )

    beats = proc(act)

    bars = []
    current_bar = []

    for _, beat_num in beats:

        beat_num = int(beat_num)

        current_bar.append(beat_num)

        # new bar started
        if beat_num == 1 and len(current_bar) > 1:

            previous_bar = current_bar[:-1]

            if previous_bar:
                bars.append(max(previous_bar))

            current_bar = [1]

    if not bars:
        return best_key, best_mode, "unknown"

    # keep only supported meters
    filtered = [
        b for b in bars
        if b in (2, 3, 4)
    ]

    if not filtered:
        return best_key, best_mode, "unknown"

    counts = Counter(filtered)

    best_time_signature = counts.most_common(1)[0][0]

    return (
        best_key,
        best_mode,
        f"{best_time_signature}/4"
    )


# ==========================================
# ENTRY
# ==========================================

if __name__ == '__main__':

    print(detect_key('test/untitled.wav'))
