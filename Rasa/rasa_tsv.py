import csv
from pathlib import Path

BASE = Path("/data0/Sougata/Dataset/Rasa/Extracted")
OUT = Path("1.tsv")

LANGMAP = {
    "Assamese": "as", "Bengali": "bn", "Bodo": "brx", "Dogri": "doi",
    "Gujarati": "gu", "Kannada": "kn", "Konkani": "kok", "Maithili": "mai",
    "Malayalam": "ml", "Marathi": "mr", "Nepali": "ne", "Odia": "or",
    "Punjabi": "pa", "Sanskrit": "sa", "Tamil": "ta", "Telugu": "te"
}

rows = []

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

        # find ANY .csv file inside train/ or test/
        csv_files = list(split_dir.glob("*.csv"))
        if not csv_files:
            print(f"No CSV found in: {split_dir}")
            continue

        csv_file = csv_files[0]
        print(f"Processing {csv_file}")

        prefix = f"{BASE}/{lang_dir.name}/{split}/"

        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.reader(f)

            # skip header
            header = next(reader, None)

            for row in reader:
                if len(row) < 5:
                    continue

                id, audio_path, text, lang, splitcol = row

                uniq_id = f"Ra_{lang_code}_{split}_{id}"

                # modify audio path → replace last filename with {uniq_id}.wav
                path_parts = audio_path.split("/")
                path_parts[-1] = uniq_id + ".wav"

                wav_path = prefix + "/".join(path_parts)

                rows.append([uniq_id, text, wav_path])

with open(OUT, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerows(rows)

print(f"✔ TSV written to {OUT} with {len(rows)} rows")

