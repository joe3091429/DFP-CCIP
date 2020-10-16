#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
    File name: ccip_utils
    Group members: Kiana, Xiaoye, Joe
    Purpose: Utility class for processing data
'''
import pandas as pd
import os

class CCIPUtils(object):
    
    @staticmethod
    def download_files(df):

        op_name = 'output'
        rel_path = 'output'
        format_dict = {'1':'.csv', '2':'.json', '3': '.txt'}
        
        # ask for path
        print('Input the path if you want to download in the specific place. \nIf not, leave the blank and the file will be in output file.\n')
        abs_path = input('Path: ').strip()

        # check path exist
        isPath = os.path.exists(abs_path)
      
        # ask for format
        print('\nChoose the format of downloaded file (Default as TXT)\n1) CSV\n2) JSON\n3) TXT')
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
        print("Complete downloading files.\n")
    
    @staticmethod
    def verify_output_name(path, fileformat):
        i = 0
        while os.path.exists((path + '/'+ 'output%s' + fileformat) % i):
            i += 1
        filename =  'output' + str(i)
        return filename
