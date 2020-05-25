# -*- coding: utf-8 -*-
"""
Created on Sat May 16 13:12:30 2020

@author: adams
"""


#%% 
import pandas as pd
import numpy as np
import math
import itertools



from sklearn.linear_model import LinearRegression, LogisticRegressionCV, SGDClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
#%%
severity_high = pd.read_csv(r'.\part 2\severity_high_students.csv')


national_db = pd.read_csv(r'.\part 1\national_citizen_database.csv')

#%%

correlations = abs(national_db.corr())

#%%
cols = list(severity_high)
cols.insert(0, 'docile')

labelled = national_db.reindex(columns = cols)
raw = severity_high.copy()

possible_features = correlations['docile'].sort_values(ascending = False)

features = list(possible_features.index[1:8])


#%%
# clf = make_pipeline(StandardScaler(), SGDClassifier(loss='log', max_iter=10000, tol=1e-5))
# clf.fit(labelled[features], labelled['docile'])

# predictions = clf.predict(raw[features])
# output = raw.copy()
# output['docile'] = predictions

# clf_agitators = output[output['docile'] == 0]

#%%
lowest_error = 10e10
best_selction = []
n_rounds = 5
for feature_selection in list(itertools.combinations(features,4)):
    print(feature_selection)
    round_error = 0
    for i in range(n_rounds):
        feature_selection = list(feature_selection)
        random_indices = np.random.permutation(labelled.index)
        test_cutoff = math.floor(len(labelled)/10)
        
        test = labelled.loc[random_indices[0:test_cutoff]]
        train = labelled.loc[random_indices[test_cutoff:]]
        
        reg = LinearRegression(normalize = True)
        reg.fit(train[feature_selection], train['docile'])
        
        predictions = reg.predict(test[feature_selection])
        
        error = test['docile']-predictions
        
        round_error += abs(error.sum())
        print(round_error)
    average_error = round_error/n_rounds
    print(average_error)
    
    if average_error<lowest_error:
        lowest_error = average_error
        best_selection = feature_selection

#%% from the output above best_vector = ['z_index', 'citizen_quality_score', 'facial_ratio', 'consumer_score']

reg = LogisticRegressionCV()
reg.fit(labelled[best_selection], labelled['docile'])

predictions = reg.predict(raw[best_selection])
output = raw.copy()
output['docile'] = predictions

reg_agitators = output.sort_values('docile').head(10)


