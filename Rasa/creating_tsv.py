import os
import csv
from pathlib import Path

# Base directory where text and audio files are located
BASE_DIR = Path("/data0/Sougata/Dataset/Rasa/Extracted_modified/Extracted")

# Output file path
OUT_FILE = "6.tsv"

# Define the function to generate the TSV file
def generate_tsv(base_dir, out_file):
    rows = []

    # Iterate through each language folder
    for lang_dir in base_dir.iterdir():
        if not lang_dir.is_dir() or lang_dir.name == "data":  # Skip the 'data' directory
            continue
        
        # Iterate through the 'train' and 'test' splits
        for split in ['train', 'test']:
            text_dir = lang_dir / split / "text" / lang_dir.name / split
            audio_dir = lang_dir / split / "audio" / lang_dir.name / split

            if not text_dir.exists() or not audio_dir.exists():
                continue

            # Iterate through each text file in the text directory
            for text_file in text_dir.glob("*.txt"):
                uniq_id = text_file.stem  # Remove the .txt extension
                text_content = text_file.read_text(encoding="utf-8").strip()

                # Find the corresponding .wav file
                wav_file = audio_dir / (uniq_id + ".wav")
                if wav_file.exists():
                    # Append the row with {uniq_id}, {text}, {wav_path}
                    wav_path = str(wav_file)
                    rows.append([uniq_id, text_content, wav_path])

    # Write the rows to the output TSV file
    with open(out_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerows(rows)

    print(f"✔ TSV file generated: {out_file}")


# Run the function to generate the TSV
generate_tsv(BASE_DIR, OUT_FILE)

