import sys
from ._cmp import cmp, ordering_from_cmp
from ._types import ClassType, NoneType

# Exec statement
if sys.version_info.major == 2:
    from ._exec_py2 import execute
    from ._reraise_py2 import reraise
else:
    from ._exec_py3 import execute
    from ._reraise_py3 import reraise

# Builtins that no longer exist
try:
    xrange = xrange
except NameError:
    xrange = range

# Dict methods
if sys.version_info.major == 2:
    def iteritems(d):
        return d.iteritems()

    def iterkeys(d):
        return d.iterkeys()

    def itervalues(d):
        return d.itervalues()

else:
    def iteritems(d):
        return iter(d.items())

    def iterkeys(d):
        return iter(d.keys())

    def itervalues(d):
        return iter(d.values())


# Metaclass compatibility
def with_metaclass(metaclass):
    """Use this decorator to add a metaclass to classes."""

    def decorator(cls):
        orig_vars = cls.__dict__.copy()
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        return metaclass(cls.__name__, cls.__bases__, orig_vars)

    return decorator


__all__ = [
    "ClassType",
    "NoneType",
    "cmp",
    "execute",
    "iteritems",
    "iterkeys",
    "itervalues",
    "ordering_from_cmp",
    "reraise",
    "with_metaclass",
    "xrange",
]
