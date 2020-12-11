# script to detect outliers using unsupervised machine learning techniques

#-------------------
# import libraries
#-------------------
import os
import pandas as pd
import numpy as np
import get_files as gf
# from sklearn import preprocessing
from sklearn.cluster import DBSCAN
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

#--------------------
# define variables
#--------------------
missing_values = ['None']
outlier_columns = ['Number of Services']

# command line variables
#data_source = sys.argv[1] # 'kaggle'
#data_sample = sys.argv[2] # 'av_healthcare'

data_source = 'kaggle'
data_sample = 'healthcare_providers'

#--------------------
# read in the data
#--------------------

# get information needed to read files
dat_path, dat_source, sample_data, files = gf.get_files(data_source, data_sample)

# define a list of possible values that would indicate missings
dat = pd.read_csv(os.path.join(sample_data, files[0]), na_values = missing_values, thousands= ',').convert_dtypes()

# define the column(s) to perform outlier detection on
x = dat[outlier_columns]

# perform pre-processing of the data
# label_encode = preprocessing.LabelEncoder()
# dat_outlier = dat[outlier_columns].apply(label_encode.fit_transform)
# dat_outlier.head()

#------------------------------
# dbscan (no training needed)
#------------------------------

outlier_detection = DBSCAN(eps = .2, 
                           metric='euclidean', 
                           min_samples = 5)

# reshape the variable
#x = dat[outlier_columns].values.reshape(-1,1)
clusters = outlier_detection.fit_predict(x)

#----------------------------------------
# isolation forest (no training needed)
#----------------------------------------

clf = IsolationForest(max_samples=100, 
                      random_state = 1, 
                      contamination= 'auto')
clf.fit(x)

dat['scores_iso_forest'] = clf.decision_function(x)
dat['anomaly_iso_forest'] = clf.predict(x)

#-------------------------------------------
# local outlier factor (no training needed)
#-------------------------------------------

# model specification
model1 = LocalOutlierFactor(n_neighbors = 2, 
                            metric = "manhattan", 
                            contamination = 0.02)

# model fitting
y_pred = model1.fit_predict(x)

# filter outlier index
outlier_index = np.where(y_pred == -1) # negative values are outliers and positives inliers

y = dat.iloc[outlier_index]








