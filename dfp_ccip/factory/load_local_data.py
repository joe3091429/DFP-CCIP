#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd

def get_data():
    print("Load local files.")
    data = pd.DataFrame([[ 1, 2, 3, 4],[5, 6, 7, 8], [9, 10, 11, 12]], index = ['aa', 'bb', 'cc'], columns = ['c1', 'c2', 'c3', 'c4'])
    return data

if __name__ == "__main__":
    get_data()