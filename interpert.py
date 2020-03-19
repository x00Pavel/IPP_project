#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
 __author__  =  "Pavel Yadlouski (xyadlo00)"
 __project__ =  "Interpret for IPPcode20 language" 
 __brief__   =  "Interpert of XML representation of IPPcode20 language" 
 __file__    =  "interpret.py"
 __date__    =  "03.2020"
"""

import os
import sys
import getopt
import fileinput
import xml.etree.ElementTree as ET
import pprint as pp
import interpert.opcodes as ops
import interpert.other_functions as fnc

source_file = None
input_file = None


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
        fnc.write_log(
            "You did not specified required argument of parameter\n", 10)

    if '--help' in params.keys():
        if len(params.keys()) != 1 | len(arguments) != 0:
            fnc.write_log("Parameter '--help' can't be combined with other "
                          "parameters or arguments\n", 10)
        else:
            sys.stdout.write(
                "Program načte XML reprezentaci programu a tento program s "
                "využitím vstupu dle parametrů příkazové řádky interpretuje a "
                "generuje výstup. Vstupní XML reprezentace je např. Generována "
                "skriptem parse.php (ale ne nutně) ze zdrojového kódu v "
                "IPPcode20. Interpret navíc oproti sekci 3.1 podporujeexistenci"
                " volitelných dokumentačních textových atributů name a "
                "description v kořenovém elementuprogram. Sémantika "
                "jednotlivých instrukcí IPPcode20 je popsána v sekci 6."
                " Interpretace instrukcíprobíhá dle atributu order vzestupně"
                " (sekvence nemusí být souvislá na rozdíl od sekce 3.1)\n""")
            sys.exit(0)
    if '--source' in params.keys():
        try:
            source_file = ET.parse(params['--source'])
        except IOError:
            fnc.write_log("File {} does not exist or can't be open to read\n"
                          .format(params['--source'])if params['--source'] != ''
                          else "You did not specified file for some parameter\n")
        except ET.ParseError:
            fnc.write_log("There is something wrong with tags\n", 32)
    if '--input' in params.keys():
        try:
            with open(params['--input'], 'r') as input_file:
                pass
        except IOError:
            fnc.write_log(f"File {params['--input']} does not exist or can't be "
                          "open to read\n") if params['--input'] != '' \
                else "You did not specified file for some parameter\n"

    if source_file is None:
        try:
            with open("tmp.xml", "w") as f:
                fnc.write_log(
                    "I'm waiting for you to input source code in XML format:\n")
                for line in sys.stdin:
                    f.write(line)
            source_file = ET.parse('tmp.xml')
            os.remove('tmp.xml')

        except:
            fnc.write_log("Error while reading code from STDIN."
                          "Maybe error in creating temporary file\n", 99)

    if input_file is None:
        input_file = ''
        fnc.write_log("I'm waiting for you to input parameters for script:\n")
        for line in sys.stdin:
            input_file += line


fnc_dict = {'ADD': ops.add_fnc,
            'SUB': ops.sub_fnc,
            'MUL': ops.mul_fnc,
            'IDIV': ops.idiv_fnc,
            'LABEL': ops.label_fnc,
            'DEFVAR': ops.def_var_fnc,
            'WRITE': ops.write_fnc,
            'MOVE': ops.move_fnc,
            'LABEL': ops.label_fnc,
            "CREATEFRAME": ops.create_frame_fnc,
            "PUSHFRAME": ops.push_frame_fnc,
            "POPFRAME": ops.pop_frame_fnc,
            'CALL': ops.call_fnc,
            "RETURN": ops.return_fnc,
            'POPS': ops.pops_fnc,
            'PUSHS': ops.pushs_fnc,
            'INT2CHAR': ops.int_2_char_fnc,
            }


def process_xml(xml_file):
    order = 0
    root = None
    if ET.iselement(source_file):
        root = source_file.getiterator()
    else:
        root = source_file.getroot()

    for child in root:
        if child.tag != 'program':
            if int(child.attrib['order']) <= order:
                fnc.write_log(f"Wrong order:{child.attrib['order']}\n"
                              f"Current order must be: {order}\n", 32)
            order = order + 1
            try:
                opcode = child.attrib['opcode']
                function = fnc_dict[opcode.upper()]
                function(child)
            except:
                fnc.write_log(f"Wrong opcode: {child.attrib['opcode']}.\n", 32)


if __name__ == "__main__":
    main()
    process_xml(source_file)
