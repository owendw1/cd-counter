from collections import OrderedDict
import numpy as np
import os
import pandas as pd
import re
import sys

# TODO
# 1) Perform additional pre-processing of utterances
#    a) lemmatise tokens
#    b) remove special characters (including hashtags?)
# 2) Summarise results meaningfully (using Matplotlib?)
# 3) Exception handling
# 4) Much refactoring using functional programming idioms and perhaps OO design

# Seeks occurrences of Cognitive Distortion Types in free-text utterances
def main():

    # Display progress message on standard output
    sys.stdout.write('Seeking Cognitive Distortion Types in input files...please wait...')
    sys.stdout.flush()

    # Set relative path of data files
    input_data = 'input_data/'

    # Populate dictionary of Cognitive Distortion Markers (as keys) and their Cognitive Distortion Types (as values)
    cdt_dict = { x.lower(): y for x, y in pd.read_csv('cdt_list.tsv', sep = '\t', index_col = 'Marker').to_dict()['CD Category'].items() }

    # Populate list of utterances ensuring no duplicates are included
    utterances = []
    for filename in os.listdir(input_data):
        with open(os.path.join(input_data, filename), 'r') as file:
            utterances.extend(list(OrderedDict.fromkeys([line.strip().lower() for line in file.readlines()])))

    # Total the occurrences of each Cognitive Distortion Marker found amongst the utterances
    # Prepare output file to write results to
    with open('cdt_occurrences.txt', 'w') as output_file:

        # Write number of utterances to output file
        output_file.write('Number of utterances,' + str(len(utterances)) + '\n')

        # Total Marker occurrences one Category at a time
        for category in set(cdt_dict.values()):
            # Populate list of Markers belonging to current Category
            markers_in_category = [marker for marker in cdt_dict if cdt_dict[marker] == category]

            # Initialise Category counter
            category_occurrence_count = 0

            # Total the occurrences of each Marker in the current Category found amongst the utterances
            for marker in markers_in_category:
                # Initialise Marker counter
                marker_occurrence_count = 0

                # Compile regular expression representing current Marker
                marker_pattern = re.compile(r'\b%s\b' % re.escape(marker))

                # Total the occurrences of current Marker found amongst the utterances
                for utterance in utterances:
                    marker_occurrences = sum(1 for _ in re.finditer(marker_pattern, utterance))
                    if marker_occurrences  > 0:
                        marker_occurrence_count += marker_occurrences

                # Total the occurrences of all Markers found amongst the utterances in the current category
                category_occurrence_count += marker_occurrence_count

                # Write Marker name and its total occurrences to output file
                output_file.write(marker + ',' + str(marker_occurrence_count) + '\n')

            # Write Category name and its total occurrences to output file
            output_file.write(category + ',' + str(category_occurrence_count) + '\n')

    # Display progress message on standard output
    sys.stdout.write('FINISHED')

if __name__ == '__main__':
    main()
