import pandas as pd
import glob
from pathlib import Path

output_dir = Path(r"C:\Users\RLESo\OneDrive - TPT\Documents\PokemonClassification\ocrout")

print("=" * 100)
print("ALL MATCHED OUTPUT FILES")
print("=" * 100)

files = sorted(output_dir.glob('matched*.csv'))

results = []
for f in files:
    try:
        df = pd.read_csv(f)
        results.append({
            'filename': f.name,
            'matches': len(df),
            'file': f
        })
    except Exception as e:
        print(f"Error reading {f.name}: {e}")

# Sort by number of matches (descending)
results.sort(key=lambda x: x['matches'], reverse=True)

print(f"\nFound {len(results)} output files:\n")
for r in results:
    print(f"{r['matches']:6d} matches - {r['filename']}")

# Show details of the file with most matches
if results:
    best = results[0]
    print(f"\n" + "=" * 100)
    print(f"FILE WITH MOST MATCHES: {best['filename']} ({best['matches']} matches)")
    print("=" * 100)

    df = pd.read_csv(best['file'])
    print("\nColumns:", df.columns.tolist())

    if 'similarity' in df.columns:
        print("\nSimilarity stats:")
        print(df['similarity'].describe())

    if 'event_type' in df.columns:
        print("\nEvent type breakdown:")
        print(df['event_type'].value_counts())

    print("\nFirst 5 matches:")
    print(df.head()[['ocr_text', 'script_text', 'similarity']].to_string() if 'similarity' in df.columns else df.head().to_string())
