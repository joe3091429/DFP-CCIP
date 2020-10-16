#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
    File name: val_map_tb
    Group members: Kiana, Xiaoye, Joe
    Purpose: Create mapping table
'''
import pandas as pd

def val_map_tb():
    # create mapping table
    table = pd.read_csv('data/us_county_sociohealth_data.csv')
    map_table = table[['state','county']].copy()
    map_table = map_table.apply(lambda x: x.astype(str).str.lower())
    map_table.to_csv('data/mapping_table_county_state.csv', index = False)
    return

if __name__ == "__main__":
    val_aspect()