import csv
import sys

def detect_oversized_lines(filename, limit=131072):
    """
    Prints line number + full line whenever a field exceeds CSV max length.
    Default limit = Python's CSV field_size_limit (128 KB).
    """

    # Do NOT set csv.field_size_limit here, we want to manually detect violations.
    with open(filename, "r", encoding="utf-8", errors="replace") as f:
        for lineno, line in enumerate(f, start=1):

            # Strip newline for length measurement, but keep original for printing
            stripped = line.rstrip("\n")

            # Split fields manually
            fields = stripped.split("\t") if "\t" in stripped else stripped.split(",")

            for idx, field in enumerate(fields):
                if len(field) > limit:
                    print("\n❗ Oversized field detected")
                    print(f"Line number: {lineno}")
                    print(f"Field number: {idx+1}")
                    print(f"Field length: {len(field)} characters (limit = {limit})")
                    print(f"Full line:\n{line}")
                    break  # stop checking fields in this line


# ------------------- USAGE -------------------
detect_oversized_lines("3.tsv")

