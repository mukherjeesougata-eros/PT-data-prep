"""
Build an instruct-style JSONL for the L2-ARCTIC corpus.

For every wav file under  <SPEAKER>.zip_extracted/<SPEAKER>/wav/*.wav
it emits one JSON object per line:

    {"id": "arctic_a0537",
     "audio_path": "/mnt/.../ABA.zip_extracted/ABA/wav/arctic_a0537.wav",
     "text": "He was an enthusiast and a desert dweller",
     "instruct": "arabic accent"}

- text     -> read from <SPEAKER>/transcript/<id>.txt
- instruct -> "<native language> accent", taken from the speaker table in README.md
"""

import glob
import json
import os
import random
import re

ROOT = "/mnt/data0/Sougata/Dataset/TTS_data/L2Arctic"
README = os.path.join(ROOT, "README.md")
OUTPUT = os.path.join(ROOT, "l2arctic.jsonl")

# fixed seed so the random gender/accent ordering is reproducible across runs
SEED = 42

# native languages (accents) to exclude from the output
EXCLUDE_ACCENTS = {"spanish", "vietnamese", "arabic"}

# rename accents in the output (applied after the exclude filter)
ACCENT_MAP = {"hindi": "indian"}

# map the README gender code to a word used in the "instruct" field
GENDER_MAP = {"M": "male", "F": "female"}


def build_instruct(gender, accent):
    """Randomly order gender / accent, e.g. 'male, indian accent' or 'indian accent, male'."""
    parts = [gender, f"{accent} accent"]
    random.shuffle(parts)
    return ", ".join(parts)


def parse_speaker_table(readme_path):
    """Parse the |Speaker|Gender|Native Language|...| table in the README."""
    info = {}
    # matches rows like: |ABA|M|Arabic|1129|150|
    row = re.compile(r"^\|\s*([A-Z]{2,6})\s*\|\s*([MF])\s*\|\s*([A-Za-z ]+?)\s*\|")
    with open(readme_path, encoding="utf-8") as f:
        for line in f:
            m = row.match(line.strip())
            if not m:
                continue
            code, gender, native_lang = m.group(1), m.group(2), m.group(3)
            info[code] = {
                "gender": gender,                       # "M" / "F"  (parsed, available if needed)
                "accent": native_lang.strip().lower(),  # e.g. "arabic"
            }
    return info


def read_transcript(path):
    """Return the cleaned sentence from a transcript .txt file."""
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read().strip()
    # some corpora wrap the sentence in quotes / parens; strip defensively
    text = text.strip().strip('"').strip()
    return text


def main():
    random.seed(SEED)  # reproducible random ordering of gender/accent
    speakers = parse_speaker_table(README)
    print(f"Parsed {len(speakers)} speakers from README: {sorted(speakers)}")

    records = []
    missing_transcript = 0

    # iterate speakers in table order for deterministic output
    for code in sorted(speakers):
        accent = speakers[code]["accent"]
        if accent in EXCLUDE_ACCENTS:
            print(f"  [skip] {code}: '{accent} accent' excluded")
            continue
        accent = ACCENT_MAP.get(accent, accent)  # e.g. hindi -> indian
        gender = GENDER_MAP.get(speakers[code]["gender"], "")  # M -> male, F -> female
        wav_dir = os.path.join(ROOT, f"{code}.zip_extracted", code, "wav")
        transcript_dir = os.path.join(ROOT, f"{code}.zip_extracted", code, "transcript")

        if not os.path.isdir(wav_dir):
            print(f"  [skip] no wav dir for {code}: {wav_dir}")
            continue

        wavs = sorted(glob.glob(os.path.join(wav_dir, "*.wav")))
        kept = 0
        for wav_path in wavs:
            utt_id = os.path.splitext(os.path.basename(wav_path))[0]  # arctic_a0537
            txt_path = os.path.join(transcript_dir, utt_id + ".txt")

            if not os.path.isfile(txt_path):
                missing_transcript += 1
                continue  # tip in README: no transcript -> skip

            records.append({
                "id": f"{code}_{utt_id}",  # e.g. NJS_arctic_a0001
                "text": read_transcript(txt_path),
                "instruct": build_instruct(gender, accent),
            })
            kept += 1

        print(f"  {code:6} ({accent:10}): {kept} utterances")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"\n✅ Wrote {len(records)} records -> {OUTPUT}")
    if missing_transcript:
        print(f"⚠️  {missing_transcript} wav files had no matching transcript (skipped)")


if __name__ == "__main__":
    main()
