import os
from glob import glob

LANG_CODES = {
   "Hindi": "hi",
   "Kashmiri": "ks",
   "Manipuri": "mni",
   "Santali": "sat",
   "Sindhi": "sd",
   "Urdu": "ur",
   }

BASE_DIR = "/data0/Sougata/Dataset/IndicVoices_r/Extracted_modified"
SPLITS = ["train", "test"]  # Add "dev" if needed


def rename_files():
    for lang_name, lang_code in LANG_CODES.items():
        lang_dir = os.path.join(BASE_DIR, lang_name)

        if not os.path.exists(lang_dir):
            print(f"⚠ Skipping missing language folder: {lang_dir}")
            continue

        for split in SPLITS:
            audio_dir = os.path.join(lang_dir, split, "audio", lang_code, split)
            text_dir = os.path.join(lang_dir, split, "text", lang_code, split)

            if not os.path.exists(audio_dir) or not os.path.exists(text_dir):
                print(f"⚠ Missing split folder for {lang_code} - {split}")
                continue

            print(f"🔁 Processing: {lang_code} | split: {split}")

            # Process WAV files
            wav_files = sorted(glob(os.path.join(audio_dir, "*.wav")))
            for idx, wav_file in enumerate(wav_files, start=1):
                new_name = f"IV_{lang_code}_{split}_sample_{idx}.wav"
                new_path = os.path.join(audio_dir, new_name)
                os.rename(wav_file, new_path)

            # Process TXT files
            txt_files = sorted(glob(os.path.join(text_dir, "*.txt")))
            for idx, txt_file in enumerate(txt_files, start=1):
                new_name = f"IV_{lang_code}_{split}_sample_{idx}.txt"
                new_path = os.path.join(text_dir, new_name)
                os.rename(txt_file, new_path)

            print(f"✔ Done renaming for {lang_code} {split}")

    print("🎉 All renaming completed successfully!")


if __name__ == "__main__":
    rename_files()

