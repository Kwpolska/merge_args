====================================================================
merge_args — merge signatures of two functions with Advanced Hackery
====================================================================

.. image:: https://travis-ci.org/Kwpolska/merge_args.svg?branch=master
   :target: https://travis-ci.org/Kwpolska/merge_args

This small library uses Advanced Python Hackery to change the signature of a
function to be a mixture of itself and a function that it wraps. It’s like
``functools.wraps``, but it allows the wrapped function to add its own
arguments into the mix.

Usage
-----

.. code:: python

    from merge_args import merge_args

    def old(foo, bar):
        """This is old's docstring."""
        print(foo, bar)
        return foo + bar

    @merge_args(old)
    def new(prefix, foo, *args, **kwargs):
        return old(prefix + foo, *args, **kwargs)

If you then run ``help(new)``, this is the output:

.. code:: text

    Help on function new in module __main__:

    new(prefix, foo, bar)
        This is old's docstring.

How it works?
-------------

I wrote a detailed blog post, describing the ins and outs of how this package works:

https://chriswarrick.com/blog/2018/09/20/python-hackery-merging-signatures-of-two-python-functions/

This module was inspired by F4D3C0D3 on #python (freenode IRC).

License
-------
Copyright © 2018, Chris Warrick.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions, and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions, and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

3. Neither the name of the author of this software nor the names of
   contributors to this software may be used to endorse or promote
   products derived from this software without specific prior written
   consent.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
