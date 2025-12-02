import os

# Base directory
BASE_DIR = "/data0/Sougata/Dataset/Rasa/Extracted_modified/Extracted"

def find_languages_with_sample_files():
    # Iterate over all language directories
    for lang_dir in os.listdir(BASE_DIR):
        lang_path = os.path.join(BASE_DIR, lang_dir)
        
        # Check if it's a directory
        if not os.path.isdir(lang_path):
            continue

        # Iterate over 'train' and 'test' splits
        for split in ['train', 'test']:
            text_dir = os.path.join(lang_path, split, 'text', lang_dir, split)
            audio_dir = os.path.join(lang_path, split, 'audio', lang_dir, split)
            
            # Check if text and audio directories exist
            if not os.path.exists(text_dir) or not os.path.exists(audio_dir):
                continue

            # Check if there are .txt and .wav files starting with 'sample_'
            txt_files = [f for f in os.listdir(text_dir) if f.endswith('.txt') and f.startswith('sample_')]
            wav_files = [f for f in os.listdir(audio_dir) if f.endswith('.wav') and f.startswith('sample_')]

            # If both text and audio files are found, print the language
            if txt_files and wav_files:
                print(f"Language: {lang_dir}")

# Run the function
find_languages_with_sample_files()

