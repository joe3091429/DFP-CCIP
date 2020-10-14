#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd

# kiana's code
def sum_tb(s_state, s_county):
    print("Generating summary table.")
    #print('use ' + state +'and '+ county + ' for tables')
    data = pd.DataFrame([[ 1, 2, 3, 4],[5, 6, 7, 8], ['a', 'b', 'c', 'd']], index = ['aa', 'bb', 'cc'], 
                 columns = [s_state, 'bbb', s_county, 'ddd'])
    return data

if __name__ == "__main__":
    sum_tb(s_state, s_county)