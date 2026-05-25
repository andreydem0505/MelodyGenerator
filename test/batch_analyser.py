# test/batch_analyzer.py
import argparse
import csv
from pathlib import Path
from analyser import detect_key

def analyse_batch(input_dir: str, output_csv: str) -> None:
    results = []
    
    for wav_file in sorted(Path(input_dir).glob('*.wav')):
        try:
            key, mode, time_sig = detect_key(str(wav_file))
            results.append({
                'filename': wav_file.name,
                'key': key,
                'mode': mode,
                'time_signature': time_sig
            })
            print(f"{wav_file.name}: {key} {mode} {time_sig}")
        except Exception as e:
            print(f"{wav_file.name}: {e}")
    
    with open(output_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['filename', 'key', 'mode', 'time_signature'])
        writer.writeheader() #возможно, стоит убрать
        writer.writerows(results)
    
    print(f"\nSaved {len(results)} results to {output_csv}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Batch analyze WAV files')
    parser.add_argument('--input-dir', '-i', default= 'test/generated_wavs', help='Directory with WAV files')
    parser.add_argument('--output', '-o', default='test/detected.csv', help='Output CSV file')
    
    args = parser.parse_args()
    analyse_batch(args.input_dir, args.output)