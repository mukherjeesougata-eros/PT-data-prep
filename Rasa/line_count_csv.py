import csv
from pathlib import Path

BASE = Path("/data0/Sougata/Dataset/Rasa/Extracted_modified/Extracted")

def fix_and_count(csv_path):
    fixed_lines = []
    buffer = ""

    with open(csv_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")

            # split by comma manually; CSV field may contain commas, but the
            # important rule is: valid rows always have >= 5 columns
            cols = line.split(",")

            if len(cols) < 5:
                # broken row → accumulate
                buffer = (buffer + " " + line).strip()
                continue

            # when we reach a valid >=5-column row:
            if buffer:
                fixed_lines.append(buffer + " " + line)
                buffer = ""
            else:
                fixed_lines.append(line)

        # leftover partial
        if buffer:
            fixed_lines.append(buffer)

    # output count
    return len(fixed_lines)


def main():
    base = Path("/data0/Sougata/Dataset/Rasa/Extracted_modified/Extracted")

    for csv_file in base.rglob("manifest_*.csv"):
        count = fix_and_count(csv_file)
        print(f"{csv_file}: {count}")

if __name__ == "__main__":
    main()

