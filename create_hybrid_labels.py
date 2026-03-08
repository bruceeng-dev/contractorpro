"""
Hybrid Labeling: Combine location labels + script text matching
This gives you both game progression (location) AND dialog content (script)
"""
import pandas as pd
import difflib
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# Paths
OCR_CSV = Path(r"C:\Users\RLESo\OneDrive - TPT\Documents\PokemonClassification\ocrout\all_parts_ocr_events.csv")
SCRIPT_CSV = Path(r"C:\Users\RLESo\OneDrive - TPT\Documents\PokemonClassification\scriptdf.csv")
OUTPUT_CSV = Path(r"C:\Users\RLESo\OneDrive - TPT\Documents\PokemonClassification\ocrout\hybrid_labeled_clips.csv")

# Settings
TIME_WINDOW = 10.0  # Aggregate events within 10 seconds
MIN_TEXT_LENGTH = 15  # Minimum text length
MIN_SIMILARITY = 0.35  # 35% similarity for script matching (lower threshold)
MATCH_WINDOW = 500     # Search 500 script lines

# ==================== TEXT CLEANING ====================

def clean_text_for_matching(text: str) -> str:
    """Normalize text for comparison - with border artifact removal"""
    if not text or pd.isna(text):
        return ""

    text = str(text).upper()

    # Remove dialog box border artifacts FIRST (before other cleaning)
    text = text.strip()
    if text.startswith('LL '):
        text = text[3:]  # Remove "ll " from start
    if text.startswith('LL'):
        text = text[2:]  # Remove "ll" from start
    if text.endswith(' LL'):
        text = text[:-3]  # Remove " ll" from end
    if text.endswith('LL'):
        text = text[:-2]  # Remove "ll" from end
    # Remove isolated "ll" in middle
    text = text.replace(' LL ', ' ')
    text = text.replace('[LL ', '[')
    text = text.replace(' LL]', ']')

    # Fix OCR errors
    text = text.replace('?', 'E')
    text = text.replace('É', 'E')
    text = text.replace('Á', 'A')
    text = text.replace('0', 'O')
    text = text.replace('ACMON', 'EMON')
    text = text.replace('POK EMON', 'POKEMON')
    text = text.replace('POKACMON', 'POKEMON')

    # Remove player name
    text = text.replace('KAAMOS', '')

    # Remove non-alphanumeric
    text = re.sub(r'[^A-Z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

# ==================== LOCATION EXTRACTION ====================

def extract_location_from_filename(filename: str) -> str:
    """Extract game location from video filename"""
    match = re.search(r'Part \d+ - (.+)\.mp4', filename)
    if match:
        location = match.group(1)
        location = location.replace('⧸', '/').replace('｜｜', '-')
        return location.strip()
    return "Unknown"

# ==================== SCRIPT MATCHING ====================

def find_script_match(text: str, script_df: pd.DataFrame, start_idx: int = 0) -> Tuple[Optional[Dict], float]:
    """
    Find best matching script line.
    Returns script info + similarity score
    """
    best_match = None
    best_score = 0.0

    clean_ocr = clean_text_for_matching(text)
    if len(clean_ocr) < MIN_TEXT_LENGTH:
        return None, 0.0

    end_idx = min(start_idx + MATCH_WINDOW, len(script_df))

    for idx in range(start_idx, end_idx):
        script_text = script_df.iloc[idx]['clean_text']
        if pd.isna(script_text):
            continue

        score = calculate_similarity(clean_ocr, script_text)

        if score > best_score:
            best_score = score
            row = script_df.iloc[idx]
            best_match = {
                'script_text': script_text,
                'section_title': row.get('section_title', ''),
                'context_title': row.get('context_title', ''),
                'speaker': row.get('speaker', ''),
                'event_type': row.get('event_type', ''),
                'script_index': idx
            }

    if best_score >= MIN_SIMILARITY and best_match:
        return best_match, best_score

    return None, 0.0

def calculate_similarity(ocr_text: str, script_text: str) -> float:
    """Calculate text similarity"""
    ocr_clean = clean_text_for_matching(ocr_text)
    script_clean = clean_text_for_matching(script_text)

    if not ocr_clean or not script_clean:
        return 0.0

    # Strategy 1: Substring match
    if ocr_clean in script_clean:
        return min(1.0, 0.7 + (len(ocr_clean) / len(script_clean)) * 0.3)

    # Strategy 2: Word overlap
    ocr_words = set(ocr_clean.split())
    script_words = set(script_clean.split())

    common = {'THE', 'A', 'AN', 'IS', 'ARE', 'TO', 'OF', 'AND', 'OR', 'IN', 'ON'}
    ocr_words -= common
    script_words -= common

    if ocr_words and script_words:
        matching = ocr_words.intersection(script_words)
        coverage = len(matching) / len(ocr_words)
        if coverage >= 0.5:
            return 0.4 + coverage * 0.4

    # Strategy 3: Fuzzy
    return difflib.SequenceMatcher(None, ocr_clean, script_clean).ratio()

# ==================== AGGREGATE OCR ====================

def aggregate_ocr_events(ocr_df: pd.DataFrame, script_df: pd.DataFrame) -> List[Dict]:
    """Aggregate OCR and match to both location AND script"""

    print("Processing OCR events...")
    print(f"  Time window: {TIME_WINDOW}s")
    print(f"  Minimum text length: {MIN_TEXT_LENGTH} chars")
    print(f"  Script similarity threshold: {MIN_SIMILARITY * 100:.0f}%")
    print()

    clips = []
    last_script_idx = 0

    for part_num in sorted(ocr_df['part'].unique()):
        part_events = ocr_df[ocr_df['part'] == part_num].sort_values('local_time')

        if part_events.empty:
            continue

        # Get location from filename
        location = extract_location_from_filename(part_events.iloc[0]['part_file'])

        # Group by time window
        current_group = []
        group_start_time = None

        for idx, row in part_events.iterrows():
            current_time = row['local_time']

            if not current_group:
                current_group = [row]
                group_start_time = current_time
            elif current_time - group_start_time <= TIME_WINDOW:
                current_group.append(row)
            else:
                # Process group
                clip = process_group(current_group, location, script_df, last_script_idx)
                if clip:
                    clips.append(clip)
                    if clip.get('script_index'):
                        last_script_idx = max(last_script_idx, clip['script_index'])

                current_group = [row]
                group_start_time = current_time

        # Final group
        if current_group:
            clip = process_group(current_group, location, script_df, last_script_idx)
            if clip:
                clips.append(clip)
                if clip.get('script_index'):
                    last_script_idx = max(last_script_idx, clip['script_index'])

        if len(clips) % 100 == 0:
            print(f"  Processed {len(clips)} clips...")

    print()
    print(f"Total clips created: {len(clips)}")

    return clips

def process_group(events: List, location: str, script_df: pd.DataFrame, last_script_idx: int) -> Optional[Dict]:
    """Process a group of OCR events into a labeled clip"""

    # Aggregate text
    texts = []
    seen = set()

    for event in events:
        text = str(event['text']).strip()
        if len(text) >= 3 and text not in seen:
            is_substring = any(text in existing for existing in texts)
            if not is_substring:
                texts.append(text)
                seen.add(text)

    combined_text = ' '.join(texts)

    if len(combined_text) < MIN_TEXT_LENGTH:
        return None

    # Try to match to script
    script_match, similarity = find_script_match(combined_text, script_df, last_script_idx)

    first = events[0]
    last = events[-1]

    clip_data = {
        'part': first['part'],
        'part_file': first['part_file'],
        'location': location,
        'start_time': first['local_time'],
        'end_time': last['local_time'],
        'start_timestamp': first['local_timestamp'],
        'end_timestamp': last['local_timestamp'],
        'global_start_time': first['global_time'],
        'global_end_time': last['global_time'],
        'duration': last['local_time'] - first['local_time'],
        'ocr_text': combined_text,
        'num_fragments': len(events),
        'has_script_match': script_match is not None,
        'script_similarity': similarity if script_match else 0.0
    }

    # Add script fields if matched
    if script_match:
        clip_data.update({
            'script_text': script_match['script_text'],
            'script_section': script_match['section_title'],
            'script_context': script_match['context_title'],
            'script_speaker': script_match['speaker'],
            'script_event_type': script_match['event_type'],
            'script_index': script_match['script_index']
        })
    else:
        clip_data.update({
            'script_text': '',
            'script_section': '',
            'script_context': '',
            'script_speaker': '',
            'script_event_type': '',
            'script_index': -1
        })

    return clip_data

# ==================== MAIN ====================

def main():
    print("=" * 80)
    print("HYBRID LABELING: LOCATION + SCRIPT MATCHING")
    print("=" * 80)
    print()

    # Load data
    print("Loading data...")
    ocr_df = pd.read_csv(OCR_CSV)
    print(f"  OCR events: {len(ocr_df):,}")

    script_df = pd.read_csv(SCRIPT_CSV)

    # Filter to actual in-game text only (exclude meta-descriptions)
    # - dialog: Character speech that appears on screen
    # - narration: NPC speech, interior monologue that appears on screen
    # - sign: Text from signs/objects that appears on screen
    # - action: Stage directions/descriptions (NOT shown on screen) - EXCLUDE
    all_content = script_df[script_df['event_type'].isin(['dialog', 'narration', 'sign', 'action'])].copy()
    content_script = script_df[script_df['event_type'].isin(['dialog', 'narration', 'sign'])].copy()

    # Additionally remove the "* -" conditional markers from narration
    before_asterisk_filter = len(content_script)
    content_script = content_script[~content_script['raw_text'].str.startswith('* -', na=False)].copy()
    content_script = content_script.reset_index(drop=True)
    asterisk_filtered = before_asterisk_filter - len(content_script)

    print(f"  {len(all_content):,} total content lines (including stage directions)")
    print(f"  {len(all_content) - before_asterisk_filter:,} 'action' type stage directions excluded")
    print(f"  {asterisk_filtered:,} '* -' conditional markers excluded")
    print(f"  {len(content_script):,} actual in-game text lines for matching")
    print()

    # Process
    clips = aggregate_ocr_events(ocr_df, content_script)

    # Analyze results
    clips_df = pd.DataFrame(clips)

    print()
    print("=" * 80)
    print("RESULTS")
    print("=" * 80)
    print(f"Total clips: {len(clips):,}")
    print()

    # Script matching stats
    matched = clips_df[clips_df['has_script_match'] == True]
    print(f"Clips with script match: {len(matched):,} ({len(matched)/len(clips)*100:.1f}%)")
    print(f"Clips with location only: {len(clips) - len(matched):,} ({(len(clips) - len(matched))/len(clips)*100:.1f}%)")
    print()

    if len(matched) > 0:
        print("Script Match Quality:")
        high = len(matched[matched['script_similarity'] >= 0.7])
        medium = len(matched[(matched['script_similarity'] >= 0.5) & (matched['script_similarity'] < 0.7)])
        low = len(matched[matched['script_similarity'] < 0.5])
        print(f"  High quality (70%+):    {high:4d} matches")
        print(f"  Medium quality (50-70%): {medium:4d} matches")
        print(f"  Low quality (<50%):      {low:4d} matches")
        print()

    # Location distribution
    print("Clips by Location:")
    print("-" * 80)
    location_counts = clips_df.groupby('location').size().sort_values(ascending=False)
    for location, count in location_counts.head(15).items():
        matched_count = len(clips_df[(clips_df['location'] == location) & (clips_df['has_script_match'] == True)])
        print(f"  {location:45s}: {count:4d} total ({matched_count:3d} with script)")
    print("-" * 80)
    print()

    # Script section distribution (for matched clips)
    if len(matched) > 0:
        print("Top Script Sections (matched clips only):")
        print("-" * 80)
        section_counts = matched['script_section'].value_counts().head(10)
        for section, count in section_counts.items():
            print(f"  {section:45s}: {count:3d} matches")
        print("-" * 80)
        print()

    # Save
    clips_df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
    print(f"Saved: {OUTPUT_CSV}")
    print()

    # Sample matches
    if len(matched) > 0:
        print("Sample High-Quality Matches:")
        print("-" * 80)
        best = matched.nlargest(5, 'script_similarity')
        for _, row in best.iterrows():
            ocr_preview = row['ocr_text'][:50].encode('ascii', errors='replace').decode('ascii')
            script_preview = row['script_text'][:50].encode('ascii', errors='replace').decode('ascii')
            print(f"[{row['script_similarity']:.0%}] Part {row['part']} @ {row['start_time']:.1f}s")
            print(f"  Location: {row['location']}")
            print(f"  OCR:      {ocr_preview}")
            print(f"  Script:   {script_preview}")
            print(f"  Section:  {row['script_section']}")
            print()

if __name__ == "__main__":
    main()
