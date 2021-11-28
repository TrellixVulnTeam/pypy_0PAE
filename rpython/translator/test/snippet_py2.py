"""Py2-only snippets for translation

This module holds various snippets, to be used by translator
unittests.

We define argument types as default arguments to the snippet
functions.
"""
from snippet import Exc, exception_deduction0, witness

def exception_deduction_with_raise3(x):
    try:
        exception_deduction0(2)
        if x:
            raise Exc, Exc()
    except Exc as e:
        witness(e)
        return e
    return Exc()
