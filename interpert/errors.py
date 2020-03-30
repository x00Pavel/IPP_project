#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-


"""
__author__ = "Pavel Yadlouski (xyadlo00)"
__project__ = "Interpret for IPPcode20 language"
__brief__ = "Module contating all error classes that coresponds 
             to errors which may arise in interpert "
__file__ = "interpret/errors.py"
__date__ = "03.2020"
"""

class OrderError(Exception):
    def __init__(self, *args):
        self.msg = f"Wrong order. Must be greater then {args[0]}, but you have {args[1]}.\n"


class Err_10(Exception):
    def __init__(self, msg=None):
        if msg is None:
            self.msg = "You did not specified required argument of parameter\n"
        else:
            self.msg = msg

class Err_32(Exception):
    def __init__(self, msg=None, fnc=None):
        if msg:
            self.msg = msg
        else:
            self.msg = f"Unexpected structure of XML file in function '{fnc}'.\n"


class Err_31(Exception):
    def __init__(self, msg=None, fnc=None):
        if msg:
            self.msg = msg
        else:
            self.msg = f"Not well-formated XML file. Raised in '{fnc}'.\n"


class Err_58(Exception):
    def __init__(self, msg=None, fnc=None):
        if msg is not None:
            self.msg = msg
        else:
            self.msg = f"Error in processing string in function {fnc}.\n"


class Err_57(Exception):
    def __init__(self, msg=None, fnc=None):
        if msg is not None:
            self.msg = msg
        else:
            self.msg = "Wrong exit code.\n"


class Err_56(Exception):
    def __init__(self, msg=None, fnc=None):
        if msg is not None:
            self.msg = msg
        else:
            self.msg = "Given value is None.\n"


class Err_55(Exception):
    def __init__(self, msg=None, frame=None):
        if msg is not None:
            self.msg = msg
        else:
            self.msg = f"Frame does '{frame}' not exist.\n"


class Err_54(Exception):
    def __init__(self, msg=None, fnc=None, **kwargs):
        if msg is not None:
            self.msg = msg
        else:
            self.msg = f"Given variabel ({fnc}) is not defined in given scope ({kwargs['frame']}).\n"


class Err_53(Exception):
    def __init__(self, msg=None, fnc=None, **kwargs):
        if msg is not None:
            self.msg = msg
        else:
            self.msg = msg = f"Wrong type of argument in function '{fnc}'. " \
                f"Required '{kwargs['req_type']}' type, but you have '{kwargs['src_type']}'.\n"


class Err_52(Exception):
    def __init__(self, msg=None, var=None):
        if msg is not None:
            self.msg = msg
        else:
            self.msg = "Error in semantic control. Maybe caused be using of undefined" \
                f" label or redefinition of variable: {var}.\n"


class Err_99(Exception):
    def __init__(self, msg=None, fnc=None, **kwargs):
        if msg is not None:
            self.msg = msg
        else:
            self.msg = "Error in semantic control. Maybe caused be using of undefined" \
                f" label or redefinition of variable: {kwargs['var']}.\n"

class Err_exit(Exception):
    def __init__(self, code: int):
        self.code = code
