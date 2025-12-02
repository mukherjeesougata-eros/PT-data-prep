def remove_blank_lines(input_tsv, output_tsv):
    with open(input_tsv, "r", encoding="utf-8") as fin, \
         open(output_tsv, "w", encoding="utf-8", newline="") as fout:

        for line in fin:
            # Strip spaces, tabs, and newlines
            if line.strip() != "":
                fout.write(line)

    print(f"✔ Removed blank lines. Clean file saved to: {output_tsv}")


# Example usage:
remove_blank_lines("4.tsv", "5.tsv")

