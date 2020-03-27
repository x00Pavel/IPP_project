#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
import interpert.errors as err


class GlobalFrame():
    global_frame = None

    def __init__(self):
        GlobalFrame.global_frame = []

    def get_var(self, name):
        if name not in [item['name'] for item in GlobalFrame.global_frame]:
            raise err.Err_54(None, None, var=name, frame='GF')
        else:
            for item in GlobalFrame.global_frame:
                if item['name'] == name:
                    return item, GlobalFrame.global_frame.index(item)

    def set_var(self, var: {}, index=None):
        if index is None:
            GlobalFrame.global_frame.append(var)
        elif index is not None and \
                GlobalFrame.global_frame[index]['name'] == var['name']:
            GlobalFrame.global_frame[index] = var
        else:
            raise err.Err_54(var=var['name'], frame='GF')

    def get_frame(self):
        if GlobalFrame.global_frame is None:
            raise err.Err_55(frame='GF')
        return GlobalFrame.global_frame


class LocalFrame():
    local_frame_stack = None

    def __init__(self):
        LocalFrame.local_frame_stack = []

    def create_local_frame(self, frame=None):
        if frame is not None:
            LocalFrame.local_frame_stack.append(frame)
        else:
            LocalFrame.local_frame_stack.append([])

    def remove_frame(self):
        if LocalFrame.local_frame_stack is None or \
                len(LocalFrame.local_frame_stack) == 0:
            raise err.Err_55(frame='LF')
        LocalFrame.local_frame_stack.pop(-1)

    def get_var(self, name: str):
        if LocalFrame.local_frame_stack is None:
            raise err.Err_55(frame='LF')
        if len(LocalFrame.local_frame_stack) == 0:
            raise err.Err_55(frame='LF')

        if name not in [item['name'] for item in LocalFrame.local_frame_stack[-1]]:
            raise err.Err_54(None, fnc='get_var',var=name, frame='LF')
        else:
            for item in LocalFrame.local_frame_stack[-1]:
                if item['name'] == name:
                    return (item, LocalFrame.local_frame_stack[-1].index(item))

    def set_var(self, var_to_insert: dict, index: int = None):
        if LocalFrame.local_frame_stack is None:
            raise err.Err_55(frame='LF')
        if index is None:
           LocalFrame.local_frame_stack[-1].append(var_to_insert)
        elif LocalFrame.local_frame_stack[-1][index]['name'] == var_to_insert['name']:
            LocalFrame.local_frame_stack[-1][index] = var_to_insert
        else:
            raise err.Err_54(var=var_to_insert['name'], frame='LF')

    def get_frame(self):
        if LocalFrame.local_frame_stack is None or \
                len(LocalFrame.local_frame_stack) == 0:
            raise err.Err_55(frame='LF')
        return LocalFrame.local_frame_stack[-1]


class TemporaryFrame():
    temporary_frame = None

    def __init__(self):
        TemporaryFrame.temporary_frame = []
        # return 

    def get_var(self, name: str):
        if TemporaryFrame.temporary_frame is None:
            raise err.Err_55(frame='TF')
        if name not in [item['name'] for item in TemporaryFrame.temporary_frame]:
            raise err.Err_54(None, None, var=name, frame='LF')
        else:
            for item in TemporaryFrame.temporary_frame:
                if item['name'] == name:
                    return (item, TemporaryFrame.temporary_frame.index(item))

    def set_var(self, var_to_insert: dict, index: int = None):
        if TemporaryFrame.temporary_frame is None:
            raise err.Err_55(frame='TF')
        if index is None:
            TemporaryFrame.temporary_frame.append(var_to_insert)
        elif TemporaryFrame.temporary_frame[index]['name'] == var_to_insert['name']:
            TemporaryFrame.temporary_frame[index] = var_to_insert
        else:
            raise err.Err_54(var=var_to_insert['name'], frame='TF')

    def remove(self):
        if TemporaryFrame.temporary_frame is None:
            raise err.Err_55(frame='TF')

        TemporaryFrame.temporary_frame = None

    def set_frame(self, frame: []):
        TemporaryFrame.temporary_frame = frame


    def get_frame(self):
        if TemporaryFrame.temporary_frame is None:
            raise err.Err_55(frame='TF')
        else:
            return TemporaryFrame.temporary_frame


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
            raise err.Err_56
        else:
            return self.stack.pop()

    def top(self):
        if self.is_empty():
            return None
        else:
            return self.stack[-1]

    def size(self):
        return len(self.stack)
