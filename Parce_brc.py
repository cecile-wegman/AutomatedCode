

import csv
import argparse
import os

# Argument parsing for the input file and optional encoding
parser = argparse.ArgumentParser(description='Parse bam-readcount output file.')
parser.add_argument('input_file', help='Input bam-readcount TSV file')
parser.add_argument('--encoding', default='utf-16-le', help='File encoding (default: utf-16-le)')
args = parser.parse_args()

# Define fields for per-base data from bam-readcount
base_fields = [
    'base', 'count', 'avg_mapping_quality', 'avg_basequality',
    'avg_se_mapping_quality', 'num_plus_strand', 'num_minus_strand',
    'avg_pos_as_fraction', 'avg_num_mismatches_as_fraction',
    'avg_sum_mismatch_qualities', 'num_q2_containing_reads',
    'avg_distance_to_q2_start_in_q2_reads', 'avg_clipped_length',
    'avg_distance_to_effective_3p_end'
]

# Create the output file name based on the input file
input_filename = os.path.basename(args.input_file)
output_filename = f"{os.path.splitext(input_filename)[0]}_parsed_output.tsv"

# Initialize variables to track max number of insertions and deletions
max_insertions = 0
max_deletions = 0

# First pass: scan to determine maximum insertions and deletions across all positions
with open(args.input_file, encoding=args.encoding) as infile:
    reader = csv.reader(infile, delimiter='\t')
    
    # Process each line in the bam-readcount output
    for line in reader:
        insertion_count = 0
        deletion_count = 0
        
        # Iterate over each base data string in the line
        for base_data_string in line[4:]:
            base_values = base_data_string.split(':')
            base_data = dict(zip(base_fields, base_values))
            base = base_data['base'].upper()
            count = int(base_data['count'])

            # Check for insertion (+) or deletion (-)
            if count > 0:
                if base.startswith('+'):
                    insertion_count += 1
                elif base.startswith('-'):
                    deletion_count += 1

        # Update max insertion and deletion counts
        max_insertions = max(max_insertions, insertion_count)
        max_deletions = max(max_deletions, deletion_count)

# Second pass: now write the output with the correct number of columns
with open(args.input_file, encoding=args.encoding) as infile, open(output_filename, 'w', newline='') as outfile:
    reader = csv.reader(infile, delimiter='\t')
    writer = csv.writer(outfile, delimiter='\t')

    # Create the header
    header = ['chrom', 'position', 'wildtype', 'single base mutation', 'A count', 'T count', 'G count', 'C count', 'Total count', 'Frequency wildtype', 'Frequency mutation']
    
    # Add the columns for insertions and deletions based on max_insertions and max_deletions
    for i in range(1, max_insertions + 1):
        header.append(f'Insertion {i}')
        header.append(f'Insertion {i} count')

    for i in range(1, max_deletions + 1):
        header.append(f'Deletion {i}')
        header.append(f'Deletion {i} count')

    # Write the header
    writer.writerow(header)

    # Process each line in the bam-readcount output again
    for line in reader:
        fields = line[:4]  # Chromosome, position, reference base, depth
        chrom, position, wildtype, total_count = fields[:4]
        
        # Convert wildtype to uppercase to handle lowercase input
        wildtype = wildtype.upper()

        # Initialize counts for each nucleotide and list for insertion/deletion details
        a_count = t_count = g_count = c_count = 0
        wildtype_count = 0
        mutation = 'No mutation'  # Default value if no mutation
        mutation_count = 0
        insertion_details = []  # List to store insertion details (sequence, count)
        deletion_details = []  # List to store deletion details (sequence, count)
        total_insertion_deletion_count = 0
        indel_present = False  # Flag to track presence of indels

        # Iterate over each base data string in the line
        for base_data_string in line[4:]:
            base_values = base_data_string.split(':')
            base_data = dict(zip(base_fields, base_values))
            base = base_data['base'].upper()  # Convert base to uppercase
            count = int(base_data['count'])  # Count of this base

            # Update nucleotide counts
            if base == 'A':
                a_count += count
            elif base == 'T':
                t_count += count
            elif base == 'G':
                g_count += count
            elif base == 'C':
                c_count += count

            # Check for wildtype
            if base == wildtype:
                wildtype_count = count

            # Check for insertion (+) or deletion (-)
            elif base.startswith('+'):
                insertion_details.append((base[1:], count))
                total_insertion_deletion_count += count
                indel_present = True
            elif base.startswith('-'):
                deletion_details.append((base[1:], count))
                total_insertion_deletion_count += count
                indel_present = True

        # Determine the mutation and its frequency
        if indel_present:
            mutation = 'indel'  # Mark mutation as "indel"
            mutation_count = total_insertion_deletion_count
            frequency_mutation = mutation_count / int(total_count) if total_count.isdigit() and int(total_count) > 0 else 0
        else:
            # Create a dictionary of non-wildtype counts
            non_wildtype_counts = {
                'A': a_count if wildtype != 'A' else 0,
                'T': t_count if wildtype != 'T' else 0,
                'G': g_count if wildtype != 'G' else 0,
                'C': c_count if wildtype != 'C' else 0,
            }
            # Find the highest count among non-wildtype nucleotides
            mutation, mutation_count = max(non_wildtype_counts.items(), key=lambda item: item[1])
            if mutation_count == 0:
                mutation = 'No mutation'
            frequency_mutation = mutation_count / int(total_count) if total_count.isdigit() and int(total_count) > 0 else 0

        # Calculate frequency of wildtype
        total_count = int(total_count)
        frequency_wildtype = wildtype_count / total_count if total_count > 0 else 0

        # Prepare the row with basic nucleotide counts, mutation info, and frequencies
        row = [chrom, position, wildtype, mutation, a_count, t_count, g_count, c_count, total_count, frequency_wildtype, frequency_mutation]

        # Add insertion values
        for idx in range(max_insertions):
            if idx < len(insertion_details):
                sequence, count = insertion_details[idx]
                row.append(sequence)
                row.append(count)
            else:
                row.append('')  # Empty insertion sequence
                row.append('')  # Empty insertion count

        # Add deletion values
        for idx in range(max_deletions):
            if idx < len(deletion_details):
                sequence, count = deletion_details[idx]
                row.append(sequence)
                row.append(count)
            else:
                row.append('')  # Empty deletion sequence
                row.append('')  # Empty deletion count

        # Write the row
        writer.writerow(row)

print(f"Parsing complete! Check '{output_filename}' for results.")





