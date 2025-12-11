import csv
from collections import defaultdict

# Mapping of language codes
LANG_CODES = {
    "as", "bn", "brx", "doi", "gu", "kn", "kok", "mai",
    "ml", "mr", "ne", "or", "pa", "sa", "ta", "te"
}

SPLITS = {"train", "test"}

def count_lines_by_lang_split(tsv_file):
    counts = defaultdict(int)

    with open(tsv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        
        for row in reader:
            if len(row) == 0:
                continue
            
            uniq_id = row[0]  # first column e.g. IV_as_train_sample_00001
            parts = uniq_id.split("_")

            if len(parts) < 4 or parts[0] != "IV":
                continue  # Skip malformed lines

            lang_code = parts[1]
            split = parts[2]

            if lang_code in LANG_CODES and split in SPLITS:
                key = f"{lang_code}_{split}"
                counts[key] += 1

    return counts


# Example usage
tsv_path = "1.tsv"  # replace with your .tsv path
result = count_lines_by_lang_split(tsv_path)

# Print results
for key, value in sorted(result.items()):
    lang_code, split = key.split("_")
    print(f"Language: {lang_code}, Split: {split}, Count: {value}")

