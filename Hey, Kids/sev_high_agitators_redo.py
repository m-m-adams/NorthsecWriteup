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
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import make_pipeline
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2, mutual_info_regression
from sklearn.metrics import mutual_info_score
from scipy.stats import chi2_contingency


def calc_MI(x, y, bins):
    c_xy = np.histogram2d(x, y, bins)[0]
    mi = mutual_info_score(None, None, contingency=c_xy)
    return mi
#%%
severity_high = pd.read_csv(r'.\part 2 - find the threats\severity_high_students.csv')


national_db = pd.read_csv(r'.\part 1 - find corruption\national_citizen_database.csv')

#%%

correlations = abs(national_db.corr())


cols = list(severity_high)
cols.insert(0, 'docile')

labelled = national_db.reindex(columns = cols)
raw = severity_high.copy()

possible_features = correlations['docile'].sort_values(ascending = False)

features = list(possible_features.index[:])


#%%

MI = dict()
for feature in features:
    MI[feature] = calc_MI(national_db[feature], national_db['docile'], 50)

info = pd.Series(MI)

features = list(info.index[1:10])

#%%
scaler = StandardScaler()
train = scaler.fit_transform(national_db[features])
test = scaler.fit_transform(raw[features])


#%%
dtree = RandomForestRegressor(n_estimators=500, oob_score=True, random_state=100)
dtree.fit(train, national_db['docile'])

predictions = dtree.predict(test)
output = raw.copy()
output['docile'] = predictions  

reg_agitators = output.sort_values('docile').head(10)




# %%
