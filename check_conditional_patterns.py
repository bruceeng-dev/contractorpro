import pandas as pd

# Load the script CSV
df = pd.read_csv(r'c:\Users\RLESo\Downloads\Website_Test_Folder\pokemon_red_script_table.csv')

print("Searching for conditional/descriptive patterns in raw_text...\n")
print("=" * 80)

# Pattern 1: Lines starting with "* -"
pattern1 = df[df['raw_text'].astype(str).str.contains(r'^\*\s*-', na=False, regex=True)]
print(f"\nPattern 1: Lines starting with '* -': {len(pattern1)}")
if len(pattern1) > 0:
    for idx, row in pattern1.iterrows():
        print(f"  Row {idx}: {row['event_type']}")
        print(f"    {row['raw_text'][:150]}")

# Pattern 2: Lines starting with "If" (likely conditional descriptions)
pattern2 = df[df['raw_text'].astype(str).str.match(r'^If ', na=False)]
print(f"\nPattern 2: Lines starting with 'If ': {len(pattern2)}")
if len(pattern2) > 0:
    print("  First 10 examples:")
    for idx, row in pattern2.head(10).iterrows():
        print(f"  Row {idx}: {row['event_type']}")
        print(f"    {row['raw_text'][:150]}")

# Pattern 3: Any line containing asterisk
pattern3 = df[df['raw_text'].astype(str).str.contains(r'\*', na=False, regex=True)]
print(f"\nPattern 3: Lines containing '*': {len(pattern3)}")
if len(pattern3) > 0:
    print("  All examples:")
    for idx, row in pattern3.iterrows():
        print(f"  Row {idx}: {row['event_type']}")
        print(f"    {row['raw_text'][:150]}")

# Pattern 4: Check event_type distribution for lines with "If"
content_df = df[df['event_type'].isin(['dialog', 'narration', 'sign', 'action'])].copy()
if_lines = content_df[content_df['raw_text'].astype(str).str.match(r'^If ', na=False)]
print(f"\nPattern 4: Content lines (dialog/narration/sign/action) starting with 'If': {len(if_lines)}")
if len(if_lines) > 0:
    print("  Event type breakdown:")
    print(if_lines['event_type'].value_counts())
    print("\n  First 10 examples:")
    for idx, row in if_lines.head(10).iterrows():
        print(f"  Row {idx}: {row['event_type']}")
        print(f"    {row['raw_text'][:200]}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Total script lines: {len(df)}")
print(f"Content lines (dialog/narration/sign/action): {len(content_df)}")
print(f"Lines with '* -' pattern: {len(pattern1)}")
print(f"Content lines starting with 'If': {len(if_lines)}")
