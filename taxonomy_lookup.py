import csv

# Open the CSV file containing the lookup keys in read mode
with open('taxonomy.csv', mode='r') as keys_file:
    # Create a CSV reader object and set the delimiter to tabs
    keys_reader = csv.reader(keys_file, delimiter=',')

    # Create an empty list to store the lookup keys
    rows = []

    # Iterate over each row in the keys file and add the keys to the list
    for row in keys_reader:
        if len(row[1].split('~')) > 1:
            rows.append(row)

# Open the CSV file containing the data to be looked up in read mode
with open('db_taxonomy.csv', mode='r') as data_file:
    # Create a CSV reader object and set the delimiter to tabs
    data_reader = csv.reader(data_file, delimiter=',')

    # Create an empty dictionary to store the data
    data = {}

    # Iterate over each row in the data file
    for row in data_reader:
        # Use the first column as the key and the second column as the value
        key = row[0] + '~' + row[1]
        value = row

        # Add the key-value pair to the dictionary
        data[key] = value

# Open the keys file again, this time in write mode
with open('blastn_taxonomy.csv', mode='w', newline='') as keys_file:
    # Create a CSV writer object and set the delimiter to tabs
    keys_writer = csv.writer(keys_file, delimiter=',')

    # Add column names
    value = ['query_id', 'subject_id', '%identity', 'alignment_length', 'mismatches', 'gap_open', 'q_start', 'q_end',
             's_start', 's_end', 'evalue', 'bit_score', 'prokaryote/virus/eukaryote', 'database_identifier', 'taxonomy',
             'TRUE/FALSE', 'ref_seq_no']
    keys_writer.writerow(value)

    # Iterate over the lookup keys and perform a lookup in the data dictionary
    for row in rows:
        # need p~22609 from p~22609~1527~lcl|NZ_CP054306.1_rrna_28~~1489~27 which is in column 2
        key = row[1].split('~')[0] + '~' + row[1].split('~')[1]
        value = list(row + data[key])

        # Write a new row to the keys file with the key and the lookup value
        keys_writer.writerow(value)


