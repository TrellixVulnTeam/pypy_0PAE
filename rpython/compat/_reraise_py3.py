def reraise(_, evalue, etb):
    """Reraise the exception, preserving the traceback."""
    raise evalue.with_traceback(etb)
