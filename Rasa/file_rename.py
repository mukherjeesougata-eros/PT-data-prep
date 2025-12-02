#!/usr/bin/env python3
import sys
from pathlib import Path

# Base containing language folders (Assamese, Bengali, ...)
BASE = Path("/data0/Sougata/Dataset/Rasa/Extracted")

# Map top-level language folder name -> language code used in the prefix
NAME_TO_CODE = {
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
    "Manipuri": "mni",
    "Marathi": "mr",
    "Malayalam": "ml",
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

AUDIO_EXTS = {".wav", ".flac", ".mp3", ".ogg"}
TEXT_EXTS  = {".txt"}

def rename_under(root: Path, prefix: str, valid_exts: set[str]) -> tuple[int, int]:
    """Recursively rename files under 'root', prefixing with 'prefix'.
       Returns (scanned_files, renamed_files)."""
    seen = renamed = 0
    if not root.exists():
        return seen, renamed
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        seen += 1
        if valid_exts and p.suffix.lower() not in valid_exts:
            continue
        if p.name.startswith(prefix):
            continue
        try:
            p.rename(p.with_name(prefix + p.name))
            renamed += 1
        except Exception as e:
            print(f"[warn] failed to rename {p}: {e}")
    return seen, renamed

def process_language(lang_name: str):
    code = NAME_TO_CODE.get(lang_name)
    if not code:
        print(f"[warn] No code mapping for '{lang_name}'. Skipping.")
        return

    prefix = f"Ra_{code}_"
    print(f"\n=== {lang_name} (code={code}) ===")

    totals = {"a_seen":0, "a_ren":0, "t_seen":0, "t_ren":0}

    for split in ("train", "test"):
        # *** EXACT PATH SHAPE YOU SPECIFIED ***
        audio_root = BASE / lang_name / split / "audio" / lang_name / split
        text_root  = BASE / lang_name / split / "text"  / lang_name / split

        a_seen, a_ren = rename_under(audio_root, prefix, AUDIO_EXTS)
        t_seen, t_ren = rename_under(text_root,  prefix, TEXT_EXTS)

        totals["a_seen"] += a_seen; totals["a_ren"] += a_ren
        totals["t_seen"] += t_seen; totals["t_ren"] += t_ren

        print(f"  [{split}]")
        print(f"    audio_root: {audio_root}  -> scanned={a_seen}, renamed={a_ren}")
        print(f"    text_root : {text_root}   -> scanned={t_seen}, renamed={t_ren}")

    print(f"  -> SUMMARY audio: {totals['a_ren']}/{totals['a_seen']}  "
          f"text: {totals['t_ren']}/{totals['t_seen']}")

def main():
    if not BASE.exists():
        print(f"[error] Base path not found: {BASE}")
        sys.exit(2)

    languages = sorted([p.name for p in BASE.iterdir() if p.is_dir()])
    if not languages:
        print(f"[error] No language folders under {BASE}")
        sys.exit(2)

    print(f"Discovered languages: {languages}")
    for lang_name in languages:
        process_language(lang_name)

if __name__ == "__main__":
    main()



