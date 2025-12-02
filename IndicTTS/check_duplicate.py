def check_duplicate_lines(tsv_path):
    seen = set()
    duplicates = []

    with open(tsv_path, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            line = line.rstrip("\n")
            if line in seen:
                duplicates.append((lineno, line))
            else:
                seen.add(line)

    if duplicates:
        print(f"Found {len(duplicates)} duplicate lines:\n")
        for lineno, dup in duplicates:
            print(f"Line {lineno}: {dup}")
    else:
        print("No duplicate lines found.")

# Example usage:
check_duplicate_lines("1_m.tsv")

