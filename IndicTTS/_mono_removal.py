import csv

input_file = "consolidated_output.tsv"
output_file = "IT.tsv"

with open(input_file, "r", encoding="utf-8") as fin, \
     open(output_file, "w", encoding="utf-8", newline="") as fout:

    reader = csv.reader(fin, delimiter="\t")
    writer = csv.writer(fout, delimiter="\t")

    for row in reader:
        if len(row) < 3:
            writer.writerow(row)
            continue

        path = row[2]
        parts = path.split("/")

        if len(parts) >= 2:
            # last-but-one directory
            d = parts[-2]  # e.g. Hindi_male_mono_audio

            # remove only the _mono that sits before _audio
            d = d.replace("_mono_audio", "_audio")

            parts[-2] = d

        row[2] = "/".join(parts)
        writer.writerow(row)

print("✔ Done. Output saved to", output_file)

