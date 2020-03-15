#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
 __author__  =  "Pavel Yadlouski (xyadlo00)"
 __project__ =  "Interpret for IPPcode20 language" 
 __brief__   =  "Functions for all valid operation codes" 
 __file__    =  "interpret/opcodes.py"
 __date__    =  "03.2020"
"""

import xml.etree.ElementTree as ET
import interpert.other_functions as fnc
import pprint as pp
import sys
import re


def def_var_fnc(params: ET.Element):
    # TODO split by @ and append to corresponding list of variables
    if (len(params) != 1):
        fnc.write_log("Wrong count of parameters while defining LABEL\n", 32)

    try:
        if params[0].attrib['type'] != 'var':
            fnc.write_log(
                f"Type of parameter in DEFVAR is not 'var', but '{params[0].attrib['type']}'\n", 32)

        frame, var = (re.findall(r'^(GF|LF|TF)@(\w*)$', params[0].text))[0]
        fnc.frames[frame].append({var: None, 'type': None})
    except:
        fnc.write_log("Something wrong with parsing variables in DEFVAR\n", 32)


def label_fnc(sub_child: ET.Element, **kwargs) -> int:
    # TODO add label to tuple. If label already exist in tuple -> ERROR or NOT?
    return 0

def add_fnc(params) -> int:
    if (len(params) != 3):
        fnc.write_log("Wrong count of parameters for function ADD\n", 32)
    def_var = params[0]
    first_val = params[1]
    second_val = params[2]
    # Check that there is variable to write result of adding
    if def_var.attrib['type'] != 'var':
        fnc.write_log(
            f"""You did not specified variable to write result of ADD function.
            Here is something different: '{def_var.attrib['type']}'\n""", 32)

    first_type = first_val.attrib['type']
    second_type = second_val.attrib['type']
    # Extracting information to correct processing of operaion
    frame, var = fnc.get_frame_n_var(def_var.text)
    item, index = fnc.get_item_from_frame(frame, var)
    if first_type == 'int' and second_type == 'int':
        try:
            item[var] = int(first_val.text) + int(second_val.text)
        except:
            fnc.write_log("Something wrong in TRY block of ADD function.\n", 32)
    elif first_type == 'int' and second_type == 'var':
        try:
            # Extract value from given variable
            frame, name_of_var = fnc.get_frame_n_var(second_val.text)
            item_of_var, index_of_var = fnc.get_item_from_frame(frame, name_of_var)
            # Extract variable to write down
            if(item_of_var['type'] != 'int'):
                fnc.write_log(
                    f"Wrong type of second parameter in function ADD: {second_type}.\n", 32)
            item[var] = int(first_val.text) + int(item_of_var[name_of_var])
        except:
            fnc.write_log("""Something wrong in TRY block of ADD
            function when there is variable as second parameter\n""", 32)
    elif first_type == 'var' and second_type == 'int':
        try:
            # Extract variable to write down
            frame, name_of_var = fnc.get_frame_n_var(first_val.text)
            item_of_var, index_of_var = fnc.get_item_from_frame(frame, name_of_var)
            if(item_of_var['type'] != 'int'):
                fnc.write_log(f"Wrong type of second parameter in function ADD: {second_type}.\n", 32)
            item[var] = int(item_of_var[name_of_var]) + int(second_val.text) 
        except:
            fnc.write_log("""Something wrong in TRY block of ADD function when there is variable as first parameter in first TRY block\n""", 32)
    elif first_type == 'var' and second_type == 'var':
            try:
                # Extract value from given variable
                frame_1, name_1= fnc.get_frame_n_var(first_val.text)
                item_of_var_1, index_of_var_1 = fnc.get_item_from_frame(frame_1, name_1)

                frame_2, name_2 = fnc.get_frame_n_var(second_val.text)
                item_of_var_2, index_of_var_2 = fnc.get_item_from_frame(frame_2, name_2)
                # Extract variable to write down
                if(item_of_var_1['type'] != 'int' or item_of_var_2['type'] != 'int'):
                    fnc.write_log(
                        f"Wrong type of second parameter in function ADD: {second_type}.\n", 32)
                item[var] = int(item_of_var_1[name_1]) + int(item_of_var_2[name_2])
            except:
                raise
                fnc.write_log("""Something wrong in TRY block of ADD function when there is variable as second parameter in last TRY.\n""", 32)
    else:
        fnc.write_log(
            f"Wrong type for function ADD {first_type} and {second_type}.\n", 32)

    item['type'] = 'int'
    fnc.set_value_in_frame(frame, item, index)

def concat_fnc(params):
    # b'a\040\146\165\156\143\164more string\151\157\156\040\163\167'.decode('utf-8')
    if (len(params) != 3):
        fnc.write_log("Wrong count of parameters for function ADD\n", 32)
    def_var = params[0]
    first_val = params[1]
    second_val = params[2]

    # Check that there is variable to write result of adding
    if def_var.attrib['type'] != 'var':
        fnc.write_log(
            f"""You did not specified variable to write result of ADD function.
            Here is something different: '{def_var.attrib['type']}'\n""", 32)
    first_type = first_val.attrib['type']
    second_type = second_val.attrib['type']

    if first_type == 'string':
        if fnc.check_types(first_type, second_type):
            if second_type == 'string':
                try:
                    # Extracting information to correct processing of operaion
                    frame, var = fnc.get_frame_n_var(def_var.text)
                    item, index = fnc.get_item_from_frame(frame, var)

                    # Actual helding of operation
                    new_str = first_val.text + second_val.text
                    decoded_string = bytes(
                        new_str, "utf-8").decode("unicode_escape")
                    item[var] = decoded_string
                    fnc.set_value_in_frame(frame, item, index)
                    return
                except:
                    fnc.write_log(
                        "Something wrong in TRY block of ADD function with STR", 32)
            else:
                try:
                    # Extract value from given variable
                    frame, var_of_val = fnc.get_frame_n_var(second_val.text)
                    item_of_val, index = fnc.get_item_from_frame(frame, var_of_val)

                    # Extract variable to write down
                    frame, var = fnc.get_frame_n_var(def_var.text)
                    item, index = fnc.get_item_from_frame(frame, var)

                    # TODO convert escape sequences to charcaters
                    item[var] = first_val.text + item_of_val[var_of_val]
                    fnc.set_value_in_frame(frame, item, index)
                    return
                except:
                    fnc.write_log("""Something wrong in TRY block of ADD
                    function when there is variable as second parameter\n""", 32)

        else:
            fnc.write_log(
                f"""wrong type in ADD function. You have: 
                    '{first_type}' + '{second_type}'\n""", 32)



    pass 

def sub_fnc():
    pass


def mul_fnc():
    pass


def idiv_fnc():
    pass
