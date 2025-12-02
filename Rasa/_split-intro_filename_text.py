import os
from pathlib import Path

BASE = Path("/data0/Sougata/Dataset/Rasa/Extracted_modified/Extracted")

def rename_files(base_dir):
    for lang_dir in base_dir.iterdir():
        if not lang_dir.is_dir():
            continue

        for split in ["train", "test"]:
            audio_dir = lang_dir / split / "text" / lang_dir.name / split

            if not audio_dir.exists():
                print(f"Skipping missing directory: {audio_dir}")
                continue

            print(f"\nProcessing: {audio_dir}")

            for wav in audio_dir.glob("*.txt"):
                old = wav.name  # e.g., Ra_as_sample_000028527.wav

                # Expect format: Ra_{langcode}_sample_{id}.wav
                parts = old.split("_")

                if len(parts) < 4 or not parts[0] == "Ra":
                    print(f"Skipping unrecognized filename: {old}")
                    continue

                lang_code = parts[1]
                sample_id = parts[-1]  # e.g., 000028527.wav

                new = f"Ra_{lang_code}_{split}_sample_{sample_id}"

                new_path = wav.parent / new

                wav.rename(new_path)
                print(f"{old} → {new}")

    print("\n✔ All renames completed.")


rename_files(BASE)
