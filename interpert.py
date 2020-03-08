#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
import sys
import getopt
import fileinput
import xml.etree.ElementTree as ET

source_file = None
input_file = None


def write_log(msg, err_code=None):
    """
    Function for writing down logs to STDERR and exiting with given error code
    """
    sys.stderr.write(msg)
    if err_code is not None:
        sys.exit(err_code)


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
        write_log("File {} does not exist or can't be open to read\n".format(file)
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
        write_log("You did not specified required argument of parameter\n", 10)

    if '--help' in params.keys():
        if len(params.keys()) != 1 | len(arguments) != 0:
            write_log(
                "Parameter '--help' can't be combined with other parameters or arguments\n", 10)
        else:
            sys.stdout.write("""Program načte XML reprezentaci programu a tento program s využitím vstupu dle parametrů příkazové řádky interpretuje a generuje výstup. Vstupní XML reprezentace je např. generována skriptemparse.php (ale ne nutně) ze zdrojového kódu v IPPcode20. Interpret navíc oproti sekci 3.1 podporujeexistenci volitelných dokumentačních textových atributů name a description v kořenovém elementuprogram. Sémantika jednotlivých instrukcí IPPcode20 je popsána v sekci 6. Interpretace instrukcíprobíhá dle atributu order vzestupně (sekvence nemusí být souvislá na rozdíl od sekce 3.1)\n""")
            sys.exit(0)
    if '--source' in params.keys():
        try:
            source_file = ET.parse(params['--source'])
        except IOError:
            write_log("File {} does not exist or can't be open to read\n".format(params['--source'])
                      if params['--source'] != '' else "You did not specified file for some parameter\n")

    if '--input' in params.keys():
        try:
            with open(params['--input'], 'r') as input_file:
                pass
        except IOError:
            write_log("File {} does not exist or can't be open to read\n".format(params['--input'])
                      if params['--input'] != '' else "You did not specified file for some parameter\n")

    if source_file is None:
        source_file = ''
        write_log("I'm waiting for you to input source code in XML format:\n")
        for line in sys.stdin:
            source_file += line
        source_file = ET.fromstring(source_file)

    if input_file is None:
        input_file = ''
        write_log("I'm waiting for you to input parameters for script:\n")
        # try:
        #     while True:
        #         input_file += input() + "\n"
        # except EOFError:
        #     pass
        # print(input_file)
        # input_file = fileinput.input()
        for line in sys.stdin:
            input_file += line

def process_xml(xml_file):
    root = source_file.getroot()
    print(ET.tostring(root, encoding='utf8').decode('utf8')) # Print whole document
    print(root.attrib)
    for elem in root.findall("./program/insruction/argv1"):
        print(elem.attrib, elem.text)
        pass
    # for child in root:
    #     print(child.tag, child. attrib)
    # print(source_file.attrib)


if __name__ == "__main__":
    main()
    process_xml(source_file)
