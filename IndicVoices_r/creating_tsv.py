import os
import csv
from glob import glob

BASE_DIR = "/data0/Sougata/Dataset/IndicVoices_r/Extracted_modified"
OUTPUT_TSV = "/data0/Sougata/Dataset/IndicVoices_r/Extracted_modified/1.tsv"

LANG_CODES = {
    "Assamese": "as",
    "Bengali": "bn",
    "Bodo": "brx",
    "Dogri": "doi",
    "Gujarati": "gu",
    "Hindi": "hi",
    "Kannada": "kn",
    "Kashmiri": "ks",
    "Konkani": "kok",
    "Maithili": "mai",
    "Malayalam": "ml",
    "Manipuri": "mni",
    "Marathi": "mr",
    "Nepali": "ne",
    "Odia": "or",
    "Punjabi": "pa",
    "Sanskrit": "sa",
    "Santali": "sat",
    "Sindhi": "sd",
    "Tamil": "ta",
    "Telugu": "te",
    "Urdu": "ur",
}

SPLITS = ["train", "test"]


def create_tsv():
    rows = []

    for language, lang_code in LANG_CODES.items():
        lang_path = os.path.join(BASE_DIR, language)

        if not os.path.exists(lang_path):
            print(f"⚠ Language folder missing, skipping: {language}")
            continue

        for split in SPLITS:
            audio_dir = os.path.join(lang_path, split, "audio", lang_code, split)
            text_dir = os.path.join(lang_path, split, "text", lang_code, split)

            if not os.path.exists(audio_dir) or not os.path.exists(text_dir):
                print(f"⚠ Missing split folders for {language}-{split}, skipping...")
                continue

            wav_files = sorted(glob(os.path.join(audio_dir, "*.wav")))

            for wav_path in wav_files:
                uniq_id = os.path.splitext(os.path.basename(wav_path))[0]
                txt_path = os.path.join(text_dir, uniq_id + ".txt")

                if not os.path.exists(txt_path):
                    print(f"❌ Missing text file for {uniq_id}, skipping...")
                    continue

                # Read transcription
                with open(txt_path, "r", encoding="utf-8") as f:
                    text = f.read().strip()

                # Construct entry
                rows.append([uniq_id, text, wav_path])

            print(f"✔ Processed {language}-{split}, entries: {len(rows)} total so far")

    # Write TSV
    with open(OUTPUT_TSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerows(rows)

    print(f"🎉 TSV file created successfully at: {OUTPUT_TSV}")
    print(f"📌 Total entries written: {len(rows)}")


if __name__ == "__main__":
    create_tsv()

