import csv
from pydub.utils import mediainfo

def get_audio_duration(audio_path):
    """Returns the duration of the audio in seconds. Returns 0.0 if file is empty or invalid."""
    try:
        # Get audio file info using pydub's mediainfo
        info = mediainfo(audio_path)
        duration = float(info['duration'])  # Duration in seconds
        return duration
    except Exception as e:
        # If there's an error (e.g., invalid file), return 0.0
        print(f"Error reading {audio_path}: {e}")
        return 0.0

def filter_audio_tsv(input_tsv, output_tsv):
    rows_to_keep = []

    with open(input_tsv, 'r', encoding='utf-8') as infile, \
         open(output_tsv, 'w', encoding='utf-8', newline='') as outfile:
        
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')

        for row in reader:
            if len(row) < 3:
                continue  # Skip rows with less than 3 columns
            
            audio_path = row[2]  # 3rd column contains the path to the audio file

            # Get the audio file duration
            duration = get_audio_duration(audio_path)

            if duration != 0.0:
                rows_to_keep.append(row)

        # Write the filtered rows to the output TSV
        writer.writerows(rows_to_keep)

    print(f"✔ Filtered TSV saved to {output_tsv}")

# Example usage:
input_file = '8.tsv'  # Replace with your input file path
output_file = '9.tsv'  # Replace with your output file path

filter_audio_tsv(input_file, output_file)

