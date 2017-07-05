#! python3
# formatCSVforOGR.py - Formats all CSV files in the current
# working directory to match the reference CSV - Using Pandas

import csv
import os
import sys
import errno
import pandas as pd
import glob
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

# A list of building names we have wkt for
wkt_buildings = ['']

def build_list_of_wkt_filenames():
    
    # Get list of directories
    wkt_parent_dir = '/Users/stevevandervalk/Dropbox/eResearch/ConnectedUrbanTropics/csv-geojson-shapefiles/input/building-coords/'
    wkt_subject_dirs = [os.path.join(wkt_parent_dir, dir) for dir in os.listdir(wkt_parent_dir) if os.path.isdir(os.path.join(wkt_parent_dir, dir))]
            
    # Get list of csv files        
    for dir in wkt_subject_dirs:
        wkt_csv_files = [os.path.join(dir, csv) for csv in os.listdir(dir) if os.path.isfile(os.path.join(dir, csv)) and csv.endswith('.csv')]
        for wkt_file in wkt_csv_files:
            building_name = (wkt_file.split("/")[10])
            wkt_buildings.append(building_name)

# Build a list we can compare against later
build_list_of_wkt_filenames()

# Loop through every csv file in the data input directory.
parent_dir = '/Users/stevevandervalk/Dropbox/eResearch/ConnectedUrbanTropics/csv-geojson-shapefiles/input/building-data/'
subject_dirs = [os.path.join(parent_dir, dir) for dir in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, dir))]
counter = 0
year_building = ''



for dir in subject_dirs:
    csv_files = [os.path.join(dir, csv) for csv in os.listdir(dir) if os.path.isfile(os.path.join(dir, csv)) and csv.endswith('.csv')]
    for file in csv_files:
        print('Reading in ' + file + ' ...\n')
        # print(file.split("/"))

        # Read the CSV file in
        print('Importing csv...\n')
        df = pd.read_csv(file, index_col=False)
        
        # print('Head of data frame: \n')
        # print(df.head())
        
        # Drop the useless first row
        df.drop(df.index[:1], inplace=True)
        
        # Rename the data column for easier access
        print('renaming columns... \n')
        new_columns = df.columns.values
        new_columns[0] = 'original'
        df.columns = new_columns
        
        # Split original into time and value
        df['time'], df['value'] = df['original'].str.split(';', 1).str
        
        # Convert time column into a date object
        print('Convert time column into a date object... \n')
        df['timestamp'] = pd.to_datetime(df['time'])

        # Delete superfluous columns
        print('Delete superfluous columns \n')
        del df['original']
        del df['time']
    
        # Check CSV matches spec
        print('Check head of dataframe matches spec : value | timestamp \n')
        print(df.head())

        # Get the year and building for later
        year_building = (file.split("/")[10])

        # Merge in the matching building WKT coordinates into another column for every row
        
        def return_matching_wkt_file():
            building_name_only = year_building.split("-")[1]
            for building_name in wkt_buildings:
                if building_name == building_name_only:
                    print("matching building name found in wkt")
                    return building_name
            else:
                print('no matching filename in wkt_files')
    
        matching_wkt_string = return_matching_wkt_file()

        # Create the path to the csv that is the matching_wkt_string
        matching_wkt_file = '/Users/stevevandervalk/Dropbox/eResearch/ConnectedUrbanTropics/csv-geojson-shapefiles/input/building-coords-merged/' + matching_wkt_string

        # Use the matching wkt file
        print("Reading in the matching wkt file : " + repr(matching_wkt_file))
        wkt = pd.read_csv(matching_wkt_file,index_col=False)
        
        # Extract the polygon WKT string
        polygon_string = wkt['wkt_geom'].values[0]
        
        # Create a column of entirely polygon string
        df['wkt_geom'] = polygon_string
        
        # Write out the CSV file.
        print ('Writing out the CSV file with polygon column.... \n')
        print(df.head())
        df.to_csv('output/output' + year_building + '.csv', header=True, index=False, date_format='%Y-%m-%dT%H:%M:%S+10:00')
    
        print ("end of loop " + repr(counter))
        counter+= 1
    else:
        print('Finished.' + counter + 'files processed')