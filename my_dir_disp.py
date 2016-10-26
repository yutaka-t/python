#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os


def get_py_dir():
    return os.path.abspath(os.path.dirname(__file__))


def get_py_full_path():
    return os.path.abspath(__file__)


if __name__ == '__main__':
    print("py file      path : {0}".format(get_py_dir()))
    print("py file full path : {0}".format(get_py_full_path()))
