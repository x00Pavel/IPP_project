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
                "Type of parameter in DEFVAR is not 'var', but "
                f"'{params[0].attrib['type']}'\n", 32)

        frame, var = (re.findall(r'^(GF|LF|TF)@(\w*)$', params[0].text))[0]
        fnc.frames[frame].append({var: None, 'type': None})
    except:
        fnc.write_log("Something wrong with parsing variables in DEFVAR\n", 32)


def add_fnc(params):
    """
    Function for handling opcode ADD
    Arguments:
        * params: list of attributes of ElementTree Element  
    """
    if (len(params) != 3):
        fnc.write_log("Wrong count of parameters for function ADD\n", 32)
    def_var = params[0]
    first_val = params[1]
    second_val = params[2]
    # Check that there is variable to write result of adding
    if def_var.attrib['type'] != 'var':
        fnc.write_log(
            "You did not specified variable to write result of ADD function."
            f"Here is something different: '{def_var.attrib['type']}'\n",  32)

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
            item_of_var, index_of_var = fnc.get_item_from_frame(
                frame, name_of_var)
            # Extract variable to write down
            if(item_of_var['type'] != 'int'):
                fnc.write_log("Wrong type of second parameter in function "
                              f"ADD: {second_type}.\n", 32)
            item[var] = int(first_val.text) + int(item_of_var[name_of_var])
        except:
            fnc.write_log("Something wrong in TRY block of ADD function when "
                          "there is variable as second parameter\n", 32)
    elif first_type == 'var' and second_type == 'int':
        try:
            # Extract variable to write down
            frame, name_of_var = fnc.get_frame_n_var(first_val.text)
            item_of_var, index_of_var = fnc.get_item_from_frame(
                frame, name_of_var)
            if(item_of_var['type'] != 'int'):
                fnc.write_log(
                    "Wrong type of second parameter in function "
                    f"ADD: {second_type}.\n", 32)
            item[var] = int(item_of_var[name_of_var]) + int(second_val.text)
        except:
            fnc.write_log(
                "Something wrong in TRY block of ADD function when "
                "there is variable as first parameter in first TRY block\n", 32)
    elif first_type == 'var' and second_type == 'var':
        try:
            # Extract value from given variable
            frame_1, name_1 = fnc.get_frame_n_var(first_val.text)
            item_of_var_1, index_of_var_1 = fnc.get_item_from_frame(
                frame_1, name_1)

            frame_2, name_2 = fnc.get_frame_n_var(second_val.text)
            item_of_var_2, index_of_var_2 = fnc.get_item_from_frame(
                frame_2, name_2)
            # Extract variable to write down
            if(item_of_var_1['type'] != 'int' or item_of_var_2['type'] != 'int'):
                fnc.write_log(
                    "Wrong type of second parameter in function "
                    f"ADD: {second_type}.\n", 32)
            item[var] = int(item_of_var_1[name_1]) + int(item_of_var_2[name_2])
        except:
            raise
            fnc.write_log(
                "Something wrong in TRY block of ADD function when there is"
                " variable as second parameter in last TRY.\n", 32)
    else:
        fnc.write_log(
            f"Wrong type for function ADD {first_type} and {second_type}.\n", 32)

    item['type'] = 'int'
    fnc.set_value_in_frame(frame, item, index)

# TODO


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
            "You did not specified variable to write result of ADD function."
            f"Here is something different: '{def_var.attrib['type']}'\n", 32)
    first_type = first_val.attrib['type']
    second_type = second_val.attrib['type']

    # Extracting information to correct processing of operaion
    frame, var = fnc.get_frame_n_var(def_var.text)
    item, index = fnc.get_item_from_frame(frame, var)
    if first_type == 'string' and second_type == 'string':
        try:
            # Actual helding of operation
            new_str = first_val.text + second_val.text
            ar = re.findall(r'\\(\d{3})', new_str)
            for a in ar:
                new_str = re.sub(r'\\{}'.format(a), chr(int(a)), new_str)
        except:
            fnc.write_log(
                "Something wrong in TRY block of ADD function with STR", 32)
    elif first_type == 'string' and second_type == 'var':
        try:
            frame_1, var_1 = fnc.get_frame_n_var(second_val.text)
            item_1, index_1 = fnc.get_item_from_frame(frame_1, var_1)
            # Actual helding of operation
            if item_1['type'] != 'string':
                fnc.write_log(
                    f"Value with type {first_type} and {item_1['type']}"
                    " can't be concatenated.\n", 32
                )
            new_str = first_val.text + item_1[var_1]
            ar = re.findall(r'\\(\d{3})', new_str)
            for a in ar:
                new_str = re.sub(r'\\{}'.format(a), chr(int(a)), new_str)
        except:
            fnc.write_log(
                "Something wrong in TRY block of CONCAT function", 32)

    elif first_type == 'var' and second_type == 'string':
        try:
            frame_1, var_1 = fnc.get_frame_n_var(first_val.text)
            item_1, index_1 = fnc.get_item_from_frame(frame_1, var_1)
            # Actual helding of operation
            if item_1['type'] != 'string':
                fnc.write_log(
                    f"Value with type {item_1['type']} and {second_type}"
                    " can't be concatenated.\n", 32
                )
            new_str = first_val.text + item_1[var_1]
            ar = re.findall(r'\\(\d{3})', new_str)
            for a in ar:
                new_str = re.sub(r'\\{}'.format(a), chr(int(a)), new_str)
        except:
            fnc.write_log(
                "Something wrong in TRY block of CONCAT function", 32)
    elif first_type == 'var' and second_type == 'var':
        try:
            frame_1, var_1 = fnc.get_frame_n_var(first_val.text)
            item_1, index_1 = fnc.get_item_from_frame(frame_1, var_1)

            frame_2, var_2 = fnc.get_frame_n_var(second_val.text)
            item_2, index_2 = fnc.get_item_from_frame(frame_2, var_2)

            # Actual helding of operation
            if item_1['type'] != 'string' or item_2['type'] != 'string':
                fnc.write_log(
                    f"Value with type {item_1['type']} and {item_2['type']}"
                    " can't be concatenated.\n", 32
                )

            new_str = item_1[var_1] + item_2[var_2]
            ar = re.findall(r'\\(\d{3})', new_str)
            for a in ar:
                new_str = re.sub(r'\\{}'.format(a), chr(int(a)), new_str)
        except:
            fnc.write_log(
                "Something wrong in TRY block of ADD function with STR", 32)

    item[var] = new_str
    fnc.set_value_in_frame(frame, item, index)


def write_fnc(params):
    if len(params) != 1:
        fnc.write_log(
            "Wrong number of arguments in function WRITE", 32
        )
    arg = params[0]
    arg_type = arg.attrib['type']
    arg_val = arg.text

    if arg_type == 'var':
        frame, var = fnc.get_frame_n_var(arg_val)
        item, index = fnc.get_item_from_frame(frame, var)
        if item['type'] == 'nil':
            sys.stdout.write('')
        elif item['type'] == 'string':
            print("HER")
            decoded_string = bytes(
                item[var], "utf-8").decode("utf-8")
        else:
            sys.stdout.write(item[var])
    elif arg_type == 'string':
        ar = re.findall(r'\\(\d{3})', arg_val)
        for a in ar:
            arg_val = re.sub(r'\\{}'.format(a), chr(int(a)), arg_val)
        sys.stdout.write(arg_val)
    elif arg_type == 'int' or arg_type == 'bool':
        sys.stdout.write(str(arg_val))


def move_fnc(params):
    if len(params) != 2:
        fnc.write_log(
            "Wrong number of parameters in function MOVE. "
            f"You have: {len(params)}, but 2 required\n", 32
        )

    dest_var = params[0]
    value = params[1]

    if dest_var.attrib['type'] != 'var':
        fnc.write_log(
            "Error in MOVE function. You can not move not to variable\n", 32
        )

    frame, var = fnc.get_frame_n_var(dest_var.text)
    item, index = fnc.get_item_from_frame(frame, var)
    if value.attrib['type'] == 'var':
        frame_src, var_src = fnc.get_frame_n_var(value.text)
        item_src, index_src = fnc.get_item_from_frame(frame_src, var_src)
        fnc.set_value_in_frame(frame, item_src, index)
    else:
        fnc.set_value_in_frame(
            frame, {var: value.text, 'type': value.attrib['type']}, index)


def label_fnc(sub_child: ET.Element, **kwargs) -> int:
    # TODO add label to tuple. If label already exist in tuple -> ERROR or NOT?
    return 0


def sub_fnc():
    pass


def mul_fnc():
    pass


def idiv_fnc():
    pass
