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


# __list_labels = ()
# __list_var = []
# __frames = {'GF': [], 'LF': [], 'TF': []}


def def_var_fnc(params: ET.Element):
    # TODO split by @ and append to corresponding list of variables
    if (len(params) != 1):
        write_log("Wrong count of parameters while defining LABEL\n", 32)

    try:
        if params[0].attrib['type'] != 'var':
            write_log(
                f"Type of parameter in DEFVAR is not 'var', but '{params[0].attrib['type']}'\n", 32)

        frame, var = (re.findall(r'^(GF|LF|TF)@(\w*)$', params[0].text))[0]
        __frames[frame].append({var: None, 'type': None})
    except:
        write_log("Something wrong with parsing variables in DEFVAR\n", 32)


def label_fnc(sub_child: ET.Element, **kwargs) -> int:
    # TODO add label to tuple. If label already exist in tuple -> ERROR or NOT?
    return 0


__list_labels = []
__list_var = []
__frames = {'GF': [], 'LF': [], 'TF': None}


def get_frame_list(frame: str) -> list:
    return __frames[frame]
    pass


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
    return None


def set_value_in_frame(frame: str, var: dict, index: int):
    # Here can be an error
    try:
        __frames[frame][index] = var
        print(__frames[frame])
    except KeyError:
        write_log("""Error in seting new value in dict in set_value.
        Maybe some of indexes is not exits.""", 32)
    except:
        write_log("Error in inserting new value in set_value.", 32)


def check_types(first_type, second_type):
    type_dict = {'int': ('var', 'int'), 'string': (
        'var', 'string'), 'bool': ('var', 'bool')}
    return second_type in type_dict[first_type]


def add_fnc(params) -> int:
    if (len(params) != 3):
        write_log("Wrong count of parameters for function ADD\n", 32)
    def_var = params[0]
    first_val = params[1]
    second_val = params[2]

    # Check that there is variable to write result of adding
    if def_var.attrib['type'] != 'var':
        write_log(
            f"""You did not specified variable to write result of ADD function.
            Here is something different: '{def_var.attrib['type']}'\n""", 32)
    first_type = first_val.attrib['type']
    second_type = second_val.attrib['type']

    frame, var = get_frame_n_var(def_var.text)
    item, index = get_item_from_frame(frame, var)
    if first_type == 'int':
        # Extracting information to correct processing of operaion
        if second_type == 'int':
            try:
                # Actual helding of operation
                item[var] = int(first_val.text) + int(second_val.text)
            except:
                write_log("Something wrong in TRY block of ADD function.\n", 32)
        elif second_type == 'var':
            try:
                # Extract value from given variable
                frame, var_of_val = get_frame_n_var(second_val.text)
                item_of_val, index = get_item_from_frame(frame, var_of_val)
                # Extract variable to write down
                if(item_of_val['type'] != 'int'):
                    write_log(
                        f"Wrong type of second parameter in function ADD: {second_type}.\n", 32)
                item[var] = int(first_val.text) + int(item_of_val[var_of_val])
            except:
                write_log("""Something wrong in TRY block of ADD
                function when there is variable as second parameter\n""", 32)
        else:
            write_log(
                f"Wrong type for function ADD {first_type} and {second_type}.\n", 32)

    elif first_type == 'var':
        print("HER")
        try:
            # Extract value from given variable
            frame, var_of_val = get_frame_n_var(first_val.text)
            item_of_val, index = get_item_from_frame(frame, var_of_val)
            # Extract varitemiable to write down
            if(item_of_val['type'] != 'int'):
                write_log(f"Wrong type of second parameter in function ADD: {second_type}.\n", 32)
        except:
            write_log("""Something wrong in TRY block of ADD function when there is variable as first parameter in first TRY block\n""", 32)
                
        if second_type == 'int':
            item[var] = int(item_of_val[var_of_val]) + int(second_val.text) 
        elif second_type == 'var':
            try:
                # Extract value from given variable
                frame, var_of_val_2 = get_frame_n_var(second_val.text)
                item_of_val_2, index = get_item_from_frame(frame, var_of_val_2)
                # Extract variable to write down
                if(item_of_val['type'] != 'int'):
                    write_log(
                        f"Wrong type of second parameter in function ADD: {second_type}.\n", 32)
                item[var] = int(item_of_val[var_of_val]) + int(item_of_val_2[var_of_val_2])
            except:
                write_log("""Something wrong in TRY block of ADD function when there is variable as second parameter in last TRY.\n""", 32)

    else:
        write_log(f"Wrong type for function ADD {first_type} and {second_type}.\n", 32)

    item['type'] = 'int'
    set_value_in_frame(frame, item, index)

def concat_fnc(params):
    if (len(params) != 3):
        write_log("Wrong count of parameters for function ADD\n", 32)
    def_var = params[0]
    first_val = params[1]
    second_val = params[2]

    # Check that there is variable to write result of adding
    if def_var.attrib['type'] != 'var':
        write_log(
            f"""You did not specified variable to write result of ADD function.
            Here is something different: '{def_var.attrib['type']}'\n""", 32)
    first_type = first_val.attrib['type']
    second_type = second_val.attrib['type']

    if first_type == 'string':
        if check_types(first_type, second_type):
            if second_type == 'string':
                try:
                    # Extracting information to correct processing of operaion
                    frame, var = get_frame_n_var(def_var.text)
                    item, index = get_item_from_frame(frame, var)

                    # Actual helding of operation
                    new_str = first_val.text + second_val.text
                    decoded_string = bytes(
                        new_str, "utf-8").decode("unicode_escape")
                    item[var] = decoded_string
                    set_value_in_frame(frame, item, index)
                    return
                except:
                    write_log(
                        "Something wrong in TRY block of ADD function with STR", 32)
            else:
                try:
                    # Extract value from given variable
                    frame, var_of_val = get_frame_n_var(second_val.text)
                    item_of_val, index = get_item_from_frame(frame, var_of_val)

                    # Extract variable to write down
                    frame, var = get_frame_n_var(def_var.text)
                    item, index = get_item_from_frame(frame, var)

                    # TODO convert escape sequences to charcaters
                    item[var] = first_val.text + item_of_val[var_of_val]
                    set_value_in_frame(frame, item, index)
                    return
                except:
                    write_log("""Something wrong in TRY block of ADD
                    function when there is variable as second parameter\n""", 32)

        else:
            write_log(
                f"""wrong type in ADD function. You have: 
                    '{first_type}' + '{second_type}'\n""", 32)



    pass 

def sub_fnc():
    pass


def mul_fnc():
    pass


def idiv_fnc():
    pass
