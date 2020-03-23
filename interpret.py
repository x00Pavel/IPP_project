#!/usr/bin/env python3.8
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
import interpert.errors as err
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
        raise err.Err_10()

    if '--help' in params.keys():
        if len(params.keys()) != 1 | len(arguments) != 0:
            raise err.Err_10("Parameter '--help' can't be combined with other "
                             "parameters or arguments\n")
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
            raise err.Err_99("File {} does not exist or can't be open to read\n"
                             .format(params['--source'])if params['--source'] != ''
                             else "You did not specified file for some parameter\n")

        except ET.ParseError:
            raise err.Err_32(
                "There is something wrong with tags while parsing XML.\n")
    if '--input' in params.keys():
        input_file = params['--input']
        try:
            with open(params['--input'], 'r') as f:
                input_file = f.read()
                input_file = input_file.split('\n')
        except IOError:
            raise err.Err_99(f"File {params['--input']} does not exist or can't be "
                             "open to read\n" if params['--input'] != ''
                             else "You did not specified file for some parameter\n")

    if source_file is None:
        try:
            with open("tmp.xml", "w") as f:
                for line in sys.stdin:
                    f.write(line)
            source_file = ET.parse('tmp.xml')
            os.remove('tmp.xml')

        except:
            raise err.Err_99("Error while reading code from STDIN."
                          "Maybe error in creating temporary file\n")


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
            'STRI2INT': ops.str_2_int_fnc,
            'TYPE': ops.type_fnc,
            'CONCAT': ops.concat_fnc,
            'READ': ops.read_fnc,
            'STRLEN': ops.strlen_fnc,
            'AND': ops.and_fnc,
            'OR': ops.or_fnc,
            'NOT': ops.not_fnc,
            'EQ': ops.equal_fnc,
            'LT': ops.less_fnc,
            'GT': ops.greater_fnc
            }


def process_xml(xml_file):
    order = 1
    root = None
    if ET.iselement(source_file):
        root = source_file.getiterator()
    else:
        root = source_file.getroot()

    for child in root:
        if child.tag != 'program':
            try:
                if order > int(child.attrib['order']):
                    raise err.OrderError(order, int(child.attrib['order']))
                order = int(child.attrib['order'])
                opcode = child.attrib['opcode']
                function = fnc_dict[opcode.upper()]
                if opcode.upper() == 'READ':
                    function(child, input_file)
                    if input_file is not None:
                        input_file.pop(0)
                else:
                    function(child)

            except KeyError:
                raise err.Err_32("No reference to function for"
                                 f" operation code {opcode}.\n")
            except:
                raise err.Err_32(fnc=opcode)


if __name__ == "__main__":
    try:
        main()
        process_xml(source_file)
    except:
        raise
    # except (err.OrderError, err.Err_32) as err:
    #     sys.stderr.write(err.msg)
    #     exit(32)
    # except err.Err_31 as err:
    #     sys.stderr.write(str(err.msg))
    #     exit(31)
    # except err.Err_52 as err:
    #     sys.stderr.write(str(err.msg))
    #     exit(52)
    # except err.Err_53 as err:
    #     sys.stderr.write(str(err.msg))
    #     exit(53)
    # except err.Err_54 as err:
    #     sys.stderr.write(str(err.msg))
    #     exit(54)
    # except err.Err_55 as err:
    #     sys.stderr.write(str(err.msg))
    #     exit(55)
    # except err.Err_56 as err:
    #     sys.stderr.write(str(err.msg))
    #     exit(56)
    # except err.Err_57 as err:
    #     sys.stderr.write(str(err.msg))
    #     exit(57)
    # except err.Err_58 as err:
    #     sys.stderr.write(str(err.msg))
    #     exit(58)
