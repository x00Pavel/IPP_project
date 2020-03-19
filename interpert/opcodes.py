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

# Don't have arguments


def create_frame_fnc(*args):
    pass


# Don't have arguments
def push_frame_fnc(*args):
    pass


# Don't have arguments
def pop_frame_fnc(*args):
    pass


# TODO
def call_fnc(params: ET.Element):
    label = fnc.check_params(params, 1, 'CALL')

    if label not in fnc.list_labels.keys():
        fnc.write_log(f"Label {label} is not specified yet.\n", 52)


# Don't have arguments
def return_fnc(params: ET.Element):
    pass


def pushs_fnc(params: ET.Element):
    fnc.check_params(params, 1, 'PUSHS')
    # frame, item, index = fnc.get_item_from_frame(params[0].text)
    src_type = params[0].attrib['type']
    src_val = params[0].text
    fnc.stack.append({'value': src_val, 'type': src_type})



def pops_fnc(params: ET.Element):
    fnc.check_params(params, 1, 'POPS')
    frame, item, index = fnc.get_item_from_frame(params[0].text)
    val_to_insert = fnc.stack.pop()
    item['type'] = val_to_insert['type']
    item['value'] = val_to_insert['value']
    fnc.set_value_in_frame(frame, item, index)


def less_fnc(params: ET.Element):
    pass


def greater_fnc(params: ET.Element):
    pass


def equal_fnc(params: ET.Element):
    pass


def and_fnc(params: ET.Element):
    pass


def or_fnc(params: ET.Element):
    pass


def not_fnc(params: ET.Element):
    pass


def int_2_char_fnc(params: ET.Element):
    destination, source = fnc.check_params(params, 2, 'INT2CHAR')
    frame, item, index = fnc.get_item_from_frame(destination.text)
    src_type = ''
    src_val = '' 
    if source.attrib['type'] == 'var':
        frame, item, index = fnc.get_item_from_frame(source.text)
        src_type = item['type']
        src_val = item['value']
    else:
        src_type = source.attrib['type']
        src_val = source.text
    
    if src_type != 'int':
        fnc.write_log(
            "Wrong type of second argument in function 'INT2CHAR'. "
            f"Required 'int' type, but you have {src_type}.\n", 53
        )
    try:
        item['value'] = chr(src_val)
        item['type'] = 'string'
    except:
        fnc.write_log(
            f"Value '{src_val}' can't be converted from 'int' type to "
            "'string' type.\n", 58
        )
    fnc.set_value_in_frame(frame, item, index)

def str_2_int_fnc(params: ET.Element):
    pass


def read_fnc(params: ET.Element):
    pass


def strlen_fnc(params: ET.Element):
    pass


def get_char_fnc(params: ET.Element):
    pass


def set_char_fnc(params: ET.Element):
    pass


def type_fnc(params: ET.Element):
    pass


def jump_fnc(params: ET.Element):
    pass


def jump_if_eq_fnc(params: ET.Element):
    pass


def jump_if_neq_fnc(params: ET.Element):
    pass


def exit_fnc(params: ET.Element):
    pass


def dprint_fnc(params: ET.Element):
    pass


def break_fnc(params: ET.Element):
    pass


def def_var_fnc(params: ET.Element):
    # TODO split by @ and append to corresponding list of variables
    if (len(params) != 1):
        fnc.write_log("Wrong count of parameters while defining LABEL\n", 32)

    try:
        if params[0].attrib['type'] != 'var':
            fnc.write_log(
                "Type of parameter in DEFVAR is not 'var', but "
                f"'{params[0].attrib['type']}'\n", 53)

        frame, var = (re.findall(r'^(GF|LF|TF)@(\w*)$', params[0].text))[0]
        if var in [x['name'] for x in fnc.frames[frame]]:
            fnc.write_log(
                f"Variable {var} already defined in {frame} frame.\n", 52
            )
        fnc.frames[frame].append({'name': var, 'value': '', 'type': 'nil'})
    except:
        fnc.write_log("Something wrong with parsing variables in DEFVAR\n", 32)


def add_fnc(params: ET.Element):
    """
    Function for handling opcode ADD
    Arguments:
        * params: list of attributes of ElementTree Element  
    """
    try:
        def_var, first_val, second_val = fnc.check_params(params, 3, 'ADD')
        frame, item, index, args = fnc.check_math(
            def_var, first_val, second_val)
        item['value'] = args[0] + args[1]
        item['type'] = 'int'
        fnc.set_value_in_frame(frame, item, index)
    except:
        raise
        fnc.write_log("Something wrong in TRY block of ADD function.\n", 32)


def concat_fnc(params: ET.Element):
    """
    Function for handling 'CONCAT' operation code
    Arguments:
        * params: list of attributes of ElementTree Element
    """
    try:
        def_var, first_val, second_val = fnc.check_params(params, 3, 'ADD')
        frame, item, index, args = fnc.check_math(
            def_var, first_val, second_val, 'string')
        new_str = args[0] + args[1]
        ar = re.findall(r'\\(\d{3})', new_str)
        for a in ar:
            new_str = re.sub(r'\\{}'.format(a), chr(int(a)), new_str)
        item['value'] = new_str
        fnc.set_value_in_frame(frame, item, index)
    except:
        fnc.write_log(
            "Something wrong in TRY block of CONCAT", 32)


def write_fnc(params: ET.Element):
    arg = fnc.check_params(params, 1, 'WRITE')

    arg_type = arg.attrib['type']
    arg_val = arg.text
    to_print = ''
    if arg_type == 'var':
        frame, item, index = fnc.get_item_from_frame(arg_val)
        if item['type'] == 'nil':
            pass
        elif item['type'] == 'string':
            to_print = bytes(
                item['value'], "utf-8").decode("utf-8")
        else:
            to_print = item['value']
    elif arg_type == 'string':
        ar = re.findall(r'\\(\d{3})', arg_val)
        for a in ar:
            arg_val = re.sub(r'\\{}'.format(a), chr(int(a)), arg_val)
        to_print = arg_val
    elif arg_type == 'int' or arg_type == 'bool':
        to_print = arg_val
    sys.stdout.write(str(to_print))


def move_fnc(params):
    dest_var, value = fnc.check_params(params, 2, 'MOVE')

    if dest_var.attrib['type'] != 'var':
        fnc.write_log(
            "Error in MOVE function. You can not move not to variable\n", 53
        )

    frame, item, index = fnc.get_item_from_frame(dest_var.text)
    if value.attrib['type'] == 'var':
        frame_src, item_src, index_src = fnc.get_item_from_frame(value.text)
        item['value'] = item_src['value']
        item['type'] = item_src['type']
    else:
        item['value'] = value.text
        item['type'] = value.attrib['type']

    fnc.set_value_in_frame(frame, item, index)


def label_fnc(params):
    label = fnc.check_params(params, 1, 'LABEL')
    if label.text not in fnc.list_labels:
        fnc.list_labels.append({label.text: params.attrib['order']})
    else:
        fnc.write_log(
            f"Label {label.text} already defined.\n", 52
        )


def sub_fnc(params):
    """
    Function for handling 'SUB' operation code
    Arguments:
        * params: list of attributes of ElementTree Element  
    """
    try:
        def_var, first_val, second_val = fnc.check_params(params, 3, 'SUB')
        frame, item, index, args = fnc.check_math(
            def_var, first_val, second_val)
        item['value'] = args[0] + args[1]
        item['type'] = 'int'
        fnc.set_value_in_frame(frame, item, index)
    except:
        fnc.write_log("Something wrong in TRY block of ADD function.\n", 32)


def mul_fnc(params):
    """
    Function for handling opcode MUL
    Arguments:
        * params: list of attributes of ElementTree Element
    """
    try:
        def_var, first_val, second_val = fnc.check_params(params, 3, 'MUL')
        frame, item, index, args = fnc.check_math(
            def_var, first_val, second_val)
        item['value'] = args[0] * args[1]
        item['type'] = 'int'
        fnc.set_value_in_frame(frame, item, index)
    except:
        fnc.write_log("Something wrong in TRY block of ADD function.\n", 32)


def idiv_fnc(params):
    """
    Function for handling opcode IDIV
    Arguments:
        * params: list of attributes of ElementTree Element  
    """
    try:
        def_var, first_val, second_val = fnc.check_params(params, 3, 'IDIV')
        frame, item, index, args = fnc.check_math(
            def_var, first_val, second_val)
        if 0 in args:
            fnc.write_log("There is devision by zero.\n", 57)
        item['value'] = args[0] + args[1]
        item['type'] = 'int'
        fnc.set_value_in_frame(frame, item, index)
    except:
        fnc.write_log("Something wrong in TRY block of ADD function.\n", 32)
