#!/usr/bin/env python3
import os, csv, shutil, glob, sys, pathlib
# os.environ["HF_HOME"] = "/data0/Sougata/Dataset/IndicVoices_r_cpy/hf"
# os.environ["HF_DATASETS_CACHE"] = "/data0/Sougata/Dataset/IndicVoices_r_cpy/hf/datasets"
# os.environ["HF_HUB_CACHE"] = "/data0/Sougata/Dataset/IndicVoices_r_cpy/hf/hub"
# os.environ["TMPDIR"] = "/data0/Sougata/Dataset/IndicVoices_r_cpy/tmp"
# pathlib.Path(os.environ["HF_DATASETS_CACHE"]).mkdir(parents=True, exist_ok=True)
# pathlib.Path(os.environ["HF_HUB_CACHE"]).mkdir(parents=True, exist_ok=True)
# pathlib.Path(os.environ["TMPDIR"]).mkdir(parents=True, exist_ok=True)
from pathlib import Path
os.environ["HF_HOME"] = "/data0/Sougata/Dataset/Rasa/hf"
os.environ["HF_DATASETS_CACHE"] = "/data0/Sougata/Dataset/Rasa/hf/datasets"
os.environ["HF_HUB_CACHE"] = "/data0/Sougata/Dataset/Rasa/hf/hub"
os.environ["TMPDIR"] = "/data0/Sougata/Dataset/Rasa/tmp"
pathlib.Path(os.environ["HF_DATASETS_CACHE"]).mkdir(parents=True, exist_ok=True)
pathlib.Path(os.environ["HF_HUB_CACHE"]).mkdir(parents=True, exist_ok=True)
pathlib.Path(os.environ["TMPDIR"]).mkdir(parents=True, exist_ok=True)
from tqdm import tqdm
from datasets import load_dataset, get_dataset_config_names, Audio, Dataset

# ========= CONFIG (edit these) =========
REPO_ID   = "ai4bharat/Rasa"
LOCAL_SRC = Path("/data0/Sougata/Dataset/Rasa")  # your hf download dir (root)
OUT_ROOT  = Path("/data0/Sougata/Dataset/Rasa/Extracted")
SPLITS    = ["train", "test"]
# ======================================

OUT_ROOT.mkdir(parents=True, exist_ok=True)

def guess_ext(path_basename: str | None, b: bytes | None) -> str:
    if path_basename:
        ext = Path(path_basename).suffix.lower()
        if ext:
            return ext
    if b:
        if b[:4] == b"RIFF": return ".wav"
        if b[:4] == b"fLaC": return ".flac"
        if b[:3] == b"ID3" or (len(b) > 2 and b[0] == 0xFF and (b[1] & 0xE0) == 0xE0): return ".mp3"
        if b[:4] == b"OggS": return ".ogg"
    return ".wav"

def try_resolve_path(basename: str) -> Path | None:
    p = Path(basename)
    if p.is_file():
        return p
    roots = [
        LOCAL_SRC,
        Path(os.environ.get("HF_DATASETS_CACHE", "/data0/Sougata/Dataset/Rasa")),
    ]
    for root in roots:
        if root and root.exists():
            hits = list(root.rglob(Path(basename).name))
            if hits:
                return hits[0]
    return None

def load_from_hub_or_none(lang: str, split: str):
    try:
        ds = load_dataset(REPO_ID, lang, split=split, cache_dir=os.environ["HF_DATASETS_CACHE"])  # no trust_remote_code
        ds = ds.cast_column("audio", Audio(decode=False))
        ds.set_format("python")
        return ds
    except Exception as e:
        print(f"    [hub miss] {lang}/{split}: {e}")
        return None

def find_local_parquet_files(lang: str, split: str):
    """Return a de-duplicated, sorted list of parquet files for lang/split."""
    # Map 'default' to root when we don't have per-language dirs
    lang_seg = lang if lang != "default" else ""
    patterns = [
        str(LOCAL_SRC / lang_seg / f"{split}-*.parquet"),
        str(LOCAL_SRC / lang_seg / "**" / f"{split}-*.parquet"),
        str(LOCAL_SRC / "**" / lang_seg / f"{split}-*.parquet") if lang_seg else str(LOCAL_SRC / "**" / f"{split}-*.parquet"),
    ]
    files = []
    for pat in patterns:
        files.extend(glob.glob(pat, recursive=True))
    files = sorted(set(files))
    return files

def extract_split_from_parquets(files, lang: str, split: str, out_root: Path):
    """Process each parquet shard individually (robust for huge train splits)."""
    split_out = out_root / lang / split
    (split_out / "audio").mkdir(parents=True, exist_ok=True)
    (split_out / "text").mkdir(parents=True, exist_ok=True)
    manifest_path = split_out / f"manifest_{split}.csv"

    written = 0
    with open(manifest_path, "w", newline="", encoding="utf-8") as mf:
        w = csv.writer(mf)
        w.writerow(["id", "audio_path", "text", "lang", "split"])

        global_index = 0
        for pf in tqdm(files, desc=f"{lang}:{split} shards", leave=False):
            try:
                ds = Dataset.from_parquet(pf)
            except Exception as e:
                print(f"    [skip shard] cannot read {pf}: {e}")
                continue

            # ensure columns exist
            if not {"audio", "text"}.issubset(ds.column_names):
                print(f"    [skip shard] missing columns in {pf}: {ds.column_names}")
                continue

            # TorchCodec-free: bytes/path only
            try:
                ds = ds.cast_column("audio", Audio(decode=False))
            except Exception:
                pass
            ds.set_format("python")

            for j in range(len(ds)):
                row = ds[j]
                a = row.get("audio") or {}
                b = a.get("bytes")
                p = a.get("path")
                text = row.get("text") or ""
                lang_value = row.get("lang") or lang

                base = f"sample_{global_index:09d}"
                global_index += 1

                ext  = guess_ext(p, b)
                audio_rel = Path("audio") / lang_value / split / f"{base}{ext}"
                text_rel  = Path("text")  / lang_value / split / f"{base}.txt"
                audio_abs = split_out / audio_rel
                text_abs  = split_out / text_rel

                # audio
                if b:
                    audio_abs.parent.mkdir(parents=True, exist_ok=True)
                    with open(audio_abs, "wb") as f:
                        f.write(b)
                else:
                    src = try_resolve_path(p) if p else None
                    if not src or not src.is_file():
                        continue
                    audio_abs = audio_abs.with_suffix(src.suffix)
                    audio_abs.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, audio_abs)
                    audio_rel = audio_rel.with_suffix(src.suffix)

                # text
                text_abs.parent.mkdir(parents=True, exist_ok=True)
                with open(text_abs, "w", encoding="utf-8") as f:
                    f.write(str(text))

                w.writerow([base, str(audio_rel).replace(os.sep, "/"), str(text), lang_value, split])
                written += 1

    print(f"    ✅ wrote {written} items → {split_out}")
    return written

def main():
    # Try hub configs; otherwise derive from local tree
    try:
        configs = get_dataset_config_names(REPO_ID)
        if not configs:
            raise RuntimeError("no configs from hub")
        print(f"Found {len(configs)} configs from hub: {configs}")
    except Exception:
        print("Hub configs not available; deriving configs from local tree...")
        configs = sorted({Path(p).parts[-2] for p in glob.glob(str(LOCAL_SRC / "**" / "train-*.parquet"), recursive=True)})
        if not configs:
            if glob.glob(str(LOCAL_SRC / "train-*.parquet")):
                configs = ["default"]
            else:
                print("No local parquets found. Please set LOCAL_SRC correctly.")
                sys.exit(2)
        print(f"Using local configs: {configs}")

    for lang in configs:
        print(f"\n=== {lang} ===")
        for split in SPLITS:
            # 1) Try the hub
            ds = load_from_hub_or_none(lang, split)
            if ds is not None:
                # Hub path succeeded → extract directly from hub dataset
                # (small splits are fine to load wholly)
                extract_dir = OUT_ROOT / lang / split
                (extract_dir / "audio").mkdir(parents=True, exist_ok=True)
                (extract_dir / "text").mkdir(parents=True, exist_ok=True)
                # Reuse the per-parquet extraction logic by creating a one-off in-memory loop
                # (keep the same manifest format)
                manifest = extract_dir / f"manifest_{split}.csv"
                written = 0
                with open(manifest, "w", newline="", encoding="utf-8") as mf:
                    w = csv.writer(mf)
                    w.writerow(["id", "audio_path", "text", "lang", "split"])
                    for i in tqdm(range(len(ds)), desc=f"{lang}:{split}", leave=False):
                        row = ds[i]
                        a = row.get("audio") or {}
                        b = a.get("bytes")
                        p = a.get("path")
                        text = row.get("text") or ""
                        lang_value = row.get("lang") or lang
                        base = f"sample_{i:09d}"
                        ext  = guess_ext(p, b)
                        audio_rel = Path("audio") / lang_value / split / f"{base}{ext}"
                        text_rel  = Path("text")  / lang_value / split / f"{base}.txt"
                        audio_abs = extract_dir / audio_rel
                        text_abs  = extract_dir / text_rel

                        if b:
                            audio_abs.parent.mkdir(parents=True, exist_ok=True)
                            with open(audio_abs, "wb") as f:
                                f.write(b)
                        else:
                            src = try_resolve_path(p) if p else None
                            if not src or not src.is_file():
                                continue
                            audio_abs = audio_abs.with_suffix(src.suffix)
                            audio_abs.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(src, audio_abs)
                            audio_rel = audio_rel.with_suffix(src.suffix)

                        text_abs.parent.mkdir(parents=True, exist_ok=True)
                        with open(text_abs, "w", encoding="utf-8") as f:
                            f.write(str(text))

                        w.writerow([base, str(audio_rel).replace(os.sep, "/"), str(text), lang_value, split])
                        written += 1
                print(f"    ✅ wrote {written} items → {extract_dir}")
                continue  # go to next split

            # 2) Hub failed → per-shard local fallback (robust for huge train)
            files = find_local_parquet_files(lang, split)
            if not files:
                print(f"    [skip] no local parquets for {lang}/{split}")
                continue
            extract_split_from_parquets(files, lang, split, OUT_ROOT)

if __name__ == "__main__":
    main()
