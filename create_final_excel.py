import pandas as pd
from pathlib import Path

# Paths
llm_file = Path(r"C:\Users\RLESo\OneDrive - TPT\Documents\PokemonClassification\ocrout\llm_alignment_full.csv")
script_file = Path(r"c:\Users\RLESo\Downloads\Website_Test_Folder\pokemon_red_script_table_FIXED.csv")
output_file = Path(r"C:\Users\RLESo\Downloads\Website_Test_Folder\LLM_OCR_and_Script_Data_FINAL.xlsx")

print("Loading data...")
print("=" * 80)

# Load LLM OCR data
llm_df = pd.read_csv(llm_file)
print(f"[OK] Loaded {len(llm_df):,} LLM OCR entries")

# Load FIXED script data
script_df = pd.read_csv(script_file)
print(f"[OK] Loaded {len(script_df):,} script entries")

# Filter script to actual in-game text (dialog, narration, sign, S, C, E, A)
script_filtered = script_df[script_df['event_type'].isin(['dialog', 'narration', 'sign', 'S', 'C', 'E', 'A'])].copy()
script_filtered = script_filtered[~script_filtered['raw_text'].str.startswith('* -', na=False)].copy()
print(f"[OK] Filtered script to {len(script_filtered):,} actual in-game text entries")

# Count trainer battles
trainer_battles = script_filtered[script_filtered['event_type'].isin(['S', 'C', 'E', 'A'])]
print(f"     - Including {len(trainer_battles):,} trainer battle entries")

print("\n" + "=" * 80)
print("Creating Excel file...")
print("=" * 80)

# Create Excel file
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # Tab 1: LLM OCR outputs
    print("Writing Tab 1: LLM OCR Outputs...")
    llm_df.to_excel(writer, sheet_name='LLM OCR Outputs', index=False)

    # Tab 2: Filtered script
    print("Writing Tab 2: Script Database (Filtered)...")
    script_filtered.to_excel(writer, sheet_name='Script Database (Filtered)', index=False)

    # Tab 3: Full script
    print("Writing Tab 3: Script Database (Full)...")
    script_df.to_excel(writer, sheet_name='Script Database (Full)', index=False)

    # Tab 4: Trainer battles by type
    print("Writing Tab 4: Trainer Battles...")
    trainer_battles.to_excel(writer, sheet_name='Trainer Battles', index=False)

    # Tab 5: Regular dialogue (no trainers)
    regular_dialogue = script_filtered[script_filtered['event_type'].isin(['dialog', 'narration', 'sign'])]
    print(f"Writing Tab 5: Regular Dialogue ({len(regular_dialogue)} entries)...")
    regular_dialogue.to_excel(writer, sheet_name='Regular Dialogue', index=False)

print("\n" + "=" * 80)
print("[SUCCESS]")
print("=" * 80)
print(f"\nExcel file: {output_file}")
print(f"\nTabs:")
print(f"  1. LLM OCR Outputs: {len(llm_df):,} entries")
print(f"  2. Script Database (Filtered): {len(script_filtered):,} entries")
print(f"  3. Script Database (Full): {len(script_df):,} entries")
print(f"  4. Trainer Battles: {len(trainer_battles):,} entries (S={len(trainer_battles[trainer_battles['event_type']=='S'])}, C={len(trainer_battles[trainer_battles['event_type']=='C'])}, E={len(trainer_battles[trainer_battles['event_type']=='E'])}, A={len(trainer_battles[trainer_battles['event_type']=='A'])})")
print(f"  5. Regular Dialogue: {len(regular_dialogue):,} entries")
