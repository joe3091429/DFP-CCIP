#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd
import os

class CCIPUtils(object):
    '''
        Utility class for processing data
    '''
    @staticmethod
    def download_files(df):

        op_name = 'output'
        rel_path = 'output'
        format_dict = {'1':'.csv', '2':'.json', '3': '.txt'}
        
        # ask for path
        print('''Input the path if you want to download in the specific place. 
        If not, leave the blank and the file will be in output file.
        ''')
        abs_path = input('Path: ').strip()

        # check path exist
        isPath = os.path.exists(abs_path)
      
        # ask for format
        print('''
        Choose the format of downloaded file (Default as TXT)
        1) CSV
        2) JSON
        3) TXT
        ''')
        format_opt = input('Format Option: ').strip()
        if format_opt != ('1' or '2' or '3'): format_opt = '3'
        
        # download file in specific format
        if isPath == True:
            op_name = CCIPUtils.verify_output_name(abs_path, format_dict[format_opt])
            print('this is op_name:' + op_name)
            if format_opt == '1':
                df.to_csv(abs_path + '/' + op_name + format_dict[format_opt])
            elif format_opt == '2':
                df.to_json(abs_path + '/' + op_name + format_dict[format_opt])
            else:
                df.to_csv(abs_path + '/' + op_name + format_dict[format_opt])
            print('Download the file ' + op_name + ' to the path ' + abs_path)
        else:
            op_name = CCIPUtils.verify_output_name(rel_path, format_dict[format_opt])
            if format_opt == '1':
                df.to_csv(rel_path + '/' + op_name + format_dict[format_opt])
            elif format_opt == '2':
                df.to_json(rel_path + '/' + op_name + format_dict[format_opt])
            else:
                df.to_csv(rel_path + '/' + op_name + format_dict[format_opt])
            print('Download the file ' + op_name + ' to the path ' + rel_path)
        print("Complete downloading files.")
    
    @staticmethod
    def verify_output_name(path, fileformat):
        i = 0
        while os.path.exists((path + '/'+ 'output%s' + fileformat) % i):
            i += 1
        filename =  'output' + str(i)
        return filename

    def create_health_data(s_state, s_county):

        # xiaoye's code
        print("Creating health plot and map...")
        data = pd.DataFrame([[ 1, 2, 3, 4],[5, 6, 7, 8], ['a', 'b', 'c', 'd']], index = ['aa', 'bb', 'cc'], 
                 columns = [s_state, s_state, s_county, s_county])
        return data

    def create_economy_data(s_state, s_county):

        # kiana's code
        print("Creating economy plot and map...")
        data = pd.DataFrame([[ 1, 2, 3, 4],[5, 6, 7, 8], [s_state, 'b', s_county, 'd']], index = ['aa', 'bb', 'cc'], 
                 columns = ['aa', 'bb', 'cc', 'dd'])
        return data

    def create_demo_health_data(s_state, s_county):

        # xiaoye's code
        print("Creating health plot and map...")
        data = pd.DataFrame([[ 1, 2, 3, 4],[5, 6, 7, 8], ['a', 'b', 'c', 'd']], index = ['aa', 'bb', 'cc'], 
                 columns = [s_state, s_state, s_county, s_county])
        return data

    def create_eco_health_data(s_state, s_county):

        # xiaoye's code
        print("Creating health plot and map...")
        data = pd.DataFrame([[ 1, 2, 3, 4],[5, 6, 7, 8], ['a', 'b', 'c', 'd']], index = ['aa', 'bb', 'cc'], 
                 columns = [s_state, s_state, s_county, s_county])
        return data
