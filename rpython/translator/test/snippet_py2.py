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

def powerset(setsize=int):
    """Powerset

    This one is from a Philippine Pythonista Hangout, an modified
    version of Andy Sy's code.

    list.append is modified to list concatenation, and powerset
    is pre-allocated and stored, instead of printed.

    URL is: http://lists.free.net.ph/pipermail/python/2002-November/
    """
    set = range(setsize)
    maxcardinality = pow(2, setsize)
    bitmask = 0L
    powerset = [None] * maxcardinality
    ptr = 0
    while bitmask < maxcardinality:
        bitpos = 1L
        index = 0
        subset = []
        while bitpos < maxcardinality:
            if bitpos & bitmask:
                subset = subset + [set[index]]
            index += 1
            bitpos <<= 1
        powerset[ptr] = subset
        ptr += 1
        bitmask += 1
    return powerset
