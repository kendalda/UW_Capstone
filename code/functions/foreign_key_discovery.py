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

# function to find and return foreign keys
def find_foreign_keys(data_source, data_sample):
    
    foreign_keys = {}
    
    # get information needed to read files
    dat_path, dat_source, sample_data, files = gf.get_files(data_source, data_sample)
    json_path = os.path.join(os.path.normpath(dat_path + os.sep + os.pardir), 'results')
    json_name_primary = data_sample + '_primarykeys' + '.json'
    
    # get the primary keys from the json file created with the primary key detection module
    with open(os.path.join(json_path, json_name_primary)) as file:
        primary_keys = json.load(file)
    
    # extract the primary keys (files with primary keys)
    keys_files = list(primary_keys.keys())
        
    # loop through the files that do not contain primary keys
    for f in list(files):
        
        if f not in keys_files:
            dat_foreign = pd.read_csv(os.path.join(sample_data, f), 
                                      na_values = missing_values,
                                      low_memory = False,
                                      encoding='latin1')
                    
            # get the columns
            columns = dat_foreign.columns
            
            # extract the primary key values from the primary key dictionary
            for key in keys_files:
                
                key_files_columns = primary_keys[key].keys()
                
                for key_column in key_files_columns:
                    
                    temp_primary_keys = primary_keys[key][key_column]
    
                    # loop through the columns and get unique values:
                    for col in columns:
                                        
                        temp_foreign_keys = dat_foreign[col].unique()
                        
                        # find the proportion of potential foreign key values that are in the list of primary key values
                        foreign_key_bool = set(temp_foreign_keys).intersection(temp_primary_keys)
                        prop_foreign = len(foreign_key_bool) / len(temp_primary_keys)
                        
                        # if the proportion > 0, we can infer foreign key
                        if prop_foreign > 0:
                            
                            if f not in foreign_keys.keys():
                                foreign_keys[f] = {}
                                foreign_keys[f][col] = prop_foreign
                                
                            else:
                                foreign_keys[f][col] = prop_foreign
    
    # create the name for the json file
    json_name_foreign = data_sample + '_foreignkeys' + '.json'
        
    # write the json file
    with open(os.path.join(json_path, json_name_foreign), 'w') as file:
        json.dump(foreign_keys, 
                  file, 
                  cls = ne.NumpyEncoder,
                  indent = 2)
    
    # return the foreign keys
    return foreign_keys
    
    
    
    
    