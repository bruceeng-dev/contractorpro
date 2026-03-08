import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv('pokemon_red_script_table_EXPANDED.csv')

print("=" * 100)
print("CHECKING IF TRAINER BATTLES ARE ACTUALLY SEPARATED")
print("=" * 100)

# Find rows that STILL have multiple markers together
still_combined = df[df['raw_text'].astype(str).str.contains(r'\{S\}.*\{C\}', na=False, regex=True)]

print(f"\nRows that STILL have multiple markers in one cell: {len(still_combined)}")

if len(still_combined) > 0:
    print("\nExamples of rows that weren't properly split:\n")
    for idx, row in still_combined.head(5).iterrows():
        print(f"Row {idx}:")
        print(f"  Event Type: {row['event_type']}")
        print(f"  Context: {row['context_title']}")
        print(f"  Raw Text: {row['raw_text'][:200]}...")
        print()

# Check rows with context_title set to {S}, {C}, etc
properly_split = df[df['context_title'].isin(['{S}', '{C}', '{E}', '{A}'])]
print(f"\nRows with context_title markers: {len(properly_split)}")

if len(properly_split) > 0:
    print("\nExamples of properly split entries:\n")
    for idx, row in properly_split.head(5).iterrows():
        print(f"Row {idx}:")
        print(f"  Context: {row['context_title']}")
        print(f"  Raw Text: {row['raw_text'][:100]}")
        print()
