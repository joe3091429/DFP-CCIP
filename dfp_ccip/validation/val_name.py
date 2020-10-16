#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
    File name: val_name
    Group members: Kiana, Xiaoye, Joe
    Purpose: Validate users' input of region level
'''
import pandas as pd

def val_name(v_state, v_county, result):

    tb = 'data/mapping_table_county_state.csv'
    mp_table = pd.read_csv(tb, header = 0)
    print("Validating input state and county......")

    if v_state == '' and v_county == '':
        result = True
        return v_state, v_county, result
    elif v_state != '' and v_county != '':
        #lowercase the input
        v_state = v_state.lower()
        v_county = v_county.lower()
        #verify table
        result = v_state in mp_table['state'].unique() and v_county in mp_table['county'].unique()
        return v_state, v_county, result
    elif v_state != '' and v_county == '':
        #lowercase the input
        v_state = v_state.lower()
        #verify table
        result = v_state in mp_table['state'].unique()
        return v_state, v_county, result

if __name__ == "__main__":
    val_name()