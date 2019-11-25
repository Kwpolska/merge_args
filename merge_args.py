# -*- encoding: utf-8 -*-
# merge_args v0.1.2
# Merge signatures of two functions with Advanced Hackery.
# Copyright © 2018, Chris Warrick.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions, and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions, and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the author of this software nor the names of
#    contributors to this software may be used to endorse or promote
#    products derived from this software without specific prior written
#    consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Merge signatures of two functions with Advanced Hackery. Useful for wrappers.

Usage: @merge_args(old_function)
"""

import inspect
import itertools
import types
import functools
import sys

__version__ = '0.1.2'
__all__ = ('merge_args',)


PY38 = sys.version_info >= (3, 8)


def _blank():  # pragma: no cover
    pass


def _merge(source, dest):
    """Merge the signatures of ``source`` and ``dest``.

    ``dest`` args go before ``source`` args in all three categories
    (positional, keyword-maybe, keyword-only).
    """
    source_spec = inspect.getfullargspec(source)
    dest_spec = inspect.getfullargspec(dest)

    if source_spec.varargs or source_spec.varkw:
        raise ValueError("The source function may not take variable arguments.")

    source_all = source_spec.args
    dest_all = dest_spec.args

    if source_spec.defaults:
        source_pos = source_all[:-len(source_spec.defaults)]
        source_kw = source_all[-len(source_spec.defaults):]
    else:
        source_pos = source_all
        source_kw = []

    if dest_spec.defaults:
        dest_pos = dest_all[:-len(dest_spec.defaults)]
        dest_kw = dest_all[-len(dest_spec.defaults):]
    else:
        dest_pos = dest_all
        dest_kw = []

    args_merged = dest_pos

    for a in itertools.chain(source_pos, dest_kw, source_kw):
        if a not in args_merged:
            args_merged.append(a)

    kwonlyargs_merged = dest_spec.kwonlyargs
    for a in source_spec.kwonlyargs:
        if a not in kwonlyargs_merged:
            kwonlyargs_merged.append(a)

    args_all = tuple(args_merged + kwonlyargs_merged)

    passer_args = [len(args_merged)]
    if PY38:
        passer_args.append(dest.__code__.co_posonlyargcount)

    passer_args.extend([
        len(kwonlyargs_merged),
        _blank.__code__.co_nlocals,
        _blank.__code__.co_stacksize,
        source.__code__.co_flags,
        _blank.__code__.co_code, (), (),
        args_all, dest.__code__.co_filename,
        dest.__code__.co_name,
        dest.__code__.co_firstlineno,
        dest.__code__.co_lnotab])

    passer_code = types.CodeType(*passer_args)
    passer = types.FunctionType(passer_code, globals())
    dest.__wrapped__ = passer

    # defaults, annotations
    defaults = dest.__defaults__
    if defaults is None:
        defaults = []
    else:
        defaults = list(defaults)
    if source.__defaults__ is not None:
        defaults.extend(source.__defaults__)

    # ensure we take destination’s return annotation
    has_dest_ret = 'return' in dest.__annotations__
    if has_dest_ret:
        dest_ret = dest.__annotations__['return']

    for v in ('__kwdefaults__', '__annotations__'):
        out = getattr(source, v)
        if out is None:
            out = {}
        if getattr(dest, v) is not None:
            out = out.copy()
            out.update(getattr(dest, v))
            setattr(passer, v, out)

    if has_dest_ret:
        passer.__annotations__['return'] = dest_ret
    dest.__annotations__ = passer.__annotations__

    passer.__defaults__ = tuple(defaults)
    if not dest.__doc__:
        dest.__doc__ = source.__doc__
    return dest


def merge_args(source):
    """Merge the signatures of two functions."""
    return functools.partial(_merge, source)
