# script to identify primary and foreign keys

# import libraries
import os
import pandas as pd
import primary_key_discovery as pk
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
    
    # get information needed to read files
    dat_path, dat_source, sample_data, files = gf.get_files(data_source, data_sample)
    
    # get the primary keys
    primary_keys = pk.find_primary_keys(data_source, data_sample)
    
    # define an empty dict for the keys
    foreign_keys = {}
    
    # read the files with primary keys and attempt to determine the foreign keys
    keys = primary_keys.keys()
    
    for key in keys:
        
        # read in the csv files
        dat = pd.read_csv(os.path.join(sample_data, key))
        
        # get a list of the primary key values
        temp_primary_keys = dat[primary_keys[key]].unique()
        
        # loop through the files that do not contain primary keys
        for f in files:
            
            if f not in keys:
                dat_foreign = pd.read_csv(os.path.join(sample_data, f))
            
                # get the columns
                columns = dat_foreign.columns
            
                # loop through the columns and get unique values:
                for col in columns:
                    
                    temp_foreign_keys = dat_foreign[col].unique()
                    
                    # find the proportion of potential foreign key values that are in the list of primary key values
                    foreign_key_bool = [foreign for foreign in temp_foreign_keys if foreign in temp_primary_keys]
                    prop_foreign = len(foreign_key_bool) / len(temp_primary_keys)
                    
                    
                    # if the proportion > 0, we can infer foreign key
                    if prop_foreign > 0:
                        
                        if f not in foreign_keys.keys():
                            foreign_keys[f] = {}
                            foreign_keys[f][col] = prop_foreign
                            
                        else:
                            foreign_keys[f][col] = prop_foreign
                            
    # return the foreign keys
    return foreign_keys
    
    
    
    
    