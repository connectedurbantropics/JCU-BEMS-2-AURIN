# README

Converting from raw dumps from JCU BEMS to the geo referenced value types for AURIN.

## Requirements 
* Python3
* GDAL

## Getting Started

* Change all the hardcoded directories to correct paths

## Notes

The geometry of the buildings is located in `building-coords-csv/`.  The building number matches the building number in the raw input CSV filename. e.g. `2007-018.csv`

It has to be added to the pre OGR CSV as the geometry for each value.

You have to input ISO8601 date formats as strings - `yyyy-mm-dd` - since you can't retain type DATE in CSV. 
Specifically, AURIN requires `yyyy-mm-ddThh:mm:ss+10:00` where `+10:00` is the UTC TZ and there is a `T` between the date and time values.