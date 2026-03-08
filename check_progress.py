"""Quick progress check for Pokemon OCR"""
import os
import json
import pandas as pd

STATE_FILE = r"C:\Users\RLESo\OneDrive - TPT\Documents\PokemonClassification\ocrout\multipart_state.json"
RESULTS_FILE = r"C:\Users\RLESo\OneDrive - TPT\Documents\PokemonClassification\ocrout\all_parts_ocr_events.csv"

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

print("=" * 80)
print("POKEMON OCR PROGRESS CHECK")
print("=" * 80)

# Check state
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, 'r') as f:
        state = json.load(f)

    completed = state.get('last_completed_part', -1) + 1
    global_time = state.get('global_time_offset', 0)

    print(f"\nParts completed: {completed}/18")
    print(f"Global time processed: {format_time(global_time)}")

    if state.get('part_durations'):
        print(f"\nPart durations:")
        for part_dur in state['part_durations']:
            print(f"  Part {part_dur['part']:2d}: {format_time(part_dur['duration'])}")
else:
    print("\nNo state file found - processing hasn't started yet")

# Check results
if os.path.exists(RESULTS_FILE):
    import pandas as pd
    df = pd.read_csv(RESULTS_FILE)
    total = len(df)

    print(f"\nTotal OCR events: {total:,}")

    if total > 0:
        by_part = df.groupby('part').size()
        print(f"\nEvents by part:")
        for part, count in by_part.items():
            print(f"  Part {part:2d}: {count:4d} events")

        last = df.iloc[-1]
        print(f"\nMost recent event:")
        print(f"  Part {last['part']}: {last['global_timestamp']}")
        text_safe = str(last['text'])[:50].encode('ascii', errors='replace').decode('ascii')
        print(f"  Text: {text_safe}")
else:
    print("\nNo results file found yet")

print("\n" + "=" * 80)
