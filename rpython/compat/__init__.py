import sys

if sys.version_info[0] == 2:
    from ._reraise_py2 import reraise  # noqa: F401
else:
    from ._reraise_py3 import reraise  # noqa: F401
