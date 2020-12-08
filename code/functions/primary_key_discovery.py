# script to identify primary and foreign keys

# import libraries
import os
import sys
import pandas as pd
import get_files as gf


#--------------------
# define variables
#--------------------
missing_values = ['None']

# command line variables
#data_source = sys.argv[1] # 'kaggle'
#data_sample = sys.argv[2] # 'av_healthcare'

#------------------------------------------
# function to find and return primary keys
#------------------------------------------

def find_primary_keys(data_source, data_sample):
    
    # define an empty dict for the keys
    primary_keys = {}
    
    # get information needed to read files
    dat_path, dat_source, sample_data, files = gf.get_files(data_source, data_sample)
    
    # read in each file and attempt to find any primary keys
    for f in files:
        
        # read in each csv file
        dat = pd.read_csv(os.path.join(sample_data, f), na_values = missing_values)
            
        # get the total number of rows
        rows = dat.shape[0]
        
        # get list of columns
        columns = dat.columns
        
        # loop through each column and determine the proportion of unique values
        for col in columns:
            
            # try to convert potential date columns
            if dat[col].dtype == 'object':
                try:
                    dat[col] = pd.to_datetime(dat[col])
                except:
                    pass
            
            unique_vals = len(dat[col].unique())
            proportion_unique = unique_vals / rows
            
            # if the proportion == 1, then we can infer primary key
            if proportion_unique == 1:
                primary_keys[f] = col
                
        # return the keys
        return primary_keys