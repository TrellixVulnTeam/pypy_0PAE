import sys

if sys.version_info.major == 2:
    from ._exec_py2 import execute
    from ._reraise_py2 import reraise
else:
    from ._exec_py3 import execute
    from ._reraise_py3 import reraise

try:
    xrange = xrange
except NameError:
    xrange = range


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


__all__ = ["execute", "iteritems", "iterkeys", "itervalues", "reraise", "xrange"]
