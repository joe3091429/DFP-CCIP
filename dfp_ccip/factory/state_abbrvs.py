#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 10:57:34 2020

@author: kianaocean
"""

cd = '/Users/kianaocean/Documents/CMU/Python (95888)/Project/DFP-CCIP/'

import pandas as pd

file_in = open(cd+'data/states.txt')
abbrv_list = []
state_list = []
for line in file_in:
    if (line[2:3]=='\''):
        list = line.split('=>')
        abbrv = list[0].strip()
        abbrv = abbrv.strip('\"\'')
        abbrv_list.append(abbrv)
        state = list[1].strip()
        state = state.replace('\'','')
        state = state.replace(',','')
        state_list.append(state)
data = {'state_abbrv': abbrv_list, 'state': state_list}
df = pd.DataFrame.from_dict(data)

# Function for calling dataframe in other module
def get_df():
    return df
