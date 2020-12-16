# script to detect outliers using unsupervised machine learning techniques

#-------------------
# import libraries
#-------------------
import os
import pandas as pd
import numpy as np
import get_files as gf
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import scipy.io
from sklearn.cluster import DBSCAN
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor

#--------------------
# define variables
#--------------------
missing_values = ['None']
outlier_columns = []

# command line variables
#data_source = sys.argv[1] # 'kaggle'
#data_sample = sys.argv[2] # 'av_healthcare'

data_source = 'harvard'
#data_sample = 'cancer'
data_sample = 'thyroid'

#--------------------
# read in the data
#--------------------

# get information needed to read files
dat_path, dat_source, sample_data, files = gf.get_files(data_source, data_sample)

# remove any files from the list that are not csv
for f in files:
    
    if f.endswith('.csv') or f.endswith('.txt'):
        ''        
    else:
        files.remove(f)
        
# read the data
dat = pd.read_csv(os.path.join(sample_data, files[0]), na_values = missing_values, thousands= ',', header=None)

ignore_column = len(dat.columns)

# define the column(s) to perform outlier detection on
if len(outlier_columns) == 0:
    outlier_dat = dat
    
else:
    outlier_dat = dat[outlier_columns]
    
# remove any pre-labeled column
outlier_dat = outlier_dat.drop(dat.columns[ignore_column - 1], axis=1)

# keep only the numeric columns for now
outlier_dat = outlier_dat._get_numeric_data()

#--------------------------------------------------------
# perform pca in order to remove any unecessary columns
#--------------------------------------------------------

# standardize the data prior to pca analysis
scaler = StandardScaler()

# fit the data and apply the transformation
scaler.fit(outlier_dat)
outlier_dat = scaler.transform(outlier_dat)

# create an instance of the pca model
pca = PCA(.95)

# fit the model on the standardized data and apply tranformation
pca.fit(outlier_dat)
outlier_dat = pca.transform(outlier_dat)

#------------------------------
# dbscan (no training needed)
#------------------------------

# initiate the model
dbscan_outliers = DBSCAN(eps = 2, min_samples = 3)

# fit the model
dbscan_model = dbscan_outliers.fit(outlier_dat)

# get the labels
labels = dbscan_model.labels_

# find the core points
core_points = np.zeros_like(labels, dtype = bool)
core_points[dbscan_outliers.core_sample_indices_] = True

# find the number of clusters
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

# print the silhouette score, min sample, and eps value
silhouette_ = metrics.silhouette_score(outlier_dat, labels)
                
# join the outlier labels back to the original dataset
dat['dbscan_outliers'] = labels

# values of -1 are outliers, code these as 1 and anything else as 0
dat['dbscan_outliers'] = (dat['dbscan_outliers'] == -1)
dat['dbscan_outliers'] = dat['dbscan_outliers'].astype(int)

print(dat['dbscan_outliers'].value_counts())

#----------------------------------------
# isolation forest (no training needed)
#----------------------------------------

# initiate the model
iso_forest = IsolationForest()

# fit the model
iso_forest.fit(outlier_dat)

# store the results back to the original dataframe
# dat['iso_forest_scores'] = iso_forest.decision_function(outlier_dat)
dat['iso_forest_outlier'] = iso_forest.predict(outlier_dat)

# values of -1 are outliers, code these as 1 and anything else as 0
dat['iso_forest_outlier'] = (dat['iso_forest_outlier'] == -1)
dat['iso_forest_outlier'] = dat['iso_forest_outlier'].astype(int)

# false positive rate
true_negative = len(dat[(dat[ignore_column - 1] == 'n') & (dat['iso_forest_outlier'] == 0)])
false_positives = len(dat[(dat[ignore_column - 1] == 'n') & (dat['iso_forest_outlier'] == 1)])
print("Isolation Forest - False Positive Rate:", 100*(false_positives/(true_negative + false_positives)))

# false negative rate
false_negative = len(dat[(dat[ignore_column - 1] == 'o') & (dat['iso_forest_outlier'] == 0)])
true_positives = len(dat[(dat[ignore_column - 1] == 'o') & (dat['iso_forest_outlier'] == 1)])
print("Isolation Forest - False Negative Rate:", 100*(false_negative/(false_negative + true_positives)))

# find the accuracy of the model
num_correct = len(dat[(dat[ignore_column - 1] == 'n') & (dat['iso_forest_outlier'] == 0) | (dat[ignore_column - 1] == 'o') & (dat['iso_forest_outlier'] == 1)])
print("Isolation Forest - Accuracy:", 100*(num_correct/dat.shape[0]))

#-------------------------------------------
# local outlier factor (no training needed)
#-------------------------------------------

# initiate the model
lof = LocalOutlierFactor()

# fit the model and get the predictions
pred = lof.fit_predict(outlier_dat)

# store the results back to the original dataframe
dat['lof_outlier'] = pred

# values of -1 are outliers, code these as 1 and anything else as 0
dat['lof_outlier'] = (dat['lof_outlier'] == -1)
dat['lof_outlier'] = dat['lof_outlier'].astype(int)

# false positive rate
true_negative = len(dat[(dat[ignore_column - 1] == 'n') & (dat['lof_outlier'] == 0)])
false_positives = len(dat[(dat[ignore_column - 1] == 'n') & (dat['lof_outlier'] == 1)])
print("Local Outlier Factor - False Positive Rate:", 100*(false_positives/(true_negative + false_positives)))

# false negative rate
false_negative = len(dat[(dat[ignore_column - 1] == 'o') & (dat['lof_outlier'] == 0)])
true_positives = len(dat[(dat[ignore_column - 1] == 'o') & (dat['lof_outlier'] == 1)])
print("Local Outlier Factor - False Negative Rate:", 100*(false_negative/(false_negative + true_positives)))

# find the accuracy of the model
num_correct = len(dat[(dat[ignore_column - 1] == 'n') & (dat['lof_outlier'] == 0) | (dat[ignore_column - 1] == 'o') & (dat['lof_outlier'] == 1)])
print("Local Outlier Factor - Accuracy:", 100*(num_correct/dat.shape[0]))








