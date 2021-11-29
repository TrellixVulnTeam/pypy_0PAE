import sys

if sys.version_info.major == 2:
    from ._exec_py2 import execute
    from ._reraise_py2 import reraise
else:
    from ._exec_py3 import execute
    from ._reraise_py3 import reraise


__all__ = ["execute", "reraise"]
