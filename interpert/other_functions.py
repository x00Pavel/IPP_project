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
import xml.etree.ElementTree as ET

list_labels = []
list_var = []
# frames = {'GF': gf, 'LF': LocalFrame, 'TF': TemporaryFrame}
frames = {'GF': [], 'LF': [], 'TF': None}
stack = []


class GlobalFrame():
    global_frame = None

    def __init__(self):
        global_frame = []

    def set_var(self, var: {}):
        if var not in global_frame.keys():
            global_frame.append(var)
            LocalFrame.local_frame[0] = global_frame
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


class LocalFrame(GlobalFrame):
    local_frame = None

    def __init__(self):
        local_frame = []
        local_frame.append(GlobalFrame.global_frame)

    def crate_local_frame(self):
        local_frame.append([])

    def delate_local_frame(self):
        local_frame.pop()

    def insert(self, var_to_insert: dict, index: int):
        try:
            local_frame[-1][index] = var_to_insert
            # print(frames[frame][index])
        except KeyError:
            write_log("""Error in seting new value in dict in local frame.
            Maybe some of indexes is not exits.""", 32)
        except:
            write_log("Error in inserting new value in set_value.", 32)

    def get_list(self):
        return local_frame.pop()

    def pop_frame(self):
        pass


class TemporaryFrame(GlobalFrame):
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

    def push_frame(self):
        pass


gf = GlobalFrame()
lf = LocalFrame()
tf = TemporaryFrame()


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


def check_params(params: ET.Element, cnt: int, fnc: str = None):
    if len(params) != cnt:
        write_log(
            f"Wrong count of parameters in function {fnc}. "
            f"Required {len(params)}, but you have {cnt}.\n", 32
        )

    if fnc == 'CALL' or fnc == 'LABEL':
        if params[0].attrib['type'] != 'label':
            write_log(
                f"Wrong type of argument in function {fnc}. "
                f"Required 'label', but you have {params[0].attrib['type']}.\n",
                32
            )
        else:
            return params[0].text
    elif fnc == 'SUB' or fnc == 'ADD' or fnc == 'MUL' or fnc == 'IDIV':
        return (params[0], params[1], params[2])

    elif fnc == 'POPS':
        if params[0].attrib['type'] != 'var':
            write_log(
                f"Function {fnc} require first argument to be of type 'vat', "
                f"but you have '{params[0].attrib['type']}' type.\n", 53
            )
    elif fnc == 'PUSHS':
        pass
    elif fnc == 'MOVE':
        return (params[0], params[1])
    elif fnc == 'WRITE':
        return params[0]
    elif fnc == 'INT2CHAR':
        dst = params[0]
        src = params[1]
        if dst.attrib['type'] != 'var':
            write_log(
                f"Function {fnc} require first argument to be variable. "
                f"You have type '{dst.attrib['type']}'.\n", 53
            )
        return (dst, src)


def get_item_from_frame(var: str) -> tuple:
    frame, var = get_frame_n_var(var)
    frame_list = get_frame_list(frame)
    for item in frame_list:
        if var == item['name']:
            return (frame, item, frame_list.index(item))
    write_log(f"Given variabel is not defined in given scope ({frame}).\n", 32)


def set_value_in_frame(frame: str, var_to_insert: dict, index: int):
    # Here can be an error
    try:
        frames[frame][index]['value'] = var_to_insert['value']
        frames[frame][index]['type'] = var_to_insert['type']
        # print(frames[frame][index])
    except KeyError:
        write_log("""Error in seting new value in dict in set_value.
        Maybe some of indexes is not exits.""", 53)
    except:
        write_log("Error in inserting new value in set_value.", 32)


def check_math(def_var, first_val, second_val, ref_type='int'):
    if def_var.attrib['type'] != 'var':
        write_log(
            "You did not specified variable to write result of ADD function."
            f"Here is something different: '{def_var.attrib['type']}'\n",  53)

    # Extracting information to correct processing of operaion
    #  var = get_frame_n_var(def_var.text)
    frame, item, index = get_item_from_frame(def_var.text)
    first_type = first_val.attrib['type']
    second_type = second_val.attrib['type']
    args = None

    def return_list(first, second):
        if ref_type == 'int':
            return [int(first), int(second)]
        elif ref_type == 'string':
            return [first, second]

    if first_type == ref_type and second_type == ref_type:
        args = return_list(first_val.text, second_val.text)

    elif first_type == ref_type and second_type == 'var':
        try:
            # Extract value from given variable
            frame, name_of_var = get_frame_n_var(second_val.text)
            var_item, var_index = get_item_from_frame(
                frame, name_of_var)
            # Extract variable to write down
            if(var_item['type'] != ref_type):
                write_log("Wrong type of second parameter in function "
                          f"ADD: {second_type}.\n", 53)
            args = return_list(first_val.text, var_item['value'])
        except:
            write_log("Something wrong in TRY block of ADD function when "
                      "there is variable as second parameter\n", 32)
    elif first_type == 'var' and second_type == ref_type:
        try:
            # Extract variable to write down
            # frame, name_of_var = get_frame_n_var(first_val.text)
            var_frame, var_item, var_index = get_item_from_frame(first_val.text)
            if(var_item['type'] != ref_type):
                write_log(
                    "Wrong type of first parameter in function "
                    f"ADD: {second_type}.\n", 53)
            args = return_list(var_item['value'], second_val.text)
        except:
            write_log(
                "Something wrong in TRY block of ADD function when "
                "there is variable as first parameter in first TRY block\n", 32)
    elif first_type == 'var' and second_type == 'var':
        try:
            # Extract value from given variable
            frame_1, name_1 = get_frame_n_var(first_val.text)
            item_of_var_1, index_of_var_1 = get_item_from_frame(
                frame_1, name_1)

            frame_2, name_2 = get_frame_n_var(second_val.text)
            item_of_var_2, index_of_var_2 = get_item_from_frame(
                frame_2, name_2)
            # Extract variable to write down
            if(item_of_var_1['type'] != 'int' or item_of_var_2['type'] != 'int'):
                write_log(
                    "Wrong type of second parameter in function "
                    f"ADD: {second_type}.\n", 53)
            args = return_list(item_of_var_1['value'], item_of_var_2['value'])
        except:
            write_log(
                "Something wrong in TRY block of ADD function when there is"
                " variable as second parameter in last TRY.\n", 32)
    else:
        write_log(
            f"Wrong type for function ADD {first_type} and {second_type}.\n", 53)

    return (frame, item, index, args)
