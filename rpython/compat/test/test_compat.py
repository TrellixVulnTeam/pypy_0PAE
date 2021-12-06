import rpython.compat as compat


def test_cmp():

    def true(*args):
        return True

    def false(*args):
        return False

    # This truth table is derived from pypy2
    truth_table = [
        (true, true, 0),
        (true, false, 0),
        (false, true, -1),
        (false, false, 1),
    ]
    class_table = []
    for k, (eq, lt, expected) in enumerate(truth_table):
        name = 'CmpCheck{}'.format(k)
        attrs = {'__eq__': eq, '__lt__': lt}
        class_table.append((type(name, (object,), attrs), expected))

    try:
        for klass, expected in class_table:
            assert cmp(klass(), klass()) == expected

    except NameError:
        pass  # cmp does not exist under python3

    for klass, expected in class_table:
        if not compat.cmp(klass(), klass()) == expected:
            raise AssertionError

    class CustomCmp(object):

        def __eq__(self, other):
            return True

        def __cmp__(self, other):
            return -1

    a, b = CustomCmp(), CustomCmp()
    try:
        assert cmp(a, b) == -1
    except NameError:
        pass

    assert compat.cmp(CustomCmp(), CustomCmp()) == -1
    assert not CustomCmp < CustomCmp


def test_ordering_from_cmp():

    @compat.ordering_from_cmp
    class Foo(object):

        def __eq__(self, other):
            return True

        def __cmp__(self, other):
            return 1

    assert Foo() == Foo()
    assert Foo() > Foo()
    assert Foo().__gt__(Foo())
    assert not Foo() < Foo()
    assert not Foo().__lt__(Foo())


def test_execute():
    env = {}
    compat.execute('def foo(): pass', env)
    assert 'foo' in env
    assert callable(env['foo'])


def test_dict_iter_methods():
    d = dict(a=1)
    assert next(compat.iterkeys(d)) == 'a'
    assert next(compat.itervalues(d)) == 1
    assert next(compat.iteritems(d)) == ('a', 1)


def test_with_metaclass():

    class MetaFoo(type):

        def __new__(meta, name, bases, attrs):
            attrs['meta'] = object()
            return super(MetaFoo, meta).__new__(meta, name, bases, attrs)

    @compat.with_metaclass(MetaFoo)
    class Foo(object):
        pass

    class Bar(Foo):
        pass

    assert Foo.meta
    assert Bar.meta
    assert Foo.meta != Bar.meta
