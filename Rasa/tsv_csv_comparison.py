import csv

def load_csv_lines_with_lineno(csv_path):
    """
    Load lines from a CSV file and return a dict:
    line_string -> line_number
    """
    line_dict = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for lineno, row in enumerate(reader, start=1):
            line = ",".join(row).strip()
            if line:
                line_dict[line] = lineno
    return line_dict


def load_tsv_lines_with_lineno(tsv_path):
    """
    Load lines from a TSV file and return a dict:
    line_string -> line_number
    """
    line_dict = {}
    with open(tsv_path, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if line:
                line_dict[line] = lineno
    return line_dict


def compare(csv1, csv2, tsv):
    # Load files with line numbers
    csv1_lines = load_csv_lines_with_lineno(csv1)
    csv2_lines = load_csv_lines_with_lineno(csv2)
    tsv_lines  = load_tsv_lines_with_lineno(tsv)

    # Merge CSV sets
    all_csv_lines = {**csv1_lines, **csv2_lines}   # CSV1 takes priority, then CSV2

    # Sets of keys
    csv_set = set(all_csv_lines.keys())
    tsv_set = set(tsv_lines.keys())

    # Compute mismatches
    csv_not_in_tsv = sorted(csv_set - tsv_set)
    tsv_not_in_csv = sorted(tsv_set - csv_set)

    # Output
    print("========== LINES IN CSV BUT NOT IN TSV ==========")
    print(f"Count: {len(csv_not_in_tsv)}\n")
    for line in csv_not_in_tsv[:3]:
        lineno = all_csv_lines[line]
        print(f"(CSV line {lineno})  {line}")

    print("\n========== LINES IN TSV BUT NOT IN BOTH CSVs ==========")
    print(f"Count: {len(tsv_not_in_csv)}\n")
    for line in tsv_not_in_csv[:3]:
        lineno = tsv_lines[line]
        print(f"(TSV line {lineno})  {line}")


# ---------------------- USAGE ----------------------
compare("/data0/Sougata/Dataset/Rasa/Extracted_modified/Extracted/Assamese/train/manifest_train.csv", "/data0/Sougata/Dataset/Rasa/Extracted_modified/Extracted/Assamese/test/manifest_test.csv", "2.tsv")

