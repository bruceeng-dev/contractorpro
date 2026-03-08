"""
Create a timeline summary of matched events for game state tracking
"""
import pandas as pd

MATCHED_CSV = r"C:\Users\RLESo\OneDrive - TPT\Documents\PokemonClassification\ocrout\matched_script_timeline_improved.csv"
OUTPUT_TXT = r"C:\Users\RLESo\OneDrive - TPT\Documents\PokemonClassification\ocrout\game_timeline.txt"

# Load matched events
df = pd.read_csv(MATCHED_CSV)

print("=" * 80)
print("POKEMON RED PART 1 - GAME EVENT TIMELINE")
print("=" * 80)
print()
print(f"Total matched events: {len(df)}")
print(f"Unique script lines: {df['script_index'].nunique()}")
print(f"Time span: {df['timestamp'].min():.1f}s - {df['timestamp'].max():.1f}s ({(df['timestamp'].max() - df['timestamp'].min())/60:.1f} minutes)")
print()

# Sort by timestamp
df = df.sort_values('timestamp')

# Create timeline
timeline_lines = []
timeline_lines.append("=" * 80)
timeline_lines.append("POKEMON RED PART 1 - GAME EVENT TIMELINE")
timeline_lines.append("=" * 80)
timeline_lines.append("")
timeline_lines.append(f"Total matched events: {len(df)}")
timeline_lines.append(f"Time span: {df['timestamp'].min():.1f}s - {df['timestamp'].max():.1f}s")
timeline_lines.append("")

# Group by section
current_section = None
for idx, row in df.iterrows():
    section = str(row['section_title']) if pd.notna(row['section_title']) else 'Unknown'

    # Section header
    if section != current_section:
        timeline_lines.append("")
        timeline_lines.append("-" * 80)
        section_safe = section.encode('ascii', errors='replace').decode('ascii')
        timeline_lines.append(f"SECTION: {section_safe}")
        timeline_lines.append("-" * 80)
        current_section = section

    # Event details
    timestamp = row['timestamp']
    minutes = int(timestamp // 60)
    seconds = int(timestamp % 60)

    speaker = str(row['speaker']) if pd.notna(row['speaker']) else ''
    script_text = str(row['script_text']) if pd.notna(row['script_text']) else ''
    score = row['overall_score']

    # Make safe for ASCII
    speaker_safe = speaker.encode('ascii', errors='replace').decode('ascii')
    script_safe = script_text[:80].encode('ascii', errors='replace').decode('ascii')

    timeline_lines.append(f"[{minutes:02d}:{seconds:02d}] {speaker_safe:12s} (score:{score:.2f})")
    timeline_lines.append(f"  {script_safe}")
    timeline_lines.append("")

timeline_lines.append("=" * 80)

# Print timeline
for line in timeline_lines:
    print(line)

# Save timeline
with open(OUTPUT_TXT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(timeline_lines))

print()
print(f"Timeline saved to: {OUTPUT_TXT}")
print()

# Show statistics by section
print("EVENTS BY GAME SECTION:")
print("-" * 80)
section_counts = df['section_title'].value_counts()
for section, count in section_counts.items():
    if pd.notna(section):
        section_safe = str(section).encode('ascii', errors='replace').decode('ascii')
        print(f"  {section_safe:30s}: {count:3d} events")

print()
print("=" * 80)
