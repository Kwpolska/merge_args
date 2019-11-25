#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# merge_args test suite
# Copyright © 2018, Chris Warrick.
# See /LICENSE for licensing information.

import pytest
import merge_args
import sys
from inspect import signature


def test_orig():

    def old(foo, bar):
        """This is old's docstring."""
        return foo + bar

    def new(prefix, foo, *args, **kwargs):
        return old(prefix + foo, *args, **kwargs)

    assert str(signature(new)) == '(prefix, foo, *args, **kwargs)'

    new = merge_args._merge(old, new)
    assert str(signature(new)) == '(prefix, foo, bar)'
    assert new.__doc__ == old.__doc__
    assert new.__doc__
    assert old('a', 'b') == 'ab'
    assert new('!', 'a', 'b') == '!ab'


def test_with_kwargs():

    def src(a, b, c=1): pass

    @merge_args.merge_args(src)
    def dest(d, e=2, *args, **kwargs): pass

    assert str(signature(dest)) == '(d, a, b, e=2, c=1)'


def test_kwonlyargs():

    def src(q, w, e=1, *, r=2): pass

    @merge_args.merge_args(src)
    def dest(*, t=3, **kwargs): pass

    assert str(signature(dest)) == '(q, w, e=1, *, t=3, r=2)'

    def src2(*, a=1): pass

    @merge_args.merge_args(src2)
    def dest2(*, a=2, b=3): pass

    assert str(signature(dest2)) == '(*, a=2, b=3)'


def test_var_fails():

    def src(*args, **kwargs): pass

    def dest(*args, **kwargs): pass

    with pytest.raises(ValueError):
        merge_args._merge(src, dest)


def test_no_docstring_override():

    def src(foo):
        """src docs"""

    @merge_args.merge_args(src)
    def dest(bar):
        """dest docs"""

    assert str(signature(dest)) == '(bar, foo)'
    assert src.__doc__ == "src docs"
    assert dest.__doc__ == "dest docs"


def test_annotations():

    def src(s: int) -> str:
        pass

    @merge_args.merge_args(src)
    def dest(d: float) -> list:
        pass

    assert str(signature(dest)) in (
        '(d:float, s:int) -> list',
        '(d: float, s: int) -> list'
    )


@pytest.mark.skipif(sys.version_info < (3, 8), reason="positional-only args added in Python 3.8")
def test_positional_only():
    from tests.posonly import old, new


    assert str(signature(new)) == '(prefix, foo, /, *args, **kwargs)'

    new = merge_args._merge(old, new)
    assert str(signature(new)) == '(prefix, foo, /, bar)'
