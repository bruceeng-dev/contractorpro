import pandas as pd

df = pd.read_csv('pokemon_red_script_table.csv')

# Apply the same filtering as the updated scripts
content_script = df[df['event_type'].isin(['dialog', 'narration', 'sign'])]
content_script = content_script[~content_script['raw_text'].str.startswith('* -', na=False)]

print('Event type breakdown of final filtered script:')
print(content_script['event_type'].value_counts())

print('\nRandom sample of 15 final entries:')
print('=' * 100)
samples = content_script.sample(15, random_state=42)
for idx, row in samples.iterrows():
    text = str(row['raw_text'])[:100].replace('\n', ' ')
    print(f"{row['event_type']:12s} | {text}")

print('\n' + '=' * 100)
print('SUMMARY:')
print(f"Total in-game text lines: {len(content_script)}")
print(f"  - dialog: {len(content_script[content_script['event_type'] == 'dialog'])}")
print(f"  - narration: {len(content_script[content_script['event_type'] == 'narration'])}")
print(f"  - sign: {len(content_script[content_script['event_type'] == 'sign'])}")
