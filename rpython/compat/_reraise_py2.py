def reraise(etype, evalue, etb):
    """Reraise the exception, preserving the traceback."""
    raise etype, evalue, etb
