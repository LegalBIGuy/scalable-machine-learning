'''
    scalable-machine-learning
    
    The Legal BI Guy
    https://legalbiguy.com
    legalbiguy@gmail.com
    
    This project contains code examples for my Pluralsight class
    	Scalable Machine Learning with the Microsoft Machine Learning Server
    available on Pluralsight
    
    import.py
    	This example demonstrates how to import data from flat files: CSV, XDF using the revoscalepy package
    	The data used in this example is available at:
    		https://packages.revolutionanalytics.com/datasets/
'''

import sys
import os
import pandas as pd
from revoscalepy import rx_import,  rx_get_info, RxOptions, RxTextData, RxXdfData, rx_create_col_info, rx_data_step


# For this example, we assume the airOT201201.csv file was downloaded into the current working directory
dirpath = os.getcwd()
# Other samples in RxOptions.get_option("sampleDataDir")

# CSV File (Raw Data for one month)
airlineDemoPathCSV = os.path.join(dirpath, "airOT201201.csv")

# Create the CSV Data Source using RxTextData
ds = RxTextData(airlineDemoPathCSV)

# Import first 10 rows of the CSV file
airlineDemo = rx_import(input_data=ds, number_rows=10)

# Inspect data types using rx_get_info
print(rx_get_info(airlineDemo, get_var_info=True))

# Inspect Unique Carrier (factor)
print(rx_get_info(airlineDemo, vars_to_keep="UNIQUE_CARRIER", get_var_info=True))

# Import the first 10 rows again, and this time use strings_as_factors = True
airlineDemo = rx_import(input_data=ds, strings_as_factors = True, number_rows=10)

# Inspect data types
print(rx_get_info(airlineDemo, get_var_info=True))

# Inspect Unique Carrier (factor) to see the difference using strings_as_factors = True
print(rx_get_info(airlineDemo, vars_to_keep="UNIQUE_CARRIER", get_var_info=True))

# Manually create column_info for the factor column UniqueCarrier
# we can use column_infog to specify data types and update factor levels
# Allowable column types are:
#    ”bool” (stored as uchar),
#    “integer” (stored as int32),
#    “float32” (the default for floating point data for ‘.xdf’ files),
#    “numeric” (stored as float64 as in R),
#    “character” (stored as string),
#    “factor” (stored as uint32),
#    “ordered” (ordered factor stored as uint32. Ordered factors are
column_info = {
    'UNIQUE_CARRIER': {
        'newName': 'UniqueCarrier',
        'type': 'factor',
        'levels': ['AA'],
        'newLevels': ['American Airlines']
    }
}

# Import the first 10 rows again, and this time use column_info
airlineDemo = rx_import(input_data=ds, strings_as_factors = True, column_info=column_info, number_rows=10)

# Inspect Unique Carrier (factor) to see the newLevels
print(rx_get_info(airlineDemo, vars_to_keep="UniqueCarrier", get_var_info=True))

# Now, let's import an XDF file
# Once again, we assume the AirOnTime2012.xdf file was downloaded into the current working directory
airlineDemoPath = os.path.join(dirpath, "AirOnTime2012.xdf")

# Create the XDF Data Source
ds = RxXdfData(airlineDemoPath)

## Import 10 rows as a sample
airlineDemo = rx_import(input_data=ds, number_rows=10)

# Inspect data types, note that the types are set correctly, unlike use the CSV file
print(rx_get_info(airlineDemo, get_var_info=True))

# Print factor column info for XDF file, note list of all levels
column_info = rx_create_col_info(data=ds, factors_only=True, sort_levels=True)
print(column_info)

# Import all data into dataframe
airlineDemo = rx_import(input_data=ds)

# Check size in memory
sys.getsizeof(airlineDemo)

# Desribe some numeric values, in order to make a decision of which columns are needed for our experiment
airlineDemo["ArrDelay"].describe()
airlineDemo["CarrierDelay"].describe()

# Specify vars to keep
vars_to_keep = ["Year", "Month", "DayOfWeek", "UniqueCarrier", "FlightNum", "TailNum", "Origin", "OriginState", "Dest", "DestState", "DepTime",
                "DepDelayMinutes", "DepDel15", "ArrTime", "ArrDelayMinutes", "ArrDel15", "Cancelled", "Diverted", "ActualElapsedTime", "AirTime", "Distance", "DistanceGroup"]

# Import into dataframe with vars_to_keep
airlineDemo = rx_import(input_data=ds, vars_to_keep=vars_to_keep)

# Get Info on the latest import
print(rx_get_info(airlineDemo, get_var_info=True))

# Check size in memory.  Note, we have a significant reduction in memory by specifyin only the var we need
sys.getsizeof(airlineDemo)

# Create a transform function to add Gain in Minutes
def transformFunc(data):
    ret = data
    ret["GainMinutes"] = data["DepDelayMinutes"] - data["ArrDelayMinutes"]
    return ret


# Import the data again using the transformation function
airlineDemo = rx_import(input_data=ds, vars_to_keep=vars_to_keep,
                         transform_function=transformFunc)
# Review the new calculated column, GainMinutes
airlineDemo["GainMinutes"].describe()

# Write data to Output File using rx_data_step
outPath = os.path.join(dirpath, "AirOnTime2012_Processed.xdf")
rx_data_step(input_data = airlineDemo,
    output_file = outPath,
    rows_per_read = 200000, 
    overwrite = True,
    xdf_compression_level = 5) # 5 is faster and the file is not much bigger than 9
