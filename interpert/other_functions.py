#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
 __author__  =  "Pavel Yadlouski (xyadlo00)"
 __project__ =  "Interpret for IPPcode20 language" 
 __brief__   =  "Auxiliary functions for processing code" 
 __file__    =  "interpret/other_functions.py"
 __date__    =  "03.2020"
"""
import sys
import re

list_labels = []
list_var = []
frames = {'GF': [], 'LF': [], 'TF': None}

def write_log(msg, err_code=None):
    """
    Function for writing down logs to STDERR and exiting with given error code
    """
    sys.stderr.write(msg)
    if err_code is not None:
        sys.exit(err_code)

def get_frame_list(frame: str) -> list:
    return frames[frame]
    pass


def get_frame_n_var(variable: str):
    try:
        frame, var = (re.findall(
            r'^(GF|LF|TF)@(\w*)$', variable))[0]
    except:
        raise
        write_log(f"Wrong format of variable. You have '{variable}'\n", 32)
    return (frame, var)


def get_item_from_frame(frame: str, var: str) -> tuple:
    frame_list = get_frame_list(frame)
    for item in frame_list:
        if var in item.keys():
            return (item, frame_list.index(item))
    write_log("Given variabel is not defined in this scope.\n", 32)


def set_value_in_frame(frame: str, var: dict, index: int):
    # Here can be an error
    try:
        frames[frame][index] = var
        # print(frames[frame][index])
    except KeyError:
        write_log("""Error in seting new value in dict in set_value.
        Maybe some of indexes is not exits.""", 32)
    except:
        write_log("Error in inserting new value in set_value.", 32)


def check_types(first_type, second_type):
    type_dict = {'int': ('var', 'int'), 'string': (
        'var', 'string'), 'bool': ('var', 'bool')}
    return second_type in type_dict[first_type]
