#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
"""
 __author__  =  "Pavel Yadlouski (xyadlo00)"
 __project__ =  "Interpret for IPPcode20 language" 
 __brief__   =  "Interpert of XML representation of IPPcode20 language" 
 __file__    =  "interpret.py"
 __date__    =  "03.2020"
"""

import sys
import getopt
import fileinput
import xml.etree.ElementTree as ET
import pprint as pp
import interpert.operations as ops

source_file = None
input_file = None

def open_file(file, var):
    """
    Function for handling opening file 
    """
    print(file)
    try:
        with open(file, 'r') as var:
            print(var.read())
            # return var.read()
            pass
    except IOError:
        ops.write_log("File {} does not exist or can't be open to read\n".format(file)
                  if file != '' else "You did not specified file for some parameter\n")


def main(*args, **kwargs):
    """
    Function for preprocessing parameters of script
    """
    global source_file
    global input_file
    args = sys.argv[1:]
    try:
        # TODO check that if sources ot input is specified, then arguments cant be empty
        params, arguments = getopt.getopt(
            args, 'h', ['input=', 'source=', 'help'])
        params = dict(params)
    except getopt.GetoptError:
        ops.write_log("You did not specified required argument of parameter\n", 10)

    if '--help' in params.keys():
        if len(params.keys()) != 1 | len(arguments) != 0:
            ops.write_log(
                "Parameter '--help' can't be combined with other parameters or arguments\n", 10)
        else:
            sys.stdout.write("""Program načte XML reprezentaci programu a tento program s využitím vstupu dle parametrů příkazové řádky interpretuje a generuje výstup. Vstupní XML reprezentace je např. generována skriptemparse.php (ale ne nutně) ze zdrojového kódu v IPPcode20. Interpret navíc oproti sekci 3.1 podporujeexistenci volitelných dokumentačních textových atributů name a description v kořenovém elementuprogram. Sémantika jednotlivých instrukcí IPPcode20 je popsána v sekci 6. Interpretace instrukcíprobíhá dle atributu order vzestupně (sekvence nemusí být souvislá na rozdíl od sekce 3.1)\n""")
            sys.exit(0)
    if '--source' in params.keys():
        try:
            source_file = ET.parse(params['--source'])
        except IOError:
            ops.write_log("File {} does not exist or can't be open to read\n".format(params['--source'])
                      if params['--source'] != '' else "You did not specified file for some parameter\n")

    if '--input' in params.keys():
        try:
            with open(params['--input'], 'r') as input_file:
                pass
        except IOError:
            ops.write_log("File {} does not exist or can't be open to read\n".format(params['--input'])
                      if params['--input'] != '' else "You did not specified file for some parameter\n")

    if source_file is None:
        source_file = ''
        ops.write_log("I'm waiting for you to input source code in XML format:\n")
        for line in sys.stdin:
            source_file += line
        source_file = ET.fromstring(source_file)

    if input_file is None:
        input_file = ''
        ops.write_log("I'm waiting for you to input parameters for script:\n")
        for line in sys.stdin:
            input_file += line


fnc_dict = {'ADD': ops.add_fnc,
            'SUB': ops.sub_fnc,
            'MUL': ops.mul_fnc,
            'IDIV': ops.idiv_fnc,
            'LABEL': ops.label_fnc,
            'DEFVAR': ops.def_var_fnc,
            }


def process_xml(xml_file):
    order = 0
    root = source_file.getroot()
    # print(ET.tostring(root, encoding='utf8').decode('utf8'))  # Print whole document
    # print(root.attrib)
    for child in root:
        order = order + 1
        if int(child.attrib['order']) <= 0 | int(child.attrib['order']) != order:
            exit(32)

        # print(
        #     f"{child.attrib['order']}. {child.tag} - {child.attrib['opcode']}")
        try:
            print(len(child))
            opcode = child.attrib['opcode']
            fnc = fnc_dict[opcode]
            fnc(child)
        except KeyError:
            pass

        # code = child['opcode']
        # if code == 'ADD':

        #     pass
        # elif code == 'SUB':
        #     pass
        # elif code == 'IDIV':
        #     pass
        # elif code == 'MULL':

        # for sub_child in child:
            # print(type(sub_child))

            # print(
            #     f"\t{sub_child.tag}: {sub_child.attrib} -- {sub_child.text}")


if __name__ == "__main__":
    main()
    process_xml(source_file)
