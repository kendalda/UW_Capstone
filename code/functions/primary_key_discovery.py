# script to identify primary and foreign keys

# import libraries
import os
import sys
import pandas as pd
from code import config

#--------------------
# define variables
#--------------------
sample_data = config.sample_data
files = config.files
missing_values = ['None']

# command line variables
data_source = sys.argv[1] # 'kaggle'
data_sample = sys.argv[2] # 'av_healthcare'

#------------------------------------------
# function to find and return primary keys
#------------------------------------------

def find_primary_keys(data_source, data_sample):
    
    # define an empty dict for the keys
    primary_keys = {}
        
    # get the directory of where the data lives
    dat_path = os.path.abspath(os.path.join(os.getcwd(), '../data'))
    
    # navigate to the source of data we're using
    dat_source = os.path.join(dat_path, data_source)
    
    # navigate to the sample date if applicable
    sample_data = os.path.join(dat_source, data_sample)
    
    # get a list of files in the sample data folder
    files = os.listdir(sample_data)
    
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