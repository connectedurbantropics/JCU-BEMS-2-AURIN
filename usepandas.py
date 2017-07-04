#! python3
# formatCSVforOGR.py - Formats all CSV files in the current
# working directory to match the reference CSV - Using Pandas

import csv
import os
import errno
import pandas as pd

import datetime

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
make_sure_path_exists('output')

# Loop through every file in the current working directory.
# for csvFilename in os.listdir('.'):
    # if not csvFilename.endswith('.csv'):
        # continue    # skip non-csv files
    # print('Reading in ' + csvFilename + '...')

    # Read the CSV file in
    # df = pd.read_csv(csvFilename, delim_whitespace=True, error_bad_lines=False)

# Read in the data csv
df = pd.read_csv('exampleInput.csv', error_bad_lines=False)

# Drop the useless year row
df.drop(df.index[:1], inplace=True)

# Rename the data column for easier access
new_columns = df.columns.values
new_columns[0] = 'original'
df.columns = new_columns

# def logstring_to_data(logstr):
#     # first, split time and data
#     (timestr, datastr) = logstr.split(';')

#     datavalue = float(datastr)

#     time = datetime.datetime.strptime(timestr, "%y/%m/%d %I")

#     print( ' @@@ '.join([timestr, str(datavalue)]) )


# # Split the 'original' column on the ; character and make two new columns

# logstring_to_data('12/11/07 1:00:00 PM;111.8')


df['time'], df['value'] = df['original'].str.split(';', 1).str


# Convert time column into a date object
df['timestamp'] = pd.to_datetime(df['time'])

del df['original']
del df['time']

print(df.head())

# TODO: Check CSV matches spec

# Merge in the matching building WKT coordinates into another column for every row

wkt = pd.read_csv('exampleWktInput.csv', error_bad_lines=False)

# wkt_geom_only = wkt[['wkt_geom']]

polygon_string = wkt['wkt_geom'].values[0]

df['wkt_geom'] = polygon_string

print(df.head())

# Write out the CSV file.

df.to_csv('exampleOutput.csv', header=True, index=False, date_format='%Y-%m-%dT%H:%M:%S+10:00')















