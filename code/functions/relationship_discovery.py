# script to measure relationships amongst variables that aren't primary or foreign keys

#------------------
# import libraries
#------------------
from itertools import permutations
from collections import OrderedDict
import pandas as pd
import sys
import os
import get_files as gf
# import numpy as np

#--------------------
# define variables
#--------------------
# wharf_matrix = np.array
ignore_columns = []
missing_values = ['None']
wharf_dict = {}

# command line variables
#data_source = sys.argv[1] # 'kaggle'
#data_sample = sys.argv[2] # 'av_healthcare'

#--------------------------------------------------------------------------------
# function to find and return relationship strengths based on wharf coefficient
#--------------------------------------------------------------------------------

def find_relationships(data_source, data_sample):
    
    # get information needed to read files
    dat_path, dat_source, sample_data, files = gf.get_files(data_source, data_sample)
    
     # read in each file and attempt to find any primary keys
    for f in files:
        
        # read in each csv file
        dat = pd.read_csv(os.path.join(sample_data, f), na_values = missing_values)
        dat.columns = dat.columns.str.replace(' ','_')

        # import the data
        rows = dat.shape[0]
        
        # find the cardinality of each column
        for col in dat.columns:
            
            # find potential keys
            unique_vals = len(dat[col].unique())
            proportion_unique = unique_vals / rows
                
            # if the column is a key, ignore it
            if proportion_unique == 1 and col not in ignore_columns:
                ignore_columns.append(col)
                
            # get the column type
            # col_type = dat[col].dtypes
                
            # ignore columns that don't appear to be boolean integers
            # if str(col_type) in ['float', 'float64', 'int', 'int64'] and unique_vals > 2 and col not in ignore_columns:
                # ignore_columns.append(col)
            
        # get all column combinations
        column_combinations = permutations(dat.columns, 2)
        
        # extract column names and get them into list form
        column_combo_lists = [' '.join(i) for i in column_combinations]
        column_combo_lists0 = list(OrderedDict.fromkeys([i.split()[0] for i in column_combo_lists if i.split()[0] not in ignore_columns]))
        column_combo_lists1 = list(OrderedDict.fromkeys([i.split()[1] for i in column_combo_lists if i.split()[1] not in ignore_columns]))
        
        # sort the lists
        column_combo_lists0.sort()
        column_combo_lists1.sort()
        
        # create an empty matrix
        # wharf_matrix = np.zeros((len(column_combo_lists0), len(column_combo_lists0)))
        
        # fill nan values
        # dat.fillna(0)
        
        # compute the wharf coefficient for each column combination
        for counter0, col1 in enumerate(column_combo_lists0):
            
            for counter1, col2 in enumerate(column_combo_lists1):
                
                if col1 == col2:
                    pass
                
                elif col2 in column_combo_lists0:
                    
                    # compute the wharf coefficient
                    w = (dat.groupby([col1, col2])[col2].count().max(level=0)).sum()/dat.shape[0]
                
                    # add the column combination to the dictionary
                    wharf_dict[col1, col2] = w
                
            # remove the col1 value to ensure there are no duplicate values returned
            column_combo_lists0.remove(col1)
                
    return wharf_dict

#-------------------------------------------------------------------------
# the code below is part of future development for viewing the graph model
#-------------------------------------------------------------------------

# a wharf value of 1 probably indicates a primary key, ignore these and set to 0
# if w == 1:
    # w = 0
# else:
    # w = w

# update the matrix position with the wharf coefficient
# wharf_matrix[counter0, counter1] = w

# view the graph
# gr = nx.from_numpy_matrix(wharf_matrix, create_using=nx.DiGraph)
# print(nx.draw(gr))
