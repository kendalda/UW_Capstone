# import libraries
from itertools import combinations, permutations
from collections import OrderedDict
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# setup variables
wharf_matrix = np.array
rows = dat.shape[0]
ignore_columns = []

# find the cardinality of each column
for col in dat.columns:
    
    # find potential keys
    unique_vals = len(dat[col].unique())
    proportion_unique = unique_vals / rows
    
    # get the column type
    col_type = dat[col].dtypes
    
    # find the median column length 
    col_values = dat[col].tolist()
    
    try:
        col_values = [len(val) for val in col_values if str(val) != 'nan']
        col_length = np.median(col_values)  
        
    except:
        col_length = np.nan
        
    # if the column is a key, ignore it
    if proportion_unique == 1 and col not in ignore_columns:
        ignore_columns.append(col)
        
    # ignore columns that don't appear to be boolean integers
    if str(col_type) in ['float', 'float64', 'int', 'int64'] and unique_vals > 2 and col not in ignore_columns:
        ignore_columns.append(col)
    
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
wharf_matrix = np.zeros((len(column_combo_lists0), len(column_combo_lists0)))

# fill nan values
dat.fillna(0)

# compute the wharf coefficient for each column combination
for counter0, col1 in enumerate(column_combo_lists0):
    
    for counter1, col2 in enumerate(column_combo_lists1):
    
        # compute the wharf coefficient
        w = (dat.groupby([col1, col2])[col2].count().max(level=0)).sum()/dat.shape[0]
        
        # a wharf value of 1 probably indicates a primary key, ignore these and set to 0
        if w == 1:
            w = 0
        else:
            w = w
        
        # update the matrix position with the wharf coefficient
        wharf_matrix[counter0, counter1] = w

# view the graph
gr = nx.from_numpy_matrix(wharf_matrix, create_using=nx.DiGraph)
#print(nx.draw(gr))
