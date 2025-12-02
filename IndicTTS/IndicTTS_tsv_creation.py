#!/usr/bin/env python3
import os
from pathlib import Path
import csv

BASE = Path("/data0/Sougata/Dataset/IndicTTS")
OUT_FILE = "consolidated_output_o.tsv"

def process_file(txt_path: Path, writer):
    lang_dir = txt_path.parent.name.replace(".txt", "")
    audio_dir = BASE / (lang_dir + "_audio")

    with txt_path.open("r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t", 1)
            if len(parts) != 2:
                continue

            filename_txt, text = parts
            uniq_id = filename_txt.replace(".txt", "")
            wav_path = str(audio_dir / (uniq_id + ".wav"))

            writer.writerow([uniq_id, text, wav_path])

def main():
    txt_files = list(BASE.rglob("*.txt"))

    with open(OUT_FILE, "w", encoding="utf-8", newline="") as out_f:
        writer = csv.writer(out_f, delimiter="\t")
        for txt_file in txt_files:
            process_file(txt_file, writer)

    print(f"✅ Consolidated TSV written to: {OUT_FILE}")

if __name__ == "__main__":
    main()

