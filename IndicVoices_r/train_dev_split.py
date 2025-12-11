import random
import csv
import csv
import sys
csv.field_size_limit(sys.maxsize)

# Function to split the TSV file
def split_tsv(input_file, train_file, test_file, train_ratio=0.9):
    # Read the entire file into a list of rows
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter='\t')
        rows = list(reader)
    
    # Shuffle the rows to randomize them
    random.shuffle(rows)
    
    # Calculate the index to split the data
    split_index = int(len(rows) * train_ratio)
    
    # Split into train and test sets
    train_data = rows[:split_index]
    test_data = rows[split_index:]
    
    # Write the training set to the train_file
    with open(train_file, 'w', encoding='utf-8', newline='') as train:
        writer = csv.writer(train, delimiter='\t')
        writer.writerows(train_data)
    
    # Write the test set to the test_file
    with open(test_file, 'w', encoding='utf-8', newline='') as test:
        writer = csv.writer(test, delimiter='\t')
        writer.writerows(test_data)

    print(f"Training set saved to {train_file}")
    print(f"Test set saved to {test_file}")

# Example usage
input_file = '1.tsv'
train_file = 'custom_train.tsv'
test_file = 'custom_dev.tsv'

split_tsv(input_file, train_file, test_file)

