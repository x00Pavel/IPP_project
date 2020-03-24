#!/usr/bin/env python3.8
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
import interpert.errors as err
import interpert.frames as fr

list_labels = []

stack = fr.Stack()

frames = {'GF': None, 'LF': None, 'TF': None}
frames['GF'] = fr.GlobalFrame()
# gf = frames.GlobalFrame()


def get_frame_n_name(variable: str):
    try:
        frame, var = (re.findall(
            r'^(GF|LF|TF)@(\w*)$', variable))[0]
        return (frame, var)
    except:
        raise err.Err_31(None, fnc='get_frame_v_var')


def check_params(params: ET.Element, cnt: int, fnc: str = None):
    if len(params) != cnt:
        raise err.Err_32(f"Wrong count of parameters in function {fnc}. "
                  f"Required {len(params)}, but you have {cnt}.\n",
                  )

    if fnc == 'CALL' or fnc == 'LABEL':
        if params[0].attrib['type'] != 'label':
            raise err.Err_53(None, 'CALL', req_type='label',
                       src_type=params[0].attrib['type'])
        else:
            return params[0].text
    elif fnc == 'POPS':
        if params[0].attrib['type'] != 'var':
            raise err.Err_53(None, fnc='POPS', req_type='var',
                             src_type=params[0].attrib['type'])
    elif fnc == 'PUSHS':
        pass
    elif fnc == 'WRITE':
        return params[0]
    elif fnc == 'STRI2INT' or \
            fnc == 'GETCHAR' or \
            fnc == 'SETCHAR' or \
            fnc == 'SUB' or \
            fnc == 'ADD' or \
            fnc == 'MUL' or \
            fnc == 'IDIV' or \
            fnc == 'LT' or \
            fnc == 'EQ' or \
            fnc == 'GT' or \
            fnc == 'AND' or \
            fnc == 'OR':
        dst = params[0]
        src = params[1]
        ind = params[2]
        if dst.attrib['type'] != 'var':
            raise err.Err_53(None, fnc=fnc, req_type='var',
                             src_type=dst.attrib['type'])
        return (dst, src, ind)
    elif fnc == 'TYPE' or \
            fnc == 'MOVE' or \
            fnc == 'INT2CHAR' or \
            fnc == 'STRLEN' or \
            fnc == 'READ' or \
            fnc == 'NOT':
        dst = params[0]
        src = params[1]
        if dst.attrib['type'] != 'var':
            raise err.Err_53(None, fnc=fnc, req_type='var',
                             src_type=dst.attrib['type'])
        return (dst, src)


def convert_str(string: str):
    ar = re.findall(r'\\(\d{3})', string)
    new_str = ''
    for a in ar:
        string = re.sub(r'\\{}'.format(a), chr(int(a)), string)
    return string

def get_item_from_frame(var: str) -> tuple:
    frame, name = get_frame_n_name(var)
    try:
        if frames[frame] is None:
            raise err.Err_55()
        else:
            return frame, frames[frame].get_var(name)
    except (err.Err_54, err.Err_55) as error:
        raise error

def get_type(var: ET.ElementTree) -> str:
    if var.attrib['type'] == 'var':
        args = get_item_from_frame(var.text)
        item = args[1][0]
        return item['type']
    else:
        return var.attrib['type']


def set_value_in_frame(frame: str, var_to_insert: dict, index: int):
    # Here can be an error
    try:
        if frames[frame] is None:
            raise err.Err_55(frame=frame)
        else:
            frames[frame].set_var(var_to_insert, index)
    except (err.Err_55, err.Err_54) as error:
        raise error
    except KeyError:
        raise err.Err_53("""Error in seting new value in dict in set_value.
        Maybe some of indexes is not exits.""")
    except:
        raise err.Err_32("Error in inserting new value in set_value.")


def return_value(var: ET.ElementTree, req_type: str, fnc: str = ''):
    tmp = None

    if var.attrib['type'] == 'var':
        frame, (item, ind) = get_item_from_frame(var.text)
        if item['type'] is None:
            raise err.Err_56()
        if fnc == 'TYPE':
            return item['type']
        if item['type'] != req_type:
            raise err.Err_53(None, fnc=fnc, req_type=req_type,
                             src_type=item['type'])
            # write_log(53, '', fnc=fnc, req_type=req_type, src_type=item['type'])
        else:
            tmp = item['value']
    elif fnc == 'TYPE':
        return var.attrib['type']
    elif var.attrib['type'] == req_type:
        tmp = var.text
    else:
        raise err.Err_53(None, fnc=fnc, req_type=req_type,
                         src_type=var.attrib['type'])
    return tmp


def set_n_insert_val_type(dst: str, src_type: str, src_value):
    frame, (item, index) = get_item_from_frame(dst)
    item['type'] = src_type
    item['value'] = src_value
    set_value_in_frame(frame, item, index)


def check_math(def_var, first_val, second_val, ref_type='int'):
    # Extracting information to correct processing of operaion

    frame, (item, index) = get_item_from_frame(def_var.text)
    first_type = first_val.attrib['type']
    second_type = second_val.attrib['type']
    args = None

    def return_list(first, second):
        if ref_type == 'int':
            return [int(first), int(second)]
        elif ref_type == 'string':
            if first is None:
                first = ''
            if second is None:
                second = ''
            return [first, second]
        elif ref_type == 'bool':
            return (bool(first), second)

    if first_type == ref_type and second_type == ref_type:
        args = return_list(first_val.text, second_val.text)

    elif first_type == ref_type and second_type == 'var':
        try:
            # Extract value from given variable
            var_frame, (var_item, var_index) = get_item_from_frame(
                second_val.text)
            # Extract variable to write down
            if var_item['type'] is None:
                raise err.Err_56
            if(var_item['type'] != ref_type):
                raise err.Err_53(None, fnc='check_math', req_type=ref_type,
                                 src_type=var_item['type'])
            args = return_list(first_val.text, var_item['value'])
        except :
            raise     
    elif first_type == 'var' and second_type == ref_type:
        try:
            # Extract variable to write down
            var_frame, (var_item, var_index) = get_item_from_frame(first_val.text)
            if var_item['type'] is None:
                raise err.Err_56
            if(var_item['type'] != ref_type):
                raise err.Err_53(None, fnc='check_math', req_type=ref_type,
                                 src_type=var_item['type'])
            args = return_list(var_item['value'], second_val.text)
        except:
            raise
    elif first_type == 'var' and second_type == 'var':
        try:
            # Extract value from given variable
            frame_1, item_of_var_1, index_of_var_1 = get_item_from_frame(
                first_val.text)

            frame_2, item_of_var_2, index_of_var_2 = get_item_from_frame(
                second_val.text)
            # Extract variable to write down
            if item_of_var_1['type'] is None or item_of_var_2['type'] is None:
                raise err.Err_56
            if(item_of_var_1['type'] != 'int' or item_of_var_2['type'] != 'int'):
                raise err.Err_53(None, fnc='check_math', req_type=ref_type,
                                 src_type=var_item['type'])
            args = return_list(item_of_var_1['value'], item_of_var_2['value'])
        except:
            raise
    else:
        raise err.Err_53(
            f"Wrong type for math function {first_type} and {second_type}.\n")

    return (frame, item, index, args)
