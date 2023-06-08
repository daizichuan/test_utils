# -- coding:UTF-8 --
# !/usr/bin/env python
"""

"""
import dictdiffer


def compare_datacount(second_dict, first_dict):
    tmp = []
    for diff in list(dictdiffer.diff(first_dict, second_dict)):
        tmp.append(diff)
    return tmp
