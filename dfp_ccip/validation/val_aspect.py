#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
    File name: val_aspect
    Group members: Kiana, Xiaoye, Joe
    Purpose: Validate users' input of aspects
'''

def val_aspect(v_aspect):
    print("\nValidating input aspect.......\n")
    if v_aspect not in ['1','2','3','4'] :
        print('It is not a valid option, please select again \n')
        return False
    return True

if __name__ == "__main__":
    val_aspect()