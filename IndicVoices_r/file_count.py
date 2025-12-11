import os

BASE_DIR = "/data0/Sougata/Dataset/IndicVoices_r/Extracted_modified"

LANG_CODES = {
    "Assamese": "as", "Bengali": "bn", "Bodo": "brx", "Dogri": "doi",
    "Gujarati": "gu", "Kannada": "kn", "Konkani": "kok", "Maithili": "mai",
    "Malayalam": "ml", "Marathi": "mr", "Nepali": "ne", "Odia": "or",
    "Punjabi": "pa", "Sanskrit": "sa", "Tamil": "ta", "Telugu": "te"
}

SPLITS = ["train", "test"]

def count_files():
    for language, lang_code in LANG_CODES.items():
        print(f"\n===== {language} ({lang_code}) =====")

        for split in SPLITS:
            audio_dir = os.path.join(BASE_DIR, language, split, "audio", lang_code, split)
            text_dir  = os.path.join(BASE_DIR, language, split, "text", lang_code, split)

            audio_count = len(os.listdir(audio_dir)) if os.path.exists(audio_dir) else 0
            text_count  = len(os.listdir(text_dir))  if os.path.exists(text_dir) else 0

            print(f"  [{split}]  Audio files: {audio_count},  Text files: {text_count}")

if __name__ == "__main__":
    count_files()

