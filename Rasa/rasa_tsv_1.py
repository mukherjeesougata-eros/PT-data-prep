import csv
from pathlib import Path

BASE = Path("/data0/Sougata/Dataset/Rasa/Extracted")
OUT = Path("3.tsv")

LANGMAP = {
    "Assamese": "as", "Bengali": "bn", "Bodo": "brx", "Dogri": "doi",
    "Gujarati": "gu", "Kannada": "kn", "Konkani": "kok", "Maithili": "mai",
    "Malayalam": "ml", "Marathi": "mr", "Nepali": "ne", "Odia": "or",
    "Punjabi": "pa", "Sanskrit": "sa", "Tamil": "ta", "Telugu": "te"
}

rows = []

def read_csv_fix_newlines(csv_path):
    """
    Fixes CSV lines where a newline appears before a line starting with ".
    Returns a list of cleaned CSV lines.
    """
    fixed_lines = []
    with open(csv_path, "r", encoding="utf-8") as f:
        prev = ""
        for line in f:
            line = line.rstrip("\n")

            if line.startswith('"') and prev:
                # append this to previous line, remove newline
                prev += " " + line
            else:
                if prev:
                    fixed_lines.append(prev)
                prev = line

        if prev:
            fixed_lines.append(prev)

    return fixed_lines


for lang_dir in BASE.iterdir():
    if not lang_dir.is_dir():
        continue

    lang_code = LANGMAP.get(lang_dir.name)
    if lang_code is None:
        print(f"Skipping unknown language: {lang_dir.name}")
        continue

    for split in ["train", "test"]:
        split_dir = lang_dir / split
        if not split_dir.exists():
            continue

        # find ANY .csv file inside split/
        csv_files = list(split_dir.glob("*.csv"))
        if not csv_files:
            print(f"No CSV found in: {split_dir}")
            continue

        csv_file = csv_files[0]
        print(f"Processing {csv_file}")

        prefix = f"{BASE}/{lang_dir.name}/{split}/"

        # read CSV with newline fixes
        cleaned_lines = read_csv_fix_newlines(csv_file)
        reader = csv.reader(cleaned_lines)

        next(reader, None)  # skip header

        for row in reader:
            if len(row) < 5:
                continue

            id, audio_path, text, lang, splitcol = row

            uniq_id = f"Ra_{lang_code}_{split}_{id}"

            # modify audio path → replace last filename with {uniq_id}.wav
            path_parts = audio_path.split("/")
            path_parts[-1] = uniq_id + ".wav"

            wav_path = prefix + "/".join(path_parts)

            # ---- FIX INTERNAL TABS IN TEXT ----
            # Replace all tabs inside text with ONE space
            text_clean = text.replace("\t", " ")

            # Build row manually:
            # uniq_id <TAB> text <TAB> wav_path
            rows.append(f"{uniq_id}\t{text_clean}\t{wav_path}")


# Write to output TSV
with open(OUT, "w", encoding="utf-8") as f:
    for line in rows:
        f.write(line + "\n")

print(f"✔ TSV written to {OUT} with {len(rows)} rows")

