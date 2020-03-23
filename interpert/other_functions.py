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

list_labels = []
list_var = []
# frames = {'GF': gf, 'LF': LocalFrame, 'TF': TemporaryFrame}
frames = {'GF': [], 'LF': [], 'TF': None}


class GlobalFrame():
    global_frame = None

    def __init__(self):
        global_frame = []

    def set_var(self, var: {}):
        if var not in global_frame.keys():
            global_frame.append(var)
            LocalFrame.local_frame[0] = global_frame
        else:
            raise err.Err_32("In global frame")

    def insert(self, var_to_insert: dict, index: int):
        try:
            global_frame[index] = var_to_insert
        except:
            raise err.Err_32("In global frame")
            # write_log("""Error in seting new value in dict in global frame.
            # Maybe some of indexes is not exits.""", 32)

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
        except:
            raise err.Err_32("In Local frame")

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
        except:
            raise err.Err_32("In temporary frame")

        #     write_log("""Error in seting new value in temporay frame.
        #     Maybe some of indexes is not exits.""", 32)
        # except:
        #     write_log("Error in inserting new value in set_value.", 32)

    def push_frame(self):
        pass


class Stack():

    # stack = None

    def __init__(self):
        self.stack = []

    def is_empty(self):
        return self.stack == []

    def push(self, var):
        self.stack.append(var)

    def pop(self):
        if self.is_empty():
            return None
        else:
            return self.stack.pop()

    def top(self):
        if self.is_empty():
            return None
        else:
            return self.stack[-1]

    def size(self):
        return len(self.stack)


gf = GlobalFrame()
lf = LocalFrame()
tf = TemporaryFrame()
stack = Stack()


def get_frame_list(frame: str) -> list:
    return frames[frame]


def get_frame_n_var(variable: str):
    try:
        frame, var = (re.findall(
            r'^(GF|LF|TF)@(\w*)$', variable))[0]
    except:
        raise err.Err_31(None, fnc='get_frame_v_var')
    return (frame, var)


def check_params(params: ET.Element, cnt: int, fnc: str = None):
    if len(params) != cnt:
        raise err.Err_32(f"Wrong count of parameters in function {fnc}. "
                  f"Required {len(params)}, but you have {cnt}.\n",
                  )

    if fnc == 'CALL' or fnc == 'LABEL':
        if params[0].attrib['type'] != 'label':
            raise err.Err_53(None, 'CALL', req_type='label',
                       src_type=params[0].attrib['type'])
            # write_log(53, fnc=fnc, req_type='label',
            #           src_type=params[0].attrib['type'])
        else:
            return params[0].text
    elif fnc == 'POPS':
        if params[0].attrib['type'] != 'var':
            raise err.Err_53(None, fnc='POPS', req_type='var',
                             src_type=params[0].attrib['type'])
            # write_log(53, fnc='POPS', req_type='var',
            #           src_type=params[0].attrib['type'])
    elif fnc == 'PUSHS':
        pass
    elif fnc == 'WRITE':
        return params[0]
    elif fnc == 'STRI2INT' or \
            fnc == 'INT2CHAR' or \
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
            fnc == 'STRLEN' or \
            fnc == 'READ' or \
            fnc == 'NOT':
        dst = params[0]
        src = params[1]
        if dst.attrib['type'] != 'var':
            raise err.Err_53(None, fnc=fnc, req_type='var',
                             src_type=dst.attrib['type'])
        return (dst, src)


def get_item_from_frame(var: str) -> tuple:
    frame, var = get_frame_n_var(var)
    frame_list = get_frame_list(frame)
    try:
        for item in frame_list:
            if var == item['name']:
                return (frame, item, frame_list.index(item))
    except TypeError:
        raise err.Err_55(
                    f"Given variabel ({var}) is not defined in given scope ({frame}).\n")


def get_type(var: ET.ElementTree) -> str:
    if var.attrib['type'] == 'var':
        args = get_item_from_frame(var.text)
        item = args[1]
        return item['type']
    else:
        return var.attrib['type']


def set_value_in_frame(frame: str, var_to_insert: dict, index: int):
    # Here can be an error
    try:
        frames[frame][index]['value'] = var_to_insert['value']
        frames[frame][index]['type'] = var_to_insert['type']
        # print(frames[frame][index])
    except KeyError:
        raise err.Err_53("""Error in seting new value in dict in set_value.
        Maybe some of indexes is not exits.""")
        # write_log(msg="""Error in seting new value in dict in set_value.
        # Maybe some of indexes is not exits.""", err_code=53)
    except:
        raise err.Err_32("Error in inserting new value in set_value.")
        # write_log(msg="Error in inserting new value in set_value.", err_code=32)


def return_value(var: ET.ElementTree, req_type: str, fnc: str = ''):
    tmp = None

    if var.attrib['type'] == 'var':
        frame, item, ind = get_item_from_frame(var.text)
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
    frame, item, index = get_item_from_frame(dst)
    item['type'] = src_type
    item['value'] = src_value
    set_value_in_frame(frame, item, index)


def check_math(def_var, first_val, second_val, ref_type='int'):
    # Extracting information to correct processing of operaion

    frame, item, index = get_item_from_frame(def_var.text)
    first_type = first_val.attrib['type']
    second_type = second_val.attrib['type']
    args = None

    def return_list(first, second):
        if ref_type == 'int':
            return [int(first), int(second)]
        elif ref_type == 'string':
            return [first, second]
        elif ref_type == 'bool':
            return (bool(first), second)

    if first_type == ref_type and second_type == ref_type:
        args = return_list(first_val.text, second_val.text)

    elif first_type == ref_type and second_type == 'var':
        try:
            # Extract value from given variable
            var_frame, var_item, var_index = get_item_from_frame(
                second_val.text)
            # Extract variable to write down
            if(var_item['type'] != ref_type):
                raise err.Err_53(None, fnc='check_math', req_type=ref_type,
                                 src_type=var_item['type'])
            args = return_list(first_val.text, var_item['value'])
        except:
            raise err.Err_32("Something wrong in TRY block of ADD function when "
                       "there is variable as second parameter\n")
            # write_log(msg="Something wrong in TRY block of ADD function when "
            #           "there is variable as second parameter\n", err_code=32)
    elif first_type == 'var' and second_type == ref_type:
        try:
            # Extract variable to write down
            var_frame, var_item, var_index = get_item_from_frame(first_val.text)
            if(var_item['type'] != ref_type):
                raise err.Err_53(None, fnc='check_math', req_type=ref_type,
                                 src_type=var_item['type'])
            args = return_list(var_item['value'], second_val.text)
        except:
            raise err.Err_32("Something wrong in TRY block of ADD function when "
                             "there is variable as first parameter in first TRY block\n")
            # write_log(
            #     msg="Something wrong in TRY block of ADD function when "
            #     "there is variable as first parameter in first TRY block\n", err_code=32)
    elif first_type == 'var' and second_type == 'var':
        try:
            # Extract value from given variable
            frame_1, item_of_var_1, index_of_var_1 = get_item_from_frame(
                first_val.text)

            frame_2, item_of_var_2, index_of_var_2 = get_item_from_frame(
                second_val.text)
            # Extract variable to write down
            if(item_of_var_1['type'] != 'int' or item_of_var_2['type'] != 'int'):
                raise err.Err_53(None, fnc='check_math', req_type=ref_type,
                                 src_type=var_item['type'])
            args = return_list(item_of_var_1['value'], item_of_var_2['value'])
        except:
            raise err.Err_32("Something wrong in TRY block of ADD function when there is"
                             " variable as second parameter in last TRY.\n")
    else:
        raise err.Err_53(
            f"Wrong type for math function {first_type} and {second_type}.\n")

    return (frame, item, index, args)
