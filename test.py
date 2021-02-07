"""test.py"""


import os
import typing
from collections import Counter
from typing import List, Tuple


def hello(strange: str) -> Tuple[str, List[str], typing.Counter[str]]:
    """say hello"""
    dir_list = os.listdir()
    new_dict = Counter("asdakljsfdlkjs")

    return f"{strange} hello", dir_list, new_dict
