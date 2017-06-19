#! python3
# formatCSVforOGR.py - Formats all CSV files in the current
# working directory to match the reference CSV - Using Pandas

import csv
import os
import errno
import pandas as pd

def make_sure_path_exists(path):
    """Check the os path for the output folder exists to write into.

    Args:
        path - A folder name

    Raises:
        OSError but smothers it
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

# Make an output directory
make_sure_path_exists('formattedOutput')

# Loop through every file in the current working directory.
# for csvFilename in os.listdir('.'):
    # if not csvFilename.endswith('.csv'):
        # continue    # skip non-csv files
    # print('Reading in ' + csvFilename + '...')

    # Read the CSV file in
    # df = pd.read_csv(csvFilename, delim_whitespace=True, error_bad_lines=False)

# Read in the data csv
df = pd.read_csv('exampleInput.csv', error_bad_lines=False)

# Dump a quick summary
df.dtypes
df.head()

# Drop the useless year row
df.drop(df.index[:1], inplace=True)

# Rename the data column for easier access
new_columns = df.columns.values
new_columns[0] = 'original'
df.columns = new_columns

# Split the 'original' column on the ; character and make two new columns
df['time'], df['value'] = df['original'].str.split(';', 1).str
df['time'].head()
df['value'].head()

# Convert time column into a date object
df['timestamp'] = pd.to_datetime(df['time'])
df['timestamp'].head()

# Write out the CSV file.

# TODO: Check CSV matches spec

# TODO: Merge in the matching building WKT coordinates into another column for every row
