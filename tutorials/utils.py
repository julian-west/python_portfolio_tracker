"""utility functions for notebooks"""


def print_properties(object):
    """Print the public properties of an object"""
    for attr in dir(object):
        if attr[0] != "_":
            print(attr)
