#!/usr/bin/env python3
"""
Build a TSV with rows: {uniq_id}\t{text}\t{wav_path}

- WAVs live under:
  /data0/Sougata/Dataset/SYSPIN/IISc_SYSPIN_Data/IISc_SYSPINProject_Bengali_Female_Spk001_NHC/wav

- Transcripts come from a JSON file with structure:
  {
    "MetaData": {...},
    "SpeakersMetaData": {...},
    "Transcripts": {
        "<uniq_id>": {"Transcript": "<text>", "Domain": "..."},
        ...
    }
  }

Usage:
  python make_bn_tsv.py /path/to/transcripts.json [--wav-dir WAV_DIR] [--out out.tsv]

Defaults:
  --wav-dir is the path above
  --out is bengali.tsv
"""

import argparse
import json
from pathlib import Path
import csv
import sys

DEFAULT_WAV_DIR = "/data0/Sougata/Dataset/SYSPIN/IISc_SYSPIN_Data/IISc_SYSPINProject_Bengali_Female_Spk001_NHC/wav"
DEFAULT_OUT = "bengali.tsv"

def load_transcripts(json_path: Path) -> dict[str, str]:
    """Return {uniq_id: transcript_text} from the JSON."""
    try:
        data = json_path.read_text(encoding="utf-8")
        obj = json.loads(data)
    except Exception as e:
        print(f"[ERROR] Failed to read/parse JSON: {json_path}\n  {e}", file=sys.stderr)
        sys.exit(1)

    if "Transcripts" not in obj or not isinstance(obj["Transcripts"], dict):
        print(f"[ERROR] JSON missing 'Transcripts' dict.", file=sys.stderr)
        sys.exit(1)

    out: dict[str, str] = {}
    for uid, payload in obj["Transcripts"].items():
        if not isinstance(payload, dict):
            continue
        text = payload.get("Transcript")
        if isinstance(text, str):
            out[uid] = " ".join(text.splitlines()).strip()
    return out

def build_tsv(json_path: Path, wav_dir: Path, out_path: Path) -> None:
    transcripts = load_transcripts(json_path)

    if not wav_dir.is_dir():
        print(f"[ERROR] WAV directory not found: {wav_dir}", file=sys.stderr)
        sys.exit(1)

    rows = []
    missing_text = []
    # Use rglob to be safe if there are nested folders
    for wav in wav_dir.rglob("*.wav"):
        uid = wav.stem  # filename without .wav
        text = transcripts.get(uid)
        if text is None:
            missing_text.append(uid)
            continue
        rows.append((uid, text, str(wav)))

    # Write TSV
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
        for uid, text, wav_path in rows:
            writer.writerow([uid, text, wav_path])

    # Diagnostics
    print(f"[OK] Wrote {len(rows)} rows -> {out_path}")
    if missing_text:
        print(f"[WARN] Missing transcript for {len(missing_text)} WAVs (first 10): {missing_text[:10]}", file=sys.stderr)

    # Any transcripts without matching WAV?
    matched_ids = {uid for uid, _, _ in rows}
    orphans = sorted(set(transcripts.keys()) - matched_ids)
    if orphans:
        print(f"[WARN] Transcripts with no matching WAV: {len(orphans)} (first 10): {orphans[:10]}", file=sys.stderr)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json", type=Path, help="Path to transcripts JSON")
    ap.add_argument("--wav-dir", type=Path, default=Path(DEFAULT_WAV_DIR), help="Root directory containing WAV files")
    ap.add_argument("--out", type=Path, default=Path(DEFAULT_OUT), help="Output TSV path")
    args = ap.parse_args()

    build_tsv(args.json, args.wav_dir, args.out)

if __name__ == "__main__":
    main()





