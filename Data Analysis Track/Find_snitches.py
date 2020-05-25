# -*- coding: utf-8 -*-
"""
Created on Sat May 16 15:48:55 2020

@author: adams
"""


#%% 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import math
import binascii
import base64
import collections
import itertools
import sqlite3



def xor_bytestring(str1, str2):
    return [(c1 ^ c2) for (c1, c2) in zip(str1, itertools.cycle(str2))]

def debase_snitch_string(snitch_string):
    string = snitch_string
    decoded = base64.b64decode(string)
    return list(decoded)

def clean_base64(snitch_string):
    return snitch_string[2:-1]


def add_decoded(dataframe):
    dataframe['data'] = dataframe['data'].map(clean_base64, na_action='ignore')
    dataframe['decoded'] = dataframe['data'].map(debase_snitch_string, na_action='ignore')
    

#%%

con = sqlite3.connect('4-Find_The_Snich/sev_high.sqlite')
secret = pd.read_sql('SELECT * FROM secret',con)
sev_high_studid_mac = pd.read_sql('SELECT * FROM student_id_mac_addr',con)

wifi = pd.read_csv('leak/wifi_logs', sep='\t')

snitches = pd.read_csv('snitches/snitches_logs.csv', sep='\t')
severity_high = pd.read_csv(r'.\part 2\severity_high_students.csv')
severity_high_names = severity_high[['name', 'last_name', 'student_id']]

snitches = snitches.sort_values('obs_time')
snitches.dropna()
add_decoded(snitches)
#%%

combined = snitches.merge(severity_high_names, on='student_id').dropna()


combined_snitched = combined.merge(severity_high_names, left_on='snitched_by', right_on='student_id', suffixes=('', '_snitched'))
combined_snitched.drop('student_id_snitched',axis=1, inplace=True)
#%%
add_decoded(snitches)

snitches = snitches.dropna()
#%%

known_agitators = ['691aa1d3-09de-4d86-8fed-51710b2cc479', '278e7b64-0347-4e7e-b7e2-6b47fef8cf97', 'f6622b3c-33aa-4b42-bbe7-d44cafb8b1ae']

agitators_snitched = snitches[snitches['student_id'].isin(known_agitators) | snitches['snitched_by'].isin(known_agitators)].sort_values('obs_time')

agitators_data = agitators_snitched[['student_id', 'data', 'decoded']].dropna()

#%%

decode_list = list(agitators_data['decoded'])

for pair in list(itertools.combinations(decode_list,2)):
    print(pair)
    print(xor_bytestring(pair[0], pair[1]), '\n')
    print('\n')
#%%

unique_students = snitches.groupby(['student_id', 'data']).size().to_frame()
unique_students = unique_students.reset_index()


#%%
decode_list = list(combined['data'])
for thing in decode_list:
    decoded = base64.b64decode(thing)
    try: 
        string = str(decoded, 'utf8')
        if string.isprintable():
            print(string)
    except:
        pass
    
