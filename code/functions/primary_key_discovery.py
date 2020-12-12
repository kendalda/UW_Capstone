# script to identify primary and foreign keys

#------------------
# import libraries
#------------------
import os
# import sys
import pandas as pd
import json
import numpyencoder as ne
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
        
        if os.path.splitext(f)[1] == '.csv':
            
            # define an empty dictionary for the columns
            cols = {}
                    
            # read in each csv file
            dat = pd.read_csv(os.path.join(sample_data, f), 
                              na_values = missing_values, 
                              low_memory= False)
                
            # get the total number of rows
            rows = dat.shape[0]
            
            # get list of columns
            columns = dat.columns
            
            # print(f)
            # print(rows)
            
            # loop through each column and determine the proportion of unique values
            for col in columns:
                
                # try to convert potential date columns
                # if dat[col].dtype == 'object':
                    # try:
                        # dat[col] = pd.to_datetime(dat[col])
                    # except:
                        # ""
                
                unique_vals = list(dat[col].unique())
                unique_vals_length = len(dat[col].unique())
                proportion_unique = unique_vals_length / rows
                                
                # if the proportion == 1, then we can infer primary key
                # if proportion_unique == 1:
                # an alternate is so introduce the possibility for data errors and decrease the proportion
                if proportion_unique >= .95:
                    cols[col] = unique_vals
                    primary_keys[f] = cols
                    
                # print(f)    
                # print(unique_vals)
                # print(proportion_unique)
                
    # create the file path to write a json file of the results to
    json_path = os.path.join(os.path.normpath(dat_path + os.sep + os.pardir), 'results')
    
    # create the name for the json file
    json_name = data_sample + '_primarykeys' + '.json'
        
    # write the json file
    with open(os.path.join(json_path, json_name), 'w') as file:
        json.dump(primary_keys, 
                  file, 
                  cls = ne.NumpyEncoder,
                  indent = 2)
                
    # return the keys
    return primary_keys