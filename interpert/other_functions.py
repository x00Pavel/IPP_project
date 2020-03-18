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
# frames = {'GF': gf, 'LF': LocalFrame, 'TF': TemporaryFrame}
frames = {'GF': [], 'LF': [], 'TF': None}


class Frame():
    global_frame = None

    def __init__(self):
        global_frame = []

    def set_var(self, var: {}):
        if var not in global_frame.keys():
            global_frame.append(var)
        else:
            write_log

    def insert(self, var_to_insert: dict, index: int):
        try:
            global_frame[index] = var_to_insert
            # print(frames[frame][index])
        except KeyError:
            write_log("""Error in seting new value in dict in global frame.
            Maybe some of indexes is not exits.""", 32)
        except:
            write_log("Error in inserting new value in set_value.", 32)


    def get_list(self):
        return global_frame

class LocalFrame(Frame):
    local_frame = None

    def __init__(self):
        self.local_frame = None
        local_frame = Frame.global_frame

    def crate_local_frame(self):
        self.local_frame = []

    def delate_local_frame(self):
        self.local_frame = None

    def insert(self, var_to_insert: dict, index: int):
        try:
            self.local_frame[index] = var_to_insert
            # print(frames[frame][index])
        except KeyError:
            write_log("""Error in seting new value in dict in local frame.
            Maybe some of indexes is not exits.""", 32)
        except:
            write_log("Error in inserting new value in set_value.", 32)

    def get_list(self):
        if self.local_frame is not None:
            return self.local_frame
        else:
            return local_frame    

class TemporaryFrame(Frame):
    temporary_frame = None

    def __init__(self):
        self.temporary_frame = []

    def insert(self, var_to_insert: dict, index: int):
        try:
            self.temporary_frame[index] = var_to_insert
            # print(frames[frame][index])
        except KeyError:
            write_log("""Error in seting new value in temporay frame.
            Maybe some of indexes is not exits.""", 32)
        except:
            write_log("Error in inserting new value in set_value.", 32)


gf = Frame()
lf = LocalFrame()


def write_log(msg, err_code=None):
    """
    Function for writing down logs to STDERR and exiting with given error code
    """
    sys.stderr.write(msg)
    if err_code is not None:
        sys.exit(err_code)

def get_frame_list(frame: str) -> list:
    return frames[frame]
    


def get_frame_n_var(variable: str):
    try:
        frame, var = (re.findall(
            r'^(GF|LF|TF)@(\w*)$', variable))[0]
    except:
        write_log(f"Wrong format of variable. You have '{variable}'\n", 32)
    return (frame, var)


def get_item_from_frame(frame: str, var: str) -> tuple:
    frame_list = get_frame_list(frame)
    for item in frame_list:
        if var in item.keys():
            return (item, frame_list.index(item))
    write_log("Given variabel is not defined in this scope.\n", 32)


def set_value_in_frame(frame: str, var_to_insert: dict, index: int):
    # Here can be an error
    try:
        frames[frame][index] = var_to_insert
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
