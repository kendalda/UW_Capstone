# script to read the file(s) we are interested in
# import libraries
import os

def get_files(data_source, data_sample):

    # get the directory of where the data lives
    dat_path = os.path.abspath(os.path.join(os.getcwd(), '../', '../', 'data'))
    
    # navigate to the source of data we're using
    dat_source = os.path.join(dat_path, data_source)
    
    # navigate to the sample date if applicable
    sample_data = os.path.join(dat_source, data_sample)
    
    # get a list of files in the sample data folder
    files = os.listdir(sample_data)
    
    return (dat_path, dat_source, sample_data, files)