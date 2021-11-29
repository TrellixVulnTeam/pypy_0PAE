from __future__ import print_function
from rpython.rtyper.test.test_llinterp import interpret
from rpython.rlib.rarithmetic import r_int


class Test_r_int:
    def test__pow__(self):
        self.binary_test(lambda x, y: pow(x, y, 42L), (2, 3, 5, 1000))

    def binary_test(self, f, rargs=None, includes_floats=False):
        if not rargs:
            rargs = (-10, -1, 3, 55)
        types_list = [(int, r_int), (r_int, int), (r_int, r_int)]
        if includes_floats:
            types_list += [(float, r_int), (r_int, float)]
        for larg in (-10, -1, 0, 3, 1234):
            for rarg in rargs:
                for types in types_list:
                    res = f(larg, rarg)
                    left, right = types
                    cmp = f(left(larg), right(rarg))
                    assert res == cmp
