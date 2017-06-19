# README

Converting from everything being strings to the value types that AURIN want.

## Goal

Convert the reference input csv's in `input/` into the correct output e.g. `output/example-output.geojson` - using whatever method makes you happy.

## Previous methods

1. 
    * Use Excel formulas to clean and assemble a pre `ogr2ogr` CSV e.g. `input/source.csv`.
    * Create a GDAL `.vrt` file that specifies where to extract geometry from and what date type each attribute field is. See `input/source.vrt`
    * Use `ogr2ogr` command from GDAL to convert into correct GeoJSON or Shapefile. (*Note:* Install GDAL from git HEAD to get GDAL 2.0 if you like fancy e.g. `brew install gdal --HEAD`)

2. * Write some python to do it a different and proper way.  See `pandas.py` for a start.

## Notes

The geometry of the buildings is located in `building-coords-csv/`.  The building number matches the building number in the raw input CSV filename. e.g. `2007-018.csv`

It has to be added to the pre OGR CSV as the geometry for each value.

You have to input ISO8601 date formats as strings - `yyyy-mm-dd` - since you can't retain type DATE in CSV. 
Specifically, AURIN requires `yyyy-mm-ddThh:mm:ss+10:00` where `+10:00` is the UTC TZ and there is a `T` between the date and time values.