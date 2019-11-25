# This file exists, because putting the old/new functions directly in
# `test_merge.py` would crash older Pythons with a syntax error.
"""Functions with positional-only arguments."""


def old(foo, /, bar):
    pass


def new(prefix, foo, /, *args, **kwargs):
    pass
