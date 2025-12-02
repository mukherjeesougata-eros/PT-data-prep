def check_duplicate_ids(tsv_path):
    seen = set()
    duplicates = []

    with open(tsv_path, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            line = line.rstrip("\n")
            if not line.strip():
                continue  # skip blank lines

            parts = line.split("\t")
            if len(parts) < 1:
                continue

            uid = parts[0]  # first column = ID

            if uid in seen:
                duplicates.append((lineno, uid))
            else:
                seen.add(uid)

    if duplicates:
        print(f"❌ Found {len(duplicates)} duplicate IDs:\n")
        for lineno, uid in duplicates:
            print(f"Line {lineno}: {uid}")
    else:
        print("✔ No duplicate IDs found.")


# Example usage:
check_duplicate_ids("SYSPIN.tsv")

