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

# Build a list of wkt filenames
wkt_buildings = []

def build_list_of_wkt_filenames():
    
    # Get list of directories
    wkt_parent_dir = '/Users/stevevandervalk/Dropbox/eResearch/ConnectedUrbanTropics/csv-geojson-shapefiles/input/building-coords'
    wkt_subject_dirs = [os.path.join(wkt_parent_dir, dir) for dir in os.listdir(wkt_parent_dir) if os.path.isdir(os.path.join(wkt_parent_dir, dir))]
            
    # Get list of csv files        
    for dir in wkt_subject_dirs:
        wkt_csv_files = [os.path.join(dir, csv) for csv in os.listdir(dir) if os.path.isfile(os.path.join(dir, csv)) and csv.endswith('.csv')]
        print('wkt file list: ' + repr(wkt_csv_files))
        for wkt_file in wkt_csv_files:
            
            year_building_filename = (wkt_file.split("/")[10])
            print('file is : ' + repr(year_building_filename))
            print('extracting building name string from file name...:')
            print('building number might be: ' + repr(year_building_filename.split("-")[1]))
            building_number = year_building_filename.split("-")[1]
            wkt_buildings.append(build_number)
            print('wkt_buildings list is : ' + repr(wkt_buildings))


# Build a list we can compare against later
build_list_of_wkt_filenames()

# Loop through every csv file in the data input directory.
parent_dir = '/Users/stevevandervalk/Dropbox/eResearch/ConnectedUrbanTropics/csv-geojson-shapefiles/input/building-data/'
subject_dirs = [os.path.join(parent_dir, dir) for dir in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, dir))]
counter = 0
year_building_filename = ''



for dir in subject_dirs:
    csv_files = [os.path.join(dir, csv) for csv in os.listdir(dir) if os.path.isfile(os.path.join(dir, csv)) and csv.endswith('.csv')]
    for file in csv_files:
        # print('filelist is : \n' + (repr(csv_files)))
        print('Reading in ' + file + '...\n')
        
        print(file.split("/"))
        
        year_building_filename = (file.split("/")[10])
        print('file is : ' + repr(year_building_filename))
        
        # Read the CSV file in
        print('Importing csv...\n')
        df = pd.read_csv(file, index_col=False)
        
        print ('Head of dataframe \n')
        print(df.head())
        
        # Drop the useless year row
        df.drop(df.index[:1], inplace=True)
        
        # Rename the data column for easier access
        print('renaming columns \n')
        new_columns = df.columns.values
        new_columns[0] = 'original'
        df.columns = new_columns
        
        # Split original into time and value
        df['time'], df['value'] = df['original'].str.split(';', 1).str
        
        # Convert time column into a date object
        print ('Convert time column into a date object... \n')
        df['timestamp'] = pd.to_datetime(df['time'])
        
        # print(df.head())
        
        # Delete superfluous columns
        print ('Delete superfluous columns \n')
        del df['original']
        del df['time']
    
        # Check CSV matches spec
        print('Check head of dataframe matches spec : value | timestamp \n')
        print(df.head())
        
        # Merge in the matching building WKT coordinates into another column for every row
        
        def return_matching_wkt_file():
            # wkt_parent_dir = '/Users/stevevandervalk/Dropbox/eResearch/ConnectedUrbanTropics/csv-geojson-shapefiles/input/building-coords'
            # wkt_subject_dirs = [os.path.join(wkt_parent_dir, dir) for dir in os.listdir(wkt_parent_dir) if os.path.isdir(os.path.join(wkt_parent_dir, dir))]
            
            # # if any part of a data csv filename matches a wkt file name then we use it. e.g. 2009-a1.csv matches a1.csv or 2007-018.csv matchs 018.csv
            # for dir in wkt_subject_dirs:
            #     wkt_csv_files = [os.path.join(dir, csv) for csv in os.listdir(dir) if os.path.isfile(os.path.join(dir, csv)) and csv.endswith('.csv')]
            #     print('wkt file list: ' + repr(wkt_csv_files))
            #     for wkt_file in wkt_csv_files:
            #         # Return the second part of the filename and check if present in wkt_csv_files
                    
            #         print('extracting building name string from file name...:')
            #         # print(file)
            #         print('building number might be: ' + repr(year_building_filename.split("-")[1]))
                    
                    
                    if year_building_filename.split("-")[1] in wkt_csv_files:
                        print('found matching building name: filename is :' + repr(wkt_file))
                        return wkt_file
                    else:
                        print('no matching filename in wkt_files')
    
        matching_wkt_file = return_matching_wkt_file()
        print('matching wkt file name is : ' + repr(matching_wkt_file))
        
        # Use the matching wkt file
        wkt = pd.read_csv(matching_wkt_file,index_col=False)
        
        # Extract the polygon WKT string
        polygon_string = wkt['wkt_geom'].values[0]
        
        # Create a column of entirely that
        df['wkt_geom'] = polygon_string
        
        print('Created wkt_geom column with polygon \n')
        # print(df.head())
        
        # Write out the CSV file.
        print ('Writing out the CSV file.... \n')
        # print(df.head())
        df.to_csv('output/output' +year_building_filename + '.csv', header=True, index=False, date_format='%Y-%m-%dT%H:%M:%S+10:00')
    
        print ("end of loop" + repr(counter))
        counter+= 1
    else:
        print('finished')