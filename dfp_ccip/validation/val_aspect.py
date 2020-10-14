#!/usr/bin/python
# -*- coding: UTF-8 -*-


def val_aspect(v_aspect):
    print("Validating input aspect.")
    if v_aspect not in ['1','2','3','4'] :
        print('It is not a valid option, please select again \n')
        return False
    return True

if __name__ == "__main__":
    val_aspect()