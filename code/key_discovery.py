# import libraries
import os
import pandas as pd

# setup any variables
data_source = 'kaggle'
data_sample = 'av_healthcare'
primary_keys = {}
foreign_keys = {}
missing_values = ['None']

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
        
        # print out the results of each loop
        # print(f, col, proportion_unique, sep = ' - ')
        
        # if the proportion == 1, then we can infer primary key
        if proportion_unique == 1:
            primary_keys[f] = col
            
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
                
                # print out the results of each loop
                # print(key, primary_keys[key], f, col, prop_foreign, sep = ' - ')
                
                # if the proportion > 0, we can infer foreign key
                if prop_foreign > 0:
                    
                    if f not in foreign_keys.keys():
                        foreign_keys[f] = {}
                        foreign_keys[f][col] = prop_foreign
                        
                    else:
                        foreign_keys[f][col] = prop_foreign    
    
    
    
    
    