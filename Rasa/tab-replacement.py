def replace_tabs_in_tsv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8', newline='') as outfile:

        for line in infile:
            # Split the line into columns based on tab
            columns = line.strip().split('\t')
            
            # If there are more than 2 columns, replace intermediate tabs with spaces
            if len(columns) > 3:
                # Keep the first and last column as is, replace tabs between them with space
                new_line = columns[0] + '\t' + ' '.join(columns[1:-1]) + '\t' + columns[-1]
            else:
                # If only one or two columns, just keep the line as is
                new_line = line.strip()

            # Write the new line to the output file
            outfile.write(new_line + '\n')

    print(f"✔ Output written to {output_file}")

# Example usage:
replace_tabs_in_tsv("7.tsv", "8.tsv")

