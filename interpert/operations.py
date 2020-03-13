#!/bin/python3.7
import xml.etree.ElementTree as ET
import pprint as pp
import sys
import re

def write_log(msg, err_code=None):
    """
    Function for writing down logs to STDERR and exiting with given error code
    """
    sys.stderr.write(msg)
    if err_code is not None:
        sys.exit(err_code)


__list_labels = ()
__list_var = []
__frames ={'GF': [], 'LF': [], 'TF': []}

def def_var_fnc(params: ET.Element):
    # TODO split by @ and append to corresponding list of variables
    if (len(params) != 1):
        write_log("Wrong count of parameters while defining LABEL\n", 32)

    try:
        if params[0].attrib['type'] != 'var':
            write_log(
                f"Type of parameter in DEFVAR is not 'var', but '{params[0].attrib['type']}'\n", 32)

        frame, var = (re.findall(r'^(GF|LF|TF)@(\w*)$', params[0].text))[0]
        __frames[frame].append({var: None})
    except:
        write_log("Something wrong with parsing variables in DEFVAR\n", 32)


def label_fnc(sub_child: ET.Element, **kwargs) -> int:
    # TODO add label to tuple. If label already exist in tuple -> ERROR or NOT?
    return 0

int_compatible = ('var', 'int')
str_compatible = ('var', 'string')
bool_compatible = ('var', 'bool')

def add_fnc(params) -> int:
    # TODO parse text to get frame, then check ti
    if (len(params) != 3):
        write_log("Wrong count of parameters for function ADD\n", 32)
    def_var = params[0]
    first_val = params[1]
    second_val = params[2]

    if def_var.attrib['type'] != 'var':
        write_log(
            f"""You did not specified variabel to write result of ADD function. 
            Here is something different: '{def_var.attrib['type']}'\n""", 32)
    first_type = first_val.attrib['type']
    second_type = second_val.attrib['type']

    if first_type == 'int':
        if second_type not in int_compatible:
            write_log(f"wrong type in ADD function. You have: '{first_type}' + '{second_type}'\n", 32)
        else:
            if second_type == 'int':
                try:
                    #####################################################
                    # TODO достать из листа нужный словарь и записать в него выследок сложнения
                    ####################################################
                    frame, var = (re.findall(
                        r'^(GF|LF|TF)@(\w*)$', def_var.text))[0]
                    list_of_vars = __frames[frame]
                     
 
                    val = [sub['gfg'] for sub in __frames[frame]]
                    print(__frames[frame])
                    print(val)
                    # __frames[frame][var] = int(first_val.text) + int(second_val.text)
                    # print(__frames[frame][var])
                except:
                    print("What the fuck Bro")
                    raise

    if first_type == 'var':
        if second_type == 'var':
            pass


        pass


    return 0

def sub_fnc():
    pass


def mul_fnc():
    pass

def idiv_fnc():
    pass




